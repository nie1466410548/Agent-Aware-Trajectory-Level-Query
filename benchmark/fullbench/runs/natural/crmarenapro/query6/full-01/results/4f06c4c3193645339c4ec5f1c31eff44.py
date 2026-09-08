import json
rows = json.load(open('/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/runs/natural/crmarenapro/query6/full-01/results/75a9566514fb48b18fc754cea72eb5b4.json'))
for r in rows:
    if 'discount' in (r['title'] or '').lower() or 'policy' in (r['title'] or '').lower() or 'regulation' in (r['title'] or '').lower() or 'pricing' in (r['title'] or '').lower() or 'quantity' in (r['title'] or '').lower():
        print('====', r['id'], '|', r['title'])
        print('SUMMARY:', r['summary'])
        print('ANSWER:', (r['faq_answer__c'] or '')[:2000])
        print()
