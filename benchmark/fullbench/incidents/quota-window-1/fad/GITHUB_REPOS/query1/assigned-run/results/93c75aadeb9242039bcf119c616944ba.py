import json, re

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/e54f8c01a60c4fae941c6d726ddd2e99.json") as f:
    langs = json.load(f)

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/238f263bf4b54426aabb6aadba7192bf.json") as f:
    readmes = json.load(f)

print("languages rows:", len(langs))
print("readme rows:", len(readmes))

# Build language map (one entry per repo; combine if duplicates)
lang_map = {}
dup = 0
for r in langs:
    rn = r["repo_name"]
    if rn in lang_map:
        dup += 1
        lang_map[rn] = lang_map[rn] + " | " + (r["language_description"] or "")
    else:
        lang_map[rn] = r["language_description"] or ""
print("unique repos in languages:", len(lang_map), "duplicate rows:", dup)

# Python detection: case-insensitive 'python' token in description
def uses_python(desc):
    return re.search(r"python", desc, re.IGNORECASE) is not None

# README repos
readme_repos = {}
for r in readmes:
    readme_repos.setdefault(r["sample_repo_name"], []).append(r["content"] or "")
print("unique repos with README.md:", len(readme_repos))

missing = [rn for rn in readme_repos if rn not in lang_map]
print("README repos missing from languages table:", len(missing), missing[:10])

# Copyright detection
copy_pat = re.compile(r"copyright|\u00a9|\(c\)", re.IGNORECASE)

non_py = []
py = []
unknown = []
for rn, contents in readme_repos.items():
    content = "\n".join(contents)
    has_copy = bool(copy_pat.search(content))
    if rn not in lang_map:
        unknown.append((rn, has_copy))
    elif uses_python(lang_map[rn]):
        py.append((rn, has_copy))
    else:
        non_py.append((rn, has_copy))

print("\n=== README repos classified ===")
print("Python repos:", len(py))
print("Non-Python repos:", len(non_py))
print("Unknown (not in languages):", len(unknown))

n_copy = sum(1 for _, c in non_py if c)
print("\nNon-Python repos with README.md:", len(non_py))
print("...of which README includes copyright info:", n_copy)
if len(non_py):
    print("Proportion: %.4f (%.2f%%)" % (n_copy/len(non_py), 100*n_copy/len(non_py)))

# also strict 'copyright' word only (no (c) symbol) for comparison
strict = re.compile(r"copyright|\u00a9", re.IGNORECASE)
n_strict = sum(1 for rn, contents in [(rn, None) for rn, _ in non_py] for c in readme_repos[rn] if strict.search(c))
n_strict = sum(1 for rn, _ in non_py if any(strict.search(c) for c in readme_repos[rn]))
print("Strict (copyright word or (c) sign only):", n_strict, "= %.4f" % (n_strict/len(non_py) if non_py else 0))

print("\nNon-Python repos WITH copyright:")
for rn, c in non_py:
    if c: print("  ", rn)
