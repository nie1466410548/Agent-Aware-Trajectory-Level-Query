import json, re
from collections import Counter, defaultdict

biz_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query4/full-01/results/c6eb9cd17a1d4de2bf265e604f39f155.json"
rev_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query4/full-01/results/c209a85fe1384b49929934be2851e297.json"

biz = json.load(open(biz_file))
revs = json.load(open(rev_file))

# map review refs -> business ids (businessref_N -> businessid_N)
avg_rating = {}
n_reviews = {}
for r in revs:
    bid = r["business_ref"].replace("businessref_", "businessid_")
    avg_rating[bid] = r["avg_rating"]
    n_reviews[bid] = r["n_reviews"]

anchors = ["services and products in the fields of", "products and services in the categories of",
           "services in the categories of", "services in the category of", "in the categories of",
           "in the category of", "range of services in", "services, including", "services including",
           "products across various categories, including", "products in categories such as",
           "options ranging from", "array of options ranging from", "selection of treats in the categories of",
           "premier destination for", "specializes in", "selection of", "mix of", "array of dishes in",
           "menu featuring", "atmosphere for enjoying", "solutions including", "offers a variety of treats including",
           "offers a variety of quick and delicious options in the categories of",
           "including", "featuring", " in ", " for "]

def extract(desc):
    # strip "Located at ... , this" intro
    m = re.match(r"^Located at .*?, [A-Z]{2}, (.*)$", desc)
    if m:
        text = m.group(1)
    else:
        text = desc
    # find earliest anchor
    best = None
    for a in anchors:
        i = text.find(a)
        if i != -1 and (best is None or i < best[0]):
            best = (i, a)
    if best is None:
        return []
    text = text[best[0] + len(best[1]):]
    text = text.strip().strip("'\"")
    # cut at sentence end
    text = text.rstrip(".")
    # split into segments
    segs = re.split(r",\s*|\s+and\s+|\s+to\s+", text)
    cats = []
    for s in segs:
        s = s.strip().strip("'\"").strip()
        # remove trailing descriptor words
        s = re.sub(r"\s+(cuisine|services|options|products|dishes|treats)$", "", s, flags=re.I)
        # drop segments with trailing narrative
        s = re.split(r"\s+(making|offering|to meet|for all|perfect|along with|to make|that)\b", s)[0].strip()
        if not s:
            continue
        cats.append(s)
    return cats

biz_cats = {}
all_segs = Counter()
for b in biz:
    cats = extract(b["description"])
    biz_cats[b["business_id"]] = cats
    for c in cats:
        all_segs[c] += 1

print("=== raw extracted segments (count) ===")
for c, n in all_segs.most_common():
    print(f"{n:3d}  {c!r}")
