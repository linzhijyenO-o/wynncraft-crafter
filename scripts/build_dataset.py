# -*- coding: utf-8 -*-
"""
把 raw/ingredients_raw.json 规范化成多份可用的数据文件。

设计原则
--------
1. 原始数据不改写，单独保存在 raw/ 下，任何推导都能回溯。
2. 字段名统一成 snake_case；单位统一（durabilityModifier /1000，duration 单位秒）。
3. 每个属性都落成「命名空间:值」形式的标签，便于过滤与检索。
4. 除主表外再导出两张 long/tidy 表（词条、掉落），方便直接进数据库。

输出（全部在 <root>/data 下）
    ingredients.json              规范化主数据（嵌套 + tags）
    ingredients.csv               主表（宽表，一行一个物品）
    ingredient_identifications.csv 词条长表（一行一个 物品×词条）
    ingredient_drops.csv          掉落长表（一行一个 物品×掉落源）
    tags.json                     标签词表 + 计数
    tag_index.json                标签 -> 物品 id 列表
    tags.md                       标签字典（中文说明）
    ingredients.md                按职业分组的可读清单
"""
from __future__ import print_function

import csv
import io
import json
import os
import re
import sys
from collections import Counter, OrderedDict, defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'raw', 'ingredients_raw.json')
OUT = os.path.join(ROOT, 'data')

API = ('POST https://api.wynncraft.com/v3/item/search  '
       'body: {"type":["ingredient"]}')

# ---------------------------------------------------------------- 词表

TIER_NAMES = OrderedDict([
    ('TIER_0', ('Normal',    '#ffffff')),
    ('TIER_1', ('Unique',    '#ffdc50')),
    ('TIER_2', ('Rare',      '#ff50e8')),
    ('TIER_3', ('Legendary', '#50fdff')),
])

PROFESSIONS = OrderedDict([
    ('armouring',      '防具锻造'),
    ('tailoring',      '裁缝'),
    ('weaponsmithing', '武器锻造'),
    ('woodworking',    '木工'),
    ('jeweling',       '珠宝'),
    ('cooking',        '烹饪'),
    ('alchemism',      '炼金'),
    ('scribing',       '铭文'),
])

ITEM_IDS = OrderedDict([
    ('durabilityModifier',       ('durability', '耐久度修正', 0.001)),
    ('strengthRequirement',      ('strength',   '力量需求',   1)),
    ('dexterityRequirement',     ('dexterity',  '敏捷需求',   1)),
    ('intelligenceRequirement',  ('intelligence', '智力需求', 1)),
    ('defenceRequirement',       ('defence',    '防御需求',   1)),
    ('agilityRequirement',       ('agility',    '技巧需求',   1)),
])

POSITION_KEYS = OrderedDict([
    ('left',       '左侧'),
    ('right',      '右侧'),
    ('above',      '上方'),
    ('under',      '下方'),
    ('touching',   '相邻'),
    ('notTouching', '不相邻'),
])

CONSUMABLE_KEYS = OrderedDict([
    ('duration', '持续时间(秒)'),
    ('charges',  '使用次数'),
])

# (中文名, 说明, 类别)  类别 categorical=枚举值标签 / value=带数值的明细标签
NAMESPACE_DOC = OrderedDict([
    ('type',           ('物品大类', '对象类型；目前抓取范围内恒为 ingredient', 'categorical')),
    ('tier',           ('阶级', '0=Normal 1=Unique 2=Rare 3=Legendary', 'categorical')),
    ('tier-name',      ('阶级名', '与 tier 一一对应的英文名', 'categorical')),
    ('profession',     ('制作职业', '该材料可用于哪些职业的配方', 'categorical')),
    ('crafting-level', ('制作等级', '可用于配方的最低制作等级 1-119', 'categorical')),
    ('emblem',         ('徽记', '物品图标底框样式', 'categorical')),
    ('id',             ('词条 ID', 'identifications 的键，即物品提供的属性词条', 'categorical')),
    ('item',           ('成品属性', '只作用于成品(装备)的属性，格式 item:属性:数值', 'value')),
    ('consumable',     ('消耗品属性', '只作用于消耗品(卷轴/药水)的属性，格式 consumable:属性:数值', 'value')),
    ('position',       ('相邻加成', '配方格相对位置的效果加成(%)，格式 position:位置:数值', 'value')),
])


# ---------------------------------------------------------------- 工具

