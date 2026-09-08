"""Pinned, resumable preparation of official DAB core; scope can include extras."""
import argparse,concurrent.futures,hashlib,json,os,re,shutil,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='b24c8f5586121d4d2f8a5a793ebac530858dd1ab'
BASE=f'https://raw.githubusercontent.com/ucbepic/DataAgentBench/{REV}/'
CORE=['agnews','bookreview','crmarenapro','DEPS_DEV_V1','GITHUB_REPOS','googlelocal','music_brainz_20k','PANCANCER_ATLAS','PATENTS','stockindex','stockmarket','yelp']
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--scope',choices=['core','all'],default='core');a=ap.parse_args()
 tree=json.loads((ROOT/'reports/upstream-tree.json').read_text())['tree'];configs=json.loads((ROOT/'reports/upstream-configs.json').read_text())
 tasks={}
 for x in tree:
  m=re.fullmatch(r'query_(.+)/query(\d+)/query.json',x['path'])
  if m and (a.scope=='all' or m[1] in CORE):tasks.setdefault(m[1],[]).append(int(m[2]))
 tasks={k:sorted(v) for k,v in sorted(tasks.items())}
 hashes={p:(h,int(n)) for p,h,n in (line.split('\t') for line in configs['dataset_manifest.tsv'].splitlines())}
 paths={x['path'] for x in tree if x['type']=='blob' and any(x['path'].startswith(f'query_{d}/') for d in tasks) and ('/query_dataset/' in x['path'] or re.search(r'/query\d+/',x['path']) or x['path'].endswith(('db_config.yaml','db_description.txt')))}
 paths|={x['path'] for x in tree if x['type']=='blob' and x['path'].startswith('common_scaffold/validate/')}
 paths|={p for p in hashes if p.split('/')[0][6:] in tasks}
 # Fetch query metadata first; never provide gold/validator assets to agent prompts.
 paths=sorted(paths,key=lambda p:('/query_dataset/' in p,hashes.get(p,('',0))[1]))
 (ROOT/'tasks.json').write_text(json.dumps({'commit':REV,'scope':a.scope,'tasks':tasks,'task_count':sum(map(len,tasks.values())),'groups':['natural','fad'],'run_id':'full-01','hashes':{p:hashes[p] for p in paths if p in hashes}},indent=2)+'\n')
 print('TASKS',sum(map(len,tasks.values())),'FILES',len(paths),flush=True)
 def download(p):
  target=ROOT/'upstream'/p;expected=hashes.get(p)
  if target.exists() and (not expected or target.stat().st_size==expected[1] and digest(target)==expected[0]):return
  target.parent.mkdir(parents=True,exist_ok=True)
  old=ROOT.parent/'quickcheck/upstream'/p
  if old.exists() and (not expected or digest(old)==expected[0]):shutil.copyfile(old,target);return
  # Prefer pinned GitHub for small files; HF hosts external/large LFS payloads.
  urls=[BASE+p,f'https://media.githubusercontent.com/media/ucbepic/DataAgentBench/{REV}/{p}',f'https://huggingface.co/datasets/ruiyingm/DataAgentBench-data/resolve/main/{p}?download=true']
  if expected and expected[1]>50_000_000:urls=urls[1:]+urls[:1]
  errors=[]
  for attempt in range(2):
   for url in urls:
    temp=target.with_name(target.name+'.partial')
    try:
     h=hashlib.sha256();size=0
     with urllib.request.urlopen(url,timeout=60) as src,temp.open('wb') as dst:
      for chunk in iter(lambda:src.read(4*1024*1024),b''):
       dst.write(chunk);h.update(chunk);size+=len(chunk)
     if size<1024 and temp.read_bytes().startswith(b'version https://git-lfs'):raise ValueError('LFS pointer')
     if expected and (size!=expected[1] or h.hexdigest()!=expected[0]):raise ValueError('hash/size mismatch')
     os.replace(temp,target);print('READY',p,size,flush=True);return
    except Exception as exc:errors.append(type(exc).__name__+': '+str(exc))
  raise RuntimeError(p+' '+str(errors))
 with concurrent.futures.ThreadPoolExecutor(6) as pool:
  futs={pool.submit(download,p):p for p in paths};errors=[]
  for f in concurrent.futures.as_completed(futs):
   try:f.result()
   except Exception as e:errors.append(str(e));print('FAILED',e,flush=True)
 (ROOT/'reports/preparation.json').write_text(json.dumps({'scope':a.scope,'files':paths,'errors':errors,'complete':not errors},indent=2)+'\n')
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
