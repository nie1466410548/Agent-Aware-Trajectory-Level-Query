import json, re
from collections import Counter, defaultdict

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query4/full-01/results/c6eb9cd17a1d4de2bf265e604f39f155.json"
rev_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query4/full-01/results/c209a85fe1384b49929934be2851e297.json"

biz = json.load(open(biz_file))
revs = json.load(open(rev_file))

avg_rating, n_reviews = {}, {}
for r in revs:
    bid = r["business_ref"].replace("businessref_", "businessid_")
    avg_rating[bid] = r["avg_rating"]
    n_reviews[bid] = r["n_reviews"]

TITLE_RUN = re.compile(r"(?:[A-Z][\w'&/\-\.]*|\([A-Za-z ]+\)|&)(?:\s+(?:[A-Z][\w'&/\-\.]*|\([A-Za-z ]+\)|&))*")
ANCHOR = re.compile(r"\b(offers|specializes|provides|features|featuring|is)\b")
STOP_PREFIX = ("This", "Located", "The")
STATE = re.compile(r"^[A-Z]{2}$")

def zone(desc):
    m = re.match(r"^Located at .*, [A-Z]{2}, (.*)$", desc)  # greedy -> last state code
    return m.group(1) if m else desc

def extract_runs(desc):
    text = zone(desc)
    am = ANCHOR.search(text)
    start = am.start() if am else 0
    runs = []
    for m in TITLE_RUN.finditer(text, start):
        run = m.group(0).strip()
        if run.startswith(STOP_PREFIX):
            continue
        if STATE.match(run):
            continue
        runs.append(run)
    return runs

# build vocabulary of Title-Case runs
biz_runs = {}
vocab = Counter()
for b in biz:
    runs = extract_runs(b["description"])
    biz_runs[b["business_id"]] = runs
    for r in runs:
        vocab[r] += 1

# lowercase fallback: comma/and-separated lowercase segments matching vocab case-insensitively
vocab_lower = {v.lower(): v for v in vocab}
biz_cats = {}
for b in biz:
    bid = b["business_id"]
    cats = set(biz_runs[bid])
    text = zone(b["description"])
    segs = re.split(r",\s*|\s+and\s+", text)
    for s in segs:
        s2 = s.strip().strip("'\"").strip()
        s2 = re.sub(r"\s+(cuisine|options)$", "", s2)
        key = s2.lower()
        if key in vocab_lower and s2 != vocab_lower[key]:
            cats.add(vocab_lower[key])
    biz_cats[bid] = cats

print("=== vocabulary (all runs) ===")
for c, n in sorted(vocab.items()):
    print(f"{n:3d}  {c}")

cat_count = Counter()
for bid, cats in biz_cats.items():
    for c in cats:
        cat_count[c] += 1

print("\n=== category counts (businesses accepting credit cards) ===")
for c, n in cat_count.most_common(15):
    print(f"{n:3d}  {c}")

top_cat, top_n = cat_count.most_common(1)[0]
members = [bid for bid, cats in biz_cats.items() if top_cat in cats]
print(f"\nTop category: {top_cat} with {top_n} businesses")
print("Members:", sorted(members))

# average rating: review-level and business-level
tot_r, tot_n, biz_avgs = 0.0, 0, []
for bid in members:
    if bid in avg_rating:
        tot_r += avg_rating[bid] * n_reviews[bid]
        tot_n += n_reviews[bid]
        biz_avgs.append(avg_rating[bid])
print(f"Review-level avg rating: {tot_r/tot_n:.4f} over {tot_n} reviews of {len(biz_avgs)} businesses")
print(f"Business-level avg of avg ratings: {sum(biz_avgs)/len(biz_avgs):.4f}")
print("Members without reviews:", [b for b in members if b not in avg_rating])
