import json, re
from collections import defaultdict

biz_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query2/full-01/results/8d4485d29a5c41eda6e6fdf83838c084.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query2/full-01/results/4cc7fa04ebf84975beda47a4fb0c6824.json"

biz = json.load(open(biz_path))
rev = json.load(open(rev_path))
print("businesses:", len(biz), "reviews:", len(rev))

# Extract state: pattern ", XX" where XX is 2 uppercase letters
biz_state = {}
biz_rc = {}
unmatched = []
for b in biz:
    d = b.get("description") or ""
    m = re.search(r",\s*([A-Z]{2})\b", d)
    if m:
        biz_state[b["business_id"]] = m.group(1)
    else:
        unmatched.append((b["business_id"], d[:80]))
    biz_rc[b["business_id"]] = b.get("review_count", 0)

print("unmatched businesses:", unmatched)
print("distinct states:", sorted(set(biz_state.values())))

# reviews per state via review table
rev_count = defaultdict(int)
rev_sum = defaultdict(float)
for r in rev:
    bid = r["business_ref"].replace("businessref_", "businessid_")
    st = biz_state.get(bid)
    if st is None:
        print("no state for", bid)
        continue
    rev_count[st] += 1
    rev_sum[st] += r["rating"]

print("\nReviews per state (from review table):")
for st, c in sorted(rev_count.items(), key=lambda x: -x[1]):
    print(f"  {st}: {c} reviews, avg rating {rev_sum[st]/c:.4f}")

# cross-check: sum of business review_count per state
rc_sum = defaultdict(int)
for bid, st in biz_state.items():
    rc_sum[st] += biz_rc[bid]
print("\nSum of business review_count per state:")
for st, c in sorted(rc_sum.items(), key=lambda x: -x[1]):
    print(f"  {st}: {c}")

top = max(rev_count, key=rev_count.get)
print(f"\nTOP STATE (review table count): {top} with {rev_count[top]} reviews, avg rating {rev_sum[top]/rev_count[top]:.4f}")
top2 = max(rc_sum, key=rc_sum.get)
print(f"TOP STATE (business review_count sum): {top2} with {rc_sum[top2]} reviews")

# avg rating for top2 state too
if top2 in rev_count:
    print(f"Avg rating for {top2}: {rev_sum[top2]/rev_count[top2]:.4f}")
