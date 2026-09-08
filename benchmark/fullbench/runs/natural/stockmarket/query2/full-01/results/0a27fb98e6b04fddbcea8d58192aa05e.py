import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query2/full-01/results/2139e60ca48748c3ae0e31b0e8df1aa0.json") as f:
    syms = [r["Symbol"] for r in json.load(f)]

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query2/full-01/results/798be6d7a74f4b97bebc2f517b242357.json") as f:
    tables = {r["table_name"] for r in json.load(f)}

have = sorted([s for s in syms if s in tables])
missing = sorted([s for s in syms if s not in tables])
print("Arca ETFs:", len(syms), "with trade tables:", len(have), "missing:", len(missing))
print("missing sample:", missing[:20])

parts = []
for s in have:
    parts.append(
        f"SELECT '{s}' AS Symbol, MAX(\"Adj Close\") AS max_adj FROM \"{s}\" "
        f"WHERE \"Date\" >= '2015-01-01' AND \"Date\" <= '2015-12-31'"
    )
sql = ("SELECT Symbol, max_adj FROM (\n" + "\nUNION ALL\n".join(parts) +
       "\n) t WHERE max_adj > 200 ORDER BY Symbol")
with open("big_query.sql", "w") as f:
    f.write(sql)
print("SQL length:", len(sql))
