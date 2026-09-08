import json, ast

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query3/full-01/results/bf618bf1080a4bf19550443f1d737662.json"
rows = json.load(open(path))
print("businesses fetched:", len(rows))

def parse_bp(val):
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

A, B = [], []
details = []
for r in rows:
    attrs = r.get("attributes")
    bike = False
    bp_present = False
    bp_any = False
    if isinstance(attrs, dict):
        bike = str(attrs.get("BikeParking")).strip() == "True"
        if "BusinessParking" in attrs:
            d = parse_bp(attrs.get("BusinessParking"))
            if d is not None:
                bp_present = True
                bp_any = any(v is True for v in d.values())
    if bike or bp_any:
        A.append(r["business_id"])
    if bike or bp_present:
        B.append(r["business_id"])
    details.append((r["business_id"], r.get("name"), bike, bp_present, bp_any))

print("A (parking actually offered: any True in BusinessParking OR BikeParking=True):", len(A))
print("B (BusinessParking present/non-None OR BikeParking=True):", len(B))
print()
for bid, name, bike, bpp, bpa in sorted(details, key=lambda x: int(x[0].split("_")[1])):
    if bike or bpp:
        print(f"{bid:15s} {str(name)[:40]:42s} bike={bike!s:5s} BP_present={bpp!s:5s} BP_any_true={bpa!s:5s} -> in_A={bike or bpa}")
