"""Run every declared task once per group; retain failures without answer-driven retries."""
import concurrent.futures,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def run(job):
 d,i,g=job;report=ROOT/'reports'/f'{g}-{d}-query{i}-full-01.json'
 if report.exists():return 'EXISTING '+report.name
 print('START',g,d,i,flush=True)
 with (ROOT/'reports'/f'launcher-{g}-{d}-{i}.log').open('w') as log:
  p=subprocess.run([sys.executable,str(ROOT/'tools/run_task.py'),d,str(i),g],stdout=log,stderr=subprocess.STDOUT)
 if report.exists():
  r=json.loads(report.read_text());return f"DONE {g} {d}/{i}: passed={r['validator_passed']} SQL={r['sql_calls']} Mongo={r['mongo_calls']} duration={r['duration_s']:.1f}s"
 return f'ERROR {g} {d}/{i}: launcher exit={p.returncode}'
def main():
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks'];jobs=[]
 order=sorted(tasks,key=lambda d:(d not in ['bookreview','crmarenapro','stockindex'],d))
 for n,(d,i) in enumerate((d,i) for d in order for i in tasks[d]):
  for g in (['natural','fad'] if n%2==0 else ['fad','natural']):jobs.append((d,i,g))
 (ROOT/'reports/batch-process.json').write_text(json.dumps({'pid':os.getpid(),'start':time.time(),'jobs':jobs,'workers':3},indent=2))
 queued=list(jobs);active={};done=[];last_setup=0
 with concurrent.futures.ThreadPoolExecutor(3) as pool:
  while queued or active:
   if time.time()-last_setup>30:
    with (ROOT/'reports/setup.log').open('a') as log:
     subprocess.run([sys.executable,str(ROOT/'tools/setup_databases.py')],stdout=log,stderr=subprocess.STDOUT)
    last_setup=time.time()
   ready=set(json.loads((ROOT/'reports/ready-datasets.json').read_text()))
   for job in list(queued):
    if len(active)>=3:break
    if job[0] not in ready:continue
    queued.remove(job);active[pool.submit(run,job)]=job
   for future in list(active):
    if future.done():
     job=active.pop(future)
     try:result=future.result()
     except Exception as e:result='ERROR '+str(job)+' '+repr(e)
     done.append({'job':job,'result':result});print(result,flush=True)
   tmp=ROOT/'reports/batch-status.tmp';tmp.write_text(json.dumps({'pid':os.getpid(),'updated':time.time(),'queued':queued,'active':list(active.values()),'done':done},indent=2));os.replace(tmp,ROOT/'reports/batch-status.json')
   if queued or active:time.sleep(2)
 print('BATCH FINISHED',len(done),'/',len(jobs),flush=True)
if __name__=='__main__':main()
