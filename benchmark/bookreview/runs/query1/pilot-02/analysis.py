import json, re
import pandas as pd

books_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/runs/query1/pilot-02/results/fe18cdf6bf2c459da8a25f986e755e4f.json"
reviews_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/bookreview/runs/query1/pilot-02/results/012f55da688742d1967229b782a0c8dc.json"

books = json.load(open(books_path))
reviews = json.load(open(reviews_path))

def num_suffix(x):
    if x is None:
        return None
    m = re.findall(r"\d+", str(x))
    return int(m[-1]) if m else None

months = "January|February|March|April|May|June|July|August|September|October|November|December"
date_pat1 = re.compile(rf"(?:{months})\s+\d{{1,2}},\s+(\d{{4}})", re.I)
date_pat2 = re.compile(rf"(?:{months})\s+(\d{{4}})", re.I)
year_pat = re.compile(r"\b(18\d{2}|19\d{2}|20[0-2]\d)\b")

def extract_year(details):
    if not details:
        return None
    s = str(details)
    lower = s.lower()
    # Prefer the first date/year appearing near a publication/release phrase.
    pubs = [m.start() for m in re.finditer(r"published|released|publication|first edition|edition", lower)]
    starts = pubs[:1] if pubs else [0]
    for start in starts:
        window = s[start:start+180]
        for pat in (date_pat1, date_pat2, year_pat):
            m = pat.search(window)
            if m:
                y = int(m.group(1))
                if 1800 <= y <= 2023:
                    return y
    m = year_pat.search(s)
    if m:
        y = int(m.group(1))
        if 1800 <= y <= 2023:
            return y
    return None

bdf = pd.DataFrame(books)
bdf["key"] = bdf["book_id"].map(num_suffix)
bdf["year"] = bdf["details"].map(extract_year)
bdf["decade"] = (bdf["year"] // 10 * 10).astype("Int64")

rdf = pd.DataFrame(reviews)
rdf["key"] = rdf["purchase_id"].map(num_suffix)
rdf["rating"] = pd.to_numeric(rdf["rating"], errors="coerce")

merged = rdf.merge(bdf[["key", "book_id", "title", "year", "decade"]], on="key", how="left")
print("books", len(bdf), "reviews", len(rdf), "merged", len(merged))
print("unmatched_reviews", int(merged["book_id"].isna().sum()))
print("books_missing_year", int(bdf["year"].isna().sum()))
print(bdf.loc[bdf["year"].isna(), ["book_id", "title", "details"]].to_string(index=False))

rated = merged.dropna(subset=["decade", "rating"]).copy()
rated["decade"] = rated["decade"].astype(int)
summary = rated.groupby("decade").agg(
    avg_rating=("rating", "mean"),
    n_reviews=("rating", "size"),
    n_distinct_books=("key", "nunique"),
).reset_index()
summary["decade_label"] = summary["decade"].astype(str) + "s"
summary = summary.sort_values("avg_rating", ascending=False)
print(summary.to_string(index=False, float_format=lambda x: f"{x:.6f}"))

eligible = summary[summary["n_distinct_books"] >= 10]
print("ELIGIBLE")
print(eligible.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
if len(eligible):
    best = eligible.iloc[0]
    print("BEST", best["decade_label"], best["avg_rating"], "books", best["n_distinct_books"], "reviews", best["n_reviews"])

# Show book counts by decade including unrated/missing for context
print("book decade counts")
print(bdf.groupby("decade")["book_id"].nunique().reset_index().to_string(index=False))
