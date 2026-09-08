import json
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/music_brainz_20k/query1/full-01/results/a7181c7f33c14c308e4c7e0e549d52b6.json") as f:
    rows = json.load(f)
total = sum(r["revenue_usd"] for r in rows)
units = sum(r["units_sold"] for r in rows)
print(f"rows={len(rows)} total_revenue_usd={total:.2f} total_units={units}")
for r in rows:
    print(r)
