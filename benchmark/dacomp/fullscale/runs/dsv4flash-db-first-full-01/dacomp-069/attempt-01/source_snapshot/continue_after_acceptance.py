"""Wait for all three individual recording gates; then continue authorized queue."""
import json,subprocess,time
from common import *
def main():
 while True:
  queue=json.loads((ROOT/'state/queue.json').read_text())
  if queue.get('stop_reason'):
   print('STOP',json.dumps(queue['stop_reason'],ensure_ascii=False),flush=True);return
  gates=[ROOT/'runs'/BATCH/t/'attempt-01/audit.json' for t in queue['acceptance_tasks']]
  if queue.get('updated_at') and all(p.exists() and json.loads(p.read_text()).get('passed') for p in gates):break
  time.sleep(2)
 check=subprocess.run([str(PYTHON),str(ROOT/'tools/audit.py'),'--acceptance'])
 if check.returncode:print('Acceptance failed; no dispatch',flush=True);return
 print('Three acceptance gates passed; continuing authorized remaining tasks',flush=True)
 subprocess.run([str(PYTHON),str(ROOT/'tools/run.py'),'--continue-full'],check=True)
if __name__=='__main__':main()
