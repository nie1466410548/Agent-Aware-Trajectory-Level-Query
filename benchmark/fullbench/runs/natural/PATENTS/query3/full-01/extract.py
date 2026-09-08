import json, re

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query3/full-01/results/1700b306e7af41749e1d08b25a42372f.json") as f:
    rows = json.load(f)

pubs = set()
for r in rows:
    info = r["Patents_info"]
    # publication number is the last US-XXXX-XX style identifier in the text
    m = re.findall(r"\b([A-Z]{2}-[A-Z0-9]+-[A-Z0-9]+)\b", info)
    if m:
        pubs.add(m[-1])

pubs = sorted(pubs)
print(len(pubs))
print(pubs)

# Build SQL: find citing publications (citation LIKE any of these numbers)
# Match the raw number string
conds = " OR ".join("citation LIKE '%%" + p + "%%'" for p in pubs)
sql = "SELECT Patents_info, cpc, citation FROM publicationinfo WHERE " + conds
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query3/full-01/citing.sql", "w") as f:
    f.write(sql)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/PATENTS/query3/full-01/uc_pubs.json", "w") as f:
    json.dump(pubs, f)
print("SQL written, length:", len(sql))
