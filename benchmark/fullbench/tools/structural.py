"""Task-local structural comparison, with explicit partial-analysis coverage."""
import itertools,json
from pathlib import Path
import overlap_features as f
ROOT=Path(__file__).resolve().parents[1]

def main():
 runs=[]
 for path in sorted((ROOT/'runs').glob('*/*/*/full-01/analysis.json')):
  a=json.loads(path.read_text());summary=a['summary'];ds=summary['task_id'].split('/')[0]
  qs=[];errors=[]
  for q in a['queries']:
   if not q['success'] or q['metadata']:continue
   try:qs.append(f.enrich(q,ds,path.parent))
   except Exception as e:errors.append({'call_id':q['call_id'],'error':type(e).__name__+': '+str(e),'sql':q['sql']})
  old={(p['producer'],p['consumer']):p for p in a['pairs']};pairs=[];eligible=0
  for p,q in itertools.combinations(qs,2):
   if p['database']!=q['database']:continue
   eligible+=1
   if not(set(p['tables'])&set(q['tables'])):continue
   prior=old.get((p['call_id'],q['call_id']),{})
   hit=f.hits(p,q,prior)
   pairs.append({'producer':p['call_id'],'consumer':q['call_id'],'database':q['database'],
     'metrics':[k for k,v in hit.items() if v],
     'shared_tables':sorted(set(p['tables'])&set(q['tables'])),
     'shared_bound_columns':sorted(set(map(tuple,p['bound_columns']))&set(map(tuple,q['bound_columns']))),
     'shared_filter_atoms':sorted(set(p['filter_atoms'])&set(q['filter_atoms'])),
     'shared_joins':sorted(set(p['bound_joins'])&set(q['bound_joins']))})
  runs.append({'task':summary['task_id'],'group':summary['group'],'passed':summary['validator_passed'],
    'successful':summary['successful_data_queries'],'attempted':summary['data_queries'],
    'eligible_pairs':eligible,'analyzed_queries':len(qs),'errors':errors,'pairs':pairs,
    'queries':[{k:v for k,v in q.items() if k!='output_rows'} for q in qs],
    'summary':summary,'analysis_path':str(path.relative_to(ROOT))})
 result={'definitions':f.LABELS,'runs':runs}
 (ROOT/'reports/overlap-detail.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print('Structural runs',len(runs),'unresolved',sum(len(r['errors']) for r in runs))
if __name__=='__main__':main()
