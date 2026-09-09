import os
print("CWD:", os.getcwd())
for root, dirs, files in os.walk('/'):
    if 'results' in dirs and 'S28.rows.jsonl' in os.listdir(os.path.join(root,'results')):
        print("Found:", root)
        break
# Also list work dir
print(os.listdir('.'))