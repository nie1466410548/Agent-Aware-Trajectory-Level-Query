import json
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query4/full-01/results/0398bda632db421094f2e5cd8159b5d6.json") as f:
    rows = json.load(f)
ids = [r["article_id"] for r in rows]
q = {"operation": "find", "collection": "articles",
     "filter": {"article_id": {"$in": ids}},
     "projection": {"article_id": 1, "title": 1, "description": 1, "_id": 0}}
with open("mongo_query.json", "w") as f:
    json.dump(q, f)
print("ids:", len(ids), "unique:", len(set(ids)))
