"""Guided new Agent source, full validation, two independent pairs, one report."""
import json
import subprocess
import sys
import time
from pathlib import Path
from agent_db_tool.optimization.timing import extract
from agent_db_tool.optimization.async_check import check
from agent_db_tool.optimization.replay import sha

root=Path('benchmark/dacomp/fad-optimization/async')
source=root/'source-ten-million-guided-01'
database=Path('benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite')
timing=root/'timing-ten-million-guided.json'
validation=root/'validation-ten-million-guided-v15'
run=root/'runs/reused-gaps-ten-million-guided-v15'
progress=root/'guided-ten-million-progress.json'
def status(stage,**extra):
    value={'stage':stage,'time':time.time(),**extra}
    progress.write_text(json.dumps(value,indent=2)+'\n');print(json.dumps(value),flush=True)
status('waiting_for_independent_source')
started=read_start=json.loads((source/'live-launch.json').read_text())['started_at']
while not (source/'summary.json').exists():
    if time.time()-started>3660:raise TimeoutError('source has not closed')
    time.sleep(1)
s=json.loads((source/'summary.json').read_text())
if s['timed_out'] or not s['answer_submitted']:raise RuntimeError('source incomplete; retained for inspection')
pref=json.loads((root/'preflight-v15-ten-million-guided/manifest.json').read_text())
assert all(sha(path)==digest for path,digest in pref['source_hashes'].items()),'optimizer changed since preflight'
t=extract(source,timing)
status('source_completed',calls=len(t['calls']),wait_seconds=t['total_wait_seconds'])
cmd=[sys.executable,'-m','agent_db_tool.optimization.async_replay','--database',str(database),'--timing',str(timing),'--out',str(validation),'--mode','combined','--diagnostic','--skip-idle']
status('validating_full_results');subprocess.run(cmd,check=True)
c=check(validation,timing)
if not c['all_equal']:raise RuntimeError('result mismatch; see validation correctness.json')
status('two_pairs_started',calls=len(t['calls']))
subprocess.run([sys.executable,'-m','agent_db_tool.optimization.async_experiment','--database',str(database),'--timing',str(timing),'--root',str(run),'--validation',str(validation),'--pairs','2','--skip-idle'],check=True)
status('auditing')
subprocess.run([sys.executable,str(root/'audit.py'),'--run',str(run)],check=True)
subprocess.run([sys.executable,str(root/'report_guided_ten_million.py'),'--run',str(run),'--output','benchmark/dacomp/fad-optimization/reports/REPORT.md'],check=True)
status('complete',run=str(run))
