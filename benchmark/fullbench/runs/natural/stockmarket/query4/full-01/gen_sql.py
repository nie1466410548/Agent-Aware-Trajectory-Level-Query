import json
with open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/stockmarket/query4/full-01/results/a4e65db3630f47f3bd96492d4fd7a6c0.json') as f:
    rows = json.load(f)
print(len(rows))
parts = []
for r in rows:
    s = r['Symbol']
    parts.append(f"""SELECT '{s}' AS Symbol, SUM(CASE WHEN Close > Open THEN 1 ELSE 0 END) AS up_days, SUM(CASE WHEN Close < Open THEN 1 ELSE 0 END) AS down_days, COUNT(*) AS total FROM "{s}" WHERE "Date" >= '2017-01-01' AND "Date" <= '2017-12-31'""")
sql = "\nUNION ALL\n".join(parts)
with open('q3.sql','w') as f:
    f.write(sql)
print(sql[:300])
