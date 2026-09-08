import json, re
from collections import Counter

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

def clean(run):
    return run.strip().rstrip(".'").strip()

def zone(desc):
    m = re.match(r"^Located at .*, [A-Z]{2}, (.*)$", desc)
    return m.group(1) if m else desc

def extract_runs(desc):
    text = zone(desc)
    am = ANCHOR.search(text)
    start = am.start() if am else 0
    runs = []
    for m in TITLE_RUN.finditer(text, start):
        run = clean(m.group(0))
        if not run or run.startswith(STOP_PREFIX) or STATE.match(run):
            continue
        runs.append(run)
    return runs

biz_runs, vocab = {}, Counter()
for b in biz:
    runs = extract_runs(b["description"])
    biz_runs[b["business_id"]] = runs
    for r in runs:
        vocab[r] += 1

vocab_lower = {v.lower(): v for v in vocab}
biz_cats = {}
for b in biz:
    bid = b["business_id"]
    cats = set(biz_runs[bid])
    text = zone(b["description"])
    for s in re.split(r",\s*|\s+and\s+", text):
        s2 = clean(re.sub(r"\s+(cuisine|options)$", "", s.strip().strip("'\"").strip()))
        if s2.lower() in vocab_lower and s2 != vocab_lower[s2.lower()]:
            cats.add(vocab_lower[s2.lower()])
    biz_cats[bid] = cats

cat_count = Counter()
for bid, cats in biz_cats.items():
    for c in cats:
        cat_count[c] += 1

print("=== top category counts (normalized) ===")
for c, n in cat_count.most_common(12):
    print(f"{n:3d}  {c}")

top_cat, top_n = cat_count.most_common(1)[0]
members = sorted(bid for bid, cats in biz_cats.items() if top_cat in cats)
print(f"\nTop category: {top_cat} ({top_n} businesses accepting credit cards)")

tot_r, tot_n, biz_avgs = 0.0, 0, []
for bid in members:
    if bid in avg_rating:
        tot_r += avg_rating[bid] * n_reviews[bid]
        tot_n += n_reviews[bid]
        biz_avgs.append(avg_rating[bid])
rev_level = tot_r / tot_n
biz_level = sum(biz_avgs) / len(biz_avgs)
print(f"Members: {len(members)}, all with reviews: {len(biz_avgs)}")
print(f"Review-level avg rating: {rev_level:.4f} ({tot_n} reviews)")
print(f"Business-level mean of avg ratings: {biz_level:.4f}")

# spot-check a few extractions
for bid in ["businessid_93", "businessid_49", "businessid_8"]:
    d = next(b["description"] for b in biz if b["business_id"] == bid)
    print(f"\n{bid}: {sorted(biz_cats[bid])}\n  desc: {d}")
