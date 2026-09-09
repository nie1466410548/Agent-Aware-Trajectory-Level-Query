import os
# Check current working directory
print(f"CWD: {os.getcwd()}")
print(f"Contents of /results: {os.listdir('/results')[:20] if os.path.isdir('/results') else 'NOT FOUND'}")
print(f"Contents of ./results: {os.listdir('./results')[:20] if os.path.isdir('./results') else 'NOT FOUND'}")
print(f"Contents of /data/nly/Agent-Aware-Trajectory-Level-Query/results: {os.listdir('/data/nly/Agent-Aware-Trajectory-Level-Query/results')[:20] if os.path.isdir('/data/nly/Agent-Aware-Trajectory-Level-Query/results') else 'NOT FOUND'}")