import json, re
from collections import defaultdict

with open("results/34b26f9ed6ac4102bd962bb85f167afc.json") as f:
    biz = json.load(f)
with open("results/31db6213d22d401abf97c5d6a4a75e39.json") as f:
    rev = json.load(f)

revmap = {r["business_ref"]: (r["n"], r["avg_r"]) for r in rev}

state_meta = defaultdict(int)      # sum of review_count metadata
state_reviews = defaultdict(int)   # count in review table
state_rsum = defaultdict(float)
state_bizcnt = defaultdict(int)
for b in biz:
    st = re.search(r",\s*([A-Z]{2})\b", b["description"]).group(1)
    state_meta[st] += b["review_count"]
    state_bizcnt[st] += 1
    ref = b["business_id"].replace("businessid_", "businessref_")
    if ref in revmap:
        n, avg = revmap[ref]
        state_reviews[st] += n
        state_rsum[st] += avg * n

print(f"{'ST':4} {'meta_reviews':>12} {'tbl_reviews':>11} {'avg_rating':>10}")
for st in sorted(state_meta, key=lambda s: -state_meta[s]):
    avg = state_rsum[st] / state_reviews[st] if state_reviews[st] else 0
    print(f"{st:4} {state_meta[st]:12} {state_reviews[st]:11} {avg:10.4f}")

top = max(state_meta, key=lambda s: state_meta[s])
print("\nTop state by review count:", top, state_meta[top], "reviews")
print("Avg rating (review-weighted):", round(state_rsum[top] / state_reviews[top], 4))
# simple average of per-business averages
mo_ids = [b["business_id"].replace("businessid_", "businessref_") for b in biz
          if re.search(r",\s*([A-Z]{2})\b", b["description"]).group(1) == top]
simple = sum(revmap[r][1] for r in mo_ids) / len(mo_ids)
print("Simple mean of business avg ratings:", round(simple, 4), "over", len(mo_ids), "businesses")
