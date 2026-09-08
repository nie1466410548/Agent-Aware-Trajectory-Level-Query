import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/agnews/query4/full-01/results/d0cece66a1b94506af0304f1b8c32850.json") as f:
    rows = json.load(f)

ids = [r["article_id"] for r in rows]
print(len(ids), min(ids), max(ids))

query = {
    "operation": "find",
    "collection": "articles",
    "filter": {"article_id": {"$in": ids}},
    "projection": {"_id": 0, "article_id": 1, "title": 1, "description": 1},
    "limit": 7000
}
with open("mongo_query.json", "w") as f:
    json.dump(query, f)
print("written")
