"""All within-trajectory query pairs. Structural signals never imply reuse."""
import collections,json
from common import *
def main():
 groups=collections.defaultdict(list)
 for q in records(REPORT/'sql_profile.jsonl'):
  if q['category']=='data' and q['status']=='success':groups[q['task_id']].append(q)
 summaries=[];out=REPORT/'query_pairs.jsonl'
 with out.open('w') as f:
  for tid,qs in groups.items():
   counts=collections.Counter();pairs=0;parsed_pairs=0
   def features(q):
    p=q['profile'];cols=set();predicates=set();joins=set();group=set();aggs=set()
    for b in p.get('blocks',[]):
     for reference in b.get('column_references',[]): cols.update(json.dumps(c,sort_keys=True,ensure_ascii=False) for c in reference['lineage'] if 'unknown' not in c)
     for g in b['group_by']:
      group.add(g['expression']);cols.update(json.dumps(c,sort_keys=True,ensure_ascii=False) for c in g['columns'] if 'unknown' not in c)
     for a in b['aggregates']:
      aggs.add(a['expression']);cols.update(json.dumps(c,sort_keys=True,ensure_ascii=False) for c in a['metric_columns']+a['condition_columns'] if 'unknown' not in c)
     for term in b['filters']:
      predicates.add(term['kind']+':'+term['expression']);cols.update(json.dumps(c,sort_keys=True,ensure_ascii=False) for c in term['columns'] if 'unknown' not in c)
     for j in b['joins']:joins.add(json.dumps(j,ensure_ascii=False,sort_keys=True))
    return {'tables':set(p.get('base_tables') or []),'resolved_columns':cols,'complete_predicates':predicates,'join_syntax':joins,'group_expressions':group,'aggregate_syntax':aggs}
   feats={q['sql_id']:features(q) for q in qs}
   for i,a in enumerate(qs):
    for j,b in enumerate(qs[i+1:],i+1):
     pairs+=1;row={'task_id':tid,'from':a['sql_id'],'to':b['sql_id'],'gap_data_queries':j-i-1,'adjacent':j==i+1,'parsed':a['profile'].get('parsed') and b['profile'].get('parsed'),'interpretation':'structural signal only; source/filter/grain/NULL compatibility not established'}
     if row['parsed']:
      parsed_pairs+=1;x,y=feats[a['sql_id']],feats[b['sql_id']]
      for key in x:row[key]=sorted(x[key]&y[key]);counts[key]+=bool(row[key])
      row['same_sql']=a['profile']['canonical_sql']==b['profile']['canonical_sql'] and a.get('parameters')==b.get('parameters');counts['same_sql']+=row['same_sql']
     f.write(json.dumps(row,ensure_ascii=False)+'\n')
   summaries.append({'task_id':tid,'success_data_sql':len(qs),'all_within_task_pairs':pairs,'parsed_pairs':parsed_pairs,**counts})
 dump(REPORT/'pair_summary.json',{'method':'All ordered earlier/later pairs within one task. Columns include resolved SELECT, JOIN, GROUP, aggregate, filter and schema-expanded wildcard references; unresolved columns are excluded and coverage is recorded in sql_profile. Predicates and joins are exact block syntax, without implication or alias equivalence. These are not validated optimization opportunities.','tasks':summaries})
 print('Within-task query pairs',sum(s['all_within_task_pairs'] for s in summaries))
if __name__=='__main__':main()
