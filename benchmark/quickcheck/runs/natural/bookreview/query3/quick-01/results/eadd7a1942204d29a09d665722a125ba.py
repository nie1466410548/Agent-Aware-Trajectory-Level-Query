import json
import pandas as pd

books_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query3/quick-01/results/71b1f3f7c46146d2859d5372e8b93978.json"
rev_path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query3/quick-01/results/e205ed43cb4a4072b197b1007e3a0e02.json"

books = pd.DataFrame(json.load(open(books_path)))
revs = pd.DataFrame(json.load(open(rev_path)))

# purchaseid_N -> bookid_N
revs["book_id"] = revs["purchase_id"].str.replace("purchaseid_", "bookid_", regex=False)
revs["rating"] = revs["rating"].astype(float)

merged = revs.merge(books[["book_id", "title"]], on="book_id", how="inner")
print("Children's books with >=1 review from 2020 onwards:", merged["book_id"].nunique())

g = merged.groupby(["book_id", "title"]).agg(
    n_reviews=("rating", "count"), avg_rating=("rating", "mean")
).reset_index().sort_values("avg_rating", ascending=False)

res = g[g["avg_rating"] >= 4.5]
print(res.to_string(index=False))

lines = []
for _, r in res.iterrows():
    lines.append(f"{r['title']} ({r['book_id']}): avg rating {r['avg_rating']:.2f} over {int(r['n_reviews'])} review(s) from 2020 onwards")
open("final.txt", "w").write("\n".join(lines) + "\n")
print("\nWrote final.txt")
