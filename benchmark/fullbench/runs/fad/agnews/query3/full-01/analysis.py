import json

biz_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query3/full-01/results/5e32d3c9fd0f4c5bbd59e5ff2e783019.json"
meta_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query3/full-01/results/484c741ebf5746aabd07411f3413d056.json"

biz = set(r["article_id"] for r in json.load(open(biz_path)))
meta = json.load(open(meta_path))

counts = {str(y): 0 for y in range(2010, 2021)}
for r in meta:
    if r["article_id"] in biz:
        counts[r["yr"]] += 1

print("Per-year counts:", counts)
total = sum(counts.values())
print("Total:", total)
print("Average over 11 years:", total / 11)
