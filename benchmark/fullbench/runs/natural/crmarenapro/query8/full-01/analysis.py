import json
from collections import Counter, defaultdict

hist_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query8/full-01/results/7712a5339f6445909a124d51013bf46c.json"
case_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query8/full-01/results/63381b95a6bb460ba4b7028adf76f0ac.json"

hist = json.load(open(hist_path))
cases = json.load(open(case_path))

def clean(x):
    if x is None:
        return None
    return x.lstrip('#')

TODAY = "2023-04-10"
CUTOFF = "2022-04-10"  # last 4 quarters = trailing 12 months

# Agents who handled >0 cases in the window:
#  - initial assignment (Owner Assignment newvalue with oldvalue null, or case owner)
#  - transferred-to (newvalue of a transfer row)
handled = Counter()
for h in hist:
    d = h["createddate"][:10]
    if CUTOFF <= d <= TODAY:
        handled[clean(h["newvalue__c"])] += 1
for c in cases:
    d = c["createddate"][:10]
    if CUTOFF <= d <= TODAY:
        handled[clean(c["ownerid"])] += 1

# Transfer counts: each Owner Assignment row with non-null oldvalue = transfer FROM oldvalue agent
transfers = Counter()
for h in hist:
    d = h["createddate"][:10]
    if CUTOFF <= d <= TODAY and h["oldvalue__c"] is not None:
        transfers[clean(h["oldvalue__c"])] += 1

print("Agents handled >0 cases in window:", len(handled))
rows = []
for agent, cnt in handled.items():
    rows.append((agent, cnt, transfers.get(agent, 0)))
rows.sort(key=lambda r: (r[2], -r[1]))
for r in rows:
    print(r)

min_t = min(r[2] for r in rows)
print("Min transfer count:", min_t)
print("Agents with min:", [r[0] for r in rows if r[2] == min_t])
