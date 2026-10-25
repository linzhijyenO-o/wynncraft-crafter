# -*- coding: utf-8 -*-
"""引擎自检：手工算例 + 束搜索 vs 暴力枚举比对。"""
import itertools
import sys
import time

import numpy as np

sys.path.insert(0, r'D:\C++\wynnbd\crafter\backend')
import engine as E

ds = E.Dataset()


def cfg_of(tgt, **kw):
    c = {
        'type': 'sword',
        'baseDurability': {},
        'baseTier': {'sword': 1},
        'targets': [{'key': tgt, 'weight': 1, 'min': None}],
        'compare': 'max',
        'topN': 5,
    }
    c.update(kw)
    return c


# ---------------------------------------------------------------- 1. 手工算例
sample = max(ds.items, key=lambda i: sum(abs(v) for v in i['pos'].values()))
print('样例原料:', sample['name'], sample['pos'])

cfg = cfg_of('rawHealth')
r = E.evaluate(ds, cfg, [sample['id']] * 6)
expect = []
for cell in range(6):
    total = 0
    for src in range(6):
        if src == cell:
            continue
        for k in E.PAIR[cell][src]:
            total += sample['pos'][k]
    expect.append(total)
assert [c['bonus'] for c in r['cells']] == expect, '加成计算不一致'
print('  每格加成:', [c['bonus'] for c in r['cells']], '✓')

# 基础耐久只看物品种类+档位
r0 = E.evaluate(ds, cfg_of('rawHealth', baseTier={'sword': 3},
                           baseDurability={'sword': [700, 800, 900, 1000, 1100, 1200]}),
                [sample['id']] * 6)
assert r0['baseDurability'] == 900, r0['baseDurability']
assert r0['durability'] == 900 - r0['durabilityCost']
print('  档位取基础耐久: 档3 -> %d ✓' % r0['baseDurability'])

# 取整规则：负数向 0
assert E.trunc(-3.9) == -3 and E.trunc(3.9) == 3

# ---------------------------------------------------------------- 2. 束搜索 vs 暴力


def brute(cfg, limit=9, topn=5):
    s = E.Searcher(ds, dict(cfg, candidateLimit=limit, supportLimit=0, fillerLimit=0))
    n = len(s.cands)
    seqs = list(itertools.product(range(n), repeat=6))
    vals = []
    for i in range(0, len(seqs), 200000):
        chunk = seqs[i:i + 200000]
        key_max, _, _, _, _, _ = s.score(chunk, 6)
        vals.append(key_max)
    v = np.concatenate(vals)
    order = np.argsort(-v)[:topn]
    return [(seqs[i], float(v[i])) for i in order]


def beam(cfg):
    return E.Searcher(ds, dict(cfg, candidateLimit=9, beam=400000,
                               supportLimit=0, fillerLimit=0)).run()


for tgt in ['rawSpellDamage', 'rawHealth', 'thorns']:
    c = cfg_of(tgt, topN=5)
    t0 = time.time()
    res = beam(c)
    t1 = time.time()
    exact = brute(c, topn=5)
    print('\n[%s] 束搜索 %.2fs / 暴力 %.2fs' % (tgt, t1 - t0, time.time() - t1))
    print('  束搜索前3:', [round(r['score'], 1) for r in res['results'][:3]])
    print('  暴力前3  :', [v for _, v in exact[:3]])
    assert res['results'], '束搜索没有结果'
    assert abs(res['results'][0]['score'] - exact[0][1]) < 1e-3, '最优值不一致'

# ---------------------------------------------------------------- 3. 多目标 + 五项点数 + 耐久
cfg = cfg_of('rawHealth', topN=5, beam=1500,
             targets=[{'key': 'rawHealth', 'weight': 1, 'min': 3000},
                      {'key': 'rawDefence', 'weight': 2, 'min': None}],
             minDurability=1500,
             baseDurability={'sword': [2500, 2600, 2700, 2800, 2900, 3000]},
             pointsLimit={'defence': 30, 'strength': 10})
t0 = time.time()
res = E.Searcher(ds, cfg).run()
print('\n多目标+约束: %d 条, %.2fs, 候选 %d' % (len(res['results']), time.time() - t0, res.get('candidates', -1)))
assert res['results'], '多目标约束搜索没有结果: %s' % res.get('message')
for r in res['results'][:3]:
    t = {x['key']: x['value'] for x in r['targets']}
    print('  耐久 %d  点数 %s  rawHealth %s rawDefence %s  score %.0f'
          % (r['durability'], {k: v for k, v in r['skills'].items() if v},
             t['rawHealth'], t['rawDefence'], r['score']))
    assert r['durability'] >= 1500
    assert r['skills']['defence'] <= 30 and r['skills']['strength'] <= 10
    assert t['rawHealth'] >= 3000

print('\n全部通过')
