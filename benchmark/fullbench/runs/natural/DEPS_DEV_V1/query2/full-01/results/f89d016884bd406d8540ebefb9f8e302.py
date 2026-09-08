import json

# Project info with forks
projects = json.load(open("projects.json"))
proj_forks = {}
for p in projects:
    if p["project"] and p["forks"] is not None:
        proj_forks[p["project"]] = p["forks"]
# manual fixes for the 2 unparsed rows
proj_forks["reactjs-ui/reactjs-pull-refresh"] = 5
proj_forks["sfundomhlungu/-dot.product-createlib"] = 0

# package-version -> project mapping
ppv = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/add329c0d8af4331841ebf4ed8df7442.json"))

# MIT + release package versions
pkg = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/35c29264c83a461e80850bd873f0b112.json"))
mit_release = {(r["Name"], r["Version"]) for r in pkg}
print("MIT+release pairs:", len(mit_release))

# join
hit_projects = {}
for r in ppv:
    if (r["Name"], r["Version"]) in mit_release:
        hit_projects.setdefault(r["ProjectName"], set()).add(r["Name"])

print("projects with >=1 MIT release package version:", len(hit_projects))

# check coverage: which extracted projects had no ppv rows at all
ppv_projects = {r["ProjectName"] for r in ppv}
missing = [p for p in proj_forks if p not in ppv_projects]
print("projects with no ppv match:", len(missing), missing[:20])

ranked = sorted(
    ((proj_forks.get(pr), pr, sorted(names)) for pr, names in hit_projects.items()),
    key=lambda x: (-(x[0] if x[0] is not None else -1), x[1]))
print("\nTop 15:")
for forks, pr, names in ranked[:15]:
    print(f"{forks}\t{pr}\t{names[:4]}")
