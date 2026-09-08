import json

base = '/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/GITHUB_REPOS/query1/full-01/results/'
readmes = json.load(open(base + '665c02b536b54d818800744da2ca9027.json'))
langs = {r['repo_name']: r['language_description'] for r in json.load(open(base + 'b3b6fe03509a47feb7a832ec13779f44.json'))}

extra = 0
trunc = 0
for r in readmes:
    repo = r['sample_repo_name']
    desc = langs.get(repo)
    nonpy = desc is not None and 'python' not in desc.lower()
    if not nonpy:
        continue
    c = r.get('content') or ''
    if 'copyright' not in c.lower() and ('©' in c or '(c)' in c.lower()):
        extra += 1
        print("extra-copyright-only:", repo, r['sample_path'])
print("files with ©/(c) but no 'copyright' word:", extra)
