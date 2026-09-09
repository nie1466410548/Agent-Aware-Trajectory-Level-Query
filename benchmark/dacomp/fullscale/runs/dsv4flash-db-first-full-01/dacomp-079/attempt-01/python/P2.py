import json
with open('/results/S34.rows.jsonl') as f:
    line = f.readline()
    row = json.loads(line)
    print(list(row.keys()))