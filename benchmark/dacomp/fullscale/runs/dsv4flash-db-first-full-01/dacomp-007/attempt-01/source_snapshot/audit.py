"""Offline integrity, context and acceptance gate. No model calls."""
import argparse, collections, json, re, time
from common import *
def audit_task(tid,entry):
 run=ROOT/'runs'/BATCH/tid/'attempt-01';summary=json.loads((run/'run_summary.json').read_text()) if (run/'run_summary.json').exists() else {}
 es=records(run/'sql_events.jsonl');js=records(run/'sql_journal.jsonl');calls=records(run/'tool_calls.jsonl');oc=records(run/'opencode.jsonl')
 requests=[x for x in js if x.get('record')=='request']; completions=[x for x in js if x.get('record')=='completion']; traces=[x for x in js if x.get('record')=='engine_trace']
 issues=[]
 if len(requests)!=len(completions) or len(es)!=len(requests): issues.append('SQL request/completion mismatch')
 if len({e['sql_id'] for e in es})!=len(es): issues.append('Duplicate SQL IDs')
 if any(t.get('sql_id') not in {e['sql_id'] for e in es} for t in traces): issues.append('Unattributed engine trace')
 for e in es:
  if e.get('result_file') and sha(run/e['result_file'])!=e['result_sha256']: issues.append('Archive hash mismatch '+e['sql_id'])
  if e['status']=='success' and not e['engine_statements']: issues.append('Successful statement lacks engine trace '+e['sql_id'])
  if e['call_id'] not in {c['call_id'] for c in calls}: issues.append('SQL missing tool call '+e['sql_id'])
 requests_files=sorted((run/'provider').glob('*.request.json'));models=set();toolnames=set(); backend=set(); usage=[]
 for p in requests_files:
  body=json.loads(p.read_text());models.add(body.get('model'));toolnames.update(t.get('function',{}).get('name','') for t in body.get('tools',[]))
  system='\n'.join(str(m.get('content','')) for m in body.get('messages',[]) if m.get('role') in ['system','developer'])
  if any(x in system for x in ['FULL_RUN_HANDOFF_PLAN','研究课题名称.md','Related Work 与研究定位','pilot-01']): issues.append('Unexpected background in system context')
 for p in (run/'provider').glob('*.response.raw'):
  for line in p.read_text(errors='replace').splitlines():
   if line.startswith('data: '):
    try:
     data=json.loads(line[6:]);
     if data.get('model'): backend.add(data['model'])
     if data.get('usage'): usage.append(data['usage'])
    except json.JSONDecodeError: pass
 if models and models!={MODEL.split('/',1)[1]}: issues.append('Unexpected requested model '+str(models))
 if any(not t.startswith('dacomp_') for t in toolnames): issues.append('Unexpected exposed tool '+str(toolnames))
 if requests_files and not toolnames: issues.append('No exposed MCP tools')
 tool_events=[e for e in oc if e.get('type')=='tool_use'];linked=set();links=[]
 for e in tool_events:
  part=e.get('part',{});state=part.get('state',{});output=str(state.get('output',''))+'\n'+str(state.get('error',''))
  for c in calls:
   if c['call_id'] in str(output):
    linked.add(c['call_id']);links.append({'call_id':c['call_id'],'mcp_request_id':c['mcp_request_id'],'opencode_call_id':part.get('callID'),'session_id':e.get('sessionID'),'message_id':part.get('messageID'),'opencode_tool':part.get('tool'),'opencode_status':state.get('status')})
 (run/'tool_call_links.jsonl').write_text(''.join(json.dumps(link,ensure_ascii=False)+'\n' for link in links))
 if calls and len(linked)!=len(calls): issues.append(f'OpenCode/MCP call correlation incomplete {len(linked)}/{len(calls)}')
 if any(c['tool']=='python' and not c['arguments'].get('reason') for c in calls): issues.append('Python reason missing')
 dbhash=sha(entry['database_path']) if entry.get('status')=='ready' else None
 if dbhash!=entry.get('database_sha256'): issues.append('Source database hash changed')
 result={'task_id':tid,'status':summary.get('status','not_started'),'sql_attempts':len(es),'engine_traces':len(traces),'tool_calls':len(calls),'linked_tool_calls':len(linked),'issues':issues,
         'requested_models':sorted(models),'backend_models_reported':sorted(backend),'usage':usage,'tool_names':sorted(toolnames),'database_sha256_after':dbhash,
         'upstream_requests':sum(x.get('status')!='blocked_local_retry' for x in records(run/'provider/requests.jsonl')),'blocked_local_retries':sum(x.get('status')=='blocked_local_retry' for x in records(run/'provider/requests.jsonl')),
         'passed':not issues and summary.get('status')=='submitted'}
 dump(run/'audit.json',result);return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--acceptance',action='store_true');p.add_argument('--task');args=p.parse_args()
 queue=json.loads((ROOT/'state/queue.json').read_text());entries={r['task_id']:r for r in records(ROOT/'manifests/tasks.jsonl')}
 tids=[args.task] if args.task else queue['acceptance_tasks'] if args.acceptance else [tid for tid,v in queue['tasks'].items() if v['status'] not in ['pending','preparation_failed']]
 results=[audit_task(tid,entries[tid]) for tid in tids];passed=all(r['passed'] for r in results)
 output={'checked_at':time.time(),'tasks':results,'passed':passed,'registered_tasks':len(entries),'status_counts':dict(collections.Counter(v['status'] for v in queue['tasks'].values()))}
 dump(ROOT/'state'/('acceptance.json' if args.acceptance else 'final_audit.json'),output)
 print(json.dumps(output,ensure_ascii=False,indent=2))
 if args.acceptance or args.task: raise SystemExit(not passed)
if __name__=='__main__':main()
