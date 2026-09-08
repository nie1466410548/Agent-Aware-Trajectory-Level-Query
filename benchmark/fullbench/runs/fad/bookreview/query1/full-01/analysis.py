import json, re
import pandas as pd

books_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query1/full-01/results/03d5c76cc54042659f2cb47ebdd1b113.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query1/full-01/results/a36a31355fde4336b6bf26914c919f18.json"

books = pd.DataFrame(json.load(open(books_path)))
revs = pd.DataFrame(json.load(open(rev_path)))

def extract_year(details):
    if not isinstance(details, str):
        return None
    # find plausible publication years (1500-2023), take the first occurrence
    m = re.findall(r"\b(1[5-9]\d{2}|20[0-2]\d)\b", details)
    if not m:
        return None
    y = int(m[0])
    return y if 1500 <= y <= 2023 else None

books["year"] = books["details"].apply(extract_year)
books["num"] = books["book_id"].str.extract(r"(\d+)").astype(int)
revs["num"] = revs["purchase_id"].str.extract(r"(\d+)").astype(int)

merged = books.merge(revs, on="num", how="inner")
print("books:", len(books), "with year:", books["year"].notna().sum(), "merged:", len(merged))
print("books without year:", merged[merged["year"].isna()]["book_id"].tolist())

merged = merged.dropna(subset=["year"])
merged["year"] = merged["year"].astype(int)
merged["decade"] = (merged["year"] // 10 * 10).astype(str) + "s"

# distinct rated books per decade
g = merged.groupby("decade")
summary = pd.DataFrame({
    "n_books": g["book_id"].nunique(),
    "avg_of_book_avg": g["avg_rating"].mean(),
    "weighted_avg_all_reviews": g.apply(lambda d: (d["avg_rating"]*d["n_reviews"]).sum()/d["n_reviews"].sum(), include_groups=False),
    "total_reviews": g["n_reviews"].sum(),
}).sort_index()
print(summary.to_string())

elig = summary[summary["n_books"] >= 10]
print("\nEligible decades (>=10 distinct rated books):")
print(elig.to_string())
print("\nBest by avg of book averages:", elig["avg_of_book_avg"].idxmax(), elig["avg_of_book_avg"].max())
print("Best by weighted avg of all reviews:", elig["weighted_avg_all_reviews"].idxmax(), elig["weighted_avg_all_reviews"].max())
print("\nYear range per decade check:")
print(merged.groupby("decade")["year"].agg(["min","max","count"]).to_string())
