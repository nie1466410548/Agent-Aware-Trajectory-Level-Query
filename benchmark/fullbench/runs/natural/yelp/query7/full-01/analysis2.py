import json, re
from collections import Counter

REV = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/eb152856605544129147da66dcb425f3.json"
BIZ = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/yelp/query7/full-01/results/aa4c2b6e07274a28adccbf9c1bfcf806.json"

reviews = json.load(open(REV))
biz = json.load(open(BIZ))

def split_candidates(desc):
    d = desc.replace("'", " ")
    parts = re.split(r',|\band\b', d)
    return [p.strip(' .;') for p in parts if p.strip(' .;')]

cand_counter = Counter()
for b in biz:
    for p in split_candidates(b["description"]):
        cand_counter[p] += 1

# Clean vocabulary: recurring, Title-Case (starts uppercase), not a 2-letter state code
vocab = set()
for p, c in cand_counter.items():
    if c < 2: continue
    if re.fullmatch(r'[A-Z]{2}', p): continue
    if not p[0].isupper(): continue
    vocab.add(p)
print("clean vocab size:", len(vocab))

# Non-overlapping longest-match scan per description (case-insensitive)
vlist = sorted(vocab, key=len, reverse=True)
def extract_cats(desc):
    found = []
    occupied = [False]*len(desc)
    low = desc.lower()
    for cat in vlist:
        cl = cat.lower()
        start = 0
        while True:
            i = low.find(cl, start)
            if i == -1: break
            j = i + len(cl)
            # word boundaries
            left_ok = i == 0 or not (low[i-1].isalnum())
            right_ok = j == len(low) or not (low[j].isalnum())
            if left_ok and right_ok and not any(occupied[i:j]):
                found.append(cat)
                for k in range(i, j): occupied[k] = True
            start = i + 1
    return set(found)

biz_cats = {}
empty = []
for b in biz:
    cats = extract_cats(b["description"])
    biz_cats[b["business_id"]] = cats
    if not cats:
        empty.append(b)
print("businesses with no categories:", len(empty))
for b in empty[:10]:
    print("  EMPTY:", b["business_id"], "|", b["description"][:150])

def num(s): return re.search(r'(\d+)$', s).group(1)

# all reviews are yr>=2016 (verified), still filter defensively
cat_counts = Counter()
per_review_no_cat = []
for r in reviews:
    if r["yr"] is not None and r["yr"] < 2016: continue
    bid = "businessid_" + num(r["business_ref"])
    cats = biz_cats.get(bid, set())
    if not cats:
        per_review_no_cat.append((r["review_id"], bid))
    for c in cats:
        cat_counts[c] += 1

print("reviews with no category:", len(per_review_no_cat), per_review_no_cat[:10])
print("\nTOP 15 categories by review count:")
for c, n in cat_counts.most_common(15):
    print(f"  {c}: {n}")
