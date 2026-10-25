# -*- coding: utf-8 -*-
"""检查：词条值是否严格用 floor（负数往更小方向）。自动找出现小数的格子。"""
import math
import random
import sys

sys.path.insert(0, r'D:\C++\wynnbd\crafter\backend')
import engine as E

ds = E.Dataset()
cfg = {'type': 'spear', 'baseDurability': {}, 'baseTier': {'spear': 1},
       'targets': [{'key': 'rawHealth', 'weight': 1}]}

pool = [i for i in ds.items if any(v != 0 for v in i['pos'].values())]
random.seed(3)

checked = 0
bad = 0
shown = 0
for _ in range(400):
    pick = random.sample(pool, 6)
    res = E.evaluate(ds, cfg, [p['id'] for p in pick])
    for cell, ing in zip(res['cells'], pick):
        if cell['bonus'] == 0:
            continue
        f = (100 + cell['bonus']) / 100.0
        for k, (mn, rw, mx) in ing['ids'].items():
            for got, raw in ((cell['ids'][k]['min'], mn), (cell['ids'][k]['max'], mx)):
                exact = raw * f
                want = math.floor(exact)
                checked += 1
                if got != want:
                    bad += 1
                    print('MISMATCH', ing['name'], k, 'exact=%.3f floor=%d got=%d' % (exact, want, got))
                elif abs(exact - round(exact)) > 1e-9 and shown < 6:
                    shown += 1
                    print('  frac  %-24s %-18s bonus=%+4d%%  %8.3f -> %d' % (ing['name'], k, cell['bonus'], exact, got))
    if checked > 3000:
        break

print('\nchecked %d values, mismatches %d' % (checked, bad))
assert bad == 0
