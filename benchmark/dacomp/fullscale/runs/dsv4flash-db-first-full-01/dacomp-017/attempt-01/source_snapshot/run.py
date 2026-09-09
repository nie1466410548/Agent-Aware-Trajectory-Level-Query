"""Serial OpenCode run/checkpoint orchestration. No automatic new attempts."""
import argparse, collections, copy, json, os, signal, subprocess, time
from common import *
from proxy import Relay
CLI='/data/nly/.opencode/bin/opencode'
CONFIG=json.loads((ROOT/'config'/f'{BATCH}.json').read_text())

def environment(run,base_url):
    original=json.loads(Path('/data/nly/.config/opencode/opencode.json').read_text())
    provider=copy.deepcopy(original['provider']['glm-custom']); provider['options']={'baseURL':base_url,'apiKey':'local-relay-no-credential'}
    provider['models']={MODEL.split('/',1)[1]:provider['models'][MODEL.split('/',1)[1]]}
    config={'$schema':'https://opencode.ai/config.json','model':MODEL,'small_model':MODEL,'enabled_providers':['glm-custom'],'provider':{'glm-custom':provider},
            'share':'disabled','autoupdate':False,'snapshot':False,'plugin':[],'instructions':[],
            'permission':{'*':'deny','dacomp_*':'allow'},
            'agent':{'dacomp-db-first':{'description':'Analyze the supplied database using recorded tools.','mode':'primary','model':MODEL,
                     'prompt':'You are a data analysis agent. Follow the supplied task and database-first protocol. Use only the dacomp tools. Submit the report through dacomp_answer.',
                     'permission':{'*':'deny','dacomp_*':'allow'}}},
            'mcp':{'dacomp':{'type':'local','command':[str(PYTHON),str(ROOT/'tools/server.py'),str(run)],'enabled':True,'timeout':310000}},
            'compaction':{'auto':False,'prune':False}}
    runtime=ROOT/'runtime'/run.parent.name
    for name in ['config','data','cache','state']: (runtime/name).mkdir(parents=True,exist_ok=True)
    env={k:v for k,v in os.environ.items() if not k.startswith(('OPENCODE_','ANTHROPIC_','OPENAI_'))}
    env.update({'XDG_CONFIG_HOME':str(runtime/'config'),'XDG_DATA_HOME':str(runtime/'data'),'XDG_CACHE_HOME':str(runtime/'cache'),'XDG_STATE_HOME':str(runtime/'state'),
                'OPENCODE_CONFIG_CONTENT':json.dumps(config),'OPENCODE_DISABLE_PROJECT_CONFIG':'1','OPENCODE_DISABLE_CLAUDE_CODE':'1','OPENCODE_DISABLE_CLAUDE_CODE_PROMPT':'1','OPENCODE_DISABLE_CLAUDE_CODE_SKILLS':'1',
                'OPENCODE_DISABLE_AUTOUPDATE':'1','OPENCODE_DISABLE_MODELS_FETCH':'1','OPENCODE_EXPERIMENTAL_DISABLE_FILEWATCHER':'1','OPENCODE_DISABLE_AUTOCOMPACT':'1','OPENCODE_DISABLE_PRUNE':'1'})
    return config,env

def terminate(proc,run):
    # Kill separately grouped Python sandbox launches before the OpenCode group.
    for child in records(run/'child_processes.jsonl'):
        try: os.killpg(child['pid'],signal.SIGKILL)
        except ProcessLookupError: pass
    try: os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError: pass
    try: proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        try: os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        proc.wait()

