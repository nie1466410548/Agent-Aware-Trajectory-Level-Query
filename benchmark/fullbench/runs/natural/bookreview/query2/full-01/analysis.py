import json, re

books = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query2/full-01/results/bf45e97a9a8a42a2b015542d56e394e6.json"))
perfect = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/bookreview/query2/full-01/results/08d3b2721dad44e48890dabf5ea16393.json"))

print("books:", len(books), "perfect ids:", len(perfect))

# check book_id / purchase_id formats
print("sample book_ids:", [b["book_id"] for b in books[:5]])
print("sample purchase_ids:", [p["purchase_id"] for p in perfect[:5]])

def num(s):
    m = re.search(r"(\d+)$", s or "")
    return m.group(1) if m else None

perfect_nums = {num(p["purchase_id"]): p for p in perfect}

# Inspect language mentions in details across all 40 books
langs = {}
for b in books:
    d = b.get("details") or ""
    m = re.findall(r"(?:in|language[:\s]+)\s*([A-Z][a-z]+)", d)
    langs[b["book_id"]] = (b["title"], m[:3], d[:120])
for k, v in langs.items():
    print(k, v)
