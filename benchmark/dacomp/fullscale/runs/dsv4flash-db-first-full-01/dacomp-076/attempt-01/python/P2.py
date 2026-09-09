import pandas as pd, numpy as np, json, os

# Read archived results of S20 (the full annotated dataset)
path = 'results/S20.rows.jsonl'
rows = []
with open(path) as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows)
print(df.shape)
print(df.columns.tolist())
print(df['is_anomaly'].value_counts())
print(df['profitability_segment'].value_counts())
