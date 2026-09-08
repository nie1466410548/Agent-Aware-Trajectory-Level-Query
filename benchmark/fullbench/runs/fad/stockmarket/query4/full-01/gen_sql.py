import json

res_dir = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query4/full-01/results/"

with open(res_dir + "6e9e4ba4a4aa4132824e267e2d1a0f75.json") as f:
    stockinfo = json.load(f)
with open(res_dir + "9f5fd49120f64e0ba4c59db49cb73d2f.json") as f:
    tables = json.load(f)

table_names = {t["table_name"] for t in tables}
symbols = [r["Symbol"] for r in stockinfo if r["Symbol"] in table_names]
missing = [r["Symbol"] for r in stockinfo if r["Symbol"] not in table_names]
print("symbols with tables:", len(symbols))
print("missing tables:", missing)

parts = []
for s in symbols:
    safe = s.replace('"', '""')
    parts.append(
        f"SELECT '{s}' AS Symbol, "
        f"SUM(CASE WHEN \"Close\" > \"Open\" THEN 1 ELSE 0 END) AS up_days, "
        f"SUM(CASE WHEN \"Close\" < \"Open\" THEN 1 ELSE 0 END) AS down_days, "
        f"COUNT(*) AS total_days "
        f"FROM \"{safe}\" WHERE \"Date\" >= '2017-01-01' AND \"Date\" <= '2017-12-31'"
    )

sql = "\nUNION ALL\n".join(parts) + ";\n"
with open("q4.sql", "w") as f:
    f.write(sql)
print("SQL written, length:", len(sql))
