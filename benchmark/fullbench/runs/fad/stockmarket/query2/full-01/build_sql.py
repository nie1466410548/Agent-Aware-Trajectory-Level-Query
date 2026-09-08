import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query2/full-01/results/1a4a93c2068240008557221ebeaef591.json") as f:
    tables = {r["table_name"] for r in json.load(f)}

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/stockmarket/query2/full-01/results/f4d81bf2f6c243c1af0def39562c9f6f.json") as f:
    etfs = [r["Symbol"] for r in json.load(f)]

avail = sorted(s for s in etfs if s in tables)
missing = [s for s in etfs if s not in tables]
print(f"ETFs on Arca: {len(etfs)}, with trade tables: {len(avail)}, missing: {len(missing)}")
print("Missing symbols:", missing[:50])

parts = []
for s in avail:
    parts.append(
        f"SELECT '{s}' AS Symbol, MAX(\"Adj Close\") AS MaxAdjClose "
        f"FROM \"{s}\" WHERE Date >= '2015-01-01' AND Date <= '2015-12-31'"
    )
sql = "\nUNION ALL\n".join(parts)
# split into 3 chunks for safety
chunks = [parts[i::3] for i in range(3)]
for i, ch in enumerate(chunks):
    q = "SELECT * FROM (\n" + "\nUNION ALL\n".join(ch) + "\n) WHERE MaxAdjClose > 200 ORDER BY MaxAdjClose DESC"
    with open(f"q3_{i}.sql", "w") as f:
        f.write(q)
    print(f"q3_{i}.sql: {len(ch)} tables, {len(q)} chars")
