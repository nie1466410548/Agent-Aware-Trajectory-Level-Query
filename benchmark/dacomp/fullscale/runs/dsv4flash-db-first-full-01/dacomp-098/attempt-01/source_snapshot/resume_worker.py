"""Explicitly authorized continuation of the original OpenCode session/attempt."""
import argparse, json, os, signal, subprocess, time, shutil
from common import *
import run as runner
from parallel_worker import BatchRelay

class ResumeRelay(BatchRelay):
    def __init__(self, run, provider):
        last=max([int(p.name.split('.')[0][1:]) for p in (run/'provider').glob('R*.request.json')],default=0)
        super().__init__(run,provider)
        self.count=last

def terminate_current(proc,run,child_offset):
    for child in records(run/'child_processes.jsonl')[child_offset:]:
        try: os.killpg(child['pid'],signal.SIGKILL)
        except ProcessLookupError: pass
    try: os.killpg(proc.pid,signal.SIGTERM)
    except ProcessLookupError: pass
    try: proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGKILL);proc.wait()

def resume(tid):
    run=ROOT/'runs'/BATCH/tid/'attempt-01'
    old=json.loads((run/'run_summary.json').read_text())
    assert old['status'] in ('service_error','quota_interrupted') and not (run/'answer.md').exists()
    assert len(old['session_ids'])==1 and not BatchRelay.stop_path.exists()
    auth=json.loads((ROOT/'state/recovery-authorization.json').read_text())
    assert tid in auth['resume_tasks']
    history=run/'continuations'/auth['id'];history.mkdir(parents=True,exist_ok=False)
    for name in ['run_summary.json','task_meta.json','launch.json','process.json','opencode_config.json','audit.json','provider/stop.json']:
        source=run/name
        if source.exists():
            target=history/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
    prefixes={str(p.relative_to(run)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in run.rglob('*') if p.is_file() and 'continuations' not in p.parts}
    dump(history/'original-files.json',prefixes)
    (history/'source_snapshot').mkdir()
    for p in (ROOT/'tools').glob('*.py'):shutil.copy2(p,history/'source_snapshot'/p.name)
    (run/'provider/stop.json').unlink(missing_ok=True)
    (run/'audit.json').unlink(missing_ok=True)
    meta=json.loads((run/'task_meta.json').read_text())
    remaining=meta['task_timeout_s']-old['duration_s'];assert remaining>0
    start=time.time();meta.update(deadline=start+remaining,continuation_id=auth['id'],prior_active_duration_s=old['duration_s'])
    dump(run/'task_meta.json',meta)
    provider=json.loads(Path('/data/nly/.config/opencode/opencode.json').read_text())['provider']['glm-custom']
    relay=ResumeRelay(run,provider);cfg,env=runner.environment(run,relay.base_url)
    prompt='Continue the interrupted task in this existing session, using the existing work and results. The service interruption has ended. All original task instructions, database-first protocol, and cumulative tool limits still apply. Submit the final answer through dacomp_answer.'
    cmd=[runner.CLI,'run','--session',old['session_ids'][0],'--model',MODEL,'--format','json','--pure','--agent','dacomp-db-first',prompt]
    dump(history/'launch.json',{'argv':cmd,'environment_overrides':{k:v for k,v in env.items() if k.startswith(('XDG_','OPENCODE_'))},'cwd':str(run)})
    dump(history/'begin.json',{'started_at':start,'remaining_active_seconds':remaining,'session':old['session_ids'][0],'attempt':'attempt-01','prior_opencode_events':len(records(run/'opencode.jsonl'))})
    offset=len(records(run/'child_processes.jsonl'));event_offset=len(records(run/'opencode.jsonl'));status=None
    with (run/'opencode.jsonl').open('a') as out,(run/'opencode.stderr.log').open('a') as err:
        proc=subprocess.Popen(cmd,cwd=run,env=env,stdout=out,stderr=err,start_new_session=True)
        dump(run/'process.json',{'pid':proc.pid,'started_at':start,'continuation_id':auth['id']})
        try:
            while proc.poll() is None:
                if relay.stopped:status=relay.stopped['kind'];break
                if time.time()>meta['deadline']:status='timeout';break
                time.sleep(.2)
        except BaseException:
            status='interrupted';raise
        finally:
            terminate_current(proc,run,offset);relay.close()
            current=records(run/'opencode.jsonl')[event_offset:]
            if status is None:status='submitted' if proc.returncode==0 and not any(e.get('type')=='error' for e in current) and (run/'answer.md').exists() else 'process_failed'
            duration=time.time()-start
            summary=runner.summaries(run,meta,proc.returncode,old['duration_s']+duration,status)
            dump(history/'end.json',{'status':summary['status'],'active_duration_s':duration,'ended_at':time.time(),'session_ids':summary['session_ids']})
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('task_id');p.add_argument('--concurrency',type=int,default=4);a=p.parse_args()
    print(json.dumps(resume(a.task_id)),flush=True)
