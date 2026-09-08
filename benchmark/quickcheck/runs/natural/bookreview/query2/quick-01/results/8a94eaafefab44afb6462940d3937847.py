import json, re

books_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query2/quick-01/results/ef73e65452a14ec8867b4517ab36a87b.json"
reviews_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/natural/bookreview/query2/quick-01/results/993bae1d28094106935473ff66012ecf.json"

books = json.load(open(books_file))
reviews = json.load(open(reviews_file))

print("Lit&Fiction books:", len(books))
print("Review groups:", len(reviews))

# Map purchase_id -> avg rating
avg_by_pid = {r["purchase_id"]: r["avg_rating"] for r in reviews}
nrev_by_pid = {r["purchase_id"]: r["n_reviews"] for r in reviews}

def num_suffix(s):
    m = re.search(r"_(\d+)$", s)
    return m.group(1) if m else None

# Language check: details should state the book is in English
matches = []
non_english = []
for b in books:
    det = (b.get("details") or "")
    # English-language if details say written/available/published "in English"
    is_english = re.search(r"in English\b|English-language", det, re.IGNORECASE) is not None
    # guard: exclude if details say the book is written/available in another (non-English) language
    other_lang = re.search(r"(written|available|published) in (?!English\b)([A-Z][a-z]+)", det)
    if other_lang:
        is_english = False
    if not is_english:
        non_english.append((b["book_id"], b["title"], det[:120]))
        continue
    suffix = num_suffix(b["book_id"])
    pid = f"purchaseid_{suffix}"
    avg = avg_by_pid.get(pid)
    if avg is not None and abs(avg - 5.0) < 1e-9:
        matches.append({
            "book_id": b["book_id"],
            "purchase_id": pid,
            "title": b["title"],
            "avg_rating": avg,
            "n_reviews": nrev_by_pid[pid],
        })

print("\nNon-English or unclear-language Lit&Fiction books (excluded):", len(non_english))
for x in non_english:
    print("  ", x)

# sanity: how many lit&fic books have reviews at all
with_reviews = sum(1 for b in books if f"purchaseid_{num_suffix(b['book_id'])}" in avg_by_pid)
print("Lit&Fiction books with reviews:", with_reviews)

matches.sort(key=lambda x: int(num_suffix(x["book_id"])))
print("\nMATCHING BOOKS (English, Literature & Fiction, avg rating = 5.0):", len(matches))
for m in matches:
    print(f"  {m['book_id']} | {m['title']} | avg={m['avg_rating']} | reviews={m['n_reviews']}")

with open("matches.json", "w") as f:
    json.dump(matches, f, indent=2)
