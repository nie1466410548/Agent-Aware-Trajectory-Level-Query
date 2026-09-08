import json, re

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/abd45cb172554ef8a2cce0f6b9cdf2d2.json") as f:
    rows = json.load(f)

name_pat = re.compile(r"([A-Za-z0-9_][A-Za-z0-9_.-]*/[A-Za-z0-9_][A-Za-z0-9_.-]*)")
fork_pats = [
    re.compile(r"([\d,]+)\s+forks?\b"),
    re.compile(r"forks? count of ([\d,]+)", re.I),
    re.compile(r"forked ([\d,]+) times", re.I),
]

out = []
bad = []
for r in rows:
    text = r["Project_Information"] or ""
    m = name_pat.search(text)
    proj = m.group(1) if m else None
    forks = None
    for p in fork_pats:
        fm = p.search(text)
        if fm:
            forks = int(fm.group(1).replace(",", ""))
            break
    if proj is None or forks is None:
        bad.append(text)
    out.append({"project": proj, "forks": forks,
                "licenses": r["Licenses"], "description": r["Description"],
                "homepage": r["Homepage"], "text": text})

with open("projects.json", "w") as f:
    json.dump(out, f, indent=1)

names = sorted({o["project"] for o in out if o["project"]})
with open("project_names.txt", "w") as f:
    f.write("\n".join(names))

print("rows:", len(rows), "parsed:", sum(1 for o in out if o['project'] and o['forks'] is not None))
print("unparsed:", len(bad))
for b in bad[:10]:
    print("BAD:", b)
