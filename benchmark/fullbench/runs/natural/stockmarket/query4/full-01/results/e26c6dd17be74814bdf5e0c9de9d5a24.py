import json
with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query4/full-01/results/0dac555cab374c39a5f780666aecc834.json') as f:
    rows = json.load(f)
with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query4/full-01/results/a4e65db3630f47f3bd96492d4fd7a6c0.json') as f:
    info = json.load(f)
desc = {r['Symbol']: r['Company Description'] for r in info}

valid = [r for r in rows if r['up_days'] is not None and r['up_days'] > r['down_days']]
print("with data:", sum(1 for r in rows if r['total']>0), "no data:", sum(1 for r in rows if r['total']==0))
print("up>down count:", len(valid))

by_up = sorted(valid, key=lambda r: (-r['up_days'], r['down_days']))
print("\nTop 10 by up_days:")
for r in by_up[:10]:
    print(r['Symbol'], r['up_days'], r['down_days'], '|', desc[r['Symbol']][:80])

by_diff = sorted(valid, key=lambda r: (-(r['up_days']-r['down_days']), -r['up_days']))
print("\nTop 10 by (up-down):")
for r in by_diff[:10]:
    print(r['Symbol'], r['up_days'], r['down_days'], 'diff', r['up_days']-r['down_days'])
