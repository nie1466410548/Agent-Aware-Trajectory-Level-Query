import json, re
from collections import defaultdict

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/f00079fe297e4114a2943386d14643e7.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/0197c66f295c4ca49c138a8b1afc4d04.json"))

print("books:", len(books), "rated books:", len(reviews))

year_re = re.compile(r'\b(1[89]\d{2}|20[0-2]\d)\b')

def pub_year(details):
    if not details:
        return None
    m = year_re.search(details)
    if m:
        return int(m.group(1))
    return None

years = {}
no_year = []
for b in books:
    y = pub_year(b["details"])
    if y is None:
        no_year.append(b["book_id"])
    else:
        years[b["book_id"]] = y

print("books with year:", len(years), "without:", len(no_year))
print("no-year books:", no_year)

# map purchaseid_N -> bookid_N
rated = {}
for r in reviews:
    bid = r["purchase_id"].replace("purchaseid_", "bookid_")
    rated[bid] = (r["avg_rating"], r["n"])

# check overlap
matched = [b for b in rated if b in years]
print("rated books with year:", len(matched), "rated total:", len(rated))
missing = [b for b in rated if b not in years]
print("rated but no year:", missing)

dec_books = defaultdict(list)   # decade -> list of (avg, n)
for bid, y in years.items():
    if bid in rated:
        dec = (y // 10) * 10
        dec_books[dec].append(rated[bid])

rows = []
for dec, lst in sorted(dec_books.items()):
    nb = len(lst)
    mean_book = sum(a for a, n in lst) / nb
    tot_n = sum(n for a, n in lst)
    mean_rev = sum(a * n for a, n in lst) / tot_n
    rows.append((dec, nb, tot_n, mean_book, mean_rev))
    print(f"{dec}s: books={nb:3d} reviews={tot_n:4d} avg(book-level)={mean_book:.4f} avg(review-level)={mean_rev:.4f}")

elig = [r for r in rows if r[1] >= 10]
best_book = max(elig, key=lambda r: r[3])
best_rev = max(elig, key=lambda r: r[4])
print("\nBest (book-level avg):", best_book)
print("Best (review-level avg):", best_rev)
