import json
import pandas as pd

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockindex/query2/full-01/results/38a885e2fb0d4b68aabe57c6cd05d801.json"
with open(path) as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
print("rows:", len(df), "indices:", df["Index"].unique())

# Parse mixed date formats
df["d"] = pd.to_datetime(df["Date"], format="mixed", dayfirst=False)
print("unparsed:", df["d"].isna().sum())
print("date range:", df["d"].min(), df["d"].max())

df = df.sort_values(["Index", "d"])

results = {}
for idx, g in df.groupby("Index"):
    g = g.sort_values("d").reset_index(drop=True)
    g["prev_close"] = g["Close"].shift(1)
    g18 = g[g["d"].dt.year == 2018].copy()
    # Method 1: up day = Close > previous trading day's Close
    up1 = (g18["Close"] > g18["prev_close"]).sum()
    down1 = (g18["Close"] < g18["prev_close"]).sum()
    flat1 = (g18["Close"] == g18["prev_close"]).sum()
    # Method 2: up day = Close > Open
    up2 = (g18["Close"] > g18["Open"]).sum()
    down2 = (g18["Close"] < g18["Open"]).sum()
    flat2 = (g18["Close"] == g18["Open"]).sum()
    results[idx] = dict(days18=len(g18),
                        prevclose=(int(up1), int(down1), int(flat1)),
                        close_vs_open=(int(up2), int(down2), int(flat2)))

for idx, r in results.items():
    print(idx, r)
    print(f"  Method1 (vs prev close): up={r['prevclose'][0]} down={r['prevclose'][1]} -> more up than down: {r['prevclose'][0] > r['prevclose'][1]}")
    print(f"  Method2 (close vs open): up={r['close_vs_open'][0]} down={r['close_vs_open'][1]} -> more up than down: {r['close_vs_open'][0] > r['close_vs_open'][1]}")
