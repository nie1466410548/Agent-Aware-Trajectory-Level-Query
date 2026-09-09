import json
with open('/results/S10.rows.jsonl', 'r') as f:
    lines = [f.readline() for _ in range(3)]
for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line[:200])}")