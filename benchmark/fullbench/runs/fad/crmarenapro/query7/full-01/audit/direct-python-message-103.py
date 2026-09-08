
import json
data = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query7/full-01/results/08416f89d367473baa1d7dafb8becf87.json'))
for r in data:
    print(r['id'], '|', r['title'])

