import json
import pandas as pd

LATEST = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/8b960cc18e124b97a6bc36777e4b0c48.json"
STARS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/90923f48c9444bc0b06da881c5df5549.json"

latest = pd.read_json(LATEST)
stars = pd.read_json(STARS)

latest['has_gt'] = latest['Name'].str.contains('>', regex=False)
print("names with '>':", latest['has_gt'].sum(), "of", len(latest))

merged = latest.merge(stars[['Name','Version','project','stars']], on=['Name','Version'], how='inner')

print("\n--- Top 10 including '>' names ---")
print(merged.sort_values(['stars','Name'], ascending=[False,True]).head(10)[['Name','Version','project','stars']].to_string(index=False))

clean = merged[~merged['Name'].str.contains('>', regex=False)]
print("\n--- Top 10 excluding '>' names ---")
print(clean.sort_values(['stars','Name'], ascending=[False,True]).head(10)[['Name','Version','project','stars']].to_string(index=False))

# does the stars mapping contain versions for well-known top projects (react, vue)?
print("\nTop projects by stars in mapping (all versions):")
print(stars.sort_values('stars', ascending=False).head(15)[['Name','Version','project','stars']].to_string(index=False))
