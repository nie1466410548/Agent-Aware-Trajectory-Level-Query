
# Inspect raw format
with open('/results/S44.rows.jsonl') as f:
    line = f.readline()
print(repr(line[:300]))
