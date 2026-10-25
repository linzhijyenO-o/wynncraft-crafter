# -*- coding: utf-8 -*-
"""
Wynncraft 自制装备计算引擎。

模型（按需求定义）
------------------
1. 3 行 2 列共 6 个格子，每格放 1 个原料。
2. 每格受到的「相邻加成」= 其它格子里的原料按相对位置授予它的百分比之和：
       left / right / above / under  —— 同列/同行方向（含隔一格，和官方图鉴的
                                         5x3 效果网格一致）
       touching                      —— 正交相邻（上下左右）
       not_touching                  —— 其它（斜角、隔一格）
   方向判定见 keys_at()，与 wynncraft.com/help/item-guide 的 EFFECTIVENESS 网格一致。
3. 每个格子的词条、点数需求按 (1 + 加成/100) 缩放，负数向 0 取整（截断）。
4. 耐久不受加成影响：
      成品耐久 = 基础耐久[物品种类][档位] − Σ 原料耐久消耗
   基础耐久只看物品种类和所选档位（1-6），与原料无关；消耗来自原料的
   itemOnlyIDs.durabilityModifier。
5. 消耗品（药水/卷轴/料理）没有耐久，改用「持续时间」作为限制。
6. 可以同时指定多个目标词条：每个词条有权重与下限，排名用 Σ 权重×数值。
"""
from __future__ import print_function

import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WYNNDB = os.path.dirname(os.path.dirname(HERE))
DATA_PATH = os.path.join(WYNNDB, 'data', 'ingredients.json')

# ----------------------------------------------------------------- 配置

ITEM_TYPES = [
    # id, 中文, English, 分栏, 可用职业（材料只能用在它能做的物品上）
    ('sword',      '剑',     'Sword',      'weapon',     ['weaponsmithing']),
    ('spear',      '矛',     'Spear',      'weapon',     ['weaponsmithing']),
    ('dagger',     '匕首',   'Dagger',     'weapon',     ['weaponsmithing']),
    ('bow',        '弓',     'Bow',        'weapon',     ['woodworking']),
    ('wand',       '法杖',   'Wand',       'weapon',     ['woodworking']),
    ('relik',      '遗物',   'Relik',      'weapon',     ['woodworking']),
    ('helmet',     '头盔',   'Helmet',     'armour',     ['armouring']),
    ('chestplate', '胸甲',   'Chestplate', 'armour',     ['armouring']),
    ('leggings',   '护腿',   'Leggings',   'armour',     ['tailoring']),
    ('boots',      '靴子',   'Boots',      'armour',     ['tailoring']),
    ('ring',       '戒指',   'Ring',       'accessory',  ['jeweling']),
    ('necklace',   '项链',   'Necklace',   'accessory',  ['jeweling']),
    ('bracelet',   '手镯',   'Bracelet',   'accessory',  ['jeweling']),
    ('potion',     '药水',   'Potion',     'consumable', ['alchemism']),
    ('scroll',     '卷轴',   'Scroll',     'consumable', ['scribing']),
    ('food',       '料理',   'Food',       'consumable', ['cooking']),
]

TYPE_BY_ID = {t[0]: {'id': t[0], 'cn': t[1], 'en': t[2], 'kind': t[3], 'professions': t[4]}
              for t in ITEM_TYPES}

BASE_TIERS = 6          # 基础耐久档位数
# 1~6 档的基础耐久默认值（所有物品种类统一）
DEFAULT_BASE_TABLE = [571, 666, 714, 742, 771, 799]

PROF_CN = {
    'armouring': '防具锻造', 'tailoring': '裁缝', 'weaponsmithing': '武器锻造',
    'woodworking': '木工', 'jeweling': '珠宝', 'cooking': '烹饪',
    'alchemism': '炼金', 'scribing': '铭文',
}
PROF_EN = {
    'armouring': 'Armouring', 'tailoring': 'Tailoring', 'weaponsmithing': 'Weaponsmithing',
    'woodworking': 'Woodworking', 'jeweling': 'Jeweling', 'cooking': 'Cooking',
    'alchemism': 'Alchemism', 'scribing': 'Scribing',
}

