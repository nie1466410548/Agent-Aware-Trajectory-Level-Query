import json

projects = json.load(open("projects.json"))
proj_forks = {p["project"]: p["forks"] for p in projects if p["project"] and p["forks"] is not None}
proj_forks["reactjs-ui/reactjs-pull-refresh"] = 5
proj_forks["sfundomhlungu/-dot.product-createlib"] = 0

ppv = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/43ac636561c74708a6ee449f3bb299a2.json"))
pkg = json.load(open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/DEPS_DEV_V1/query2/full-01/results/35c29264c83a461e80850bd873f0b112.json"))
mit_release = {(r["Name"], r["Version"]) for r in pkg}

for label, filt in [("ALL relation types", lambda rt: True),
                    ("SOURCE_REPO_TYPE only", lambda rt: rt == "SOURCE_REPO_TYPE")]:
    hit = {}
    for r in ppv:
        if filt(r["RelationType"]) and (r["Name"], r["Version"]) in mit_release:
            hit.setdefault(r["ProjectName"], set()).add(r["Name"])
    ranked = sorted(((proj_forks.get(pr, -1), pr) for pr in hit), key=lambda x: (-x[0], x[1]))
    print("===", label, "===")
    for f, pr in ranked[:6]:
        print(f"{f}\t{pr}")
    print()
