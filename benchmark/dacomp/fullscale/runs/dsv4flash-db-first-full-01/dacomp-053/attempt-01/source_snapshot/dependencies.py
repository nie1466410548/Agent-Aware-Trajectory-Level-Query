"""Evidence-backed interface/file consumption edges, not inferred causal intent."""
import ast,json,re
from common import *
def main():
 edges=[]
 for entry in records(ROOT/'manifests/tasks.jsonl'):
  tid=entry['task_id'];run=ROOT/'runs'/BATCH/tid/'attempt-01';queries=records(run/'sql_events.jsonl');calls=records(run/'tool_calls.jsonl');pnum=0
  for c in calls:
   if c['tool']!='python':continue
   pnum+=1;code=c['arguments']['code'];pid=f'P{pnum}'
   for q in queries:
    if q['source']=='python' and q['call_id']==c['call_id']:
     edges.append({'task_id':tid,'producer_sql':q['sql_id'],'consumer_python':pid,'type':'same_call_database_result','evidence':f'python/{pid}.py','call_id':c['call_id'],'result_file':q.get('result_file'),'semantic_use':'returned to Python caller; exact operations in source','causal_query_choice':'not_inferred'})
    else:
     for i,line in enumerate(code.splitlines(),1):
      if re.search(r'(?<![A-Za-z0-9])'+re.escape(q['sql_id'])+r'\.rows\.jsonl',line):
       edges.append({'task_id':tid,'producer_sql':q['sql_id'],'consumer_python':pid,'type':'literal_archive_reference','evidence':f'python/{pid}.py:{i}','source_line':line,'causal_query_choice':'not_inferred'})
 (REPORT/'dependencies.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in edges))
 dump(REPORT/'dependency_coverage.json',{'method':'Exact parent-call linkage and literal result archive references in Python source; no coincidental SQL literal matching. SQL-to-SQL result-dependent parameter choices are not automatically inferred.','edges':len(edges)})
 print('Dependency evidence edges',len(edges))
if __name__=='__main__':main()
