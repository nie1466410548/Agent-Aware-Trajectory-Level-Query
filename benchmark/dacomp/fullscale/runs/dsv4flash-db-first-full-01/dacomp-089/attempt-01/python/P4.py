import json
with open('/results/S40.rows.jsonl', 'r') as f:
    lines = f.readlines()
print(f"Number of lines: {len(lines)}")
print(f"First line: {lines[0][:200]}")
# Check if the file is a JSON array or JSONL
obj = json.loads(lines[0])
print(f"Type of first parsed element: {type(obj)}")
if isinstance(obj, list):
    print(f"First element of first line: {obj[:5]}")
    print(f"Length of first element: {len(obj)}")
elif isinstance(obj, dict):
    print(f"First dict keys: {list(obj.keys())[:5]}")
