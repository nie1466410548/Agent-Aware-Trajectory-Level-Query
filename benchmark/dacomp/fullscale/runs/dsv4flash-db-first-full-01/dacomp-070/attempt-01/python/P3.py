import json
# Check the first line of S14
with open('/results/S14.rows.jsonl') as f:
    line = f.readline()
    print(line)
    
# Check S15
with open('/results/S15.rows.jsonl') as f:
    line = f.readline()
    print(line[:200])
    
# Check S13
with open('/results/S13.rows.jsonl') as f:
    line = f.readline()
    print(line[:200])