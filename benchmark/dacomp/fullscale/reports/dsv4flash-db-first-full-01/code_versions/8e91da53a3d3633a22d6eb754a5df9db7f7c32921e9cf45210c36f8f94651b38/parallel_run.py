"""Single-writer parallel scheduler: no repeated main attempts, global stop latch."""
import argparse,fcntl,json,os,signal,subprocess,time
from common import *
from run import terminate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--concurrency',type=int,default=4);a=parser.parse_args();assert 1<=a.concurrency<=8
    lock=(ROOT/'state/dispatch.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
    queuepath=ROOT/'state/queue.json';stop=ROOT/'state/parallel-stop.json'
    q=json.loads(queuepath.read_text())
    assert not q.get('stop_reason') and not stop.exists(),'Explicit recovery required after stop'
    assert not any(v['status']=='running' for v in q['tasks'].values()),'Wait for serial handover; do not duplicate an active task'
    assert json.loads((ROOT/'state/acceptance.json').read_text())['passed']
    assert json.loads((ROOT/'state/local_tests.json').read_text())['passed']
    q.update(scheduler='parallel_v1',concurrency=a.concurrency,controller_pid=os.getpid(),current_tasks=[])
    active={}
    def save():
        q['current_tasks']=list(active);q['current_task']=next(iter(active),None);q['updated_at']=time.time();dump(queuepath,q)
    def latch(event):
        with stop.with_suffix('.lock').open('a') as f:
            fcntl.flock(f,fcntl.LOCK_EX)
            if not stop.exists():dump(stop,{**event,'time':time.time()})
        q['stop_reason']=json.loads(stop.read_text());save()
    save()
    try:
        while True:
            if stop.exists() and not q.get('stop_reason'):q['stop_reason']=json.loads(stop.read_text());save()
            completed=[]
            for tid,(proc,log) in list(active.items()):
                if proc.poll() is None:continue
                log.close();r=ROOT/'runs'/BATCH/tid/'attempt-01';sp=r/'run_summary.json'
                if sp.exists():
                    summary=json.loads(sp.read_text());q['tasks'][tid]={'status':summary['status'],'summary':str(sp.relative_to(ROOT))}
                    if summary['status'] in ['quota_interrupted','service_error','process_failed','orchestration_failed']:latch({'kind':summary['status'],'task_id':tid,'detail':summary.get('provider_stop')})
                else:
                    q['tasks'][tid]={'status':'orchestration_failed','exit_code':proc.returncode};latch({'kind':'orchestration_failed','task_id':tid,'exit_code':proc.returncode})
                del active[tid];completed.append(tid);save();print('END',tid,q['tasks'][tid]['status'],flush=True)
            if completed:
                # This controller is the sole queue writer and pauses queue writes
                # while report.py audits finished trajectories. Active runs skipped.
                result=subprocess.run([str(PYTHON),str(ROOT/'tools/report.py')])
                q=json.loads(queuepath.read_text())
                if result.returncode or q.get('stop_reason'):
                    latch(q.get('stop_reason') or {'kind':'report_failed','exit_code':result.returncode})
            if not q.get('stop_reason') and not stop.exists():
                for tid in q['order']:
                    if len(active)>=a.concurrency:break
                    if q['tasks'][tid]['status'] not in ('pending','resume_pending'):continue
                    resuming=q['tasks'][tid]['status']=='resume_pending'
                    if stop.exists():break
                    r=ROOT/'runs'/BATCH/tid/'attempt-01'
                    if r.exists() and not resuming:latch({'kind':'existing_attempt_conflict','task_id':tid});break
                    q['tasks'][tid]={'status':'running','started_at':time.time(),'scheduler':'parallel_v1'};save()
                    log=(ROOT/'state'/f'{tid}.worker.log').open('a')
                    proc=subprocess.Popen([str(PYTHON),str(ROOT/'tools'/('resume_worker.py' if resuming else 'parallel_worker.py')),tid,'--concurrency',str(a.concurrency)],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
                    active[tid]=(proc,log);save();print('START',tid,'worker',proc.pid,flush=True)
            if not active:break
            time.sleep(.2)
    except BaseException as e:
        latch({'kind':'controller_interrupted','error':repr(e)})
        # Workers see the shared latch, cancel their OpenCode process groups and
        # reconcile all SQL requests. Preserve them long enough to flush evidence.
        for tid,(proc,log) in active.items():
            try:proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                r=ROOT/'runs'/BATCH/tid/'attempt-01';pp=r/'process.json'
                if pp.exists():
                    try:os.killpg(json.loads(pp.read_text())['pid'],signal.SIGTERM)
                    except ProcessLookupError:pass
                proc.wait(timeout=10)
            log.close()
            sp=ROOT/'runs'/BATCH/tid/'attempt-01/run_summary.json'
            q['tasks'][tid]={'status':json.loads(sp.read_text())['status'] if sp.exists() else 'orchestration_failed','summary':str(sp.relative_to(ROOT)) if sp.exists() else None}
        active.clear();save();raise
    save();lock.close();print('DONE',json.dumps({s:sum(v['status']==s for v in q['tasks'].values()) for s in sorted({v['status'] for v in q['tasks'].values()})}),flush=True)
if __name__=='__main__':main()
