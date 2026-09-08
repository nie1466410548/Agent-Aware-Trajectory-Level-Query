import json
with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query4/full-01/results/a4e65db3630f47f3bd96492d4fd7a6c0.json') as f:
    info = json.load(f)
for r in info:
    if r['Symbol'] in ('MFO','ARGD','HDB','AIN','DTQ'):
        print(r['Symbol'], '=>', r['Company Description'][:200])
        print()
