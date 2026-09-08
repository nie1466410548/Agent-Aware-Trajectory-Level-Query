import json
rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query1/full-01/results/5af40597297b47abb7a86c3115deac6f.json"))
for i, r in enumerate(rows):
    print(i, r["article_id"], r["len"], "|", r["title"])
