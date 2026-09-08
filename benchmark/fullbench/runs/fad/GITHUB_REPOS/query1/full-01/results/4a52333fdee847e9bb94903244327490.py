import json

with open("readme_flags.json") as f:
    readme = json.load(f)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/cd03e21956cd4457af46c89ce18fe156.json") as f:
    langs = json.load(f)

lang_map = {r["repo_name"]: r["uses_python"] for r in langs}

readme_repos = {r["sample_repo_name"] for r in readme}
matched = readme_repos & set(lang_map)
unmatched = readme_repos - set(lang_map)
print("README repos:", len(readme_repos), "matched:", len(matched), "unmatched:", len(unmatched))

# Copyright info = word 'copyright' (case-insensitive) or © symbol
def has_copy(r):
    return bool(r["has_copyright_word"]) or bool(r["has_symbol"])

# File-level analysis over non-Python repos (matched only)
np_rows = [r for r in readme if lang_map.get(r["sample_repo_name"]) == 0]
n = len(np_rows)
with_c = sum(1 for r in np_rows if has_copy(r))
print(f"Non-Python README.md files (matched repos): {n}, with copyright: {with_c}, proportion: {with_c/n:.4f}")

# Repo-level: proportion of non-Python repos whose (any) README.md includes copyright
from collections import defaultdict
repo_files = defaultdict(list)
for r in np_rows:
    repo_files[r["sample_repo_name"]].append(r)
repo_any = sum(1 for fs in repo_files.values() if any(has_copy(r) for r in fs))
print(f"Non-Python repos with README.md: {len(repo_files)}, repos with copyright in any README.md: {repo_any}, proportion: {repo_any/len(repo_files):.4f}")

# Including unmatched repos as non-Python (they have no Python evidence in metadata)
np_rows2 = [r for r in readme if lang_map.get(r["sample_repo_name"], 0) == 0]
n2 = len(np_rows2)
with_c2 = sum(1 for r in np_rows2 if has_copy(r))
print(f"Incl. unmatched as non-Python: files={n2}, copyright={with_c2}, proportion: {with_c2/n2:.4f}")

# Show which non-Python files had copyright
for r in np_rows:
    if has_copy(r):
        print("COPY:", r["sample_repo_name"], "word:", r["has_copyright_word"], "symbol:", r["has_symbol"])
