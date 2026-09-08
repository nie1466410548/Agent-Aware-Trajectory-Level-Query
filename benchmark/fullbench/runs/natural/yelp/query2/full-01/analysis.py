import json, re
from collections import defaultdict

with open("results/34b26f9ed6ac4102bd962bb85f167afc.json") as f:
    rows = json.load(f)

state_reviews = defaultdict(int)
state_biz = defaultdict(list)
unmatched = []
for r in rows:
    desc = r.get("description") or ""
    m = re.search(r",\s*([A-Z]{2})\b", desc)
    if not m:
        unmatched.append(r)
        continue
    st = m.group(1)
    state_reviews[st] += r.get("review_count", 0)
    state_biz[st].append(r["business_id"])

top = sorted(state_reviews.items(), key=lambda kv: -kv[1])
print("Businesses parsed:", len(rows), "unmatched:", len(unmatched))
print("State review totals (top 10):")
for st, tot in top[:10]:
    print(f"  {st}: {tot} reviews, {len(state_biz[st])} businesses")

top_state = top[0][0]
print("Top state:", top_state)
print("Business IDs in top state:", json.dumps(sorted(state_biz[top_state])))
