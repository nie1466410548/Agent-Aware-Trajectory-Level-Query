import json, re

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
kept, dropped = [], []
for r in rows:
    info = r["Patents_info"] or ""
    m = re.search(r"pub(?:lication)?\.?\s*(?:no\.?|number)?\s*(DE-[0-9A-Z-]+)", info)
    gd = parse_date(r.get("grant_date"))
    fd = parse_date(r.get("filing_date"))
    pub = m.group(1) if m else None
    if pub and gd and gd[0] == 2019 and gd[1] >= 7:
        kept.append((pub, r["grant_date"], r["filing_date"], gd, fd))
    else:
        dropped.append((pub, r["grant_date"]))

print("kept:", len(kept))
for k in kept:
    print("  ", k)
print("dropped:", len(dropped))
for d in dropped:
    print("  ", d)
