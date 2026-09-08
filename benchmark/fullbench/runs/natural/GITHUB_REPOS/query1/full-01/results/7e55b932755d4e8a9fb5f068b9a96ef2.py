import json, re

base = '/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/GITHUB_REPOS/query1/full-01/results/'
readmes = json.load(open(base + '665c02b536b54d818800744da2ca9027.json'))
langs = {r['repo_name']: r['language_description'] for r in json.load(open(base + 'b3b6fe03509a47feb7a832ec13779f44.json'))}

def has_copyright(text):
    if not text:
        return False
    t = text.lower()
    return ('copyright' in t) or ('©' in text)

rows = []
for r in readmes:
    repo = r['sample_repo_name']
    desc = langs.get(repo)
    if desc is None:
        cls = 'unknown'
    elif 'python' in desc.lower():
        cls = 'python'
    elif desc.startswith('No language information'):
        cls = 'nolang'
    else:
        cls = 'nonpython'
    rows.append((repo, r['sample_path'], cls, has_copyright(r.get('content'))))

from collections import Counter
print("classification:", Counter(x[2] for x in rows))

# Main: non-Python = declared languages without Python + no-language repos
np_rows = [x for x in rows if x[2] in ('nonpython', 'nolang')]
tot = len(np_rows)
withc = sum(1 for x in np_rows if x[3])
print(f"non-Python (incl. no-lang) README.md files: {tot}, with copyright: {withc}, proportion: {withc/tot:.4f}")

# Strict: only repos with declared languages excluding Python
sp = [x for x in rows if x[2] == 'nonpython']
tot2 = len(sp); w2 = sum(1 for x in sp if x[3])
print(f"strict declared non-Python: {tot2}, with copyright: {w2}, proportion: {w2/tot2:.4f}")

# unique repos perspective (one per repo)
seen = {}
for repo, path, cls, c in np_rows:
    seen.setdefault(repo, []).append(c)
repos_any = sum(1 for v in seen.values() if any(v))
print(f"repo-level: {len(seen)} repos, {repos_any} with >=1 README containing copyright, proportion: {repos_any/len(seen):.4f}")

# show some examples of copyright matches
for repo, path, cls, c in np_rows:
    if c:
        pass
print("sample matches:", [x[0] for x in np_rows if x[3]][:15])
