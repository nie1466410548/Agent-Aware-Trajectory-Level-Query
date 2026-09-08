import json

repos_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query3/full-01/results/00a32c7f78df4ae380fd00d0877c08a1.json"
counts_file = "/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/GITHUB_REPOS/query3/full-01/results/7962422603fd46b7a2df9d7607e8fe38.json"

with open(repos_file) as f:
    repos = {r["repo_name"] for r in json.load(f)}
with open(counts_file) as f:
    counts = json.load(f)

print("Shell+Apache-2.0 repo count:", len(repos))
total = 0
for row in counts:
    match = row["repo_name"] in repos
    print(row["repo_name"], row["n"], "MATCH" if match else "no")
    if match:
        total += row["n"]
print("TOTAL matching commit messages:", total)
