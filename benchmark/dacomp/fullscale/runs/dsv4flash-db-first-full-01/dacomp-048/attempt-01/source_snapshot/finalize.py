"""Offline final delivery after queue completion or service stop. No model calls.
Keeps selected candidates fixed; enriches early verification records with SQL
journals, then performs the predeclared representative performance experiment.
"""
import hashlib,json,subprocess,time,os,re
from common import *
from opportunities import verify

def command(name):
 subprocess.run([str(PYTHON),str(ROOT/'tools'/name)],check=True)

def main():
 queue=json.loads((ROOT/'state/queue.json').read_text())
 assert not any(v['status']=='running' for v in queue['tasks'].values()),'Wait for active task to stop before final offline performance'
 command('report.py')
 sources=list((ROOT/'tools').glob('*.py'));version=hashlib.sha256(''.join(sha(p) for p in sorted(sources)).encode()).hexdigest();target=REPORT/'code_versions'/version;target.mkdir(parents=True,exist_ok=True)
 for p in sources:(target/p.name).write_bytes(p.read_bytes())
 dump(target/'manifest.json',{'phase':'final_offline_validation','version':version,'files':{p.name:sha(p) for p in sources}})
 entries={r['task_id']:r for r in records(ROOT/'manifests/tasks.jsonl')};profiles=records(REPORT/'sql_profile.jsonl')
 for tid in queue['order']:
  cache=REPORT/'tasks'/f'{tid}.analysis.json'
  if not cache.exists():continue
  data=json.loads(cache.read_text());candidates=data['candidates'];selected=[c for c in candidates if c['status'] not in ['pending','not_verified_cap']]
  assert len(selected)<=3,'Unique representative candidate cap'
  if all(c.get('phase')=='offline_validation' for c in selected):continue
  initial=cache.with_name(tid+'.analysis.initial.json')
  if not initial.exists():initial.write_bytes(cache.read_bytes())
  queries=[q for q in profiles if q['task_id']==tid and q['category']=='data' and q['status']=='success'];run=ROOT/'runs'/BATCH/tid/'attempt-01'
  for c in selected:
   if c.get('phase')=='offline_validation':continue
   initial_status=c['status'];verify(c,queries,run,entries[tid]['database_path'])
   c.update(initial_validation_status=initial_status,verification_source_version=version,additional_replay_reason='Same preselected candidate, repeated only to enrich phase-separated offline SQL evidence; no model invocation or candidate reselection.')
  data.update(candidates=candidates,final_verification_source_version=version);dump(cache,data)
  print('Enriched offline evidence',tid,flush=True)
 command('report.py');command('performance.py');command('dependencies.py');command('pairs.py');command('audit.py');command('report.py')
 # Audit only the reading reports; preserve any broken original agent links as
 # original evidence and record normalization in answers/*.links.json.
 broken=[]
 for path in REPORT.rglob('*.md'):
  for match in re.finditer(r'!?\[[^\]]*\]\(([^\n)]+)\)',path.read_text()):
   link=match.group(1).strip().strip('<>')
   if link.startswith(('http:','https:','mailto:','data:','#')):continue
   dest=link.split('#')[0]
   if dest and not (path.parent/dest).exists():broken.append({'file':str(path.relative_to(REPORT)),'link':link})
 dump(REPORT/'link_audit.json',{'broken_local_links':broken,'scope':'Generated workload reports and normalized answer copies; raw agent answers preserved separately.'})
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or p.is_relative_to(ROOT/'runtime') or '__pycache__' in p.parts or p.suffix in ['.part','.pyc'] or p.name=='evidence_index.json':continue
  files.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)})
 dump(REPORT/'evidence_index.json',{'generated_at':time.time(),'files':files,'databases':'Original databases are separately verified by manifests/remote-hash-check.json and per-task post-run hashes; downloaded DBs excluded from this index.'})
 print('Final evidence files',len(files),'broken reading links',len(broken),flush=True)
if __name__=='__main__':main()
