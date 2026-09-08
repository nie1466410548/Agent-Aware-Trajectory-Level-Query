import json, re

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/bookreview/query2/full-01/results/"
books = json.load(open(base + "38e30bb3230740d381cf2de5dea8b7dc.json"))
perfect = json.load(open(base + "e417efefc15645cba444b7de1e46d7a1.json"))

print("Lit&Fiction books:", len(books))

# Inspect language phrasing in details
for b in books:
    d = b["details"] or ""
    # find sentences mentioning English
    sents = re.findall(r'[^.]*[Ee]nglish[^.]*\.', d)
    print(b["book_id"], "|", b["title"][:40], "|", " || ".join(sents)[:200])
