
import pandas as pd, numpy as np, json

rows = [json.loads(l) for l in open('results/S44.rows.jsonl')]
df = pd.DataFrame(rows)
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
print(df[['avg_nps_rating']].isna().sum())
