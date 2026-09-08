import json
import pandas as pd

rel_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query1/full-01/results/a46400c1ac19499d934e4518e65ae405.json"
proj_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query1/full-01/results/8f39780a9c91476f8049aec18951828b.json"

rel = pd.DataFrame(json.load(open(rel_path)))
proj = pd.DataFrame(json.load(open(proj_path)))

rel = rel.dropna(subset=["Ordinal"])
latest = (rel.sort_values(["Ordinal", "Version"])
             .groupby("Name", as_index=False)
             .tail(1)[["Name", "Version", "Ordinal"]])

proj = proj.drop_duplicates(subset=["Name", "Version", "ProjectName"])
m = latest.merge(proj, on=["Name", "Version"], how="inner")
best = (m.sort_values("stars", ascending=False)
          .groupby("Name", as_index=False).first()
          .sort_values("stars", ascending=False).reset_index(drop=True))

print("=== ALL names (literal) ===")
print(best.head(10).to_string(index=False))

clean = best[~best["Name"].str.contains(">", regex=False)].reset_index(drop=True)
print("\n=== Excluding names with '>' ===")
print(clean.head(10).to_string(index=False))

# how many packages contain '>'
print("\npackages with '>':", best["Name"].str.contains(">", regex=False).sum(), "of", len(best))
