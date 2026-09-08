import json
import pandas as pd

rel_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query1/full-01/results/a46400c1ac19499d934e4518e65ae405.json"
proj_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query1/full-01/results/8f39780a9c91476f8049aec18951828b.json"

with open(rel_path) as f:
    rel = pd.DataFrame(json.load(f))
with open(proj_path) as f:
    proj = pd.DataFrame(json.load(f))

# Latest release version per package: max Ordinal (ties broken by max Version string)
rel = rel.dropna(subset=["Ordinal"])
latest = (rel.sort_values(["Ordinal", "Version"])
             .groupby("Name", as_index=False)
             .tail(1)[["Name", "Version", "Ordinal"]])
print("distinct packages with release:", len(latest))

# Deduplicate project-version rows
proj = proj.drop_duplicates(subset=["Name", "Version", "ProjectName"])
print("project-version rows:", len(proj), "distinct packages:", proj["Name"].nunique())

m = latest.merge(proj, on=["Name", "Version"], how="inner")
print("merged rows:", len(m), "distinct packages:", m["Name"].nunique())

# If a package maps to multiple projects, keep the max stars
best = (m.sort_values("stars", ascending=False)
          .groupby("Name", as_index=False)
          .first())
best = best.sort_values("stars", ascending=False).reset_index(drop=True)
print(best.head(15).to_string(index=False))
