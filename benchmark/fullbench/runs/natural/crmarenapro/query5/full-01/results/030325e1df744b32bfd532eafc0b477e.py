import json, collections

with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query5/full-01/results/518d351904e24c2583eb1c52dc9ece8b.json') as f:
    order_items = json.load(f)
oi_ids = {r['Id'].lstrip('#') for r in order_items}

with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query5/full-01/results/66b71abf472c4f97bd040589eac3a7f2.json') as f:
    cases = json.load(f)

start, end = '2022-08-16', '2023-01-16T23:59:59'
counter = collections.Counter()
matched = 0
for c in cases:
    oi = (c.get('orderitemid__c') or '').lstrip('#')
    d = c.get('createddate') or ''
    if oi in oi_ids and start <= d[:10] and d[:10] <= '2023-01-16':
        matched += 1
        counter[c.get('issueid__c')] += 1

print("matched cases:", matched)
for issue, n in counter.most_common():
    print(issue, n)
