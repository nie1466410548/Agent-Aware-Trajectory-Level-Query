import json, re
from collections import defaultdict

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
    # suffix cleanup
    p = re.sub(r"\s+cuisine$", "", p, flags=re.IGNORECASE)
    p = re.sub(r"\s+options?$", "", p, flags=re.IGNORECASE)
    return p.strip()

def raw_tokens(desc):
    d = desc.rstrip(".")
    m = INTRO.search(d)
    if not m:
        return []
    seg = d[m.end():].strip()
    sm = STOP.search(seg)
    if sm:
        seg = seg[:sm.start()]
    parts = re.split(r",\s*(?:and\s+)?|\s+and\s+|\s+to\s+", seg)
    return [clean_token(p) for p in parts if clean_token(p)]

JUNKEXACT = {"options", "treats", "customers", "needs", "services", "products", "dishes",
             "meet all your travel", "meet various home improvement", "enhance your personal style",
             "well-being", "cater", "products across various categories", "various categories"}

# Pass 1: gather candidate tokens
all_tokens = []
per_biz = {}
for b in biz:
    toks = [t for t in raw_tokens(b.get("description") or "") if t.lower() not in JUNKEXACT]
    per_biz[b["business_id"]] = toks
    all_tokens.extend(toks)

from collections import Counter
tc = Counter(all_tokens)
# vocab = tokens that look like proper categories (appear >=2 times, or are Title Case / contain & / ())
vocab = set()
for t, c in tc.items():
    if c >= 2:
        vocab.add(t)
for t in tc:
    if t in vocab:
        continue
    # title-cased short phrases are categories
    if re.match(r"^[A-Z0-9/&'()+.\- ]+$", t) and not t.islower():
        vocab.add(t)

# canonical case map (e.g., 'bars' -> 'Bars')
canon = {}
for v in vocab:
    canon[v.lower()] = v

def resolve(t):
    if t in vocab:
        return t
    if t.lower() in canon:
        return canon[t.lower()]
    # suffix 'services' removal when remainder known
    m = re.match(r"^(.*?)\s+[Ss]ervices$", t)
    if m and m.group(1) in vocab:
        return m.group(1)
    # substring match against vocab (longest first), word-boundary
    for v in sorted(vocab, key=len, reverse=True):
        if re.search(r"(?<![A-Za-z])" + re.escape(v) + r"(?![A-Za-z])", t, re.IGNORECASE):
            return v
    return None

cat_biz = defaultdict(set)
leftover = defaultdict(list)
for b in biz:
    bid = b["business_id"]
    cats = set()
    for t in per_biz[bid]:
        r = resolve(t)
        if r:
            cats.add(r)
        else:
            leftover[bid].append(t)
    for c in cats:
        cat_biz[c].add(bid)

print("LEFTOVER TOKENS (unresolved):")
for bid, toks in leftover.items():
    print(" ", bid, toks)
print()

counts = sorted(cat_biz.items(), key=lambda kv: (-len(kv[1]), kv[0]))
print("=== CATEGORY COUNTS (top 20) ===")
results = []
for cat, ids in counts:
    tot_n, tot_sum, biz_avgs = 0, 0.0, []
    for bid in ids:
        ref = bid.replace("businessid_", "businessref_")
        if ref in ratings:
            n, a = ratings[ref]
            tot_n += n; tot_sum += n * a; biz_avgs.append(a)
    w_avg = tot_sum / tot_n if tot_n else None
    b_avg = sum(biz_avgs) / len(biz_avgs) if biz_avgs else None
    results.append((cat, len(ids), w_avg, b_avg))
for cat, n, w, bavg in results[:20]:
    print(f"{n:3d}  {cat:40s} review_weighted_avg={w:.4f}  mean_of_biz_avg={bavg:.4f}")

print()
top = results[0]
print(f"TOP: {top[0]} with {top[1]} businesses, review-weighted avg rating = {top[2]:.4f}, mean-of-business-avg = {top[3]:.4f}")

# show member businesses of top category
print("Members:", sorted(cat_biz[top[0]]))
