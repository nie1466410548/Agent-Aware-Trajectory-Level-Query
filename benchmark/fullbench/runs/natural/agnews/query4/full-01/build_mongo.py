import json
rows = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/agnews/query4/full-01/results/ccdd38c5f55b4e35b63c4db19bddbd6e.json"))
ids = [r["article_id"] for r in rows]
q = {"operation":"find","collection":"articles",
     "filter":{"article_id":{"$in":ids}},
     "projection":{"_id":0,"article_id":1,"title":1,"description":1}}
json.dump(q, open("mongo_2015.json","w"))
print(len(ids))
