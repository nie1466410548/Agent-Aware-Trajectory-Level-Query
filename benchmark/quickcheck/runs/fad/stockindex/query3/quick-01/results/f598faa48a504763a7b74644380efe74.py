import json
from datetime import datetime
import pandas as pd

RESULT = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/stockindex/query3/quick-01/results/ab1e566e9faf441aaf06cf66ef8860fd.json"

with open(RESULT) as f:
    rows = json.load(f)

df = pd.DataFrame(rows)
print("rows:", len(df))
print("nulls:\n", df.isna().sum())

FORMATS = ["%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p", "%Y-%m-%d %H:%M:%S"]

def parse_date(s):
    for fmt in FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None

df["dt"] = df["Date"].map(parse_date)
bad = df[df["dt"].isna()]
print("unparsed dates:", len(bad))
if len(bad):
    print(bad["Date"].unique()[:20])

# Monthly investments since 2000: buy at first trading day of each month
START = datetime(2000, 1, 1)

results = []
for idx, g in df.groupby("Index"):
    g = g[g["dt"] >= START].sort_values("dt").dropna(subset=["Close", "CloseUSD"])
    if g.empty:
        continue
    g = g.copy()
    g["ym"] = g["dt"].dt.to_period("M")
    monthly = g.groupby("ym").first().reset_index()  # first trading day of month
    n_months = len(monthly)
    invested = n_months * 1.0  # 1 unit of currency per month

    shares_close = (1.0 / monthly["Close"]).sum()
    final_close = g.iloc[-1]["Close"]
    value_close = shares_close * final_close
    ret_close = value_close / invested - 1.0

    shares_usd = (1.0 / monthly["CloseUSD"]).sum()
    final_usd = g.iloc[-1]["CloseUSD"]
    value_usd = shares_usd * final_usd
    ret_usd = value_usd / invested - 1.0

    results.append({
        "Index": idx,
        "first_inv": monthly["dt"].min().date().isoformat(),
        "last_date": g["dt"].max().date().isoformat(),
        "n_months": n_months,
        "return_close": round(ret_close * 100, 2),
        "return_usd": round(ret_usd * 100, 2),
    })

res = pd.DataFrame(results).sort_values("return_usd", ascending=False)
print("\n=== Ranking by CloseUSD (USD) DCA return ===")
print(res.to_string(index=False))

res2 = res.sort_values("return_close", ascending=False)
print("\n=== Ranking by local Close DCA return ===")
print(res2.to_string(index=False))

# also simple buy-and-hold since 2000 for reference
bh = []
for idx, g in df.groupby("Index"):
    g = g[g["dt"] >= START].sort_values("dt").dropna(subset=["CloseUSD"])
    if g.empty:
        continue
    bh.append({"Index": idx, "bh_usd": round((g.iloc[-1]["CloseUSD"]/g.iloc[0]["CloseUSD"]-1)*100, 2)})
print("\n=== Buy&hold USD return reference ===")
print(pd.DataFrame(bh).sort_values("bh_usd", ascending=False).to_string(index=False))
