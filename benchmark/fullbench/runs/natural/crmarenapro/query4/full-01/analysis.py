import json
from collections import Counter

cases = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query4/full-01/results/a882b83b62b0406a860ada2aaf6e586a.json'))
items = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query4/full-01/results/33940d70c8c54b7790303921f477c872.json'))

norm = lambda s: (s or '').lstrip('#')
oi2prod = {norm(r['Id']): norm(r['Product2Id']) for r in items}
TARGET = '01tWt000006hVJdIAM'

# check how many case orderitems resolve
unresolved = sum(1 for c in cases if norm(c['orderitemid__c']) not in oi2prod)
print('cases:', len(cases), 'unresolved orderitem links:', unresolved)

# past 10 months relative to 2021-04-10
start, end = '2020-06-10', '2021-04-10'
window = [c for c in cases if start <= c['createddate'][:10] <= end]
print('cases in window:', len(window))

prod_cases = [c for c in window if oi2prod.get(norm(c['orderitemid__c'])) == TARGET]
print('target product cases in window:', len(prod_cases))
mc = Counter(c['createddate'][:7] for c in prod_cases)
print('target by month:', dict(sorted(mc.items())))

# context: monthly counts for ALL cases in window
allmc = Counter(c['createddate'][:7] for c in window)
print('all cases by month:', dict(sorted(allmc.items())))

# context: per-product max monthly count in window
perprod = {}
for c in window:
    p = oi2prod.get(norm(c['orderitemid__c']))
    perprod.setdefault(p, Counter())[c['createddate'][:7]] += 1
for p, cnt in sorted(perprod.items(), key=lambda kv: -max(kv[1].values()))[:6]:
    print(p, dict(sorted(cnt.items())))
