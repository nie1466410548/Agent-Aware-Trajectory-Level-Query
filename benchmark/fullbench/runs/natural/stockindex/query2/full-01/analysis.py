import json, re

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockindex/query2/full-01/results/8524f90f24b846da831a5df4f33bbd20.json"
rows = json.load(open(path))
stats = {}
for r in rows:
    # sanity check year
    assert '2018' in r['Date'], r['Date']
    s = stats.setdefault(r['Index'], {'up':0,'down':0,'flat':0})
    if r['Close'] > r['Open']:
        s['up'] += 1
    elif r['Close'] < r['Open']:
        s['down'] += 1
    else:
        s['flat'] += 1
for idx, s in sorted(stats.items()):
    print(idx, s, "MORE_UP_THAN_DOWN" if s['up'] > s['down'] else "not")
