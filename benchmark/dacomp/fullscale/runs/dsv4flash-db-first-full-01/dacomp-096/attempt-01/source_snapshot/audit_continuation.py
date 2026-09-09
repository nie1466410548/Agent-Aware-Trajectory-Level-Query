"""Offline append-only evidence checks for explicitly resumed attempts."""
import hashlib,json,time
from common import *

def main():
 auth=json.loads((ROOT/'state/recovery-authorization.json').read_text());results=[]
 for tid in auth['resume_tasks']:
  run=ROOT/'runs'/BATCH/tid/'attempt-01';history=run/'continuations'/auth['id'];original=json.loads((history/'original-files.json').read_text());issues=[];checked=0
  append_names={'sql_journal.jsonl','sql_events.jsonl','tool_calls.jsonl','tool_journal.jsonl','opencode.jsonl','opencode.stderr.log','child_processes.jsonl','provider/requests.jsonl'}
  for name,info in original.items():
   p=run/name
   immutable=name.startswith(('sql/','params/','results/','python/','source_snapshot/')) or (name.startswith('provider/R') and name.endswith(('.request.json','.response.raw')))
   if name not in append_names and not immutable:continue
   checked+=1
   if not p.exists():issues.append({'file':name,'issue':'missing'});continue
   with p.open('rb') as f:actual=hashlib.sha256(f.read(info['bytes'])).hexdigest()
   if actual!=info['sha256'] or (immutable and p.stat().st_size!=info['bytes']):issues.append({'file':name,'issue':'original evidence changed'})
  summary=json.loads((run/'run_summary.json').read_text());old=json.loads((history/'run_summary.json').read_text())
  if summary['session_ids']!=old['session_ids']:issues.append({'issue':'session changed'})
  events=records(run/'sql_events.jsonl');ids=[e['sql_id'] for e in events]
  if len(ids)!=len(set(ids)):issues.append({'issue':'duplicate SQL IDs'})
  attempts=list(run.parent.glob('attempt-*'))
  if len(attempts)!=1:issues.append({'issue':'extra main attempt'})
  results.append({'task_id':tid,'same_session':summary['session_ids']==old['session_ids'],'checked_original_files_or_prefixes':checked,'issues':issues,'sql_before':old['all_sql_attempts'],'sql_after':summary['all_sql_attempts'],'active_duration_s':summary['duration_s']})
 dump(ROOT/'state/continuation_audit.json',{'checked_at':time.time(),'passed':not any(r['issues'] for r in results),'tasks':results})
 print(json.dumps(results,ensure_ascii=False))
if __name__=='__main__':main()
