import os
for p in ['results/S18.rows.jsonl', '/results/S18.rows.jsonl', './results/S18.rows.jsonl']:
    print(p, os.path.exists(p))
print(os.listdir('.'))
