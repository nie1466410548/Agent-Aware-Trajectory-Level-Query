import json
rows = []
with open('/results/S28.rows.jsonl') as f:
    for i, line in enumerate(f):
        rows.append(json.loads(line))
        if i>2: break
print(type(rows[0]), rows[0][:2] if isinstance(rows[0], list) else rows[0])
