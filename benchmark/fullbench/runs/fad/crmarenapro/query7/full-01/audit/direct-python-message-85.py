
import json
data = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/fad/crmarenapro/query7/full-01/results/78ce2e6f368c4a619b28957a6b05d9f9.json'))
for r in data:
    print('ID:', r['id'])
    print('TITLE:', r['title'])
    print('---')

