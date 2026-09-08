import json, re
from collections import defaultdict

biz_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query2/full-01/results/8d4485d29a5c41eda6e6fdf83838c084.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query2/full-01/results/4cc7fa04ebf84975beda47a4fb0c6824.json"

biz = json.load(open(biz_path))
rev = json.load(open(rev_path))

biz_state = {}
for b in biz:
    m = re.search(r",\s*([A-Z]{2})\b", b.get("description") or "")
    biz_state[b["business_id"]] = m.group(1) if m else None

# restrict to US states (exclude AB = Alberta, Canada)
us_states = {"AZ","CA","FL","ID","IL","IN","LA","MO","NJ","NV","PA","TN"}

per_biz = defaultdict(list)
for r in rev:
    bid = r["business_ref"].replace("businessref_", "businessid_")
    st = biz_state.get(bid)
    if st in us_states:
        per_biz[bid].append(r["rating"])

# PA analysis
pa_biz = {b: rs for b, rs in per_biz.items() if biz_state[b] == "PA"}
all_pa = [r for rs in pa_biz.values() for r in rs]
print("PA: n_reviews =", len(all_pa))
print("PA avg rating over all reviews:", sum(all_pa)/len(all_pa))
biz_avgs = [sum(rs)/len(rs) for rs in pa_biz.values()]
print("PA avg of per-business avg ratings:", sum(biz_avgs)/len(biz_avgs), "over", len(biz_avgs), "businesses")

# MO analysis (alternative interpretation)
mo_biz = {b: rs for b, rs in per_biz.items() if biz_state[b] == "MO"}
all_mo = [r for rs in mo_biz.values() for r in rs]
print("MO: n_reviews =", len(all_mo), "avg rating:", sum(all_mo)/len(all_mo))
