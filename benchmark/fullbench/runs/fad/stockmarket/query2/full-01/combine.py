import json

files = [
    "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query2/full-01/results/c1dd223eafe844708c7c7d6ac2cb5c09.json",
    "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query2/full-01/results/7bb6a0d4bc1e4773b891e51aa50a4390.json",
    "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query2/full-01/results/a98365d1374c447084fdc3fa8d3c9d7a.json",
]
rows = []
for fp in files:
    rows.extend(json.load(open(fp)))

rows = sorted(rows, key=lambda r: r["Symbol"])
print(f"Total: {len(rows)}")
lines = ["ETF securities listed on NYSE Arca whose adjusted closing price exceeded $200 at some point during 2015:", ""]
for r in rows:
    lines.append(f"{r['Symbol']} (max 2015 Adj Close: ${r['MaxAdjClose']:.2f})")
    print(r["Symbol"], round(r["MaxAdjClose"], 2))
lines.append("")
lines.append(f"Total number of such ETFs: {len(rows)}")
with open("final.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
