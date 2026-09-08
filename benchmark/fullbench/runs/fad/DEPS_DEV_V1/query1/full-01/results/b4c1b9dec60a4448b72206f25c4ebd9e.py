import pandas as pd

LATEST = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/8b960cc18e124b97a6bc36777e4b0c48.json"
STARS = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query1/full-01/results/e344e280b837462aaef95b26b2fc32e8.json"

latest = pd.read_json(LATEST)
stars = pd.read_json(STARS)
print("null stars remaining:", stars['stars'].isna().sum())

merged = latest.merge(stars[['Name','Version','project','stars']], on=['Name','Version'], how='inner')

print("\n=== INCLUDING '>' pseudo-names (raw distinct Name values) ===")
raw = merged.sort_values(['stars','Name'], ascending=[False,True]).head(8)
print(raw[['Name','Version','project','stars']].to_string(index=False))

clean = merged[~merged['Name'].str.contains('>', regex=False)].copy()
print("\n=== EXCLUDING '>' pseudo-names (valid NPM package names) ===")
top = clean.sort_values(['stars','Name'], ascending=[False,True]).head(8)
print(top[['Name','Version','project','stars']].to_string(index=False))

top5 = top.head(5)
lines = []
lines.append("TASK: Top 5 most popular NPM packages by GitHub stars, considering only the latest release version of each distinct package.\n")
lines.append("Method: latest release version per NPM package = max Ordinal among VersionInfo.IsRelease=true (packageinfo); "
             "joined to project_packageversion (System=NPM, ProjectType=GITHUB) on (Name, Version); "
             "GitHub star counts parsed from project_info.Project_Information text.\n")
lines.append("Note: 'Names' containing '>' (e.g. '@dmrvos/infrajs>0.0.5>typescript') are dependency-relation artifacts, "
             "not valid NPM package names, and were excluded from the primary answer.\n")
lines.append("PRIMARY ANSWER (excluding '>' artifact names):")
for i, r in enumerate(top5.itertuples(), 1):
    lines.append(f"{i}. {r.Name} — latest release version {r.Version} — {int(r.stars)} GitHub stars (repo: {r.project})")
lines.append("")
lines.append("Alternative interpretation (if '>' artifact names are counted as distinct packages):")
for i, r in enumerate(raw.head(5).itertuples(), 1):
    lines.append(f"{i}. {r.Name} — version {r.Version} — {int(r.stars)} stars (repo: {r.project})")

out = "\n".join(lines) + "\n"
with open('final.txt','w') as f:
    f.write(out)
print("\n" + out)
