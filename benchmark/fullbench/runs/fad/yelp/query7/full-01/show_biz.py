import json

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query7/full-01/results/"
biz = json.load(open(base + "2f1c37273e3249d393fdb4d84317fd33.json"))
print(len(biz))
for b in sorted(biz, key=lambda x: int(x["business_id"].split("_")[1])):
    print(b["business_id"], "||", b["description"])
