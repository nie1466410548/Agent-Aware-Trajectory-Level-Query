import json, re
import pandas as pd

books_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query1/full-01/results/03d5c76cc54042659f2cb47ebdd1b113.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query1/full-01/results/a36a31355fde4336b6bf26914c919f18.json"

books = pd.DataFrame(json.load(open(books_path)))
revs = pd.DataFrame(json.load(open(rev_path)))

def extract_year(details):
    if not isinstance(details, str):
        return None
    m = re.findall(r"\b(1[5-9]\d{2}|20[0-2]\d)\b", details)
    return int(m[0]) if m else None

books["year"] = books["details"].apply(extract_year)
books["num"] = books["book_id"].str.extract(r"(\d+)").astype(int)
revs["num"] = revs["purchase_id"].str.extract(r"(\d+)").astype(int)
merged = books.merge(revs, on="num", how="inner").dropna(subset=["year"])
merged["year"] = merged["year"].astype(int)
merged["decade"] = (merged["year"]//10*10).astype(str)+"s"

for dec in ["1980s", "2020s"]:
    sub = merged[merged["decade"] == dec]
    print(f"=== {dec} ({len(sub)} books) ===")
    for _, r in sub.iterrows():
        print(r["year"], "|", str(r["details"])[:110].replace("\n", " "))
    print()

# raw-review-level average per decade (equivalent to AVG(rating) grouped by decade)
merged["total"] = merged["avg_rating"] * merged["n_reviews"]
res = merged.groupby("decade").agg(n_books=("book_id","nunique"),
                                   avg_rating=("total", lambda x: 0),
                                   tot=("total","sum"), nrev=("n_reviews","sum"))
res["avg_rating"] = res["tot"]/res["nrev"]
elig = res[res["n_books"]>=10]
print(elig[["n_books","avg_rating"]].sort_values("avg_rating", ascending=False).to_string())
