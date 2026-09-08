import json, re
from collections import defaultdict

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query1/quick-01/results/db4c3243dfcb40d0a6eff5e2303a3797.json"))
revs = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query1/quick-01/results/c5144e2ba09a49a391d5d285c1fbb885.json"))

months = "January|February|March|April|May|June|July|August|September|October|November|December"
pat_full = re.compile(r"(?:%s)\s+\d{1,2},?\s+(\d{4})" % months)
pat_mon = re.compile(r"(?:%s)\s+(\d{4})" % months)
pat_year = re.compile(r"\b(1[89]\d{2}|20[0-2]\d)\b")

def extract_year(details):
    m = pat_full.search(details)
    if m: return int(m.group(1))
    m = pat_mon.search(details)
    if m: return int(m.group(1))
    m = pat_year.search(details)
    if m: return int(m.group(1))
    return None

book_year = {}
for b in books:
    book_year[b["book_id"]] = extract_year(b["details"] or "")

# map purchaseid_N -> bookid_N
def num(x): return x.split("_")[-1]
book_by_num = {num(k): k for k in book_year}

dec_books = defaultdict(set)          # decade -> set of book ids
dec_rating_sum = defaultdict(float)   # review-weighted
dec_rating_cnt = defaultdict(int)
dec_bookavg = defaultdict(list)       # per-book average ratings

unmatched, noyear = [], []
for r in revs:
    n = num(r["purchase_id"])
    bid = book_by_num.get(n)
    if bid is None:
        unmatched.append(r["purchase_id"]); continue
    y = book_year[bid]
    if y is None:
        noyear.append(bid); continue
    dec = (y // 10) * 10
    dec_books[dec].add(bid)
    dec_rating_sum[dec] += r["avg_rating"] * r["n_reviews"]
    dec_rating_cnt[dec] += r["n_reviews"]
    dec_bookavg[dec].append(r["avg_rating"])

print("unmatched:", unmatched)
print("no year:", noyear)
rows = []
for dec in sorted(dec_books):
    nb = len(dec_books[dec])
    wavg = dec_rating_sum[dec] / dec_rating_cnt[dec]
    bavg = sum(dec_bookavg[dec]) / len(dec_bookavg[dec])
    rows.append((dec, nb, wavg, bavg, dec_rating_cnt[dec]))
    print(f"{dec}s: distinct_books={nb}, review_weighted_avg={wavg:.4f}, book_avg={bavg:.4f}, n_reviews={dec_rating_cnt[dec]}")

elig = [r for r in rows if r[1] >= 10]
best_w = max(elig, key=lambda r: r[2])
best_b = max(elig, key=lambda r: r[3])
print("\nEligible decades (>=10 books):", [(r[0], r[1]) for r in elig])
print("Best by review-weighted avg:", best_w)
print("Best by per-book avg:", best_b)

with open("final.txt", "w") as f:
    f.write(f"The {best_w[0]}s (decade starting {best_w[0]}) has the highest average rating "
            f"({best_w[2]:.4f} review-weighted, {best_w[3]:.4f} mean of per-book averages) "
            f"among decades with at least 10 distinct rated books ({best_w[1]} books).\n")
