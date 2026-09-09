import pandas as pd, json, re
with open('/results/S18.rows.jsonl') as f:
    row = json.loads(f.readline())
print(list(row.keys()))