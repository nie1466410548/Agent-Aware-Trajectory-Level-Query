import os
print(os.getcwd())
print(os.listdir('.'))
for p in ['/results/S46.rows.jsonl', 'results/S46.rows.jsonl', '/data/nly/Agent-Aware-Trajectory-Level-Query/results/S46.rows.jsonl']:
    print(p, os.path.exists(p))