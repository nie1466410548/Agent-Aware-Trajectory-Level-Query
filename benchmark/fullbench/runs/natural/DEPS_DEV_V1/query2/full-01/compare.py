import json

projects = json.load(open("projects.json"))
proj_forks, proj_mit = {}, {}
for p in projects:
    if p["project"] and p["forks"] is not None:
        proj_forks[p["project"]] = p["forks"]
        try:
            lic = json.loads(p["licenses"] or "[]")
        except Exception:
            lic = []
        proj_mit[p["project"]] = ("MIT" in lic)
proj_forks["reactjs-ui/reactjs-pull-refresh"] = 5
proj_forks["sfundomhlungu/-dot.product-createlib"] = 0
proj_mit.setdefault("reactjs-ui/reactjs-pull-refresh", False)
proj_mit.setdefault("sfundomhlungu/-dot.product-createlib", False)

ppv = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/add329c0d8af4331841ebf4ed8df7442.json"))
pkg = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/35c29264c83a461e80850bd873f0b112.json"))
mit_release = {(r["Name"], r["Version"]) for r in pkg}

hit = {}
for r in ppv:
    if (r["Name"], r["Version"]) in mit_release:
        hit.setdefault(r["ProjectName"], set()).add(r["Name"])

def rank(filter_project_mit):
    items = [(proj_forks.get(pr, -1), pr, sorted(ns))
             for pr, ns in hit.items()
             if (proj_mit.get(pr, False) or not filter_project_mit)]
    items.sort(key=lambda x: (-x[0], x[1]))
    return items

print("=== Interpretation A: package-level MIT license (packageinfo.Licenses) ===")
for f, pr, ns in rank(False)[:8]:
    print(f"{f}\t{pr}\t projectMIT={proj_mit.get(pr)}\t{ns[:3]}")

print("\n=== Interpretation B: additionally require project_info.Licenses contains MIT ===")
for f, pr, ns in rank(True)[:8]:
    print(f"{f}\t{pr}\t{ns[:3]}")
