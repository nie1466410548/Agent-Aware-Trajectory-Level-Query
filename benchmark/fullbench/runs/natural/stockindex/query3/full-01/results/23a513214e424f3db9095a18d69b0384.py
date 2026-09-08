import json
from datetime import datetime

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockindex/query3/full-01/results/ec18e5744bd2491ea02a34f862bd8ec7.json") as f:
    rows = json.load(f)

print("total rows:", len(rows))

FORMATS = ["%d %b %Y, %H:%M", "%B %d, %Y at %I:%M %p", "%Y-%m-%d %H:%M:%S"]

def parse_date(s):
    for fmt in FORMATS:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError("unparseable: " + s)

# organize data per index: list of (date, closeusd)
data = {}
bad = 0
for r in rows:
    try:
        d = parse_date(r["Date"])
    except ValueError:
        bad += 1
        continue
    p = r["CloseUSD"]
    if p is None:
        continue
    data.setdefault(r["Index"], []).append((d, p))

print("unparsed rows:", bad)

# Index -> Exchange -> Country (from index_info exchange list)
meta = {
    "000001.SS": ("Shanghai Stock Exchange", "China"),
    "399001.SZ": ("Shenzhen Stock Exchange", "China"),
    "GDAXI": ("Frankfurt Stock Exchange", "Germany"),
    "GSPTSE": ("Toronto Stock Exchange", "Canada"),
    "HSI": ("Hong Kong Stock Exchange", "Hong Kong"),
    "IXIC": ("NASDAQ", "United States"),
    "J203.JO": ("Johannesburg Stock Exchange", "South Africa"),
    "N100": ("Euronext", "Netherlands/France (pan-Europe)"),
    "N225": ("Tokyo Stock Exchange", "Japan"),
    "NSEI": ("National Stock Exchange of India", "India"),
    "NYA": ("New York Stock Exchange", "United States"),
    "SSMI": ("SIX Swiss Exchange", "Switzerland"),
    "TWII": ("Taiwan Stock Exchange", "Taiwan"),
}

START = datetime(2000, 1, 1)

results = []
for idx, recs in sorted(data.items()):
    recs = sorted(recs)
    print(f"{idx}: {recs[0][0].date()} .. {recs[-1][0].date()}  n={len(recs)}")
    recs = [r for r in recs if r[0] >= START]
    if not recs:
        continue
    # monthly investment: buy $1 worth at the FIRST trading day of each month
    seen = set()
    units = 0.0
    invested = 0.0
    for d, p in recs:
        key = (d.year, d.month)
        if key in seen:
            continue
        seen.add(key)
        units += 1.0 / p
        invested += 1.0
    last_price = recs[-1][1]
    value = units * last_price
    ret = value / invested - 1.0
    results.append((idx, invested, value, ret, recs[0][0].date(), recs[-1][0].date()))

print("\n=== Monthly $1 investments since 2000 (first trading day of month), USD prices ===")
results.sort(key=lambda x: -x[3])
for idx, inv, val, ret, d0, d1 in results:
    exch, country = meta.get(idx, ("?", "?"))
    print(f"{idx:10s} invested={inv:6.0f}  value={val:9.2f}  return={ret*100:8.1f}%  {d0} -> {d1}  {country}")

print("\nTOP 5:")
for idx, inv, val, ret, d0, d1 in results[:5]:
    exch, country = meta.get(idx, ("?", "?"))
    print(f"{idx} | {country} | {exch} | total return {ret*100:.1f}%")
