import json, re
from collections import Counter

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query5/full-01/results/b7232186c9be4885bca36206ae7eea8b.json"
rows = json.load(open(path))

US_STATES = {"AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY","DC"}

def offers_wifi(v):
    if v is None: return False
    s = str(v).lower().strip("u'").strip("'").strip()
    return s in ("free","paid","yes","true")

state_counts = Counter()
state_biz = {}
all_wifi = []
for r in rows:
    wifi = r.get("attributes",{}).get("WiFi")
    if not offers_wifi(wifi):
        continue
    desc = r.get("description","") or ""
    m = re.search(r",\s*([A-Z]{2})\b\s*,", desc)
    if not m:
        m = re.search(r" in ([A-Za-z .]+),\s*([A-Z]{2})\b", desc)
        st = m.group(2) if m else None
    else:
        st = m.group(1)
    if not st or st not in US_STATES:
        continue
    state_counts[st]+=1
    state_biz.setdefault(st,[]).append(r["business_id"])
    all_wifi.append((r["business_id"], st, wifi))

print("wifi-offering businesses:", len(all_wifi))
print("state counts:", state_counts.most_common())
top = state_counts.most_common(1)[0][0]
print("TOP STATE:", top, state_counts[top])
print("business ids in top state:", state_biz[top])
json.dump({"top_state":top,"biz_ids":state_biz[top],"counts":state_counts.most_common()}, open("top_state.json","w"))
