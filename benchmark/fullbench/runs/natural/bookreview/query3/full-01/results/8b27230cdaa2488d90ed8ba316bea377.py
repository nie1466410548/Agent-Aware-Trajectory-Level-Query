import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query3/full-01/results/6cb64f355c544ccf842b3ce8abccb9c9.json") as f:
    books = json.load(f)

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query3/full-01/results/32eecb3eaa6d47bf8f0a06992259314b.json") as f:
    reviews = json.load(f)

# Map purchaseid_N -> bookid_N
rev_by_book = {}
for r in reviews:
    num = r["purchase_id"].replace("purchaseid_", "")
    rev_by_book["bookid_" + num] = r

results = []
for b in books:
    r = rev_by_book.get(b["book_id"])
    if r and r["avg_rating"] >= 4.5:
        results.append((b["title"], b["book_id"], round(r["avg_rating"], 4), r["n"]))

results.sort(key=lambda x: x[0])
for t in results:
    print(t)
print("COUNT:", len(results))

# sanity: any unmatched purchase ids mapping to children's books?
print("books without 2020+ reviews:", [b["title"] for b in books if b["book_id"] not in rev_by_book])
