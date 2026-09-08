import json
rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query2/full-01/results/924d3b9c6f46427da202e73452570e67.json"))
for r in rows:
    if r["id"] in ("ka0Wt000000Eq0MIAS","#ka0Wt000000EpSUIA0","ka0Wt000000Ens5IAC","ka0Wt000000EqQ9IAK"):
        print("="*80)
        print(r["id"], "|", r["title"])
        print(r.get("faq_answer__c","")[:3000])
