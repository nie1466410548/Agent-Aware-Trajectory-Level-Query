import json, re

BIZ = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/googlelocal/query3/full-01/results/75a9f0a7e5e24359940f423b3429c9fd.json"
REV = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/googlelocal/query3/full-01/results/bf49142620a94a60ba473d1415d049dd.json"

biz = json.load(open(BIZ))
rev = json.load(open(REV))
ratings = {r["gmap_id"]: r["avg_rating"] for r in rev}

WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

def parse_time(t):
    m = re.match(r"^(\d{1,2})(?::(\d{2}))?\s*(AM|PM)$", t.strip())
    if not m:
        return None
    h = int(m.group(1)); mi = int(m.group(2) or 0); ap = m.group(3)
    if ap == "AM":
        h = 0 if h == 12 else h
    else:
        h = 12 if h == 12 else h + 12
    return h * 60 + mi

def close_minutes(day_hours):
    """Return max closing time in minutes for a day's hours string, or None if closed."""
    s = day_hours.strip()
    if s.lower() == "closed":
        return None
    if "24 hours" in s.lower():
        return 24 * 60  # open past midnight -> after 6PM
    closes = []
    # split multiple ranges by comma
    for part in s.split(","):
        part = part.strip()
        # split on en-dash or hyphen
        segs = re.split(r"[\u2013\u2014-]", part)
        if len(segs) < 2:
            continue
        start_s, end_s = segs[0].strip(), segs[1].strip()
        # if start lacks AM/PM, inherit from end
        if not re.search(r"(AM|PM)$", start_s):
            ap = re.search(r"(AM|PM)$", end_s).group(1)
            start_s = start_s + ap
        st = parse_time(start_s); en = parse_time(end_s)
        if st is None or en is None:
            continue
        if en <= st:
            en += 24 * 60  # overnight
        closes.append(en)
    return max(closes) if closes else None

results = []
for b in biz:
    if not b.get("hours"):
        continue
    try:
        hours = json.loads(b["hours"])
    except Exception:
        continue
    qualifies = False
    for day, h in hours:
        if day in WEEKDAYS:
            cm = close_minutes(h)
            if cm is not None and cm > 18 * 60:  # open after 6:00 PM
                qualifies = True
                break
    if qualifies:
        results.append({
            "gmap_id": b["gmap_id"],
            "name": b["name"],
            "hours": hours,
            "avg_rating": ratings.get(b["gmap_id"]),
        })

results.sort(key=lambda x: (x["avg_rating"] is None, -(x["avg_rating"] or 0), x["name"]))

for r in results[:10]:
    print(f"{r['name']} | avg={r['avg_rating']:.4f} | hours={r['hours']}")

print("\nTotal qualifying:", len(results))

with open("final.txt", "w") as f:
    f.write("Top 5 businesses open after 6:00 PM on at least one weekday, ranked by highest average rating:\n\n")
    for i, r in enumerate(results[:5], 1):
        hrs = "; ".join(f"{d}: {h}" for d, h in r["hours"])
        f.write(f"{i}. {r['name']}\n")
        f.write(f"   Average rating: {r['avg_rating']:.2f}\n")
        f.write(f"   Hours: {hrs}\n\n")