def read_json(path):
    with io.open(path, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


def write_json(path, obj):
    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, sort_keys=False)
        f.write(u'\n')


def write_csv(path, header, rows):
    with io.open(path, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def label_of(key):
    """rawHealth -> Raw Health ; 2ndSpellCost -> 2nd Spell Cost"""
    s = re.sub(r'(?<=[a-z0-9])(?=[A-Z])', ' ', key)
    s = re.sub(r'(?<=[A-Z])(?=[A-Z][a-z])', ' ', s)
    if s:
        s = s[0].upper() + s[1:]
    return s


def num(x):
    """把 0.001 缩放后的浮点数还原成干净的数字/字符串"""
    if isinstance(x, float):
        if x == int(x):
            return int(x)
        return round(x, 3)
    return x


def fmt_num(v):
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v)


def signed(v):
    return ('+%s' % fmt_num(v)) if v > 0 else fmt_num(v)


# ---------------------------------------------------------------- 规范化

def normalize(item):
    tier_code = item.get('tier', 'TIER_0')
    tier_level = int(tier_code.replace('TIER_', '')) if tier_code.startswith('TIER_') else -1
    tier_name, tier_color = TIER_NAMES.get(tier_code, ('Unknown', '#ffffff'))

    req = item.get('requirements') or {}
    skills = sorted(req.get('skills') or [])
    level = req.get('level')

    item_ids_raw = item.get('itemOnlyIDs') or {}
    item_ids = OrderedDict()
    for api_key, (norm_key, _zh, factor) in ITEM_IDS.items():
        v = item_ids_raw.get(api_key, 0) or 0
        item_ids[norm_key] = num(v * factor)

    cons_raw = item.get('consumableOnlyIDs') or {}
    cons = OrderedDict()
    for k in CONSUMABLE_KEYS:
        cons[k] = num(cons_raw.get(k, 0) or 0)

    pos_raw = item.get('ingredientPositionModifiers') or {}
    pos = OrderedDict()
    for k in POSITION_KEYS:
        pos[snake(k)] = num(pos_raw.get(k, 0) or 0)

    ids = []
    for k, v in sorted((item.get('identifications') or {}).items()):
        if isinstance(v, dict):
            ids.append(OrderedDict([
                ('id', k), ('label', label_of(k)),
                ('min', num(v.get('min'))), ('raw', num(v.get('raw'))),
                ('max', num(v.get('max'))),
            ]))
        else:  # 理论上不会出现，兜底
            ids.append(OrderedDict([
                ('id', k), ('label', label_of(k)),
                ('min', num(v)), ('raw', num(v)), ('max', num(v)),
            ]))

    drops = []
    seen_drops = set()
    raw_drop_count = 0
    for d in (item.get('droppedBy') or []):
        raw_drop_count += 1
        coords = d.get('coords') or []
        key = (d.get('name'), json.dumps(coords, sort_keys=True))
        if key in seen_drops:      # 接口偶尔重复返回同一条掉落，规范化时去重
            continue
        seen_drops.add(key)
        drops.append(OrderedDict([
            ('name', d.get('name')),
            ('has_coords', bool(coords)),
            ('coords', coords),
        ]))

    rec = OrderedDict()
    rec['id'] = item.get('internalName')
    rec['name'] = item.get('displayName')
    rec['type'] = item.get('type')
    rec['tier'] = OrderedDict([('code', tier_code), ('level', tier_level),
                               ('name', tier_name), ('color', tier_color)])
    rec['crafting_level'] = level
    rec['professions'] = skills
    rec['emblem'] = item.get('emblem')
    rec['icon'] = item.get('icon')
    rec['item_ids'] = item_ids
    rec['consumable_ids'] = cons
    rec['position_modifiers'] = pos
    rec['identifications'] = ids
    rec['drops'] = drops
    rec['drop_entries_raw'] = raw_drop_count
    rec['tags'] = build_tags(rec)
    return rec


def snake(k):
    return re.sub(r'(?<=[a-z0-9])(?=[A-Z])', '_', k).lower()


