import json

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query2/full-01/results/"
books = json.load(open(base + "38e30bb3230740d381cf2de5dea8b7dc.json"))
perfect = json.load(open(base + "e417efefc15645cba444b7de1e46d7a1.json"))

# map purchaseid_N -> bookid_N
perfect_map = {}
for p in perfect:
    bid = p["purchase_id"].replace("purchaseid_", "bookid_")
    perfect_map[bid] = p

results = []
for b in books:
    if b["book_id"] in perfect_map:
        results.append({
            "book_id": b["book_id"],
            "title": b["title"],
            "num_reviews": perfect_map[b["book_id"]]["num_reviews"],
            "avg_rating": perfect_map[b["book_id"]]["avg_rating"],
        })

results.sort(key=lambda r: int(r["book_id"].split("_")[1]))
print("Matching books:", len(results))
for r in results:
    print(f'{r["book_id"]:12s} | reviews={r["num_reviews"]:2d} | avg={r["avg_rating"]} | {r["title"]}')

with open("matches.json", "w") as f:
    json.dump(results, f, indent=2)
