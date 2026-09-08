import json
from collections import Counter

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query5/full-01/results/026bea61cb434f3b9942b5a3209a3b71.json") as f:
    order_items = json.load(f)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query5/full-01/results/16b72af16d9341c3b709d61b0be6a165.json") as f:
    cases = json.load(f)

oi_ids = {r["Id"].lstrip("#") for r in order_items}
matched = [c for c in cases if (c["orderitemid__c"] or "").lstrip("#") in oi_ids]
print("matched cases:", len(matched))
counts = Counter(c["issueid__c"] for c in matched)
for issue, n in counts.most_common():
    print(issue, n)
