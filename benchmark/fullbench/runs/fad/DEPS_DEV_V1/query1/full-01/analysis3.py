import pandas as pd

LATEST = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/8b960cc18e124b97a6bc36777e4b0c48.json"
STARS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/90923f48c9444bc0b06da881c5df5549.json"

latest = pd.read_json(LATEST)
stars = pd.read_json(STARS)
merged = latest.merge(stars[['Name','Version','project','stars']], on=['Name','Version'], how='inner')
clean = merged[~merged['Name'].str.contains('>', regex=False)].copy()

# check duplicate project mappings per (Name, Version) among top candidates
dup = clean.groupby(['Name','Version'])['project'].nunique()
print("candidates with >1 project mapping:", dup[dup>1])
top10 = clean.sort_values(['stars','Name'], ascending=[False,True]).head(10)
for _, r in top10.iterrows():
    rows = stars[(stars['Name']==r['Name']) & (stars['Version']==r['Version'])]
    print(f"\n{r['Name']} @ {r['Version']}:")
    print(rows.to_string(index=False))

# what is @docly/web latest release?
print("\n@docly/web latest row:", latest[latest['Name']=='@docly/web'].to_string(index=False))
print(stars[stars['Name']=='@docly/web']['Version'].unique())
