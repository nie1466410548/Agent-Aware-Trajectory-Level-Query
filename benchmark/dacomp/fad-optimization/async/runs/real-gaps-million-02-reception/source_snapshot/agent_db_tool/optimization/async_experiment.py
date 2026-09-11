"""Five real-gap paired trials. Serial arms, concurrent work only inside an arm."""
import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import time
from pathlib import Path
from .async_check import check
from .replay import sha,DEFAULT_CONFIG


def main():
    p=argparse.ArgumentParser();p.add_argument('--database',required=True);p.add_argument('--timing',required=True)
    p.add_argument('--root',required=True);p.add_argument('--validation',required=True)
    p.add_argument('--pairs',type=int,default=5);p.add_argument('--seed',type=int,default=20260910)
    a=p.parse_args();root=Path(a.root).resolve();root.mkdir(parents=True,exist_ok=False)
    if not check(a.validation,a.timing)['all_equal']:raise RuntimeError('semantic validation failed')
    timing=json.loads(Path(a.timing).read_text());source_paths=list(Path('agent_db_tool/optimization').glob('*.py'))
    source_paths += [Path('agent_db_tool/v02.py'),Path('agent_db_tool/sqlite_adapter.py')]
    hashes={str(p):sha(p) for p in sorted(source_paths)}
    for path in source_paths:
        dest=root/'source_snapshot'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
    affinity=sorted(os.sched_getaffinity(0));os.sched_setaffinity(0,set(affinity[:2]))
    rng=random.Random(a.seed);order=[]
    for n in range(1,a.pairs+1):
        arms=['baseline','combined'];rng.shuffle(arms);order.append({'pair':n,'arms':arms})
    manifest={'database':str(Path(a.database).resolve()),'database_sha256':sha(a.database),
              'timing':str(Path(a.timing).resolve()),'timing_sha256':sha(a.timing),'pairs':a.pairs,'seed':a.seed,
              'config':DEFAULT_CONFIG,'source_hashes':hashes,'execution_order':order,'affinity':affinity[:2],
              'storage':subprocess.check_output(['df','-T','/tmp'],text=True),
              'initial_load':os.getloadavg(),'validation':str(Path(a.validation).resolve()),
              'source_wait_seconds':timing['total_wait_seconds'],
              'estimated_minimum_wait_total_seconds':2*a.pairs*timing['total_wait_seconds']}
    (root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'started':str(root),'pairs':a.pairs,'wait_per_arm_seconds':timing['total_wait_seconds']},indent=2),flush=True)
    for job in order:
        n=job['pair']
        for arm in job['arms']:
            out=root/f'pair-{n:02d}'/arm
            cmd=[sys.executable,'-m','agent_db_tool.optimization.async_replay','--database',a.database,
                 '--timing',a.timing,'--out',str(out),'--mode',arm]
            print(f'Pair {n}/{a.pairs}: {arm} started; real gaps uncompressed',flush=True)
            started=time.monotonic()
            with tempfile_output(root,n,arm) as (stdout,stderr):
                proc=subprocess.Popen(cmd,stdout=stdout,stderr=stderr)
                while proc.poll() is None:
                    records=[]
                    if (out/'events.jsonl').exists():
                        for line in (out/'events.jsonl').read_text().splitlines():
                            try:records.append(json.loads(line))
                            except ValueError:pass
                    progress={'pair':n,'arm':arm,'pid':proc.pid,'completed_queries':len(records),
                              'total_queries':len(timing['calls']),'elapsed_seconds':time.monotonic()-started}
                    (root/'progress.json').write_text(json.dumps(progress,indent=2)+'\n')
                    if time.monotonic()-started>timing['total_wait_seconds']+len(timing['calls'])*120+180:
                        proc.terminate();proc.wait(timeout=30);raise TimeoutError('replay exceeded full workload budget')
                    time.sleep(1)
            if proc.returncode:raise RuntimeError(f'worker failed; see {out}')
            correctness=check(out,a.timing)
            if not correctness['all_equal']:raise RuntimeError(f'actual replay results differ: {out}')
            print(f'Pair {n}/{a.pairs}: {arm} completed, all results equal',flush=True)
    assert all(sha(path)==h for path,h in hashes.items()),'source changed during experiment'
    assert sha(a.database)==manifest['database_sha256'] and sha(a.timing)==manifest['timing_sha256']
    (root/'COMPLETE.json').write_text(json.dumps({'pairs':a.pairs,'all_equal':True})+'\n')


class tempfile_output:
    def __init__(self,root,n,arm):self.prefix=root/f'pair-{n:02d}'/f'{arm}-worker'
    def __enter__(self):
        self.prefix.parent.mkdir(parents=True,exist_ok=True)
        self.stdout=self.prefix.with_suffix('.stdout').open('w');self.stderr=self.prefix.with_suffix('.stderr').open('w')
        return self.stdout,self.stderr
    def __exit__(self,*exc):self.stdout.close();self.stderr.close()

if __name__=='__main__':main()
