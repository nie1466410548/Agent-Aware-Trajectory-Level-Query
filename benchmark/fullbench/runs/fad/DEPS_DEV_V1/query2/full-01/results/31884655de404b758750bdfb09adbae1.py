import json, re

base = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/DEPS_DEV_V1/query2/full-01/results/"

pkgs = json.load(open(base + "1e52603435ca46f8acd7a4f02e61b4c7.json"))
mapping = json.load(open(base + "af508072ee33442191a89c54e0a8b424.json"))
pinfo = json.load(open(base + "1f6029e33ba144eca49e5cb3265045e7.json"))

mit_names = set(r["Name"] for r in pkgs)
print("MIT released NPM packages:", len(mit_names))

# package name -> set of GitHub project names
pkg2proj = {}
for r in mapping:
    if r["ProjectType"] == "GITHUB":
        pkg2proj.setdefault(r["Name"], set()).add(r["ProjectName"])

# Parse project_info text
def parse_name(text):
    m = re.search(r"under the name ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    m = re.search(r"named ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    m = re.search(r"project ([\w.\-]+/[\w.\-]+)", text)
    if m: return m.group(1)
    return None

def parse_forks(text):
    patterns = [
        r"([\d,]+)\s+forks\b",
        r"forks count of ([\d,]+)",
        r"forked ([\d,]+) times",
        r"has ([\d,]+) fork\b",
        r"and ([\d,]+) fork\b",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return int(m.group(1).replace(",", ""))
    return None

proj_forks = {}
unparsed = []
for r in pinfo:
    t = r["Project_Information"]
    name = parse_name(t)
    forks = parse_forks(t)
    if name is None or forks is None:
        unparsed.append(t)
        continue
    proj_forks[name] = max(forks, proj_forks.get(name, -1))

print("Parsed projects:", len(proj_forks), "Unparsed:", len(unparsed))
for t in unparsed[:5]:
    print("UNPARSED:", t)

# Candidate projects from MIT released packages
cand = {}
for pkg in mit_names:
    for proj in pkg2proj.get(pkg, ()):
        if proj in proj_forks:
            cand.setdefault(proj, set()).add(pkg)

print("Candidate projects with fork data:", len(cand))
ranked = sorted(cand.items(), key=lambda kv: -proj_forks[kv[0]])
for proj, pk in ranked[:10]:
    print(proj, proj_forks[proj], sorted(pk))
