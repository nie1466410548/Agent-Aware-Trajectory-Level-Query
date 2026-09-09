"""Up to ten offline warm-cache build-versus-reuse cases; no model calls."""
import json,sqlite3,time,statistics
from common import *
from opportunities import equal
import sqlglot

def run_case(candidate,entry,run):
 start=time.time();deadline=start+300; db=sqlite3.connect(Path(entry['database_path']).resolve().as_uri()+'?mode=ro',uri=True)
 db.set_progress_handler(lambda:int(time.time()>deadline),10000)
 queries={q['sql_id']:q for q in records(run/'sql_events.jsonl')};ids=candidate['covered']; archived={}
 for sid in ids:
  q=queries[sid]
  if q['result_bytes']>32*1024*1024: return {'status':'limited','reason':'result cap'}
  archived[sid]=[json.loads(l) for l in (run/q['result_file']).read_text().splitlines()]
 def consume(sql):
  cursor=db.execute(sql);rows=[]
  while chunk:=cursor.fetchmany(1000):
   rows.extend([list(r) for r in chunk])
   if time.time()>deadline or len(rows)>1_000_000: raise TimeoutError('performance cap')
  return [d[0] for d in cursor.description],rows
 def path(materialize):
  t=time.perf_counter();build_ms=0
  if materialize:
   db.execute('CREATE TEMP TABLE reuse_candidate AS '+candidate['build_sql']);build_ms=(time.perf_counter()-t)*1000
  results={sid:consume(candidate['rewrites'][sid] if materialize else queries[sid]['sql']) for sid in ids}
  total=(time.perf_counter()-t)*1000
  if materialize: db.execute('DROP TABLE temp.reuse_candidate')
  for sid,(columns,rows) in results.items():
   ordered=bool(sqlglot.parse_one(queries[sid]['sql'],read='sqlite').args.get('order'))
   if columns!=queries[sid]['columns'] or not equal(rows,archived[sid],ordered): raise ValueError('Result mismatch during performance '+sid)
  return {'total_ms':total,'build_ms':build_ms}
 output={'task_id':entry['task_id'],'candidate_id':candidate['candidate_id'],'covered':ids,'build_sql':candidate['build_sql'],'rewrites':candidate['rewrites'],
         'phase':'offline_performance','cache':'warm/uncontrolled OS cache','timing_boundary':'execute + fetch all row arrays; candidate includes CREATE TEMP TABLE AS and all rewrites; excludes result comparison and teardown, identical consumption on both paths',
         'teardown':'DROP after trial, outside timer; no index/maintenance used','rounds':[],'engine_trace':[]}
 db.set_trace_callback(lambda statement:output['engine_trace'].append({'phase':'offline_performance','sql':statement,'time':time.time()}))
 try:
  output['correctness_warmup']={'baseline':path(False),'candidate':path(True)}
  for i in range(5):
   record={'round':i+1,'order':['baseline','candidate'] if i%2==0 else ['candidate','baseline']}
   for name in record['order']: record[name]=path(name=='candidate')
   output['rounds'].append(record)
  a=[r['baseline']['total_ms'] for r in output['rounds']];b=[r['candidate']['total_ms'] for r in output['rounds']]
  output.update(status='measured',baseline_median_ms=statistics.median(a),baseline_range_ms=[min(a),max(a)],candidate_median_ms=statistics.median(b),candidate_range_ms=[min(b),max(b)],ratio_baseline_over_candidate=statistics.median(a)/statistics.median(b))
 except Exception as e: output.update(status='limited_or_failed',error=repr(e))
 finally: db.close()
 output['duration_s']=time.time()-start;return output

def main():
 entries={r['task_id']:r for r in records(ROOT/'manifests/tasks.jsonl')};candidates=records(REPORT/'verification.jsonl');scored=[]
 for c in candidates:
  if c['status']!='verified' or c['existing_result']:continue
  run=ROOT/'runs'/BATCH/c['task_id']/'attempt-01';qs=records(run/'sql_events.jsonl');score=sum(q['execute_fetch_ms'] for q in qs if q['sql_id'] in c['covered']);scored.append((score,c))
 selected=[];seen=set()
 for score,c in sorted(scored,key=lambda x:(-x[0],x[1]['task_id'],x[1]['candidate_id'])):
  if c['task_id'] in seen:continue
  seen.add(c['task_id']);selected.append({'score_original_execute_fetch_ms':score,'candidate':c})
  if len(selected)==10:break
 dump(REPORT/'performance-selection.json',{'rule':'Up to 10 verified new materializations, one per task, ranked by covered original execute_fetch_ms descending; selection offline across available trajectories','selected':selected})
 results=[]
 for item in selected:
  c=item['candidate'];path=REPORT/'tasks'/f"{c['task_id']}.{c['candidate_id']}.performance.json"
  if path.exists(): result=json.loads(path.read_text())
  else: result=run_case(c,entries[c['task_id']],ROOT/'runs'/BATCH/c['task_id']/'attempt-01');dump(path,result)
  results.append(result);print(c['task_id'],c['candidate_id'],result['status'],flush=True)
 dump(REPORT/'performance.json',results)
if __name__=='__main__':main()