SKILLS = [('strength', '力量', 'Strength'), ('dexterity', '敏捷', 'Dexterity'),
          ('intelligence', '智力', 'Intelligence'), ('defence', '防御', 'Defence'),
          ('agility', '技巧', 'Agility')]
SKILL_KEYS = [s for s, _z, _e in SKILLS]

TIER_COLORS = ['#ffffff', '#ffdc50', '#ff50e8', '#50fdff']
TIER_NAMES = ['Normal', 'Unique', 'Rare', 'Legendary']

POS_KEYS = ['left', 'right', 'above', 'under', 'touching', 'not_touching']
ROWS, COLS = 3, 2

# ----------------------------------------------------------------- 网格几何

def keys_at(dr, dc):
    """目标格相对来源格的偏移 (dr, dc) 决定来源格授予它哪些加成。"""
    if dr == 0 and dc == 0:
        return ()
    keys = []
    if dr == 0:
        keys.append('left' if dc < 0 else 'right')
    elif dc == 0:
        keys.append('above' if dr < 0 else 'under')
    if abs(dr) + abs(dc) == 1:
        keys.append('touching')
    else:
        keys.append('not_touching')
    return tuple(keys)


def rel_keys(target, source):
    """source 格授予 target 格的加成键（均为 0..5 的格子编号）。"""
    rt, ct = divmod(target, COLS)
    rs, cs = divmod(source, COLS)
    return keys_at(rt - rs, ct - cs)


# 预计算：PAIR[target][source] = 授予时所使用的加成键
PAIR = [[rel_keys(i, j) for j in range(ROWS * COLS)] for i in range(ROWS * COLS)]


def trunc(x):
    """负数向 0 取整。"""
    return int(x)


# ----------------------------------------------------------------- 数据

