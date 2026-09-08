import json, re

path = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/PATENTS/query3/full-01/results/4fc69af1481e4f55b5201caede99dd3e.json"
rows = json.load(open(path))
print("rows:", len(rows))

pubs = set()
pat = re.compile(r'\b([A-Z]{2}-[A-Z0-9]+-[A-Z0-9]+)\s*\.\s*$')
for r in rows:
    info = r["Patents_info"]
    m = pat.search(info)
    if m:
        pubs.add(m.group(1))
    else:
        print("NO MATCH:", info)

pubs = sorted(pubs)
print("distinct publication numbers:", len(pubs))
# save
json.dump(pubs, open("uc_pubnums.json", "w"), indent=1)

# build SQL with LIKE conditions
conds = "\n   OR ".join("citation LIKE '%{}%'".format(p) for p in pubs)
sql = "SELECT Patents_info, cpc, citation FROM publicationinfo\nWHERE " + conds + "\n"
open("citing2.sql", "w").write(sql)
print("sql written, bytes:", len(sql))
