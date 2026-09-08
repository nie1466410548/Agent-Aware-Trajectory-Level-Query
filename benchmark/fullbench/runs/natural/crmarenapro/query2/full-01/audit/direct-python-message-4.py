import json
data = json.load(open('results/ef7835fce0104bb1a263cd6ce2dfd26c.json'))
for d in data:
    print(d['id'], '|', d['title'])
