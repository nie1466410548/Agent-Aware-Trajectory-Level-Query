import json
with open('/results/S11.rows.jsonl', 'r') as f:
    first = f.readline().strip()
print(first)
with open('/results/S11.rows.jsonl', 'r') as f:
    lines = [json.loads(l) for l in f]
print(type(lines[0]), len(lines[0]) if isinstance(lines[0], list) else lines[0])