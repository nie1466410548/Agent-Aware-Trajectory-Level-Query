import json
rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query2/full-01/results/924d3b9c6f46427da202e73452570e67.json"))
for r in rows:
    t = (r.get("title") or "")
    if any(k in t.lower() for k in ["quote","policy","discount","approval","pricing","cost"]):
        print(r["id"], "|", t)
