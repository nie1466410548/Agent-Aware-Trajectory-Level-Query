import json, pandas as pd

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query6/full-01/results/b425913455da4313adb6e32a5e358683.json") as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
df["dt"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
print("unparsed:", df["dt"].isna().sum())
print(df[df["dt"].isna()]["date"].unique()[:10])

mask = (df["dt"] >= "2016-01-01") & (df["dt"] < "2016-07-01")
sub = df[mask]
g = sub.groupby("business_ref").agg(avg_rating=("rating","mean"), n=("rating","count"))
g = g[g["n"] >= 5].sort_values(["avg_rating","n"], ascending=[False,False])
print(g.head(15).to_string())
