import os
# List files in results directory
print(os.listdir('/data/nly/Agent-Aware-Trajectory-Level-Query/results/'))
# Check if there's a different path
for root, dirs, files in os.walk('/data/nly/Agent-Aware-Trajectory-Level-Query/results/'):
    for f in files:
        print(os.path.join(root, f))