import json
from datetime import datetime
import pandas as pd

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockindex/query1/full-01/results/115bbcc37df243ab8f6c8f07d38807b8.json"
with open(path) as f:
    rows = json.load(f)

fmts = ["%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p", "%Y-%m-%d %H:%M:%S"]
def parse(s):
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            pass
    return None

df = pd.DataFrame(rows)
df["dt"] = df["Date"].apply(parse)
unparsed = df[df["dt"].isna()]
print("Total rows:", len(df), "| Unparsed dates:", len(unparsed))
if len(unparsed):
    print(unparsed["Date"].unique()[:20])

# date range per index (sanity)
print(df.groupby("Index")["dt"].agg(["min","max","count"]))

since = df[df["dt"] >= datetime(2020,1,1)].copy()
print("\nRows since 2020 per index:")
print(since.groupby("Index")["dt"].agg(["min","max","count"]))

since["vol_hl_close"] = (since["High"] - since["Low"]) / since["Close"]
since["vol_hl_open"] = (since["High"] - since["Low"]) / since["Open"]
res = since.groupby("Index").agg(
    n=("vol_hl_close","count"),
    avg_hl_over_close=("vol_hl_close","mean"),
    avg_hl_over_open=("vol_hl_open","mean"),
).sort_values("avg_hl_over_close", ascending=False)
print("\nAverage intraday volatility since 2020 (Asia indices):")
print(res.to_string())
