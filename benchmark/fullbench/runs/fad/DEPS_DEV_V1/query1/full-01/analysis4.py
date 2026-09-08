import pandas as pd
STARS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/90923f48c9444bc0b06da881c5df5549.json"
stars = pd.read_json(STARS)
rows = stars[stars['Name']=='@docly/web'].sort_values('Version')
print(rows.to_string(index=False))
print("\nnull star rows total:", stars['stars'].isna().sum())
print(stars[stars['stars'].isna()].head(20).to_string(index=False))
