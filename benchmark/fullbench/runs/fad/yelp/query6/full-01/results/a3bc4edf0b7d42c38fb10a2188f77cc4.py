import json
from datetime import datetime

result_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query6/full-01/results/b466363d6ecf49caa9c94bffb194d480.json"
rows = json.load(open(result_file))

formats = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%B %d, %Y at %I:%M %p",   # August 01, 2016 at 03:44 AM
    "%b %d, %Y at %I:%M %p",
    "%d %b %Y, %H:%M",         # 29 May 2013, 23:01
    "%d %B %Y, %H:%M",
    "%B %d, %Y",               # fallback date-only variants
    "%b %d, %Y",
    "%Y-%m-%d",
]

def parse(s):
    s = s.strip()
    for f in formats:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None

unparsed = set()
start = datetime(2016, 1, 1)
end = datetime(2016, 7, 1)  # exclusive: Jan 1 - Jun 30 inclusive

in_window = []
for r in rows:
    d = parse(r["date"])
    if d is None:
        unparsed.add(r["date"])
        continue
    if start <= d < end:
        in_window.append((r["business_ref"], r["rating"]))

print("total rows:", len(rows))
print("unparsed formats:", sorted(unparsed))
print("reviews in window:", len(in_window))

from collections import defaultdict
agg = defaultdict(list)
for b, rating in in_window:
    agg[b].append(rating)

stats = [(b, sum(v)/len(v), len(v)) for b, v in agg.items() if len(v) >= 5]
stats.sort(key=lambda x: (-x[1], -x[2]))
print("businesses with >=5 reviews in window:")
for b, avg, n in stats:
    print(f"  {b}: avg={avg:.4f}, n={n}")
