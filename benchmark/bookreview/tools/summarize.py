"""Export SQL statements and descriptive counts; this does not prove semantic reuse."""
import collections
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
reports=[]
for log in sorted((ROOT/'runs').glob('query*/*/tool_calls.jsonl')):
    run=log.parent
    calls=[json.loads(line) for line in log.read_text().splitlines()]
    sqls=[c for c in calls if 'sql' in c]
    out=run/'sql'
    out.mkdir(exist_ok=True)
    seen=collections.Counter()
    exact=0
    entries=[]
    for i,c in enumerate(sqls,1):
        name=f'{i:03d}-{c["database"]}-{c["call_id"]}.sql'
        (out/name).write_text(c['sql']+'\n')
        key=(c['database'],c['sql'])
        if c['success']:
            exact += int(seen[key]>0)
            seen[key]+=1
        entries.append({'sequence':i,'file':name,**c})
    (out/'index.json').write_text(json.dumps(entries,indent=2,ensure_ascii=False)+'\n')
    meta=json.loads((run/'task_meta.json').read_text())
    report_path=ROOT/'reports'/f'{run.parent.name}-{run.name}.json'
    report=json.loads(report_path.read_text()) if report_path.exists() else meta
    report.update(sql_calls=len(sqls),successful_sql_calls=sum(c['success'] for c in sqls),
                  data_query_calls=sum(c['tool']=='query-db' for c in calls),
                  metadata_query_calls=sum(c['tool']=='list-db' for c in calls),
                  exact_repeat_successful_sql_calls=exact,
                  sql_tool_wall_ms=sum(c['duration_ms'] for c in sqls),
                  python_calls=sum(c['tool']=='python' for c in calls))
    reports.append(report)
(ROOT/'reports/summary.json').write_text(json.dumps(reports,indent=2,ensure_ascii=False)+'\n')
print(json.dumps(reports,indent=2,ensure_ascii=False))
