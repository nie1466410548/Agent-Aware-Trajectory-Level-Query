import json, re
from collections import defaultdict

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/604e6e7e916d4e7abcb7e2ce011c42d0.json"
rev_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/305b1ba9ec5e4a3e9481f6e653f532bf.json"

biz = json.load(open(biz_file))
revs = json.load(open(rev_file))
ratings = {r["business_ref"]: (r["n_reviews"], r["avg_rating"]) for r in revs}

INTRO = re.compile(
    r"(?:in the category of '|in the categories of |fields of |ranging from |services in |categories of |category of |"
    r"categories such as |services including |services, including |including |specializes in |selection of |featuring |"
    r"dishes in |destination for |solutions including |options in |mix of |enjoying |options for |seeking |encompassing |"
    r"array of |fusion of flavors across |experience with )",
    re.IGNORECASE)

STOP = re.compile(
    r"(\.\s*$|\.\s|, making|, offering|, perfect|, to meet|, to satisfy|, catering|, ensuring|, providing|"
    r",? for all |,? for every |,? for your |,? for any |,? for those |,? that |, ideal|, which|, where)",
    re.IGNORECASE)

JUNK = re.compile(r"\b(needs|tastes|preferences|occasions?|palate|meals?\b|experience|atmosphere|spot\b|destination\b|"
                  r"variety|fusion|flavors|delightful|diverse|perfect|great|vibrant|ideal|enthusiasts|premier)\b", re.IGNORECASE)

def parse_categories(desc):
    d = desc.rstrip(".")
    m = INTRO.search(d)
    if not m:
        return []
    seg = d[m.end():]
    # strip surrounding quotes
    seg = seg.strip().strip("'").strip()
    # cut at stop markers
    sm = STOP.search(seg)
    if sm:
        seg = seg[:sm.start()]
    # "ranging from A, B, to C" -> remove ' to ' splitter
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+|\s+to\s+", seg)
    cats = []
    for p in parts:
        p = p.strip().strip("'").strip()
        p = re.sub(r"^(a|an|the)\s+", "", p, flags=re.IGNORECASE)
        if not p:
            continue
        if JUNK.search(p):
            continue
        if len(p.split()) > 5:
            continue
        cats.append(p)
    return cats

cat_biz = defaultdict(set)
unparsed = []
print("=== PER BUSINESS PARSE ===")
for b in biz:
    cats = parse_categories(b.get("description") or "")
    if not cats:
        unparsed.append(b["name"])
    for c in set(cats):
        cat_biz[c].add(b["business_id"])
    print(f"{b['business_id']:>15s} | {b['name'][:35]:35s} | {cats}")

print()
print("UNPARSED:", unparsed)
print()
counts = sorted(cat_biz.items(), key=lambda kv: (-len(kv[1]), kv[0]))
print("=== CATEGORY COUNTS (top 15) ===")
for cat, ids in counts[:15]:
    tot_n, tot_sum, biz_avgs = 0, 0.0, []
    for bid in ids:
        ref = bid.replace("businessid_", "businessref_")
        if ref in ratings:
            n, a = ratings[ref]
            tot_n += n; tot_sum += n * a; biz_avgs.append(a)
    w_avg = tot_sum / tot_n if tot_n else None
    b_avg = sum(biz_avgs) / len(biz_avgs) if biz_avgs else None
    print(f"{len(ids):3d}  {cat:40s} review_weighted_avg={w_avg:.4f}  mean_of_biz_avg={b_avg:.4f}")