def summaries(run,meta,code,duration,status_override=None):
    # Reconcile killed in-flight requests explicitly; do not silently omit them.
    journal=records(run/'sql_journal.jsonl'); finished={e['sql_id'] for e in records(run/'sql_events.jsonl')}
    for request in journal:
      if request.get('record')!='request' or request['sql_id'] in finished: continue
      e={k:v for k,v in request.items() if k!='record'}; path=run/'results'/(e['sql_id']+'.rows.jsonl')
      e.update(status='cancelled',end_time=time.time(),error='Process ended before SQL completion record',coverage='request_and_available_trace_incomplete',
               engine_statements=[j['engine_sql'] for j in journal if j.get('record')=='engine_trace' and j.get('sql_id')==e['sql_id']],
               columns=None,row_count=None,archived_rows=None,result_complete=False,result_bytes=path.stat().st_size if path.exists() else 0,
               result_file=str(path.relative_to(run)) if path.exists() else None,result_sha256=sha(path) if path.exists() else None,
               execute_fetch_ms=0,timing_complete=False)
      append(run/'sql_events.jsonl',e);append(run/'sql_journal.jsonl',dict(e,record='completion'))
    events=records(run/'opencode.jsonl'); calls=records(run/'tool_calls.jsonl'); sqls=records(run/'sql_events.jsonl')
    errors=[e for e in events if e.get('type')=='error']; sessions=sorted({e['sessionID'] for e in events if e.get('sessionID')})
    msgs=[{'event_index':i,**e} for i,e in enumerate(events)]
    (run/'messages.jsonl').write_text(''.join(json.dumps(e,ensure_ascii=False)+'\n' for e in msgs))
    status=status_override or ('submitted' if code==0 and not errors and (run/'answer.md').exists() else 'no_submission' if code==0 else 'process_failed')
    stop=json.loads((run/'provider/stop.json').read_text()) if (run/'provider/stop.json').exists() else None
    if stop: status=stop['kind']
    summary={**meta,'status':status,'exit_code':code,'duration_s':duration,'session_ids':sessions,'error_events':errors,'provider_stop':stop,'answer_submitted':(run/'answer.md').exists(),
             'all_sql_attempts':len(sqls),'all_sql_success':sum(q['status']=='success' for q in sqls),'data_sql_attempts':sum(q['category']=='data' for q in sqls),
             'data_sql_success':sum(q['status']=='success' and q['category']=='data' for q in sqls),'python_calls':sum(c['tool']=='python' for c in calls),
             'raw_usage_events':[e for e in events if e.get('type')=='step_finish'],'official_evaluation':'not_run'}
    dump(run/'run_summary.json',summary);return summary

