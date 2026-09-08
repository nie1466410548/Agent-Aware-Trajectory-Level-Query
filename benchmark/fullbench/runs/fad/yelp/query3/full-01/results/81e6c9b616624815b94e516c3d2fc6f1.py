import json, ast

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query3/full-01/results/3216fd3a56714ce99c3bc0767c087053.json"
rows = json.load(open(path))
print("total businesses:", len(rows))

def parse_bp(val):
    # BusinessParking may be "None" string, None, or a python-dict-like string
    if val is None:
        return None
    s = str(val).strip()
    if s.lower() in ("none", "null", ""):
        return None
    try:
        d = ast.literal_eval(s)
        if isinstance(d, dict):
            return d
    except Exception:
        pass
    return None

interp_A = []  # BusinessParking dict with any True OR BikeParking True
interp_B = []  # BusinessParking key present and not None OR BikeParking True
interp_C = []  # BikeParking True only
for r in rows:
    attrs = r.get("attributes")
    bike = False
    bp_present = False
    bp_any_true = False
    if isinstance(attrs, dict):
        if str(attrs.get("BikeParking")).strip() == "True":
            bike = True
        if "BusinessParking" in attrs:
            d = parse_bp(attrs.get("BusinessParking"))
            if d is not None:
                bp_present = True
                if any(v is True for v in d.values()):
                    bp_any_true = True
    if bike or bp_any_true:
        interp_A.append(r["business_id"])
    if bike or bp_present:
        interp_B.append(r["business_id"])
    if bike:
        interp_C.append(r["business_id"])

print("A (parking actually offered: any True in BusinessParking OR BikeParking=True):", len(interp_A))
print(sorted(interp_A))
print("B (BusinessParking attr present/non-None OR BikeParking=True):", len(interp_B))
print(sorted(interp_B))
print("C (BikeParking=True only):", len(interp_C))

# detail per business
for r in sorted(rows, key=lambda x: x["business_id"]):
    attrs = r.get("attributes")
    if isinstance(attrs, dict):
        bp = attrs.get("BusinessParking")
        bike = attrs.get("BikeParking")
        if ("BusinessParking" in attrs and parse_bp(bp) is not None) or str(bike) == "True":
            print(r["business_id"], "| bike:", bike, "| BP:", bp)
