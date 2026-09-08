import json, re
from collections import Counter

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query5/full-01/results/cf5e7d8dc49141b5b21b8652c3b6d3d0.json") as f:
    rows = json.load(f)

states = {}
counts = Counter()
for r in rows:
    m = re.search(r" in ([A-Za-z .']+), ([A-Z]{2}),", r["description"])
    if not m:
        print("NO MATCH:", r["description"][:80]); continue
    st = m.group(2)
    states.setdefault(st, []).append(r["business_id"])
    counts[st] += 1

print("Counts by state:", dict(counts.most_common()))
top = counts.most_common(1)[0][0]
print("Top state:", top)
print("Business IDs:", states[top])
