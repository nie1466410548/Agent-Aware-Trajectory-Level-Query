import json

base = '/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/GITHUB_REPOS/query1/full-01/results/'
readmes = json.load(open(base + '665c02b536b54d818800744da2ca9027.json'))
langs = {r['repo_name']: r['language_description'] for r in json.load(open(base + 'b3b6fe03509a47feb7a832ec13779f44.json'))}

npy = [r for r in readmes if langs.get(r['sample_repo_name']) is not None
       and 'python' not in langs[r['sample_repo_name']].lower()]

variants = {'word only': 0, 'word or ©': 0, 'word or © or (c)': 0}
for r in npy:
    c = r.get('content') or ''
    low = c.lower()
    w = 'copyright' in low
    s = '©' in c
    p = '(c)' in low
    variants['word only'] += w
    variants['word or ©'] += (w or s)
    variants['word or © or (c)'] += (w or s or p)

tot = len(npy)
print("total non-Python README.md files:", tot)
for k, v in variants.items():
    print(f"{k}: {v}/{tot} = {v/tot:.4f}")
