import json
biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/604e6e7e916d4e7abcb7e2ce011c42d0.json"
biz = json.load(open(biz_file))
for b in biz:
    if b["business_id"] in ("businessid_36", "businessid_82", "businessid_85", "businessid_26"):
        print(b["business_id"], b["name"], "||", b["description"])
        print()
