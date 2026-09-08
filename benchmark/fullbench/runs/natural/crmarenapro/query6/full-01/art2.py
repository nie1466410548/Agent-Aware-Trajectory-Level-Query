import json
rows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query6/full-01/results/75a9566514fb48b18fc754cea72eb5b4.json'))
for r in rows:
    if r['id'].strip('#') == 'ka0Wt000000EnwvIAC':
        print(r['id'], '|', r['title'])
        print(r['faq_answer__c'])
