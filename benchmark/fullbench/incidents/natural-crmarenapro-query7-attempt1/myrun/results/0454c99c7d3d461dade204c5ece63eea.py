import json, glob, os
files = sorted(glob.glob('results/*.json'), key=os.path.getmtime)
rows = json.load(open(files[-1]))
titles = [(r['id'], r['title']) for r in rows]
for i,(i_,t) in enumerate(titles):
    if i >= 130:
        print(i_, '|', t)
