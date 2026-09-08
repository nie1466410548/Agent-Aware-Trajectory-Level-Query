import json, re

biz_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/googlelocal/query3/full-01/results/4962efe96a4e4fbcb0986a5d46f2de22.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/googlelocal/query3/full-01/results/9034f0bb60214c77be8aa9f6ce57bf78.json"

biz = json.load(open(biz_path))
rev = json.load(open(rev_path))
ratings = {r["gmap_id"]: (r["avg_rating"], r["n_reviews"]) for r in rev}

WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

def parse_time(s):
    m = re.match(r"^\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM)\s*$", s, re.I)
    if not m:
        return None
    h = int(m.group(1)); mi = int(m.group(2) or 0); ap = m.group(3).upper()
    h = h % 12
    if ap == "PM":
        h += 12
    return h * 60 + mi

def open_after_6pm_weekday(hours_text):
    """True if business remains open past 6:00 PM on at least one weekday."""
    try:
        entries = json.loads(hours_text)
    except Exception:
        return False, []
    qualifying = []
    for day, span in entries:
        if day not in WEEKDAYS:
            continue
        s = str(span)
        if s.lower().startswith("open 24"):
            qualifying.append((day, s))
            continue
        if "closed" in s.lower():
            continue
        parts = re.split(r"[\u2013\u2014-]", s)
        if len(parts) != 2:
            continue
        o = parse_time(parts[0]); c = parse_time(parts[1])
        if o is None or c is None:
            continue
        # crosses midnight (close next day) or closes strictly after 18:00
        if c <= o or c > 18 * 60:
            qualifying.append((day, s))
    return (len(qualifying) > 0), qualifying

results = []
for b in biz:
    ok, qual = open_after_6pm_weekday(b["hours"])
    if not ok:
        continue
    gid = b["gmap_id"]
    if gid not in ratings:
        continue
    avg, n = ratings[gid]
    results.append({
        "name": b["name"],
        "gmap_id": gid,
        "avg_rating": avg,
        "n_reviews": n,
        "state": b["state"],
        "hours": b["hours"],
        "qualifying_weekdays": qual,
    })

results.sort(key=lambda r: (-r["avg_rating"], -r["n_reviews"]))

print(f"Total qualifying businesses (open past 6PM on >=1 weekday, with reviews): {len(results)}")
print()
for i, r in enumerate(results, 1):
    print(f"{i}. {r['name']} ({r['gmap_id']}) | avg_rating={r['avg_rating']:.4f} | n={r['n_reviews']} | state={r['state']}")
    print(f"   hours: {r['hours']}")
    print()

top5 = results[:5]
with open("final.txt", "w") as f:
    f.write("Top 5 businesses that remain open after 6:00 PM on at least one weekday, ranked by highest average rating\n")
    f.write("=" * 100 + "\n\n")
    for i, r in enumerate(top5, 1):
        f.write(f"{i}. {r['name']}\n")
        f.write(f"   Average rating: {r['avg_rating']:.2f} (based on {r['n_reviews']} reviews)\n")
        f.write(f"   Operating hours: {r['hours']}\n\n")
print("final.txt written")
