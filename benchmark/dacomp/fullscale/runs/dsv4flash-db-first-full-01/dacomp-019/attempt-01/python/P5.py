import os
# Try absolute path of workspace
ws = '/data/nly/Agent-Aware-Trajectory-Level-Query'
for root, dirs, files in os.walk(ws):
    depth = root[len(ws):].count(os.sep)
    if depth <= 2:
        print(root, '->', files[:5])
