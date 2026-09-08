import json

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query3/quick-01/results/d26c7fef90ed4b3e89848430f1a51f5b.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query3/quick-01/results/b30add6f0f9744a78e7557ea88fc0d09.json"))

children = {b["book_id"].replace("bookid_", ""): b for b in books}
print(f"Children's books: {len(children)}")
print("Children's book ids:", sorted(children.keys(), key=int))

results = []
for r in reviews:
    num = r["purchase_id"].replace("purchaseid_", "")
    if num in children and r["avg_rating"] >= 4.5:
        results.append((children[num]["title"], r["avg_rating"], r["n_reviews"], children[num]["book_id"]))

results.sort(key=lambda x: (-x[1], x[0]))
print("\nChildren's books with avg rating >= 4.5 (reviews from 2020 onwards):")
for t, a, n, bid in results:
    print(f"- {t} (book_id={bid}): avg={a:.4f}, n_reviews={n}")

with open("qualified.txt", "w") as f:
    for t, a, n, bid in results:
        f.write(f"{t} (book_id={bid}): avg_rating={a:.4f}, n_reviews={n}\n")
