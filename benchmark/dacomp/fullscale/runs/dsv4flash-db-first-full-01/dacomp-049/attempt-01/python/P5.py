import pandas as pd, json
with open('/results/S18.rows.jsonl') as f:
    line = f.readline()
    print(type(line), line[:300])