import json, re

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query2/full-01/results/bf45e97a9a8a42a2b015542d56e394e6.json"))
perfect = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query2/full-01/results/08d3b2721dad44e48890dabf5ea16393.json"))

def num(s):
    m = re.search(r"(\d+)$", s or "")
    return m.group(1) if m else None

perfect_nums = {num(p["purchase_id"]): p for p in perfect}

results = []
for b in books:
    n = num(b["book_id"])
    if n in perfect_nums:
        d = (b.get("details") or "")
        english = "english" in d.lower()
        p = perfect_nums[n]
        results.append({
            "book_id": b["book_id"],
            "title": b["title"],
            "avg_rating": p["avg_rating"],
            "n_reviews": p["n_reviews"],
            "rating_number": b.get("rating_number"),
            "english_in_details": english,
        })

results.sort(key=lambda r: int(num(r["book_id"])))
print("Matched:", len(results))
for r in results:
    print(r)

# sanity: any matched book not marked English?
print("Non-English matches:", [r for r in results if not r["english_in_details"]])
