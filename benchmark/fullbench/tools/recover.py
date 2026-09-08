"""Run explicitly recorded instrumentation recoveries after the live main batch ends."""
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 pid=json.loads((ROOT/'reports/batch-process.json').read_text())['pid']
 while True:
  try:os.kill(pid,0)
  except ProcessLookupError:break
  time.sleep(30)
 for p in sorted((ROOT/'reports/incidents').glob('*.json')):
  incident=json.loads(p.read_text())
  if not incident.get('recovery_required'):continue
  if p.stem!='natural-crmarenapro-query7':raise RuntimeError('Unspecified recovery: '+p.stem)
  report=ROOT/'reports/natural-crmarenapro-query7-full-01.json'
  if not report.exists():
   with (ROOT/'reports/recovery-natural-crmarenapro-query7.log').open('w') as log:
    result=subprocess.run([sys.executable,str(ROOT/'tools/run_task.py'),'crmarenapro','7','natural'],stdout=log,stderr=subprocess.STDOUT)
   if not report.exists():raise RuntimeError('Recovery did not produce terminal report')
  outcome=json.loads(report.read_text());outcome['instrumentation_recovery_of']=incident['archive'];report.write_text(json.dumps(outcome,indent=2)+'\n')
  incident.update(recovery_required=False,recovered_at=time.time(),primary_report=str(report),recovery_validator_passed=outcome['validator_passed'])
  p.write_text(json.dumps(incident,indent=2)+'\n')
 for script in ['analyze.py','structural.py','discover.py','report.py','audit_artifacts.py']:
  subprocess.run([sys.executable,str(ROOT/'tools'/script)],check=True)
 print('RECOVERIES FINISHED',flush=True)
if __name__=='__main__':main()
