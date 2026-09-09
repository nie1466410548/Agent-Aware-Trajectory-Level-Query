import json, pandas as pd, numpy as np

with open('/results/S15.rows.jsonl') as f:
    raw = f.read()

print("First 100 chars:", raw[:100])
# Try JSON array
data = json.loads(raw)
print("Type:", type(data), "Len:", len(data))
print("First element:", data[0])