class Dataset(object):
    def __init__(self, path=DATA_PATH):
        with open(path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        self.items = []
        self.by_id = {}
        for it in raw['items']:
            ing = self._prep(it)
            self.items.append(ing)
            self.by_id[ing['id']] = ing
        self.prof_index = {}
        for ing in self.items:
            for p in ing['professions']:
                self.prof_index.setdefault(p, []).append(ing)
        self.id_keys = sorted({k for ing in self.items for k in ing['ids']})
        self.id_labels = {}
        for it in raw['items']:
            for i in it['identifications']:
                self.id_labels[i['id']] = i['label']

    @staticmethod
    def _prep(it):
        ids = {}
        for i in it['identifications']:
            ids[i['id']] = (i['min'], i['raw'], i['max'])
        req = {s: 0 for s in SKILL_KEYS}
        for norm in SKILL_KEYS:
            req[norm] = it['item_ids'].get(norm, 0) or 0
        return {
            'id': it['id'],
            'name': it['name'],
            'tier': it['tier']['level'],
            'level': it['crafting_level'],
            'professions': it['professions'],
            # 有符号：负数扣耐久，正数补耐久（数据里 23 个原料是正的）
            'durability': it['item_ids'].get('durability', 0) or 0,
            'duration': it['consumable_ids'].get('duration', 0) or 0,
            'charges': it['consumable_ids'].get('charges', 0) or 0,
            'req': req,
            'ids': ids,
            'pos': {k: (it['position_modifiers'].get(k, 0) or 0) for k in POS_KEYS},
        }


# ----------------------------------------------------------------- 配置解析

def base_durability_for(cfg, type_id):
    """该物品种类的 6 档基础耐久（长度 6 的列表）。"""
    table = (cfg.get('baseDurability') or {}).get(type_id)
    if table and len(table) >= BASE_TIERS:
        return [float(x) for x in table[:BASE_TIERS]]
    return [float(x) for x in DEFAULT_BASE_TABLE]


def base_tier_of(cfg, type_id):
    """当前使用的档位（1-6）。"""
    tiers = cfg.get('baseTier') or {}
    v = tiers.get(type_id) if isinstance(tiers, dict) else tiers
    try:
        v = int(v)
    except (TypeError, ValueError):
        v = 1
    return min(max(v, 1), BASE_TIERS)


def points_limits(cfg):
    """五种属性各自的点数上限，None 表示不限。"""
    raw = cfg.get('pointsLimit') or {}
    out = {}
    for s in SKILL_KEYS:
        v = raw.get(s)
        try:
            out[s] = None if v in (None, '') else float(v)
        except (TypeError, ValueError):
            out[s] = None
    return out


def targets_of(cfg):
    """目标词条列表：[{key, weight, min}]。weight 允许 0 和负数，只有缺省时才回落到 1。"""
    raw = cfg.get('targets')
    if not raw:
        if cfg.get('targetId'):
            raw = [{'key': cfg['targetId'],
                    'min': cfg.get('minIdValue')}]
        else:
            raw = []
    out = []
    for t in raw:
        key = t.get('key')
        if not key:
            continue
        w = t.get('weight', 1)
        if w is None or w == '':
            w = 1.0
        try:
            w = float(w)
        except (TypeError, ValueError):
            w = 1.0
        mn = t.get('min')
        if mn == '':
            mn = None
        try:
            mn = None if mn is None else float(mn)
        except (TypeError, ValueError):
            mn = None
        out.append({'key': key, 'weight': w, 'min': mn})
    return out


# ----------------------------------------------------------------- 计算

def cell_bonus(cells):
    """cells: 长度 6 的列表，元素为原料 dict 或 None。返回每格加成百分比。"""
    bonus = [0] * 6
    for i in range(6):
        if cells[i] is None:
            continue
        for j in range(6):
            if i == j or cells[j] is None:
                continue
            for k in PAIR[i][j]:
                bonus[i] += cells[j]['pos'][k]
    return bonus


def evaluate(ds, cfg, ids_list):
    """完整计算一次 6 原料配方（ids_list 为 6 个原料 id）。"""
    type_id = cfg['type']
    tinfo = TYPE_BY_ID[type_id]
    cells = [ds.by_id[x] for x in ids_list]
    bonus = cell_bonus(cells)
    tier = base_tier_of(cfg, type_id)
    base_dur = base_durability_for(cfg, type_id)[tier - 1]

    dur_mod = 0
    duration = 0
    charges = 0
    reqs = {s: 0 for s in SKILL_KEYS}
    agg = {}

    out_cells = []
    for i, ing in enumerate(cells):
        b = bonus[i]
        factor = (100 + b) / 100.0
        dur_mod += ing['durability']
        duration += ing['duration']
        charges += ing['charges']
        for s in SKILL_KEYS:
            reqs[s] += trunc(ing['req'][s] * factor)
        ids_out = {}
        for k, (mn, rw, mx) in ing['ids'].items():
            vmin, vraw, vmax = trunc(mn * factor), trunc(rw * factor), trunc(mx * factor)
            ids_out[k] = [vmin, vraw, vmax]
            cur = agg.setdefault(k, [0, 0, 0])
            cur[0] += vmin
            cur[1] += vraw
            cur[2] += vmax
        out_cells.append({
            'id': ing['id'], 'name': ing['name'], 'tier': ing['tier'],
            'level': ing['level'], 'bonus': b,
            'durability': ing['durability'],
            'ids': {k: {'min': v[0], 'raw': v[1], 'max': v[2]}
                    for k, v in ids_out.items()},
        })

    base_duration = float((cfg.get('consumableBase') or {}).get(type_id, 0) or 0)
    compare = cfg.get('compare', 'max')
    tgts = []
    for t in targets_of(cfg):
        v = agg.get(t['key'], [0, 0, 0])
        tgts.append({
            'key': t['key'], 'weight': t['weight'], 'min': t['min'],
            'value': v[0] if compare == 'min' else v[2],
        })

    return {
        'type': type_id,
        'typeName': tinfo['cn'],
        'baseTier': tier,
        'cells': out_cells,
        'baseDurability': int(round(base_dur)),
        'durabilityModifier': dur_mod,
        'durabilityCost': -dur_mod,
        'durability': int(round(base_dur)) + dur_mod,
        'baseDuration': int(round(base_duration)),
        'duration': int(round(duration + base_duration)),
        'charges': charges,
        'skills': reqs,
        'maxSkill': max(reqs.values()) if reqs else 0,
        'totalSkill': sum(reqs.values()),
        'ids': {k: {'min': v[0], 'raw': v[1], 'max': v[2]} for k, v in agg.items()},
        'targets': tgts,
        'score': sum(t['weight'] * t['value'] for t in tgts),
    }


# ----------------------------------------------------------------- 搜索

class Searcher(object):
    """束搜索：逐格放置原料，末层精确评估。"""

    COST_BUCKETS = 6
    REQ_BUCKETS = 4

    def __init__(self, ds, cfg):
        self.ds = ds
        self.cfg = cfg
        self.type_id = cfg['type']
        self.tinfo = TYPE_BY_ID[self.type_id]
        self.consumable = self.tinfo['kind'] == 'consumable'
        self.targets = targets_of(cfg)
        self.tkeys = [t['key'] for t in self.targets]
        self.weights = np.array([t['weight'] for t in self.targets], dtype=np.float64)
        self.tmins = [t['min'] for t in self.targets]
        # 带下限的目标：搜索时要被「引导」，否则权重为 0 时根本搜不到满足下限的组合
        self.pinned = [(i, m) for i, m in enumerate(self.tmins) if m is not None]
        self.penalty_weight = float(cfg.get('penaltyWeight', 1.0) or 1.0)
        self.compare = cfg.get('compare', 'max')
        self.min_dur = cfg.get('minDurability')
        self.limits = points_limits(cfg)
        self.limit_keys = [s for s in SKILL_KEYS if self.limits[s] is not None]
        self.top_n = int(cfg.get('topN', 20) or 20)
        self.beam = max(20, int(cfg.get('beam', 800) or 800))
        self.cand_limit = max(8, int(cfg.get('candidateLimit', 70) or 70))
        self.filler_limit = max(0, int(cfg.get('fillerLimit', 18) or 0))
        self.support_limit = max(0, int(cfg.get('supportLimit', 12) or 0))
        self.allow_dupes = bool(cfg.get('allowDuplicates', True))
        self.disabled = set(x for x in (cfg.get('disabled') or []) if x)
        self.base_tier = base_tier_of(cfg, self.type_id)
        self.base_dur = base_durability_for(cfg, self.type_id)[self.base_tier - 1]
        self.base_duration = float((cfg.get('consumableBase') or {}).get(self.type_id, 0) or 0)
        self.cands = self._pick_candidates()

    # -- 候选筛选
    def _pool_scales(self, pool):
        """每个目标词条的「可达上限」：同职业最好的原料 × 6，用于把权重归一化。"""
        scales = []
        for k in self.tkeys:
            best = 0.0
            for ing in pool:
                v = ing['ids'].get(k)
                if v and v[2] > best:
                    best = v[2]
            scales.append(best * 6.0 if best > 0 else 1.0)
        return np.array(scales, dtype=np.float64)

    def _weighted_max(self, ing):
        """单个原料的归一化加权得分（用于挑候选）。"""
        s = 0.0
        for t, (w, k) in enumerate(zip(self.weights, self.tkeys)):
            v = ing['ids'].get(k)
            if v:
                s += w * v[2] / self.scales[t]
        return s

    def _norm_values(self, vals):
        """(B, T) -> 归一化加权得分 (B,)"""
        if not len(self.tkeys):
            return np.zeros(vals.shape[0])
        return (vals / self.scales * self.weights).sum(axis=1)

    def _penalty(self, vals):
        """低于下限的惩罚（按该词条可达上限归一化），0 表示全部达标。"""
        if not self.pinned:
            return 0.0
        pen = 0.0
        for t_idx, mn in self.pinned:
            pen = pen + np.maximum(0.0, mn - vals[:, t_idx]) / self.scales[t_idx]
        return pen

    def _pick_candidates(self):
        profs = set(self.tinfo['professions'])
        pool = [ing for ing in self.ds.items
                if (profs & set(ing['professions'])) and ing['id'] not in self.disabled]
        self.scales = self._pool_scales(pool)
        scored = [(self._weighted_max(ing), ing) for ing in pool]
        scored.sort(key=lambda x: -x[0])
        # 有正贡献的优先；若全是 0/负（例如给了负权重），就退化成按分数排序全收
        positive = [x for x in scored if x[0] > 0]
        cands = [ing for _, ing in (positive if positive else scored)[:self.cand_limit]]
        if len(cands) < 6:  # 目标词条太冷门，补充其它同职业原料
            for ing in pool:
                if ing not in cands:
                    cands.append(ing)
                if len(cands) >= self.cand_limit:
                    break
        seen = set(x['id'] for x in cands)
        # 有耐久/点数约束时，补一批「最不耗耐久」的原料（含正耐久原料）
        if self.min_dur is not None or self.limit_keys:
            by_cost = sorted(pool, key=lambda i: (-i['durability'], -self._weighted_max(i)))
            for ing in by_cost[:self.filler_limit]:
                if ing['id'] not in seen:
                    seen.add(ing['id'])
                    cands.append(ing)
        # 再补一批「纯辅助」原料：自身没有目标词条，但相邻加成很高
        if self.support_limit:
            supports = sorted(pool, key=lambda i: -sum(max(0, v) for v in i['pos'].values()))
            for ing in supports[:self.support_limit]:
                if ing['id'] not in seen:
                    seen.add(ing['id'])
                    cands.append(ing)
        # 有下限的词条：即使权重是 0，也要保证候选池里有它的高产原料
        for t_idx, _mn in self.pinned:
            k = self.tkeys[t_idx]
            providers = sorted(pool, key=lambda i: -(i['ids'].get(k, (0, 0, 0))[2]))
            for ing in providers[:12]:
                if ing['id'] not in seen:
                    seen.add(ing['id'])
                    cands.append(ing)
        self.n = len(cands)
        cands = cands[:self.n]

        T = len(self.tkeys)
        self.p_durmod = np.array([i['durability'] for i in cands], dtype=np.float64)
        self.p_dur = np.array([i['duration'] for i in cands], dtype=np.float64)
        self.p_tmin = np.array([[i['ids'].get(k, (0, 0, 0))[0] for k in self.tkeys]
                                for i in cands], dtype=np.float64).reshape(len(cands), T)
        self.p_tmax = np.array([[i['ids'].get(k, (0, 0, 0))[2] for k in self.tkeys]
                                for i in cands], dtype=np.float64).reshape(len(cands), T)
        self.p_req = np.array([[i['req'][s] for s in SKILL_KEYS] for i in cands],
                              dtype=np.float64)
        # G[i][j][c] = 原料 c 放在第 i 格时授予第 j 格的值
        self.G = [[None] * 6 for _ in range(6)]
        for i in range(6):
            for j in range(6):
                if i == j:
                    continue
                keys = PAIR[j][i]
                if keys:
                    self.G[i][j] = np.array(
                        [sum(ing['pos'][k] for k in keys) for ing in cands], dtype=np.float64)
        if self.consumable:
            self.metric_min = float((-self.p_dur).min()) if len(self.p_dur) else 0.0
        else:
            # 指标 = -耐久修正，越小越省耐久（正耐久原料会被排到最前面）
            self.metric_min = float((-self.p_durmod).min()) if len(self.p_durmod) else 0.0
        return cands

    # -- 批量打分（k 个格子已放）
    def score(self, seqs, k):
        A = np.asarray(seqs, dtype=np.int64).reshape(len(seqs), k)
        bonus = np.zeros((len(seqs), k), dtype=np.float64)
        for i in range(k):
            for j in range(k):
                if i == j or self.G[i][j] is None:
                    continue
                bonus[:, j] += self.G[i][j][A[:, i]]
        factor = (100.0 + bonus) / 100.0
        T = len(self.tkeys)
        vmax = np.zeros((len(seqs), T), dtype=np.float64)
        vmin = np.zeros((len(seqs), T), dtype=np.float64)
        for t in range(T):
            vmax[:, t] = np.trunc(self.p_tmax[A, t] * factor).sum(axis=1)
            vmin[:, t] = np.trunc(self.p_tmin[A, t] * factor).sum(axis=1)
        key_max = self._norm_values(vmax) - self.penalty_weight * self._penalty(vmax)
        key_min = self._norm_values(vmin) - self.penalty_weight * self._penalty(vmin)
        return key_max, key_min, bonus, A, vmax, vmin

    def _req_array(self, A, bonus):
        return np.trunc(self.p_req[A] * ((100.0 + bonus) / 100.0)[:, :, None]).sum(axis=1)

    # -- 束选择：无约束时纯按目标值；有约束时分桶，保证搜索多样性
    def _beam_select(self, expand, k, key, bonus, A):
        tight_dur = self.min_dur is not None
        tight_req = bool(self.limit_keys)
        if not tight_dur and not tight_req:
            order = np.argsort(-key)[:self.beam]
            return [expand[int(i)] for i in order]

        n = len(expand)
        idx_all = np.arange(n)

        if tight_dur:
            # 装备用「耐久消耗」、消耗品用「-持续时间」，都是越小越好
            if self.consumable:
                metric = -self.p_dur[A].sum(axis=1)
                limit = self.base_duration - float(self.min_dur)
                scale = max(1.0, float(abs(self.p_dur).max()) * 6.0)
            else:
                # 指标 = 耐久修正之和取负，越小越省耐久
                metric = -self.p_durmod[A].sum(axis=1)
                limit = self.base_dur - float(self.min_dur)
                scale = max(1.0, float(abs(self.p_durmod).max()) * 6.0)
            best_case = metric + (6 - k) * self.metric_min
            keep = best_case <= limit
            if keep.any():
                idx_all = idx_all[keep]
                metric = metric[keep]
                A = A[keep]
                bonus = bonus[keep]
                key = key[keep]
                n = len(idx_all)
            cw = max(1.0, scale / self.COST_BUCKETS)
            cb = np.clip((metric * (6.0 / k) / cw).astype(np.int64), 0, self.COST_BUCKETS - 1)
        else:
            cb = np.zeros(n, dtype=np.int64)

        if tight_req:
            req = self._req_array(A, bonus)
            ratio = np.zeros(n, dtype=np.float64)
            for s in self.limit_keys:
                i = SKILL_KEYS.index(s)
                ratio = np.maximum(ratio, req[:, i] / max(1.0, self.limits[s]))
            rb = np.clip((ratio * (6.0 / k) * self.REQ_BUCKETS).astype(np.int64),
                         0, self.REQ_BUCKETS)
        else:
            rb = np.zeros(n, dtype=np.int64)

        bucket = cb * (self.REQ_BUCKETS + 1) + rb
        keep_per = max(16, self.beam // (self.COST_BUCKETS * (self.REQ_BUCKETS + 1)))
        counts = {}
        picked = []
        for i in np.argsort(-key):
            b = int(bucket[i])
            c = counts.get(b, 0)
            if c >= keep_per:
                continue
            counts[b] = c + 1
            picked.append(int(idx_all[i]))
            if len(picked) >= self.beam:
                break
        return [expand[i] for i in picked]

    # -- 主流程
    def run(self):
        t0 = time.time()
        n = self.n
        if not bool(np.any(self.weights)):
            return {'results': [], 'elapsedMs': 0,
                    'message': '所有目标词条的权重都是 0，无法排序；请至少给一个词条非 0 权重',
                    'code': 'all_zero_weights'}
        if n == 0 or not self.tkeys:
            return {'results': [], 'elapsedMs': 0,
                    'message': '没有可用原料', 'code': 'no_candidates'}

        beam = [()]
        no_dupes = self.allow_dupes is False and n >= 6
        for depth in range(6):
            expand = []
            if no_dupes:
                for seq in beam:
                    for ci in range(n):
                        if ci in seq:
                            continue
                        expand.append(seq + (ci,))
            else:
                for seq in beam:
                    for ci in range(n):
                        expand.append(seq + (ci,))
            k = depth + 1
            if k < 6:
                key, _, bonus, A, _, _ = self.score(expand, k)
                beam = self._beam_select(expand, k, key, bonus, A)
            else:
                beam = expand

        key_max, key_min, bonus, A, vmax, vmin = self.score(beam, 6)
        dur = self.base_dur + self.p_durmod[A].sum(axis=1)
        duration = self.p_dur[A].sum(axis=1) + self.base_duration
        req = self._req_array(A, bonus)
        key = key_max if self.compare == 'max' else key_min
        vals = vmax if self.compare == 'max' else vmin

        mask = np.ones(len(beam), dtype=bool)
        if self.min_dur is not None:
            mask &= (duration >= float(self.min_dur)) if self.consumable else (dur >= float(self.min_dur))
        for s in self.limit_keys:
            i = SKILL_KEYS.index(s)
            mask &= req[:, i] <= float(self.limits[s])
        for t, mn in enumerate(self.tmins):
            if mn is not None:
                mask &= vals[:, t] >= mn

        idx = np.where(mask)[0]
        if len(idx) == 0:
            return {'results': [], 'elapsedMs': int((time.time() - t0) * 1000),
                    'message': '没有满足约束的组合，试试放宽耐久/时间/点数/词条下限',
                    'code': 'no_feasible'}

        order = idx[np.argsort(-key[idx])]
        seen = set()
        picked = []
        for i in order:
            seq = beam[int(i)]
            keytu = tuple(sorted(seq))
            if keytu in seen:
                continue
            seen.add(keytu)
            picked.append((int(i), seq))
            if len(picked) >= self.top_n:
                break

        results = []
        for i, seq in picked:
            ids_list = [self.cands[c]['id'] for c in seq]
            res = evaluate(self.ds, self.cfg, ids_list)
            res['score'] = round(float(key[i]), 4)
            results.append(res)

        return {
            'results': results,
            'elapsedMs': int((time.time() - t0) * 1000),
            'scanned': int(len(beam)),
            'candidates': n,
        }


# ----------------------------------------------------------------- 自检

def _selftest():
    ds = Dataset()
    print('原料 %d，词条键 %d' % (len(ds.items), len(ds.id_keys)))
    print('\n相对位置 -> 加成键（中心为自身，对照官网 EFFECTIVENESS 网格）:')
    for dr in (-2, -1, 0, 1, 2):
        row = []
        for dc in (-1, 0, 1):
            keys = keys_at(dr, dc)
            row.append(','.join(keys) if keys else '-')
        print('  dr=%+d  %s' % (dr, ' | '.join('%-22s' % x for x in row)))

    ing = ds.items[0]
    print('\n样例原料: %s  加成表 %s' % (ing['name'], ing['pos']))
    cfg = {'type': 'sword', 'baseDurability': {}, 'baseTier': {'sword': 1},
           'targets': [{'key': 'rawHealth', 'weight': 1}]}
    r = evaluate(ds, cfg, [ing['id']] * 6)
    print('6 个同原料 -> 耐久 %d (基础 %d - 消耗 %d), 每格加成 %s'
          % (r['durability'], r['baseDurability'], r['durabilityCost'],
             [c['bonus'] for c in r['cells']]))


if __name__ == '__main__':
    _selftest()
