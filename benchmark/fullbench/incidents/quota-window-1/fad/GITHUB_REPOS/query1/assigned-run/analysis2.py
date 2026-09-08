import json, re

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/e54f8c01a60c4fae941c6d726ddd2e99.json") as f:
    langs = json.load(f)
with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/238f263bf4b54426aabb6aadba7192bf.json") as f:
    readmes = json.load(f)

lang_map = {r["repo_name"]: (r["language_description"] or "") for r in langs}
readme_map = {}
for r in readmes:
    readme_map.setdefault(r["sample_repo_name"], []).append(r["content"] or "")

strict = re.compile(r"copyright|\u00a9", re.IGNORECASE)
broad = re.compile(r"copyright|\u00a9|\(c\)", re.IGNORECASE)

# find (c)-only matches among non-python repos
for rn, contents in readme_map.items():
    if rn in lang_map and not re.search(r"python", lang_map[rn], re.I):
        joined = "\n".join(contents)
        if broad.search(joined) and not strict.search(joined):
            m = re.search(r".{60}\(c\).{60}", joined, re.I | re.S)
            print("(c)-only match in", rn, "->", repr(m.group(0)) if m else "?")

# Scenario: include unknown repos as non-python
unknown = [rn for rn in readme_map if rn not in lang_map]
u_copy = sum(1 for rn in unknown if strict.search("\n".join(readme_map[rn])))
print("\nUnknown repos:", len(unknown), "with copyright(strict):", u_copy)
for rn in unknown:
    print("  ", rn, "copyright:", bool(strict.search("\n".join(readme_map[rn]))))

non_py = [rn for rn in readme_map if rn in lang_map and not re.search(r"python", lang_map[rn], re.I)]
n_strict = sum(1 for rn in non_py if strict.search("\n".join(readme_map[rn])))
print("\nMAIN: non-python README repos =", len(non_py), "; with copyright (strict) =", n_strict,
      "; proportion = %.4f" % (n_strict/len(non_py)))
print("ALT (incl. unknown as non-python): %d/%d = %.4f" % (n_strict+u_copy, len(non_py)+len(unknown), (n_strict+u_copy)/(len(non_py)+len(unknown))))