def preflight():
    run=ROOT/'state/preflight'; run.mkdir(exist_ok=True)
    cfg,env=environment(run,'http://127.0.0.1:1')
    evidence={}
    for args in [['debug','config'],['debug','agent','dacomp-db-first'],['debug','skill']]:
        p=subprocess.run([CLI,*args,'--pure'],env=env,cwd=run,capture_output=True,text=True,timeout=60)
        evidence[' '.join(args)]={'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        if p.returncode: raise RuntimeError('OpenCode configuration preflight failed: '+p.stderr)
    dump(ROOT/'state/opencode_preflight.json',evidence)
    dump(ROOT/'state/opencode_config.json',cfg)
    print('OpenCode read-only preflight complete',flush=True)

def run_task(tid,entry):
    run=ROOT/'runs'/BATCH/tid/'attempt-01'; run.mkdir(parents=True,exist_ok=False)
    meta={**CONFIG,'task_id':tid,'attempt':'attempt-01','database_path':entry['database_path'],'database_sha256':entry['database_sha256'],'database_bytes':entry['database_bytes'],
          'cli_version':subprocess.check_output([CLI,'--version'],text=True).strip(),'started_at':time.time(),'phase':'agent_trajectory','official_evaluation':'not_run'}
    meta['deadline']=meta['started_at']+CONFIG['task_timeout_s']
    meta['source_hashes']={str(p.relative_to(ROOT)):sha(p) for p in sorted((ROOT/'tools').glob('*.py'))}
    (run/'source_snapshot').mkdir()
    for p in (ROOT/'tools').glob('*.py'): (run/'source_snapshot'/p.name).write_bytes(p.read_bytes())
    (run/'requirements-lock.txt').write_bytes((BENCH/'requirements-lock.txt').read_bytes())
    dump(run/'task.json',entry['task']); dump(run/'schema.json',entry['tables'])
    prompt=(ROOT/'config/protocol.txt').read_text()+'\nORIGINAL TASK:\n'+entry['task']['instruction']+'\n\nDATABASE SCHEMA:\n'+'\n'.join(t['ddl'] for t in entry['tables'])
    (run/'prompt.txt').write_text(prompt); dump(run/'task_meta.json',meta)
    provider=json.loads(Path('/data/nly/.config/opencode/opencode.json').read_text())['provider']['glm-custom']
    relay=Relay(run,provider); cfg,env=environment(run,relay.base_url); dump(run/'opencode_config.json',cfg)
    cmd=[CLI,'run','--model',MODEL,'--format','json','--pure','--agent','dacomp-db-first','--title',tid,prompt]
    dump(run/'launch.json',{'argv':cmd,'environment_overrides':{k:v for k,v in env.items() if k.startswith(('XDG_','OPENCODE_'))},'cwd':str(run)})
    status=None
    with (run/'opencode.jsonl').open('w') as out,(run/'opencode.stderr.log').open('w') as err:
      proc=subprocess.Popen(cmd,cwd=run,env=env,stdout=out,stderr=err,start_new_session=True)
      dump(run/'process.json',{'pid':proc.pid,'started_at':time.time()})
      try:
        while proc.poll() is None:
          if relay.stopped: status=relay.stopped['kind']; terminate(proc,run);break
          if time.time()>meta['deadline']: status='timeout';terminate(proc,run);break
          time.sleep(0.2)
      except BaseException:
        terminate(proc,run); summaries(run,meta,proc.returncode,time.time()-meta['started_at'],'interrupted'); raise
      finally: relay.close()
    terminate(proc,run)
    return summaries(run,meta,proc.returncode,time.time()-meta['started_at'],status)

def main():
    p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');p.add_argument('--acceptance',action='store_true');p.add_argument('--continue-full',action='store_true'); args=p.parse_args()
    if args.preflight: preflight();return
    tests=json.loads((ROOT/'state/local_tests.json').read_text());assert tests['passed'],'Local tests must pass'
    queuepath=ROOT/'state/queue.json';queue=json.loads(queuepath.read_text()); entries={r['task_id']:r for r in records(ROOT/'manifests/tasks.jsonl')}
    if queue.get('stop_reason'): raise SystemExit('Stopped: explicit recovery required; see state/queue.json')
    if args.continue_full: assert (ROOT/'state/acceptance.json').exists() and json.loads((ROOT/'state/acceptance.json').read_text())['passed'],'Acceptance required'
    order=queue['acceptance_tasks'] if args.acceptance else queue['order'] if args.continue_full else []
    assert order,'Choose --acceptance or --continue-full'
    for tid in order:
      if queue['tasks'][tid]['status']!='pending': continue
      queue['current_task']=tid;queue['tasks'][tid]={'status':'running','started_at':time.time()};dump(queuepath,queue)
      print('START',tid,flush=True)
      try: summary=run_task(tid,entries[tid])
      except Exception as e:
        queue['tasks'][tid]={'status':'orchestration_failed','error':repr(e)};queue['stop_reason']={'kind':'orchestration_failed','task_id':tid,'error':repr(e)};dump(queuepath,queue);raise
      queue['tasks'][tid]={'status':summary['status'],'summary':f'runs/{BATCH}/{tid}/attempt-01/run_summary.json'}
      if summary['status'] in ['quota_interrupted','service_error','process_failed']: queue['stop_reason']={'kind':summary['status'],'task_id':tid,'detail':summary.get('provider_stop')}
      dump(queuepath,queue);print('END',tid,summary['status'],'SQL',summary['all_sql_attempts'],summary['data_sql_success'],'Python',summary['python_calls'],flush=True)
      subprocess.run([str(PYTHON),str(ROOT/'tools/report.py')],check=True)
      if queue.get('stop_reason'): break
      if args.acceptance:
        checked=subprocess.run([str(PYTHON),str(ROOT/'tools/audit.py'),'--task',tid])
        if checked.returncode:
          queue['stop_reason']={'kind':'acceptance_recording_gap','task_id':tid};dump(queuepath,queue);break
    queue['updated_at']=time.time();dump(queuepath,queue)
if __name__=='__main__': main()
