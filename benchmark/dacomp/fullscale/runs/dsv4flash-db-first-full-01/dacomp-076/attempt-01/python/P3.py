import os
print("CWD:", os.getcwd())
for base in ['.', '/results', '/data/nly/Agent-Aware-Trajectory-Level-Query/results', 'results']:
    try:
        print(base, os.listdir(base)[:20])
    except Exception as e:
        print(base, 'ERR', e)
