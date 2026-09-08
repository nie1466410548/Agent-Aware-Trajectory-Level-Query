import json, re
from collections import Counter

REV = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/eb152856605544129147da66dcb425f3.json"
BIZ = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/aa4c2b6e07274a28adccbf9c1bfcf806.json"

reviews = json.load(open(REV))
biz = json.load(open(BIZ))
print("reviews:", len(reviews), "biz:", len(biz))

# years check
yrs = Counter(r["yr"] for r in reviews)
print("year dist:", sorted(yrs.items(), key=lambda x: (x[0] is None, x[0])))

# mapping check
biz_ids = {b["business_id"] for b in biz}
def num(s): return re.search(r'(\d+)$', s).group(1)
unmatched = [r["business_ref"] for r in reviews if "businessid_"+num(r["business_ref"]) not in biz_ids]
print("unmatched refs:", len(unmatched), set(unmatched))

# Build category vocabulary: split descriptions on commas/'and', count exact phrase recurrence
def split_candidates(desc):
    # normalize quotes and trailing period
    d = desc.replace("'", " ")
    parts = re.split(r',|\band\b', d)
    return [p.strip(' .;') for p in parts if p.strip(' .;')]

cand_counter = Counter()
for b in biz:
    for p in split_candidates(b["description"]):
        cand_counter[p] += 1

# vocabulary = phrases appearing in >= 2 businesses (case-sensitive first)
vocab = {p for p, c in cand_counter.items() if c >= 2}
print("vocab size:", len(vocab))
for p in sorted(vocab): print("  ", p, cand_counter[p])
