import json, re
import pandas as pd

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query1/quick-01/results/c59919c876aa4580b6ad31fafb1e3310.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query1/quick-01/results/e807583df8154c0ead0b2b088b70c3f2.json"))

bdf = pd.DataFrame(books)
rdf = pd.DataFrame(reviews)

# Extract publication year: first 4-digit year 1900-2023 in details text
def extract_year(details):
    if not details:
        return None
    m = re.search(r'\b(19\d{2}|20[0-2]\d)\b', details)
    return int(m.group(1)) if m else None

bdf["year"] = bdf["details"].apply(extract_year)
print("Books with year:", bdf["year"].notna().sum(), "of", len(bdf))

# Map purchase_id -> book_id
rdf["book_id"] = rdf["purchase_id"].str.replace("purchaseid_", "bookid_", regex=False)
unmatched = set(rdf["book_id"]) - set(bdf["book_id"])
print("Unmatched review book_ids:", unmatched)

merged = rdf.merge(bdf[["book_id", "year"]], on="book_id", how="inner")
merged = merged.dropna(subset=["year"])
merged["decade"] = (merged["year"].astype(int) // 10) * 10

grp = merged.groupby("decade").agg(
    avg_rating=("rating", "mean"),
    n_reviews=("rating", "size"),
    n_books=("book_id", "nunique"),
).reset_index()
grp["decade_label"] = grp["decade"].astype(str) + "s"
print(grp.sort_values("decade").to_string(index=False))

eligible = grp[grp["n_books"] >= 10]
best = eligible.sort_values("avg_rating", ascending=False).iloc[0]
print("\nBest decade:", best["decade_label"], "avg_rating=", round(best["avg_rating"], 4),
      "n_books=", best["n_books"], "n_reviews=", best["n_reviews"])
