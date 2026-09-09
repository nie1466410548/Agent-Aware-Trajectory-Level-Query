import json

with open('/results/S38.rows.jsonl') as f:
    first_line = json.loads(f.readline())
    print(list(first_line.keys()))
    print(first_line)