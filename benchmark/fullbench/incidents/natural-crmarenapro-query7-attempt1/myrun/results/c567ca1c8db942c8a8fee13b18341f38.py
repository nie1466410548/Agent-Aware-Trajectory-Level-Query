import json, glob, os
# find the most recent result file (q21 output)
files = sorted(glob.glob('results/*.json'), key=os.path.getmtime)
rows = json.load(open(files[-1]))
for r in rows:
    print(r['id'], '|', r['title'])
