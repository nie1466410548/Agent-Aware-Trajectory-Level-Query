import json
import pandas as pd

LATEST = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/8b960cc18e124b97a6bc36777e4b0c48.json"
STARS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/90923f48c9444bc0b06da881c5df5549.json"

latest = pd.read_json(LATEST)
stars = pd.read_json(STARS)

print("latest rows:", len(latest), "distinct pkgs:", latest['Name'].nunique())
print("star mapping rows:", len(stars), "null stars:", stars['stars'].isna().sum())

merged = latest.merge(stars[['Name','Version','project','stars']], on=['Name','Version'], how='inner')
print("merged rows:", len(merged))

# one row per package (latest release version already deduped); keep max stars in case of dup mappings
agg = merged.groupby(['Name','Version'], as_index=False).agg(project=('project','first'), stars=('stars','max'))
top = agg.sort_values(['stars','Name'], ascending=[False, True]).head(10)
print(top.to_string(index=False))

top5 = top.head(5)
with open('final.txt','w') as f:
    f.write("Top 5 most popular NPM packages (latest release version only), ranked by GitHub stars:\n\n")
    for i, r in enumerate(top5.itertuples(), 1):
        f.write(f"{i}. {r.Name} — version {r.Version} (GitHub: {r.project}, {int(r.stars)} stars)\n")
print(open('final.txt').read())
