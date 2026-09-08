"""Refresh completed-episode analysis while the batch is alive; no unfinished traces."""
import json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 seen=-1
 while True:
  files=list((ROOT/'reports').glob('natural-*-full-01.json'))+list((ROOT/'reports').glob('fad-*-full-01.json'))
  try:pid=json.loads((ROOT/'reports/batch-process.json').read_text())['pid'];os.kill(pid,0);alive=True
  except (FileNotFoundError,ProcessLookupError):alive=False
  if len(files)!=seen or not alive:
   ok=True
   for script in ['analyze.py','structural.py','discover.py','report.py']:
    with (ROOT/'reports'/('refresh-'+script+'.log')).open('w') as log:
     p=subprocess.run([sys.executable,str(ROOT/'tools'/script)],stdout=log,stderr=subprocess.STDOUT)
    if p.returncode:ok=False;print('REFRESH ERROR',script,flush=True);break
   if ok:seen=len(files);print('REFRESHED',seen,flush=True)
  if not alive:break
  time.sleep(30)
if __name__=='__main__':main()
