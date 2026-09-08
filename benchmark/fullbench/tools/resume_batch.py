"""Resume missing episodes; archive quota failures and wait before retrying.

Answer validation failures are retained. Only explicit provider quota errors retry.
"""
import concurrent.futures,json,os,shutil,subprocess,sys,threading,time
from pathlib import Path
from run_batch import run,ROOT

paused=threading.Event()
QUOTA='5-hour usage limit'
def execute(job):
 result=run(job)
 ds,i,g=job
 directory=ROOT/'runs'/g/ds/f'query{i}'/'full-01'
 err=directory/'kimi.stderr.log'
 quota=err.exists() and QUOTA in err.read_text()
 if quota:paused.set()
 return result,quota

def archive(job):
 ds,i,g=job;directory=ROOT/'runs'/g/ds/f'query{i}'/'full-01'
 report=ROOT/'reports'/f'{g}-{ds}-query{i}-full-01.json'
 process=json.loads((directory/'process.json').read_text())
 try:os.kill(process['pid'],0)
 except ProcessLookupError:pass
 else:raise RuntimeError('Cannot archive a live Kimi process')
 target=ROOT/'incidents'/f'quota-{time.time_ns()}'/g/ds/f'query{i}'
 target.mkdir(parents=True)
 shutil.move(str(directory),str(target/'assigned-run'))
 shutil.move(str(report),str(target/'validation-report.json'))
 (target/'incident.json').write_text(json.dumps({'job':job,'reason':QUOTA,'excluded_from_primary':True,'recovery_required':True},indent=2)+'\n')
 return str(target.relative_to(ROOT))

def probe():
 directory=ROOT/'quota-probe';directory.mkdir(exist_ok=True)
 (directory/'empty-skills').mkdir(exist_ok=True)
 (directory/'agent.md').write_text('---\nname: quota-check\ndescription: Check model availability.\ntools: []\nsubagents: []\n---\nReply with OK.\n')
 cmd=['/data/nly/.kimi-code/bin/kimi','--model','kimi-code/k3','--skills-dir',str(directory/'empty-skills'),'--agent-file',str(directory/'agent.md'),'--prompt','Reply with OK.','--output-format','stream-json']
 try:
  p=subprocess.run(cmd,cwd=directory,text=True,capture_output=True,timeout=60)
  available=p.returncode==0 and bool(p.stdout.strip())
  record={'time':time.time(),'available':available,'exit_code':p.returncode,'quota_error':QUOTA in p.stderr}
 except subprocess.TimeoutExpired:available=False;record={'time':time.time(),'available':False,'timeout':True}
 with (ROOT/'reports/quota-probes.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
 print('QUOTA PROBE',record,flush=True)
 return available

def main():
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks'];jobs=[]
 order=sorted(tasks,key=lambda d:(d not in ['bookreview','crmarenapro','stockindex'],d))
 for n,(ds,i) in enumerate((ds,i) for ds in order for i in tasks[ds]):
  for g in (['natural','fad'] if n%2==0 else ['fad','natural']):
   if not (ROOT/'reports'/f'{g}-{ds}-query{i}-full-01.json').exists():jobs.append((ds,i,g))
 (ROOT/'reports/batch-process.json').write_text(json.dumps({'pid':os.getpid(),'start':time.time(),'jobs':jobs,'workers':3,'mode':'quota-aware-resume'},indent=2))
 queued=list(jobs);active={};done=[];paused.set();next_probe=0
 with concurrent.futures.ThreadPoolExecutor(3) as pool:
  while queued or active:
   for future in list(active):
    if not future.done():continue
    job=active.pop(future);result,quota=future.result()
    if quota:
     archived=archive(job);queued.append(job);next_probe=time.time()+300
     print('QUOTA ARCHIVED',job,archived,flush=True)
    else:done.append({'job':job,'result':result});print(result,flush=True)
   if paused.is_set() and not active and time.time()>=next_probe:
    if probe():paused.clear()
    else:next_probe=time.time()+300
   while queued and len(active)<3 and not paused.is_set():
    job=queued.pop(0);active[pool.submit(execute,job)]=job
   status={'pid':os.getpid(),'updated':time.time(),'queued':queued,'active':list(active.values()),'done':done,'quota_paused':paused.is_set(),'next_probe_at':next_probe if paused.is_set() else None}
   tmp=ROOT/'reports/batch-status.tmp';tmp.write_text(json.dumps(status,indent=2));os.replace(tmp,ROOT/'reports/batch-status.json')
   if queued or active:time.sleep(2)
 print('RESUMED BATCH FINISHED',flush=True)
 # Recovery annotations are administrative; validation failures are never retried.
 for p in (ROOT/'reports/incidents').glob('*.json'):
  incident=json.loads(p.read_text())
  if p.stem=='natural-crmarenapro-query7' and incident.get('recovery_required'):
   report=ROOT/'reports/natural-crmarenapro-query7-full-01.json';outcome=json.loads(report.read_text())
   outcome['instrumentation_recovery_of']=incident['archive'];report.write_text(json.dumps(outcome,indent=2)+'\n')
   incident.update(recovery_required=False,recovered_at=time.time(),primary_report=str(report),recovery_validator_passed=outcome['validator_passed']);p.write_text(json.dumps(incident,indent=2)+'\n')
 for script in ['analyze.py','structural.py','discover.py','provenance.py','report.py','audit_artifacts.py']:
  subprocess.run([sys.executable,str(ROOT/'tools'/script)],check=True)
if __name__=='__main__':main()