def build_tags(rec):
    tags = ['type:%s' % rec['type']]
    tags.append('tier:%s' % rec['tier']['level'])
    tags.append('tier-name:%s' % rec['tier']['name'])
    for p in rec['professions']:
        tags.append('profession:%s' % p)
    tags.append('crafting-level:%s' % rec['crafting_level'])
    tags.append('emblem:%s' % rec['emblem'])

    for k, v in rec['item_ids'].items():
        if v:
            tags.append('item:%s:%s' % (k, signed(v)))
    for k, v in rec['consumable_ids'].items():
        if v:
            tags.append('consumable:%s:%s' % (k, signed(v)))
    for k, v in rec['position_modifiers'].items():
        if v:
            tags.append('position:%s:%s' % (k, signed(v)))
    for i in rec['identifications']:
        tags.append('id:%s' % i['id'])
    return tags


# ---------------------------------------------------------------- 导出

def unique_names(drops):
    seen = []
    for d in drops:
        if d['name'] not in seen:
            seen.append(d['name'])
    return seen


def ids_to_text(ids):
    out = []
    for i in ids:
        if i['min'] == i['max']:
            out.append(u'%s=%s' % (i['id'], fmt_num(i['min'])))
        else:
            out.append(u'%s=%s~%s' % (i['id'], fmt_num(i['min']), fmt_num(i['max'])))
    return u'; '.join(out)


def drops_to_text(drops):
    out = []
    for d in drops:
        suffix = (' (%d处坐标)' % len(d['coords'])) if d['has_coords'] else ''
        out.append(u'%s%s' % (d['name'], suffix))
    return u'; '.join(out)


def main():
    if not os.path.exists(RAW):
        sys.exit('缺少 %s，请先运行 scripts/fetch_ingredients.ps1' % RAW)

    raw = read_json(RAW)
    items = raw['items']
    if os.path.isdir(OUT):
        for fn in os.listdir(OUT):
            if fn.endswith(('.json', '.csv', '.md')):
                os.remove(os.path.join(OUT, fn))
    else:
        os.makedirs(OUT)

    records = [normalize(it) for it in items]

    # 校验
    ids = [r['id'] for r in records]
    assert len(ids) == len(set(ids)), 'internalName 有重复'
    assert all(r['type'] == 'ingredient' for r in records), '混入了非 ingredient'
    assert all(r['tier']['level'] >= 0 for r in records), '未知 tier'

    records.sort(key=lambda r: (r['tier']['level'], r['crafting_level'], r['name']))

    generated_at = datetime.now().astimezone().isoformat(timespec='seconds')

    # ---- 1. ingredients.json
    write_json(os.path.join(OUT, 'ingredients.json'), OrderedDict([
        ('source', API),
        ('source_page', 'https://wynncraft.com/help/item-guide'),
        ('fetched_at', raw.get('fetched_at')),
        ('generated_at', generated_at),
        ('count', len(records)),
        ('tier_names', TIER_NAMES),
        ('profession_names', PROFESSIONS),
        ('items', records),
    ]))

    # ---- 2. ingredients.csv
    header = [
        'id', 'name', 'type', 'tier_level', 'tier_name', 'tier_code', 'crafting_level',
        'professions', 'emblem', 'icon_format',
        'durability', 'strength_req', 'dexterity_req', 'intelligence_req',
        'defence_req', 'agility_req',
        'duration', 'charges',
        'pos_left', 'pos_right', 'pos_above', 'pos_under', 'pos_touching', 'pos_not_touching',
        'id_count', 'identifications', 'drop_count', 'drops', 'tags',
    ]
    rows = []
    for r in records:
        ii = r['item_ids']
        cc = r['consumable_ids']
        pp = r['position_modifiers']
        rows.append([
            r['id'], r['name'], r['type'], r['tier']['level'], r['tier']['name'],
            r['tier']['code'], r['crafting_level'], ';'.join(r['professions']),
            r['emblem'], (r['icon'] or {}).get('format'),
            fmt_num(ii['durability']), fmt_num(ii['strength']), fmt_num(ii['dexterity']),
            fmt_num(ii['intelligence']), fmt_num(ii['defence']), fmt_num(ii['agility']),
            fmt_num(cc['duration']), fmt_num(cc['charges']),
            fmt_num(pp['left']), fmt_num(pp['right']), fmt_num(pp['above']),
            fmt_num(pp['under']), fmt_num(pp['touching']), fmt_num(pp['not_touching']),
            len(r['identifications']), ids_to_text(r['identifications']),
            len(r['drops']), drops_to_text(r['drops']), ' '.join(r['tags']),
        ])
    write_csv(os.path.join(OUT, 'ingredients.csv'), header, rows)

    # ---- 3. 词条长表
    rows = []
    for r in records:
        for i in r['identifications']:
            rows.append([r['id'], r['name'], i['id'], i['label'],
                         fmt_num(i['min']), fmt_num(i['raw']), fmt_num(i['max'])])
    write_csv(os.path.join(OUT, 'ingredient_identifications.csv'),
              ['item_id', 'item_name', 'identification', 'label', 'min', 'raw', 'max'], rows)

    # ---- 4. 掉落长表
    rows = []
    for r in records:
        for d in r['drops']:
            rows.append([r['id'], r['name'], d['name'], len(d['coords']),
                         json.dumps(d['coords'], ensure_ascii=False)])
    write_csv(os.path.join(OUT, 'ingredient_drops.csv'),
              ['item_id', 'item_name', 'drop_name', 'coord_count', 'coords'], rows)

    # ---- 5. 标签词表
    counter = Counter()
    index = defaultdict(list)
    for r in records:
        for t in r['tags']:
            counter[t] += 1
            index[t].append(r['id'])

    by_ns = defaultdict(list)
    for t, c in counter.items():
        ns = t.split(':', 1)[0]
        by_ns[ns].append((t, c))

    tag_list = []
    for ns in NAMESPACE_DOC:
        for t, c in sorted(by_ns.get(ns, []), key=lambda x: (-x[1], x[0])):
            tag_list.append(OrderedDict([
                ('tag', t), ('namespace', ns), ('count', c),
                ('share', round(c / float(len(records)), 4)),
            ]))

    write_json(os.path.join(OUT, 'tags.json'), OrderedDict([
        ('generated_at', generated_at),
        ('source', API),
        ('item_count', len(records)),
        ('namespaces', [OrderedDict([('prefix', k), ('name', v[0]),
                                      ('description', v[1]), ('kind', v[2])])
                        for k, v in NAMESPACE_DOC.items()]),
        ('tags', tag_list),
    ]))

    write_json(os.path.join(OUT, 'tag_index.json'), OrderedDict([
        ('generated_at', generated_at),
        ('item_count', len(records)),
        ('index', OrderedDict((t, sorted(index[t])) for t in sorted(index))),
    ]))

    # ---- 5b. 掉落源 -> 物品 反查索引
    drop_index = defaultdict(set)
    for r in records:
        for d in r['drops']:
            if d['name']:
                drop_index[d['name']].add(r['id'])
    write_json(os.path.join(OUT, 'drop_index.json'), OrderedDict([
        ('generated_at', generated_at),
        ('source', API),
        ('drop_source_count', len(drop_index)),
        ('index', OrderedDict((k, sorted(v)) for k, v in sorted(drop_index.items()))),
    ]))

    # ---- 6. 中文标签字典
    write_tags_md(os.path.join(OUT, 'tags.md'), generated_at, len(records), by_ns, counter)

    # ---- 7. 可读清单
    write_ingredients_md(os.path.join(OUT, 'ingredients.md'), generated_at, records)

    print('OK: %d ingredients -> %s' % (len(records), OUT))
    print('    %d distinct tags, %d identification keys' % (
        len(counter), len(set(i['id'] for r in records for i in r['identifications']))))


