import json, re
from collections import Counter

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/yelp/query7/full-01/results/"
users = json.load(open(base + "a453d71d887b4a529cad4e8b09fac51a.json"))
reviews = json.load(open(base + "3fe71260d1d6471da56e8703c7811db1.json"))
biz = json.load(open(base + "2f1c37273e3249d393fdb4d84317fd33.json"))

def year_of(s):
    m = re.search(r"(19|20)\d{2}", s or "")
    return int(m.group(0)) if m else None

users2016 = {u["user_id"] for u in users if year_of(u["yelping_since"]) == 2016}
print("users registered in 2016:", len(users2016))

TRIGGERS = ["ranging from ", "in the category of ", "in the categories of ",
            "category of ", "categories of ", "categories such as ", "such as ",
            "in the fields of ", "in the field of ", "in the areas of ",
            "in the realm of ", "services in ", "solutions in ", "options in ",
            "mix of ", "selection of ", "destination for ", "featuring ",
            "options for ", "enjoying ", "specializes in ", "specializing in ",
            "showcasing ", "seeking ", "within the ", "including ", "encompassing ",
            "array of dishes in ", "experience in "]
CUTTERS = [", making", ", perfect", ", offering", ", providing", ", ensuring",
           ", catering", " to meet", " to cater", " to enhance", " to keep",
           " for all your", " options for every palate", " enthusiasts"]
PREFIXES = ["along with a lively atmosphere perfect for ", "offering a taste of ",
            "providing essential ", "offering a comprehensive ", "offering a ",
            "providing ", "professional ", "comprehensive ", "delicious ",
            "essential "]
# lowercase-only suffixes (case-sensitive): category names like "Home Services" stay intact
SUFFIXES = [" services", " service", " categories", " category", " cuisine",
            " options", " sector"]

MANUAL = {
    "businessid_31": ["Automotive", "Car Wash", "Auto Detailing"],
    "businessid_34": ["Landmarks & Historical Buildings", "Local Flavor", "Public Services & Government"],
    "businessid_95": ["Restaurants", "Sandwiches", "Specialty Food", "Food", "Fruits & Veggies", "Fast Food"],
    "businessid_19": ["Restaurants", "Peruvian", "Food", "Food Trucks"],
}

def parse_categories(bid, desc):
    if bid in MANUAL:
        return MANUAL[bid]
    d = desc.strip()
    # use the LAST trigger occurrence (category list is at the end of the sentence)
    seg, best = None, -1
    for t in TRIGGERS:
        i = d.rfind(t)
        if i > best:
            best = i
            seg = d[i + len(t):]
    if seg is None:
        return ["__UNPARSED__"]
    for c in CUTTERS:
        j = seg.find(c)
        if j != -1:
            seg = seg[:j]
    seg = seg.strip().strip(".'\"").strip()
    parts = re.split(r",\s*|\s+and\s+", seg)
    cats = []
    for p in parts:
        p = p.strip().strip(".'\"").strip()
        p = re.sub(r"^(to|and)\s+", "", p)
        for pre in PREFIXES:
            if p.lower().startswith(pre):
                p = p[len(pre):]
                break
        p = re.sub(r"^(a|an)\s+", "", p)
        for suf in SUFFIXES:
            if p.endswith(suf):  # case-sensitive on purpose
                p = p[:-len(suf)]
                break
        p = p.strip().strip(".'\"").strip()
        if not p:
            continue
        if p == p.lower():
            p = p.title()
        cats.append(p)
    return cats

biz_cats = {}
for b in biz:
    cats = parse_categories(b["business_id"], b["description"])
    biz_cats[b["business_id"]] = cats
    print(b["business_id"], "->", cats)

cnt = Counter()
n_rev = 0
unmatched = set()
for r in reviews:
    uid = r["user_id"]
    if uid is None or uid not in users2016:
        continue
    if (year_of(r["date"]) or 0) < 2016:
        continue
    n_rev += 1
    bref = r["business_ref"].replace("businessref_", "businessid_")
    if bref not in biz_cats:
        unmatched.add(bref)
        continue
    for c in set(biz_cats[bref]):
        cnt[c] += 1

print("\nqualifying reviews:", n_rev, "unmatched refs:", unmatched)
print("\nTop categories:")
for cat, n in cnt.most_common(20):
    print(f"{n:4d}  {cat}")
