import json
with open('/results/S34.rows.jsonl') as f:
    lines = f.readlines()
print("num lines:", len(lines))
print("first line type:", type(json.loads(lines[0])))
first = json.loads(lines[0])
print("first line:", first[:5])
second = json.loads(lines[1])
print("second line first 5:", second[:5])
# If first line is a list of column names
if isinstance(first, list) and all(isinstance(x, str) for x in first):
    print("First line is headers")
    print(first)