def write_tags_md(path, generated_at, n, by_ns, counter):
    L = []
    L.append(u'# Wynncraft Ingredient 标签字典\n')
    L.append(u'- 生成时间：%s' % generated_at)
    L.append(u'- 数据来源：`%s`' % API)
    L.append(u'- 物品总数：%d' % n)
    L.append(u'- 标签种类：%d\n' % sum(len(v) for v in by_ns.values()))

    L.append(u'## 一、命名空间\n')
    L.append(u'所有标签统一写成 `命名空间:值`，值内部若还有分量则写成 `命名空间:分量:数值`。\n')
    L.append(u'`categorical` 是枚举型标签（可当分类维度），`value` 是带数值的明细标签（本质是属性表被摊平）。\n')
    L.append(u'| 命名空间 | 中文 | 含义 | 类别 | 标签数 |')
    L.append(u'| --- | --- | --- | --- | --- |')
    for ns, (zh, desc, kind) in NAMESPACE_DOC.items():
        L.append(u'| `%s` | %s | %s | %s | %d |' % (ns, zh, desc, kind, len(by_ns.get(ns, []))))
    L.append(u'')

    for ns, (zh, desc, kind) in NAMESPACE_DOC.items():
        vals = sorted(by_ns.get(ns, []), key=lambda x: (-x[1], x[0]))
        if not vals:
            continue
        L.append(u'## %s（%s）\n' % (zh, ns))
        L.append(u'> %s\n' % desc)
        L.append(u'| 标签 | 含义 | 物品数 | 占比 |')
        L.append(u'| --- | --- | ---: | ---: |')
        for t, c in vals:
            L.append(u'| `%s` | %s | %d | %.1f%% |' % (t, tag_meaning(ns, t), c, 100.0 * c / n))
        L.append(u'')

    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(u'\n'.join(L))


