import json
from datetime import datetime

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockindex/query2/full-01/results/8524f90f24b846da831a5df4f33bbd20.json"
rows = json.load(open(path))

def parse(d):
    d = d.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p", "%d %b %Y, %H:%M:%S"):
        try:
            return datetime.strptime(d, fmt)
        except ValueError:
            pass
    raise ValueError(d)

by_idx = {}
for r in rows:
    by_idx.setdefault(r['Index'], []).append((parse(r['Date']), r['Close']))

for idx, lst in sorted(by_idx.items()):
    lst.sort()
    up = down = 0
    for i in range(1, len(lst)):
        if lst[i][1] > lst[i-1][1]: up += 1
        elif lst[i][1] < lst[i-1][1]: down += 1
    print(idx, {'up_vs_prevclose': up, 'down': down}, "MORE_UP" if up > down else "not")
