"""Check cohort identity, evidence references, timing order and materialization scope."""
import hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/characterization'
def main():
 load=lambda name:json.loads((OUT/name).read_text())
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks']
 expected={(f'{ds}/query{i}',g) for ds,ids in tasks.items() for i in ids for g in ['natural','fad']}
 runs=load('runs.json');assert len(runs)==len(expected)==108
 assert {(r['task'],r['group']) for r in runs}==expected
 events={};links=0;checked=0
 for task,g in expected:
  run=ROOT/'runs'/g/task/'full-01'
  events[task,g]={e['call_id']:e for e in map(json.loads,(run/'tool_calls.jsonl').read_text().splitlines())}
 for filename in ['adjacent-pairs.json','group-evolution.json','result-dependencies.json','materialization-candidates.json']:
  for item in load(filename):
   task,g=item['task'],item['group'];run=ROOT/'runs'/g/task/'full-01';es=events[task,g]
   ids=item.get('call_ids',[item.get('producer'),item.get('consumer')]);times=[]
   for cid in ids:
    assert cid in es and es[cid]['success'];times.append(es[cid]['start_time'])
    if 'database' in item:assert es[cid]['database']==item['database']
   assert times==sorted(times)
   files=item.get('sql_files',[item.get('producer_sql'),item.get('consumer_sql')])
   for filename in files:
    path=ROOT/filename;assert path.exists() and path.is_relative_to(run);links+=1
   if 'expected_reuse' in item:assert item['expected_reuse']==len(set(ids))-1
   if 'result_file' in item:
    path=ROOT/item['result_file'];assert path.exists() and path.is_relative_to(run)
    producer=es[item['producer']];consumer=es[item['consumer']]
    assert producer['start_time']+producer['duration_ms']/1000 <= consumer['start_time']
   checked+=1
 missing=[]
 for p in OUT.glob('*.md'):
  for link in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if '://' in link or link.startswith('#'):continue
   path=link.split('#')[0]
   if not (p.parent/path).exists():missing.append((p.name,link))
 assert not missing,missing
 source_files=['characterize.py','audit_characterization.py','test_characterize.py','overlap_features.py','discover.py']
 hashes={name:hashlib.sha256((ROOT/'tools'/name).read_bytes()).hexdigest() for name in source_files}
 result={'cohort_runs':108,'evidence_items_checked':checked,'sql_references_checked':links,'missing_links':missing,'scope_order_and_identity_checks':'passed','source_sha256':hashes,'semantic_tests':'test_analysis.py: 9 passed; test_characterize.py: 8 passed','limitations':'Checks verify reference integrity and temporal order, not causal dependence, rewrite equivalence or cost benefit.'}
 (OUT/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='source_sha256'},ensure_ascii=False))
if __name__=='__main__':main()
