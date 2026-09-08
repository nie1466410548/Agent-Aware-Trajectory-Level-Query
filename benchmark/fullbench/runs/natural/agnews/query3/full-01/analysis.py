import json
from collections import Counter

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query3/full-01/results/76ccc1b95a19444ab2515383aacab6d2.json"
meta_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query3/full-01/results/e919013b4be844c98f63fcc56cdb0c6e.json"

biz = set(r["article_id"] for r in json.load(open(biz_file)))
meta = json.load(open(meta_file))

counts = Counter()
for r in meta:
    if r["article_id"] in biz:
        counts[int(r["yr"])] += 1

years = list(range(2010, 2021))
per_year = {y: counts.get(y, 0) for y in years}
total = sum(per_year.values())
avg = total / len(years)
print("Per-year counts:", per_year)
print("Total:", total)
print("Average per year (11 years):", avg)
