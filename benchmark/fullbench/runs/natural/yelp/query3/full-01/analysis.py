import json, re, ast

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query3/full-01/results/"
biz = json.load(open(base + "12e7a1ef3cec4f0a8057ef63a9daa327.json"))
refs = json.load(open(base + "d525231640b442f6936af5cfa84c9ed5.json"))

ref_nums = {r["business_ref"].split("_")[1] for r in refs}

def offers(b):
    attrs = b.get("attributes") or {}
    bp = attrs.get("BusinessParking")
    bike = attrs.get("BikeParking")
    bike_ok = (bike == "True")
    park_ok = False
    if bp and bp not in ("None",):
        # parse dict-like string, handle u'' prefixes
        try:
            d = ast.literal_eval(bp)
            park_ok = any(v is True for v in d.values())
        except Exception:
            park_ok = "True" in bp
    return bike_ok or park_ok, bike_ok, park_ok

matched, count = [], 0
for b in biz:
    num = b["business_id"].split("_")[1]
    if num in ref_nums:
        matched.append(num)
        ok, bike, park = offers(b)
        if ok:
            count += 1
            print(b["business_id"], "bike=", bike, "park=", park)

missing = ref_nums - set(matched)
print("refs:", len(ref_nums), "matched:", len(matched), "missing:", missing)
print("ANSWER:", count)
