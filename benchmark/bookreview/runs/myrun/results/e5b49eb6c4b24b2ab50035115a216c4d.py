import json, glob, os
files = sorted(glob.glob('results/*.json'), key=os.path.getmtime)
target = None
for f in files:
    try:
        rows = json.load(open(f))
    except Exception:
        continue
    if isinstance(rows, list) and len(rows) == 194 and isinstance(rows[0], dict) and 'title' in rows[0] and 'faq_answer__c' not in rows[0]:
        target = rows
for i, r in enumerate(target):
    if i >= 130:
        print(r['id'], '|', r['title'])
