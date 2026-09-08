import json
import pandas as pd

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/stockindex/query3/quick-01/results/d49ee5b4fefe40b2b7ed029a86a4d48b.json") as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
df["dt"] = pd.to_datetime(df["Date"], format="mixed")
df = df.dropna(subset=["dt"]).sort_values(["Index", "dt"])
df = df[df["dt"] >= "2000-01-01"]
df["month"] = df["dt"].dt.to_period("M")

for variant, buy_fn in [("first", "first"), ("last", "last"), ("mean", "mean")]:
    results = []
    for idx, g in df.groupby("Index"):
        g = g.sort_values("dt")
        if buy_fn == "mean":
            px = g.groupby("month")["CloseUSD"].mean()
        else:
            px = getattr(g.groupby("month"), buy_fn)()["CloseUSD"]
        final_price = g["CloseUSD"].iloc[-1]
        shares = (1.0 / px).sum()
        ret = shares * final_price / len(px) - 1.0
        results.append((idx, round(ret * 100, 2)))
    results.sort(key=lambda x: -x[1])
    print(variant, ":", results)
