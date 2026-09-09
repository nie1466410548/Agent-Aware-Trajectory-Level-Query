import json

with open('/results/S38.rows.jsonl') as f:
    first_line = json.loads(f.readline())
    print(type(first_line))
    print(first_line[:10])