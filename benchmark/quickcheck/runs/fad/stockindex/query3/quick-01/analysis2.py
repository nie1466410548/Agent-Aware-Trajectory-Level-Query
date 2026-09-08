import json
from datetime import datetime
import pandas as pd

RESULT = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/stockindex/query3/quick-01/results/ab1e566e9faf441aaf06cf66ef8860fd.json"
with open(RESULT) as f:
    rows = json.load(f)
df = pd.DataFrame(rows)
FORMATS = ["%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p", "%Y-%m-%d %H:%M:%S"]
def parse_date(s):
    for fmt in FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None
df["dt"] = df["Date"].map(parse_date)
START = datetime(2000, 1, 1)

def rank(mode):
    out = []
    for idx, g in df.groupby("Index"):
        g = g[g["dt"] >= START].sort_values("dt").dropna(subset=["CloseUSD"])
        if g.empty: continue
        g = g.copy(); g["ym"] = g["dt"].dt.to_period("M")
        if mode == "first":
            m = g.groupby("ym").first()
        elif mode == "last":
            m = g.groupby("ym").last()
        else:
            m = g.groupby("ym")["CloseUSD"].mean().to_frame()
        shares = (1.0 / m["CloseUSD"]).sum()
        ret = shares * g.iloc[-1]["CloseUSD"] / len(m) - 1.0
        out.append((idx, round(ret*100, 2)))
    return sorted(out, key=lambda x: -x[1])

for mode in ["first", "last", "mean"]:
    r = rank(mode)
    print(f"\n=== buy at {mode} of month ===")
    for i, (idx, ret) in enumerate(r[:6], 1):
        print(f"{i}. {idx}: {ret}%")
