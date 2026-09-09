import json, pandas as pd, numpy as np

# Re-read S19 properly
rows = []
with open('/results/S19.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
rep_df = pd.DataFrame(rows)
print("S19 raw shape:", rep_df.shape)
print("first row:", rep_df.iloc[0].to_dict())

# There are 1000 rows in S19 per row_count. Check for nulls
print("\nNulls per column:")
print(rep_df.isnull().sum())

# Check opp_conversion_rate outliers
oc = pd.to_numeric(rep_df.iloc[:, 13], errors='coerce')
print("\nopp_conversion_rate (col 13) describe:", oc.describe())
big = oc[oc > 1.0]
print("rows with opp_conversion_rate > 1:", len(big))
print(rep_df[oc > 1.0].to_string())

# Check efficiency outliers
eff = pd.to_numeric(rep_df.iloc[:, 4], errors='coerce')
print("\nefficiency_score describe:", eff.describe())
print("rows with efficiency > 3:", len(eff[eff > 3]))
print(rep_df[eff > 3].head(10).to_string())