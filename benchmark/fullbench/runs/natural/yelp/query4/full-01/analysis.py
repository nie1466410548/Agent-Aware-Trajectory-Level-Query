import json, re
from collections import defaultdict

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/604e6e7e916d4e7abcb7e2ce011c42d0.json"
rev_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/305b1ba9ec5e4a3e9481f6e653f532bf.json"

biz = json.load(open(biz_file))
revs = json.load(open(rev_file))

ratings = {r["business_ref"]: (r["n_reviews"], r["avg_rating"]) for r in revs}

# Extract the category segment from the description
def extract_segment(desc):
    d = desc.rstrip(".")
    # patterns that introduce the category list
    pats = [
        r"in the category of '([^']+)'",
        r"in the categories of (.+?)(?:\.|, offering|, making|, for |, to |$)",
        r"fields of (.+?)(?:\.|, offering|, making|, for |$)",
        r"ranging from (.+?)(?:, making|\.|$)",
        r"services in (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"categories of (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"category of (.+?)(?:\.|$)",
        r"services including (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"services, including (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"including (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"specializes in (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"selection of (.+?)(?:\.|, offering|, making|, for |, to meet|$)",
        r"featuring (.+?)(?:\.|, offering|, making|, for |$)",
        r"dishes in (.+?)(?:\.|$)",
        r"destination for (.+?)(?:\.|$)",
        r"solutions including (.+?)(?:\.|$)",
    ]
    for p in pats:
        m = re.search(p, d, re.IGNORECASE)
        if m:
            return m.group(1)
    return None

# stop-words that indicate trailing non-category filler
FILLER = re.compile(r"\b(options?|services?|products?|dishes|treats|selection|offerings|needs|occasions|palate|improvement|maintenance|destination|spot|atmosphere|menu|cuisine|nightlife, bars)\b", re.IGNORECASE)

def parse_categories(desc):
    seg = extract_segment(desc)
    if seg is None:
        return []
    seg = seg.strip()
    # split on commas and ' and ' / ' & ' handled later
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+", seg)
    cats = []
    for p in parts:
        p = p.strip().strip("'").strip()
        # cut trailing filler after a category, e.g. "Pizza, Restaurants for all your dining needs" already cut
        p = re.sub(r"\s+(options?|services?|products?|dishes|treats|to meet.*|for all.*|for every.*|for your.*|for any.*|making it.*)$", "", p, flags=re.IGNORECASE).strip()
        if not p:
            continue
        cats.append(p)
    return cats

cat_biz = defaultdict(list)  # category -> list of business_ids
unparsed = []
for b in biz:
    cats = parse_categories(b.get("description") or "")
    # normalize case variants
    norm = []
    for c in cats:
        c2 = c.strip()
        norm.append(c2)
    if not norm:
        unparsed.append(b["name"])
    for c in set(norm):
        cat_biz[c].append(b["business_id"])

print("UNPARSED:", unparsed)
print()

counts = sorted(cat_biz.items(), key=lambda kv: -len(kv[1]))
for cat, ids in counts:
    # avg rating: review-weighted over all reviews of businesses in this category
    tot_n, tot_sum = 0, 0.0
    biz_avgs = []
    for bid in ids:
        ref = bid.replace("businessid_", "businessref_")
        if ref in ratings:
            n, a = ratings[ref]
            tot_n += n
            tot_sum += n * a
            biz_avgs.append(a)
    w_avg = tot_sum / tot_n if tot_n else None
    b_avg = sum(biz_avgs) / len(biz_avgs) if biz_avgs else None
    print(f"{len(ids):3d}  {cat:45s} review_weighted_avg={w_avg}  mean_of_biz_avg={b_avg}")

print()
# show parsed categories for top categories verification
top = counts[0][0]
print("TOP CATEGORY:", top, "->", len(counts[0][1]), "businesses")
