import json, re
from collections import defaultdict

RESULT = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query2/full-01/results/de75e1c1822040b69867dff18c1f286a.json"

MONTHS = {m: i+1 for i, m in enumerate(
    ["january","february","march","april","may","june","july",
     "august","september","october","november","december"])}
MONTHS.update({m[:3]: v for m, v in MONTHS.items()})

def parse_date(s):
    if not s:
        return None
    s = s.lower()
    ym = re.search(r"\b(19|20)\d{2}\b", s)
    mm = None
    for name, num in MONTHS.items():
        if re.search(r"\b" + name + r"\b", s):
            mm = num
            break
    if ym and mm:
        return (int(ym.group(0)), mm)
    return None

rows = json.load(open(RESULT))
print("total rows fetched:", len(rows))

# keep DE publications granted in second half of 2019
h2 = []
for r in rows:
    info = r["Patents_info"] or ""
    # publication number must be DE (grant publications B3/B4 etc.)
    m = re.search(r"pub(?:lication)?\s*(?:no\.|number)?\s*\.?\s*(DE-[\w-]+)", info)
    pubnum = m.group(1) if m else None
    if not pubnum:
        # fallback: any DE- token that is not the application (-A/-T suffix)
        toks = re.findall(r"DE-\d+-([A-Z]\d?)", info)
        if not any(t.startswith("B") or t.startswith("C") for t in toks):
            continue
    gd = parse_date(r.get("grant_date"))
    fd = parse_date(r.get("filing_date"))
    if gd and gd[0] == 2019 and gd[1] >= 7 and fd:
        h2.append((r, fd[0]))

print("H2-2019 granted DE patents:", len(h2))

# level-4 CPC group = class = first 3 chars (letter + 2 digits), per cpc_definition level=4
group_year = defaultdict(lambda: defaultdict(int))  # group -> year -> count
for r, fyear in h2:
    try:
        codes = json.loads(r["cpc"]) if r.get("cpc") else []
    except Exception:
        continue
    groups = set()
    for c in codes:
        code = c.get("code", "").strip()
        m = re.match(r"^([A-HY]\d{2})", code)
        if m:
            groups.add(m.group(1))
    for g in groups:
        group_year[g][fyear] += 1

ALPHA = 0.1
results = []
for g, yc in group_year.items():
    years = sorted(yc)
    lo, hi = years[0], years[-1]
    ema = None
    best_year, best_ema = None, -1
    for y in range(lo, hi + 1):
        c = yc.get(y, 0)
        ema = c if ema is None else ALPHA * c + (1 - ALPHA) * ema
        if ema > best_ema:
            best_ema, best_year = ema, y
    results.append((g, best_year, round(best_ema, 4), dict(yc)))

results.sort(key=lambda x: -x[2])
print("\nCPC level-4 groups ranked by peak EMA (alpha=0.1):")
for g, by, be, yc in results:
    print(f"{g}  best_year={by}  peak_ema={be}  yearly={dict(sorted(yc.items()))}")

json.dump([{"group": g, "best_year": by, "peak_ema": be} for g, by, be, _ in results],
          open("groups.json", "w"), indent=1)
