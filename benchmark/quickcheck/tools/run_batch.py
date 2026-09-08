"""Run the predeclared 18 benchmark episodes with three independent workers."""
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
tasks=json.loads((ROOT/'tasks.json').read_text())['tasks']
# Alternate group order by task to reduce a fixed natural-before-FAD ordering effect.
jobs=[]
for n,(d,i) in enumerate((d,i) for d,ids in tasks.items() for i in ids):
    for g in (['natural','fad'] if n%2==0 else ['fad','natural']):jobs.append((d,i,g))
def run(job):
    d,i,g=job
    report=ROOT/'reports'/f'{g}-{d}-query{i}-quick-01.json'
    if report.exists():return 'EXISTING '+str(report.name)
    print('START',g,d,i,flush=True)
    p=subprocess.run([sys.executable,str(ROOT/'tools/run_task.py'),d,str(i),g],capture_output=True,text=True)
    (ROOT/'reports'/f'launcher-{g}-{d}-{i}.log').write_text(p.stdout+p.stderr)
    if report.exists():
        r=json.loads(report.read_text())
        return f"DONE {g} {d}/{i}: passed={r['validator_passed']} SQL={r['sql_calls']} duration={r['duration_s']:.1f}s"
    return f'ERROR {g} {d}/{i}: launcher exit={p.returncode}'
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    futures=[pool.submit(run,j) for j in jobs]
    for f in concurrent.futures.as_completed(futures):print(f.result(),flush=True)
