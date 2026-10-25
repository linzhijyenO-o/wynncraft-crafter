# -*- coding: utf-8 -*-
"""独立对拍：直接从 raw/ ingredients_raw.json 按规则手算，和引擎结果比对。"""
import io
import json
import sys

raw = json.load(io.open(r'D:\C++\wynnbd\raw\ingredients_raw.json', encoding='utf-8-sig'))
by_name = {it['displayName']: it for it in raw['items']}

sys.path.insert(0, r'D:\C++\wynnbd\crafter\backend')
import engine as E

ds = E.Dataset()

TARGET = 'rawHealth'
LAYOUT = ['Peculiar Oddity', 'Linear Accelerator', 'Peculiar Oddity',
          'Linear Accelerator', 'Peculiar Oddity', 'Linear Accelerator']

# ---------------- 独立实现（只依赖 raw JSON 的字段名）
def pos(it, key):
    return (it.get('ingredientPositionModifiers') or {}).get(key, 0)


def bonus_of(cells, i):
    total = 0
    rt, ct = divmod(i, 2)
    for j, it in enumerate(cells):
        if j == i:
            continue
        rs, cs = divmod(j, 2)
        dr, dc = rt - rs, ct - cs
        if dr == 0:
            total += pos(it, 'left' if dc < 0 else 'right')
        elif dc == 0:
            total += pos(it, 'above' if dr < 0 else 'under')
        if abs(dr) + abs(dc) == 1:
            total += pos(it, 'touching')
        else:
            total += pos(it, 'notTouching')
    return total


cells = [by_name[x] for x in LAYOUT]
bonus = [bonus_of(cells, i) for i in range(6)]
print('独立算的每格加成:', bonus)

dur_base = 0
cost = 0
ids = {}
for i, it in enumerate(cells):
    f = (100 + bonus[i]) / 100.0
    cost += abs(it['itemOnlyIDs']['durabilityModifier']) / 1000.0
    for k, v in (it.get('identifications') or {}).items():
        cur = ids.setdefault(k, [0, 0, 0])
        cur[0] += int(v['min'] * f)
        cur[1] += int(v['raw'] * f)
        cur[2] += int(v['max'] * f)

print('独立算的耐久: %d = %d - %d' % (1500 - cost, 1500, cost))
print('独立算的词条:', {k: v for k, v in ids.items()})

# ---------------- 引擎结果
res = E.evaluate(ds, {'type': 'sword',
                      'baseDurability': {'sword': [1500, 1600, 1700, 1800, 1900, 2000]},
                      'baseTier': {'sword': 1},
                      'targets': [{'key': TARGET, 'weight': 1}]}, LAYOUT)
print('引擎每格加成 :', [c['bonus'] for c in res['cells']])
print('引擎耐久     :', res['durability'], '基础', res['baseDurability'], '消耗', res['durabilityCost'])
print('引擎词条     :', {k: [v['min'], v['raw'], v['max']] for k, v in res['ids'].items()})

assert [c['bonus'] for c in res['cells']] == bonus, '加成不一致'
assert res['durability'] == 1500 - cost, '耐久不一致'
for k, v in ids.items():
    got = res['ids'][k]
    assert [got['min'], got['raw'], got['max']] == v, '词条 %s 不一致: %s vs %s' % (k, [got['min'], got['raw'], got['max']], v)
assert set(ids) == set(res['ids']), '词条集合不一致'
print('\n对拍通过 ✓')
