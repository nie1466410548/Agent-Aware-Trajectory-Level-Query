import json, math
import pandas as pd

base = "results/"
clin = pd.DataFrame(json.load(open(base + "0eb1aa77de8f4859b1d1a4335ab1dbc3.json")))
mol = pd.DataFrame(json.load(open(base + "13e118b3d57b41498de4fbf3edb7b5c5.json")))

print("clinical rows:", len(clin), "unique patients:", clin.patient_id.nunique())
print("mol rows:", len(mol))

# Check suffix uniqueness in molecular data
mol["suffix"] = mol["ParticipantBarcode"].str.split("-").str[-1]
dup = mol[mol.suffix.isin(clin.patient_id)]
print("suffix collisions in mol (suffix shared by >1 barcode):")
s = mol.groupby("suffix")["ParticipantBarcode"].nunique()
print(s[s > 1])

# Filter histology: not null, not enclosed in square brackets
clin2 = clin[clin.histological_type.notna()].copy()
mask_bracket = clin2.histological_type.str.strip().str.startswith("[") & clin2.histological_type.str.strip().str.endswith("]")
print("bracketed histologies excluded:", clin2[mask_bracket].histological_type.unique())
clin2 = clin2[~mask_bracket]

# Join: molecular ParticipantBarcode suffix matches clinical patient_id
m = dup.merge(clin2, left_on="suffix", right_on="patient_id", how="inner")
print("joined rows:", len(m), "patients with expression:", m.patient_id.nunique())
print("sample types present:", m.SampleTypeLetterCode.value_counts().to_dict())

# Valid expression: not null and > 0 (log10 defined)
m = m[m.normalized_count.notna() & (m.normalized_count > 0)]
print("valid expression rows:", len(m))

m["log10_expr"] = m.normalized_count.apply(math.log10)
res = m.groupby("histological_type")["log10_expr"].agg(["mean", "count"])
res = res.sort_index()
for hist, row in res.iterrows():
    print(f"{hist}: avg_log10 = {row['mean']:.6f} (n={int(row['count'])})")

with open("final.txt", "w") as f:
    f.write("Average log10-transformed IGF2 expression for LGG patients by histology type\n")
    f.write("(patients with valid IGF2 expression values and non-bracketed histology annotations)\n\n")
    for hist, row in res.iterrows():
        f.write(f"{hist}: {row['mean']:.6f}\n")
print("final.txt written")
