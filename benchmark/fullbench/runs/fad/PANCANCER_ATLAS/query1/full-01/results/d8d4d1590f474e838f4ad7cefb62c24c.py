import json
import math
import pandas as pd

clin = pd.DataFrame(json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query1/full-01/results/54dc369fd7514b48bbf0d6f09b2fd1f3.json")))
expr = pd.DataFrame(json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PANCANCER_ATLAS/query1/full-01/results/9fb8e0c90239483096ecf56b2b821dbc.json")))

print("clinical rows:", len(clin), "dup barcodes:", clin['barcode'].duplicated().sum())
print("expr rows:", len(expr), "dup participants:", expr['ParticipantBarcode'].duplicated().sum())

# valid expression: not null and > 0 (log10 requires positive)
expr = expr[pd.to_numeric(expr['normalized_count'], errors='coerce').notna()]
expr['normalized_count'] = expr['normalized_count'].astype(float)
print("non-positive expr values dropped:", int((expr['normalized_count'] <= 0).sum()))
expr = expr[expr['normalized_count'] > 0]
expr = expr.drop_duplicates(subset=['ParticipantBarcode'])

m = clin.merge(expr, left_on='barcode', right_on='ParticipantBarcode', how='inner')
print("merged rows:", len(m))
m['log10_expr'] = m['normalized_count'].map(math.log10)

res = m.groupby('histological_type')['log10_expr'].agg(['mean', 'count'])
res = res.sort_index()
for h, row in res.iterrows():
    print(f"{h}: avg_log10_IGF2 = {row['mean']:.6f}  (n={int(row['count'])})")

res['mean'].apply(lambda v: f"{v:.4f}").to_string()
with open("summary.txt", "w") as f:
    f.write("Average log10-transformed IGF2 expression for LGG patients by histological_type\n")
    for h, row in res.iterrows():
        f.write(f"{h}: {row['mean']:.4f} (n={int(row['count'])})\n")
