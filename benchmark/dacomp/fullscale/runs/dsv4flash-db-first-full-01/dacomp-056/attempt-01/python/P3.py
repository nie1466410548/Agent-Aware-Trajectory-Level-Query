import os
print("cwd:", os.getcwd())
print("files in cwd:", os.listdir('.'))
print("files in /results/:", os.listdir('/results/') if os.path.isdir('/results/') else 'no /results dir')
# Check if results exists somewhere
for root, dirs, files in os.walk('/'):
    if 'results' in root and 'rows.jsonl' in str(files):
        print(root, files[:5])