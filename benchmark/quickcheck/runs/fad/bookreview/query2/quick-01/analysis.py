import json, re

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query2/quick-01/results/3db8f21064e5448498619d830c97284a.json"))
revs = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/runs/fad/bookreview/query2/quick-01/results/b9ab27ce9b0a4e53a6655266b9469d84.json"))

def num(x):
    m = re.search(r'(\d+)$', x)
    return m.group(1) if m else None

book_by_num = {num(b["book_id"]): b for b in books}
print("candidate books:", len(book_by_num))

matches = []
for r in revs:
    n = num(r["purchase_id"])
    if n in book_by_num:
        b = book_by_num[n]
        # extract author name if possible
        auth = b.get("author") or ""
        m = re.search(r'"name":\s*"([^"]+)"', auth)
        aname = m.group(1) if m else (auth or "Unknown")
        matches.append((b["book_id"], b["title"], aname, r["avg_rating"], r["n_reviews"]))

matches.sort(key=lambda x: int(num(x[0])))
for m in matches:
    print(m)
print("total matches:", len(matches))
