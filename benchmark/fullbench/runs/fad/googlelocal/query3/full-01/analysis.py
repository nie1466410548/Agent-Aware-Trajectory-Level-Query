import json, re

biz_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/googlelocal/query3/full-01/results/4962efe96a4e4fbcb0986a5d46f2de22.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/googlelocal/query3/full-01/results/9034f0bb60214c77be8aa9f6ce57bf78.json"

biz = json.load(open(biz_path))
rev = json.load(open(rev_path))
ratings = {r["gmap_id"]: (r["avg_rating"], r["n_reviews"]) for r in rev}

WEEKDAYS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"}

def parse_time(s, default_ap=None):
    m = re.match(r"^\s*(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?\s*$", s.strip(), re.I)
    if not m:
        return None
    h = int(m.group(1)); mi = int(m.group(2) or 0)
    ap = (m.group(3) or default_ap or "").upper()
    if not ap:
        return None
    h = h % 12
    if ap == "PM":
        h += 12
    return h * 60 + mi, ap

def open_after_6pm_weekday(hours_text):
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
            qualifying.append((day, s)); continue
        if "closed" in s.lower():
            continue
        parts = re.split(r"[\u2013\u2014-]", s)
        if len(parts) != 2:
            continue
        # inherit AM/PM for the side that lacks it
        c = parse_time(parts[1])
        o = parse_time(parts[0])
        if c is None and o is not None:
            c = parse_time(parts[1], default_ap=o[1])
        if o is None and c is not None:
            o = parse_time(parts[0], default_ap=c[1])
        if c is None:
            continue
        cmin, cap = c
        if cmin > 18 * 60:
            qualifying.append((day, s)); continue
        # closing in AM = after midnight -> open past 6PM, unless it's clearly a morning-only span (open AM, close AM, open<close)
        if cap == "AM":
            if o is not None and o[1] == "AM" and o[0] < cmin:
                continue  # e.g., 8:30-10AM morning span
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
    results.append({"name": b["name"], "gmap_id": gid, "avg_rating": avg,
                    "n_reviews": n, "state": b["state"], "hours": b["hours"],
                    "qualifying_weekdays": qual})

results.sort(key=lambda r: (-r["avg_rating"], -r["n_reviews"]))

print(f"Total qualifying businesses: {len(results)}\n")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['name']} ({r['gmap_id']}) | avg={r['avg_rating']:.4f} | n={r['n_reviews']} | state={r['state']}")

top5 = results[:5]
lines = []
lines.append("Top 5 businesses that remain open after 6:00 PM on at least one weekday (Mon-Fri), ranked by highest average rating")
lines.append("=" * 100)
lines.append("")
for i, r in enumerate(top5, 1):
    lines.append(f"{i}. {r['name']}")
    lines.append(f"   Average rating: {r['avg_rating']:.2f} (from {r['n_reviews']} reviews)")
    lines.append(f"   Operating hours: {r['hours']}")
    lines.append("")
with open("final.txt", "w") as f:
    f.write("\n".join(lines))
print("\nfinal.txt written")
