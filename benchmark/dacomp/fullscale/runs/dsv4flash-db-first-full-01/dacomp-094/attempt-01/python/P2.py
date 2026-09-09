with open('/results/S20.rows.jsonl') as f:
    lines = f.readlines()
print("Number of lines:", len(lines))
for i, line in enumerate(lines[:2]):
    print(f"Line {i}: {line[:500]}")
    print("---")