def tag_meaning(ns, tag):
    parts = tag.split(':')
    if ns == 'type':
        return u'材料'
    if ns == 'tier':
        return TIER_NAMES.get('TIER_%s' % parts[1], ('?', ''))[0]
    if ns == 'tier-name':
        return u'阶级英文名'
    if ns == 'profession':
        return PROFESSIONS.get(parts[1], parts[1])
    if ns == 'crafting-level':
        return u'制作等级 %s' % parts[1]
    if ns == 'emblem':
        return u'图标底框 %s' % parts[1]
    if ns == 'position':
        key = parts[1]
        return u'%s 位置加成 %s%%' % (POSITION_ZH.get(key, key), parts[2])
    if ns == 'item':
        zh = ITEM_ZH.get(parts[1], parts[1])
        return u'%s %s' % (zh, parts[2])
    if ns == 'consumable':
        return u'%s %s' % (CONSUMABLE_ZH.get(parts[1], parts[1]), parts[2])
    if ns == 'id':
        return label_of(parts[1])
    return tag


POSITION_ZH = {'left': u'左侧', 'right': u'右侧', 'above': u'上方', 'under': u'下方',
               'touching': u'相邻', 'not_touching': u'不相邻'}
ITEM_ZH = {'durability': u'耐久度', 'strength': u'力量需求', 'dexterity': u'敏捷需求',
           'intelligence': u'智力需求', 'defence': u'防御需求', 'agility': u'技巧需求'}
CONSUMABLE_ZH = {'duration': u'持续时间', 'charges': u'使用次数'}


def write_ingredients_md(path, generated_at, records):
    L = []
    L.append(u'# Wynncraft Ingredient 全表（%d 件）\n' % len(records))
    L.append(u'- 生成时间：%s' % generated_at)
    L.append(u'- 数据来源：`%s`' % API)
    L.append(u'- 页面：<https://wynncraft.com/help/item-guide>\n')

    # 职业 × 阶级 交叉表
    matrix = defaultdict(Counter)
    for r in records:
        for p in r['professions'] or ['(none)']:
            matrix[p][r['tier']['level']] += 1
    L.append(u'## 职业 × 阶级\n')
    L.append(u'| 职业 | Normal | Unique | Rare | Legendary | 合计 |')
    L.append(u'| --- | ---: | ---: | ---: | ---: | ---: |')
    for p in list(PROFESSIONS) + [k for k in matrix if k not in PROFESSIONS]:
        if p not in matrix:
            continue
        c = matrix[p]
        L.append(u'| %s | %d | %d | %d | %d | %d |' % (
            PROFESSIONS.get(p, p), c[0], c[1], c[2], c[3], sum(c.values())))
    L.append(u'')

    by_prof = defaultdict(list)
    for r in records:
        for p in r['professions'] or ['(none)']:
            by_prof[p].append(r)

    for p in list(PROFESSIONS) + [k for k in by_prof if k not in PROFESSIONS]:
        if p not in by_prof:
            continue
        L.append(u'## %s（%s）\n' % (PROFESSIONS.get(p, p), p))
        L.append(u'| 名称 | 阶级 | 等级 | 耐久 | 消耗品 | 词条 | 掉落 |')
        L.append(u'| --- | --- | ---: | ---: | --- | --- | --- |')
        for r in by_prof[p]:
            cons = []
            for k, v in r['consumable_ids'].items():
                if v:
                    cons.append(u'%s=%s' % (k, fmt_num(v)))
            L.append(u'| %s | %s | %s | %s | %s | %s | %s |' % (
                r['name'], r['tier']['name'], r['crafting_level'],
                fmt_num(r['item_ids']['durability']),
                u' '.join(cons) or u'-',
                u', '.join(i['id'] for i in r['identifications']) or u'-',
                u', '.join(unique_names(r['drops'])) or u'-'))
        L.append(u'')

    with io.open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(u'\n'.join(L))


if __name__ == '__main__':
    main()
