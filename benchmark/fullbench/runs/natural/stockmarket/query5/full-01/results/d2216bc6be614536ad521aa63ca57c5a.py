import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query5/full-01/results/d373a3cc68d04ace801c4c5d16cfa2ae.json") as f:
    info = json.load(f)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query5/full-01/results/0139db13b1f645e58ffdd1da1a70f534.json") as f:
    tables = json.load(f)

table_names = {t["table_name"] for t in tables}
syms = [r["Symbol"] for r in info]
present = [s for s in syms if s in table_names]
missing = [s for s in syms if s not in table_names]
print("total S-category:", len(syms), "present:", len(present), "missing:", missing)

parts = []
for s in present:
    parts.append(
        f"SELECT '{s}' AS symbol, COUNT(*) AS days FROM \"{s}\" "
        f"WHERE \"Date\" >= '2019-01-01' AND \"Date\" <= '2019-12-31' "
        f"AND (\"High\" - \"Low\") / \"Low\" > 0.20"
    )
sql = "\nUNION ALL\n".join(parts) + "\nORDER BY days DESC, symbol;\n"
with open("q3.sql", "w") as f:
    f.write(sql)
print("q3.sql written, bytes:", len(sql))
