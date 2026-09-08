import json

with open("/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query1/full-01/results/b2446bcc6ce844e5be42bc6775373eed.json") as f:
    rows = json.load(f)

repos = sorted({r["sample_repo_name"] for r in rows})
print("distinct repos:", len(repos))

# Save flags for later analysis
with open("readme_flags.json", "w") as f:
    json.dump(rows, f)

in_list = ", ".join("'" + r.replace("'", "''") + "'" for r in repos)
sql = ("SELECT repo_name, CASE WHEN language_description LIKE '%Python%' THEN 1 ELSE 0 END AS uses_python "
       "FROM languages WHERE repo_name IN (" + in_list + ")")
with open("repo_lang.sql", "w") as f:
    f.write(sql)
print("sql written, length:", len(sql))
