import json, pandas as pd

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PANCANCER_ATLAS/query2/full-01/results/"
clin = pd.DataFrame(json.load(open(base + "3ce236e52b374c4fa435b8b275bb6e74.json")))
mut_all = set(r["ParticipantBarcode"] for r in json.load(open(base + "70e1c9ab1adc42f891de9509aefddf8d.json")))
mut_pass = set(r["ParticipantBarcode"] for r in json.load(open(base + "f97a9dc6c955445aab5e99d51a34facb.json")))

print("BRCA rows:", len(clin), "| vital_status values:", clin["vital_status"].value_counts(dropna=False).to_dict())
print("barcode nulls:", clin["barcode"].isna().sum(), "| dup barcodes:", clin["barcode"].duplicated().sum())
print("histology values (alive):", clin.loc[clin.vital_status.str.lower()=="alive","histological_type"].value_counts(dropna=False).to_dict())

alive = clin[clin["vital_status"].str.lower() == "alive"].copy()
alive = alive.dropna(subset=["barcode","histological_type"])
print("alive patients:", len(alive))

for label, muts in [("ALL CDH1 mutations", mut_all), ("PASS-only CDH1 mutations", mut_pass)]:
    alive["mut"] = alive["barcode"].isin(muts)
    g = alive.groupby("histological_type").agg(total=("barcode","count"), mutated=("mut","sum"))
    g["pct"] = (g["mutated"]/g["total"]*100).round(2)
    g = g.sort_values("pct", ascending=False)
    print("\n===", label, "===")
    print(g.to_string())
