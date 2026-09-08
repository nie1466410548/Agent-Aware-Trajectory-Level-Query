import json, re
from collections import defaultdict, Counter

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/604e6e7e916d4e7abcb7e2ce011c42d0.json"
rev_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query4/full-01/results/305b1ba9ec5e4a3e9481f6e653f532bf.json"

biz = json.load(open(biz_file))
revs = json.load(open(rev_file))
ratings = {r["business_ref"]: (r["n_reviews"], r["avg_rating"]) for r in revs}

INTRO = re.compile(
    r"(?:in the category of |in the categories of |fields of |ranging from |services in |categories of |category of |"
    r"categories such as |services including |services, including |including |specializes in |selection of |featuring |"
    r"dishes in |destination for |solutions including |options in |mix of |enjoying |options for |seeking |encompassing |"
    r"array of |fusion of flavors across |experience with )",
    re.IGNORECASE)

STOP = re.compile(
    r"(\.\s*$|\.\s|, making|, offering|, perfect|, to meet|, to satisfy|, catering|, ensuring|, providing|"
    r",? for all |,? for every |,? for your |,? for any |,? for those |,? that |, ideal|, which|, where|, to enhance)",
    re.IGNORECASE)

PREFIXES = ["dishes in the category of", "categories such as", "categories of", "category of",
            "field of", "fields of", "options ranging from", "ranging from", "options for", "options",
            "including", "such as", "services in", "services including", "selection of", "mix of",
            "to", "a", "an", "the", "and", "of"]

JUNK = re.compile(r"\b(needs|tastes|preferences|occasions?|palate|meals?\b|experiences?\b|atmosphere|spot\b|destination\b|"
                  r"variety|fusion|flavors|delightful|diverse|perfect|great|vibrant|ideal|enthusiasts|premier|"
                  r"offerings?|customers|options?|cater\b|well-being|improvement|maintenance|selection)\b", re.IGNORECASE)

def clean_token(p):
    p = p.strip().strip("'").strip().strip('"').strip()
    p = re.sub(r"\s+", " ", p)
    changed = True
    while changed and p:
        changed = False
        low = p.lower()
        for pre in PREFIXES:
            if low.startswith(pre + " ") and len(p) > len(pre) + 1:
                p = p[len(pre):].strip().strip("'").strip()
                changed = True
                break
    p = re.sub(r"\s+cuisine$", "", p, flags=re.IGNORECASE)
    p = re.sub(r"\s+options?$", "", p, flags=re.IGNORECASE)
    return p.strip()

def raw_tokens(desc):
    d = desc.rstrip(".")
    toks = []
    for m in INTRO.finditer(d):
        seg = d[m.end():].strip()
        sm = STOP.search(seg)
        if sm:
            seg = seg[:sm.start()]
        parts = re.split(r",\s*(?:and\s+)?|\s+and\s+|\s+to\s+", seg)
        for p in parts:
            t = clean_token(p)
            if t and not JUNK.search(t) and len(t.split()) <= 5:
                toks.append(t)
    return toks

# Pass 1: build vocabulary (tokens appearing >=2 times)
per_biz = {b["business_id"]: raw_tokens(b.get("description") or "") for b in biz}
tc = Counter(t for toks in per_biz.values() for t in toks)
vocab = {t for t, c in tc.items() if c >= 2}
canon = {v.lower(): v for v in vocab}

def resolve(t):
    if t in vocab: return t
    if t.lower() in canon: return canon[t.lower()]
    m = re.match(r"^(.*?)\s+[Ss]ervices$", t)
    if m and m.group(1) in vocab: return m.group(1)
    for v in sorted(vocab, key=len, reverse=True):
        if re.search(r"(?<![A-Za-z])" + re.escape(v) + r"(?![A-Za-z])", t, re.IGNORECASE):
            return v
    return t  # keep singleton as its own category

cat_biz = defaultdict(set)
for b in biz:
    bid = b["business_id"]
    cats = {resolve(t) for t in per_biz[bid]}
    for c in cats:
        cat_biz[c].add(bid)

results = []
for cat, ids in cat_biz.items():
    tot_n, tot_sum, biz_avgs = 0, 0.0, []
    for bid in ids:
        ref = bid.replace("businessid_", "businessref_")
        if ref in ratings:
            n, a = ratings[ref]
            tot_n += n; tot_sum += n * a; biz_avgs.append(a)
    w = tot_sum / tot_n if tot_n else None
    ba = sum(biz_avgs) / len(biz_avgs) if biz_avgs else None
    results.append((cat, len(ids), w, ba, tot_n))

results.sort(key=lambda r: (-r[1], r[0]))
print("=== TOP 10 CATEGORIES ===")
for cat, n, w, ba, tn in results[:10]:
    print(f"{n:3d}  {cat:35s} n_reviews={tn:4d}  review_weighted_avg={w:.4f}  mean_of_biz_avg={ba:.4f}")

top = results[0]
print()
print(f"ANSWER: {top[0]} | {top[1]} businesses | review-level avg rating = {top[2]:.4f} | mean of per-business avg = {top[3]:.4f}")
print("Members:", sorted(cat_biz[top[0]], key=lambda x: int(x.split('_')[1])))
