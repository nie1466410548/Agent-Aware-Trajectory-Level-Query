import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query5/full-01/results/877057d055ae48c3850feb36f95b3a02.json") as f:
    rows = json.load(f)

symbols = [r["Symbol"] for r in rows]
print("n symbols:", len(symbols))

parts = []
for s in symbols:
    tbl = '"' + s.replace('"', '""') + '"'
    parts.append(
        f"SELECT '{s}' AS symbol, COUNT(*) AS days FROM {tbl} "
        f"WHERE \"Date\" >= '2019-01-01' AND \"Date\" <= '2019-12-31' "
        f"AND \"Low\" > 0 AND (\"High\" - \"Low\") / \"Low\" > 0.20"
    )

sql = "SELECT symbol, days FROM (\n" + "\nUNION ALL\n".join(parts) + "\n) t ORDER BY days DESC, symbol ASC;"
with open("q3.sql", "w") as f:
    f.write(sql)
print("q3.sql written, length:", len(sql))
