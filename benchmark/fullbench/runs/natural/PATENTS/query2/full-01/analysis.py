import json, re
import pandas as pd

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query2/full-01/results/e1f4aa9fef1f4c6bad6d18e29df02301.json"
rows = json.load(open(path))
print("rows:", len(rows))

MONTHS = {m: i for i, m in enumerate(
    ["january","february","march","april","may","june","july","august",
     "september","october","november","december"], start=1)}
ABBR = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,
        "sep":9,"sept":9,"oct":10,"nov":11,"dec":12}

def parse_date(s):
    if not s:
        return None
    s = s.lower()
    ym = re.search(r'\b(19|20)\d{2}\b', s)
    if not ym:
        return None
    year = int(ym.group(0))
    month = None
    for name, num in {**MONTHS, **ABBR}.items():
        if re.search(r'\b' + name + r'\b', s):
            month = num
            break
    return (year, month)

def is_de(info):
    # publication number country code
    m = re.findall(r'(?:publication|pub\.?)\s*(?:number|no\.?)\s*([A-Z]{2})-', info)
    if m:
        return m[-1] == 'DE'
    m2 = re.findall(r'\b([A-Z]{2})-\d', info)
    return bool(m2) and m2[-1] == 'DE'

records = []
for r in rows:
    info = r["Patents_info"] or ""
    if not is_de(info):
        continue
    g = parse_date(r.get("grant_date"))
    if not g or g[0] != 2019 or g[1] is None or g[1] < 7:
        continue
    f = parse_date(r.get("filing_date"))
    fyear = f[0] if f else None
    try:
        cpcs = json.loads(r.get("cpc") or "[]")
    except Exception:
        cpcs = []
    codes = set()
    for c in cpcs:
        code = (c.get("code") or "").strip()
        if code:
            codes.add(code[:3])  # CPC level-4 group (class), e.g. H01
    records.append({"fyear": fyear, "codes": sorted(codes)})

print("DE patents granted H2 2019:", len(records))
no_filing = sum(1 for r in records if r["fyear"] is None)
print("missing filing year:", no_filing)

# build counts per (group, year)
from collections import Counter
cnt = Counter()
years = set()
for r in records:
    if r["fyear"] is None:
        continue
    years.add(r["fyear"])
    for g in r["codes"]:
        cnt[(g, r["fyear"])] += 1

ymin, ymax = min(years), max(years)
print("filing year range:", ymin, ymax)

groups = sorted({g for g, _ in cnt})
alpha = 0.1
results = []
for g in groups:
    series = pd.Series({y: cnt.get((g, y), 0) for y in range(ymin, ymax + 1)})
    ema = series.ewm(alpha=alpha, adjust=False).mean()
    best_year = int(ema.idxmax())
    best_ema = float(ema.max())
    peak_raw_year = int(series.idxmax())
    total = int(series.sum())
    results.append({"group": g, "best_ema": best_ema, "best_year": best_year,
                    "peak_raw_year": peak_raw_year, "total_filings": total})

df = pd.DataFrame(results).sort_values("best_ema", ascending=False).reset_index(drop=True)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 100)
print(df.head(20).to_string())
df.to_csv("ema_ranking.csv", index=False)
