"""Relative real-gap replay with independent query and background build processes."""
import argparse
import json
import os
import resource
import shutil
import tempfile
import time
from pathlib import Path
from .async_backend import AsyncBackend
from .async_engine import AsyncEngine
from .replay import DEFAULT_CONFIG,sha,io_stats
from .rewrite import rewrite,preserve_rounding_scan_order


def worker(database,timing,out,mode,diagnostic=False,correctness_only=False,skip_idle=False):
    if correctness_only and skip_idle:raise ValueError('choose one replay mode')
    out=Path(out);out.mkdir(parents=True,exist_ok=False);(out/'results').mkdir()
    source=json.loads(Path(timing).read_text())
    if source['source_database_sha256']!=sha(database):raise ValueError('trajectory/data mismatch')
    config=dict(DEFAULT_CONFIG)
    # Only the replay harness sees gaps. The controller is in a separate process.
    calls=[dict(c,arguments={'sql':c['arguments']['sql']}) if mode=='baseline' else c for c in source['calls']]
    for call in calls:call['request_json']=json.dumps(call['arguments'],ensure_ascii=False)
    manifest={'mode':mode,'pid':os.getpid(),'diagnostic':diagnostic,'timing_sha256':sha(timing),
              'database_sha256':sha(database),'config':config,'affinity':sorted(os.sched_getaffinity(0)),
              'journal_mode':'WAL','materialization_storage':'task-scoped committed main tables',
              'source_wait_seconds':source['total_wait_seconds'],'skip_idle':skip_idle,'correctness_only':correctness_only,'storage_note':'copy under /tmp; mount recorded by experiment runner'}
    with tempfile.TemporaryDirectory(prefix='fad-async-') as scratch:
        path=Path(scratch)/'task.sqlite';before=time.monotonic()
        shutil.copyfile(database,path)
        warm=AsyncBackend(path);warm.prewarm();warm.close()
        manifest['preparation_seconds']=time.monotonic()-before
        start=time.monotonic_ns();cpu=time.process_time();io_before=io_stats()
        backend=AsyncBackend(path);engine=AsyncEngine(path,mode,config) if mode!='baseline' else None
        records=[];waits=[];skipped_ns=0;previous_step=None
        def wait_until(anchor,seconds):
            nonlocal skipped_ns
            skipped=0
            began=time.monotonic_ns();deadline=anchor+round((0 if correctness_only else seconds)*1e9)
            while True:
                if engine:engine.poll()
                remaining=(deadline-time.monotonic_ns())/1e9
                if remaining<=0:break
                if skip_idle:
                    if engine and any(e['type']=='worker_error' for e in engine.events):raise RuntimeError('background worker failed')
                    done=(not engine or any(e['type']==('worker_ready' if previous_step is None else 'decision') and (previous_step is None or e.get('step')==previous_step) for e in engine.events))
                    if done:
                        skipped=max(0,deadline-time.monotonic_ns());skipped_ns+=skipped;break
                time.sleep(min(.001 if skip_idle else .1,remaining))
            waits.append({'anchor_ns':anchor,'started_ns':began,'ended_ns':time.monotonic_ns(),'requested_seconds':seconds,'skipped_idle_ns':skipped})
        anchor=start
        with (out/'events.jsonl').open('w') as log:
            for c in calls:
                wait_until(anchor,c['gap_before_seconds'])
                arrival=time.monotonic_ns();args=json.loads(c['request_json']);sql=args['sql'];step=c['step']
                # Establish a stable reader snapshot; never wait for a build job.
                snapshot_start,snapshot_end=backend.begin_snapshot()
                objects=engine.available(snapshot_start) if engine else []
                began=time.monotonic_ns();used=[];reasons=[];executed=sql
                if engine:
                    original_plan=backend.explain(sql)
                    if not (original_plan and original_plan[0][0]=='error'):
                        executed,used,reasons=rewrite(sql,objects,backend.catalog)
                        # Protect original unindexed base scans for ROUND aggregates,
                        # including an index that committed just before this snapshot.
                        if any(n.startswith('fad_i_') for n in backend.snapshot_indexes):
                            executed,guarded=preserve_rounding_scan_order(executed,set(backend.catalog))
                            if guarded:reasons.append('preserve original rounding scan order')
                rewrite_seconds=(time.monotonic_ns()-began)/1e9 if engine else 0
                plan_started=time.monotonic_ns()
                plan=backend.explain(executed) if diagnostic or engine else None
                plan_seconds=(time.monotonic_ns()-plan_started)/1e9 if diagnostic or engine else 0
                execution_start=time.monotonic_ns()
                result=backend.execute(executed,out/'results'/f'Q{step}.jsonl')
                backend.end_snapshot()
                completed=time.monotonic_ns()
                delivered=engine.submit(step,args.get('future_access')) if engine else None
                r={'step':step,'sql':sql,'executed_sql':executed,'raw_fad':args.get('future_access'),
                   'arrival_ns':arrival,'snapshot_start_ns':snapshot_start,'snapshot_end_ns':snapshot_end,
                   'execution_start_ns':execution_start,'query_completed_ns':completed,
                   'fad_delivered_ns':delivered,'available_objects':[o['name'] for o in objects],
                   'materializations_used':used,'rewrite_reasons':reasons,'rewrite_seconds':rewrite_seconds,
                   'plan':plan,'plan_seconds':plan_seconds,'snapshot_indexes':backend.snapshot_indexes,**result}
                log.write(json.dumps(r,ensure_ascii=False)+'\n');log.flush()
                # This is the simulated tool return; the next gap starts here.
                anchor=time.monotonic_ns();r['response_return_ns']=anchor
                records.append(r)
                previous_step=step
                if correctness_only and engine:
                    # Independent semantic validation: force ready paths, never
                    # publish these timings as the real-gap experiment.
                    deadline=time.monotonic()+150
                    while time.monotonic()<deadline:
                        engine.poll()
                        if any(e['type']=='decision' and e['step']==step for e in engine.events):break
                        if any(e['type']=='worker_error' for e in engine.events):raise RuntimeError('validation worker failed')
                        time.sleep(.02)
                    else:raise TimeoutError('validation worker did not finish FAD')
        wait_until(anchor,source['final_gap_seconds'])
        report_ns=time.monotonic_ns()
        close_result=engine.close() if engine else {'exit_code':0,'closed_event':True,'forced_termination':False,'errors':[]}
        background_events=engine.events if engine else []
        backend.close();closed_ns=time.monotonic_ns()
        io_after=io_stats()
        result={'task_wall_seconds':(report_ns-start)/1e9,
                'skipped_idle_seconds':skipped_ns/1e9,
                'reconstructed_task_seconds':(report_ns-start+skipped_ns)/1e9,
                'reconstructed_including_cleanup_seconds':(closed_ns-start+skipped_ns)/1e9,'including_cleanup_seconds':(closed_ns-start)/1e9,
                'tail_cleanup_seconds':(closed_ns-report_ns)/1e9,'query_seconds':sum(r['query_seconds'] for r in records),
                'database_request_seconds':sum((r['response_return_ns']-r['arrival_ns'])/1e9 for r in records),
                'rewrite_seconds':sum(r['rewrite_seconds'] for r in records),'plan_seconds':sum(r['plan_seconds'] for r in records),'source_wait_seconds':source['total_wait_seconds'],
                'query_attempts':len(records),'query_successes':sum(r['status']=='ok' for r in records),
                'foreground_cpu_seconds':time.process_time()-cpu,'foreground_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                'foreground_io_delta':{k:io_after[k]-io_before.get(k,0) for k in io_after},
                'started_ns':start,'report_ns':report_ns,'closed_ns':closed_ns,'backend_close':close_result,
                'manifest':manifest}
        (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
        (out/'timeline.json').write_text(json.dumps({'queries':records,'waits':waits,'background':background_events},ensure_ascii=False,indent=2)+'\n')
        if not close_result['closed_event'] or close_result['errors'] or close_result['exit_code']:
            raise RuntimeError('background did not close cleanly; see saved evidence')
        return result


def main():
    p=argparse.ArgumentParser();p.add_argument('--database',required=True);p.add_argument('--timing',required=True)
    p.add_argument('--out',required=True);p.add_argument('--mode',choices=['baseline','combined','index','materialization'],required=True)
    p.add_argument('--diagnostic',action='store_true');p.add_argument('--correctness-only',action='store_true');p.add_argument('--skip-idle',action='store_true');a=p.parse_args()
    r=worker(a.database,a.timing,a.out,a.mode,a.diagnostic,a.correctness_only,a.skip_idle)
    print(json.dumps({k:r[k] for k in ('task_wall_seconds','including_cleanup_seconds','query_attempts','query_successes')},indent=2))

if __name__=='__main__':main()
