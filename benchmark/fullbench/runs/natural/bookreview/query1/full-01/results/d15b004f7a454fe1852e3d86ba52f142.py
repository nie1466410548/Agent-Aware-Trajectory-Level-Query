import json, re
from collections import defaultdict

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/f00079fe297e4114a2943386d14643e7.json"))
reviews = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query1/full-01/results/0197c66f295c4ca49c138a8b1afc4d04.json"))

year_re = re.compile(r'\b(1[89]\d{2}|20[0-2]\d)\b(?!\s*KB)')

rated = {r["purchase_id"].replace("purchaseid_", "bookid_"): (r["avg_rating"], r["n"]) for r in reviews}

def years_in(details):
    return [int(m.group(1)) for m in year_re.finditer(details or "")]

def summarize(years):
    dec_books = defaultdict(list)
    for bid, y in years.items():
        if bid in rated:
            dec_books[(y // 10) * 10].append(rated[bid])
    rows = []
    for dec, lst in sorted(dec_books.items()):
        nb = len(lst)
        mean_book = sum(a for a, n in lst) / nb
        tot_n = sum(n for a, n in lst)
        mean_rev = sum(a * n for a, n in lst) / tot_n
        rows.append((dec, nb, tot_n, mean_book, mean_rev))
    return rows

for name, picker in [("first year", lambda ys: ys[0] if ys else None),
                     ("last year", lambda ys: ys[-1] if ys else None)]:
    years = {}
    for b in books:
        y = picker(years_in(b["details"]))
        if y is not None:
            years[b["book_id"]] = y
    rows = summarize(years)
    print(f"=== {name} ===")
    for r in rows:
        flag = " *" if r[1] >= 10 else ""
        print(f"{r[0]}s: books={r[1]:3d} avg(book)={r[3]:.4f} avg(review)={r[4]:.4f}{flag}")
    elig = [r for r in rows if r[1] >= 10]
    print("best book-level:", max(elig, key=lambda r: r[3])[:2], "best review-level:", max(elig, key=lambda r: r[4])[:2])
    print()
