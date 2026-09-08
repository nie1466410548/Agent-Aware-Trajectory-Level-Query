import json
import pandas as pd

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/stockindex/query3/quick-01/results/d49ee5b4fefe40b2b7ed029a86a4d48b.json") as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
print("rows:", len(df), "indices:", df["Index"].nunique())

# Parse mixed-format dates
df["dt"] = pd.to_datetime(df["Date"], format="mixed")
df = df.dropna(subset=["dt"])
df = df.sort_values(["Index", "dt"])

# Only investments since 2000
df = df[df["dt"] >= "2000-01-01"]
df["month"] = df["dt"].dt.to_period("M")

results = []
for idx, g in df.groupby("Index"):
    g = g.sort_values("dt")
    # first trading day of each month = monthly investment point
    buys = g.groupby("month").first()
    final_price = g["CloseUSD"].iloc[-1]
    final_date = g["dt"].iloc[-1]
    n_months = len(buys)
    shares = (1.0 / buys["CloseUSD"]).sum()
    final_value = shares * final_price
    total_return = final_value / n_months - 1.0
    results.append({
        "Index": idx,
        "start": str(g["dt"].iloc[0].date()),
        "end": str(final_date.date()),
        "n_months": n_months,
        "total_invested": n_months,
        "final_value": round(final_value, 2),
        "total_return_pct": round(total_return * 100, 2),
    })

res = pd.DataFrame(results).sort_values("total_return_pct", ascending=False)
print(res.to_string(index=False))
