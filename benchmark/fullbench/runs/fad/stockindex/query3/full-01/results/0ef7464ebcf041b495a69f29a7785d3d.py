import json, re
from datetime import datetime

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockindex/query3/full-01/results/570b8b8c31a440f786d5c8a163842b45.json"
rows = json.load(open(path))
print("rows:", len(rows))

MONTHS = {m:i+1 for i,m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
MONTHS_FULL = {m:i+1 for i,m in enumerate(["January","February","March","April","May","June","July","August","September","October","November","December"])}

def parse_date(s):
    # Format A: "01 Apr 2003, 00:00"
    m = re.match(r'^(\d{2}) ([A-Za-z]{3}) (\d{4})', s)
    if m:
        d, mon, y = m.groups()
        if mon in MONTHS:
            return datetime(int(y), MONTHS[mon], int(d))
    # Format B: "September 30, 2015 at 12:00 AM"
    m = re.match(r'^([A-Za-z]+) (\d{1,2}), (\d{4})', s)
    if m:
        mon, d, y = m.groups()
        if mon in MONTHS_FULL:
            return datetime(int(y), MONTHS_FULL[mon], int(d))
    return None

bad = set()
data = {}
for r in rows:
    dt = parse_date(r["Date"])
    if dt is None:
        bad.add(r["Date"][:30])
        continue
    data.setdefault(r["Index"], []).append((dt, r["CloseUSD"]))
print("unparsed examples:", list(bad)[:10], "count:", len(bad))

results = []
for idx, recs in data.items():
    recs.sort()
    recs = [(d,p) for d,p in recs if d >= datetime(2000,1,1) and p is not None]
    if not recs: continue
    # monthly: first trading day of each month
    monthly = {}
    for d,p in recs:
        key = (d.year, d.month)
        if key not in monthly:
            monthly[key] = (d,p)
    shares = 0.0
    invested = 0.0
    for key in sorted(monthly):
        d,p = monthly[key]
        shares += 1.0/p
        invested += 1.0
    last_date, last_price = recs[-1]
    final_value = shares * last_price
    ret = final_value/invested - 1
    results.append((idx, len(monthly), invested, final_value, ret, monthly[sorted(monthly)[0]][0], last_date))

results.sort(key=lambda x: -x[4])
print(f"{'Index':12} {'months':>6} {'invested':>9} {'final':>10} {'return%':>9}  first_inv -> last")
for idx, nm, inv, fv, ret, fd, ld in results:
    print(f"{idx:12} {nm:6d} {inv:9.0f} {fv:10.2f} {ret*100:9.1f}  {fd.date()} -> {ld.date()}")
