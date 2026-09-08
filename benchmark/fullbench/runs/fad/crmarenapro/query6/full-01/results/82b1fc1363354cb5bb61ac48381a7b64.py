import json
rows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query6/full-01/results/257756a8d28b4504a2d45d24456d1561.json'))
kw = ['discount','quantity','price','pricing','limit','policy','license','quote','approval','cap','maximum','minimum','volume']
for r in rows:
    t = (r.get('title') or '')
    if any(k in t.lower() for k in kw):
        print(r['id'], '|', t)
