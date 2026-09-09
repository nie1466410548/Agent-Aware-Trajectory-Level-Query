import json
import pandas as pd

# Read the full JSONL file
with open('results/S29.rows.jsonl', 'r') as f:
    raw = f.read()

# Parse the JSON array
data = json.loads(raw)
print(f"Type: {type(data)}, Length: {len(data) if isinstance(data, list) else 'dict'}")
if isinstance(data, list):
    print(f"First item type: {type(data[0])}")
    if isinstance(data[0], list):
        print(f"First item: {data[0]}")
        print(f"Length of first item: {len(data[0])}")