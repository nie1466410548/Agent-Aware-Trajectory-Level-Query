"""Descriptive trajectory characterization, conservative reuse witnesses, FAD audit."""
import collections
import itertools
import json
from pathlib import Path
import re
import statistics
import sqlglot
from sqlglot import exp

ROOT=Path(__file__).resolve().parents[1]
def normalized(e):
    if e is None:return None
    return e.sql(normalize=True,pretty=False)
def clean(s):return str(s).strip('`" ').lower().split('.')[-1]
def simple_ranges(tree):
    out={}
    where=tree.args.get('where') if isinstance(tree,exp.Select) else None
    if not where:return out
    def conjuncts(e):return conjuncts(e.this)+conjuncts(e.expression) if isinstance(e,exp.And) else [e]
    def literal(e):
        if isinstance(e,exp.Cast):e=e.this
        if not isinstance(e,exp.Literal):return None
        try:return ('text',e.this) if e.is_string else ('number',float(e.this))
        except ValueError:return None
    for e in conjuncts(where.this):
        col=e.this
        if not isinstance(col,exp.Column):continue
        name=clean(col.name)
        parts=[]
        if isinstance(e,exp.Between):parts=[('lo',literal(e.args['low']),True),('hi',literal(e.args['high']),True)]
        else:
            for cls,side,inclusive in [(exp.GTE,'lo',True),(exp.GT,'lo',False),(exp.LTE,'hi',True),(exp.LT,'hi',False),(exp.EQ,'both',True)]:
                if isinstance(e,cls):parts=[(side,literal(e.expression),inclusive)];break
        for side,value,inc in parts:
            if value is None:continue
            typ,v=value
            r=out.setdefault(name,{'type':typ,'lo':None,'hi':None})
            if r['type']!=typ:continue
            for s in (['lo','hi'] if side=='both' else [side]):
                prev=r[s]
                if prev is None or (s=='lo' and v>prev[0]) or (s=='hi' and v<prev[0]):r[s]=[v,inc]
                elif v==prev[0]:r[s]=[v,inc and prev[1]]
    return out
def compare_ranges(p,q):
    compared=[]
    for name in set(p)&set(q):
        a,b=p[name],q[name]
        if a['type']!=b['type']:continue
        disjoint=False
        for lo,hi in [(a['lo'],b['hi']),(b['lo'],a['hi'])]:
            if lo is not None and hi is not None:
                if lo[0]>hi[0] or (lo[0]==hi[0] and not(lo[1] and hi[1])):disjoint=True
        compared.append({'column':name,'relation':'disjoint' if disjoint else 'compatible_intervals','producer':a,'consumer':b})
    return compared
def features(call):
    f={'call_id':call['call_id'],'tool':call['tool'],'database':call['database'],'sql':call['sql'],
       'success':call['success'],'row_count':call.get('row_count'),'start_time':call['start_time'],
       'duration_ms':call['duration_ms'],'dialect':call['dialect'],'fad_id':call.get('fad_id'),
       'metadata':False,'parse_error':None,'tables':[],'columns':[],'operations':[],
       'filters':[],'joins':[],'aggregates':[]}
    try:
        tree=sqlglot.parse_one(call['sql'],read=call['dialect'])
        f['canonical']=normalized(tree)
        f['simple_ranges']=simple_ranges(tree)
        ctes={x.alias_or_name.lower() for x in tree.find_all(exp.CTE)}
        tables={clean(t.name) for t in tree.find_all(exp.Table) if clean(t.name) not in ctes}
        f['tables']=sorted(tables)
        f['metadata']=bool(re.match(r'\s*(pragma|show|describe|explain)\b',call['sql'],re.I) or re.search(r'\b(information_schema|sqlite_master|pg_catalog)\b',call['sql'],re.I))
        f['columns']=sorted({clean(c.name) for c in tree.find_all(exp.Column)})
        ops={'scan'} if tables else set()
        for kind,op in [(exp.Where,'filter'),(exp.Join,'join'),(exp.Group,'aggregate'),(exp.AggFunc,'aggregate'),(exp.Order,'sort'),(exp.Limit,'limit')]:
            if tree.find(kind):ops.add(op)
        if f['metadata']:ops={'metadata'}
        f['operations']=sorted(ops)
        f['filters']=sorted({normalized(w.this) for w in tree.find_all(exp.Where)})
        f['joins']=sorted({normalized(j) for j in tree.find_all(exp.Join)})
        f['aggregates']=sorted({normalized(a) for a in tree.find_all(exp.AggFunc)})
        # Sufficient syntactic condition for a complete, unfiltered base-row materialization.
        simple=isinstance(tree,exp.Select) and len(tables)==1 and len(list(tree.find_all(exp.Select)))==1
        simple=bool(simple and not any(tree.find(x) for x in [exp.Join,exp.AggFunc,exp.Group,exp.Distinct,exp.Window]))
        f['simple_single_table']=simple
        f['producer_full_rows']=bool(simple and tree.args.get('where') is None and tree.args.get('limit') is None and tree.args.get('offset') is None)
        f['producer_complete_selection']=bool(simple and tree.args.get('limit') is None and tree.args.get('offset') is None)
        f['where_conjuncts']=sorted(condition_atoms(tree.args['where'].this.sql(),call['dialect'])) if tree.args.get('where') else []
        f['star_projection']=any(isinstance(e,exp.Star) for e in tree.expressions)
        f['projected_base_columns']=sorted({clean(e.name) for e in tree.expressions if isinstance(e,exp.Column)})
        f['limit']=normalized(tree.args.get('limit'))
    except Exception as e:f['parse_error']=str(e)
    return f

def sql_pairs(queries):
    pairs=[]
    for i,q in enumerate(queries):
        for j in range(i):
            p=queries[j]
            if p['database']!=q['database'] or not(p['success'] and q['success']):continue
            shared=set(p['tables'])&set(q['tables'])
            if not shared:continue
            exact=bool(p.get('canonical') and p.get('canonical')==q.get('canonical'))
            witnesses=[]
            if exact:witnesses.append('same_canonical_query')
            if p.get('producer_full_rows') and q.get('simple_single_table') and not q.get('limit') and p['tables']==q['tables']:
                if p.get('star_projection') or (not q.get('star_projection') and set(q['columns'])<=set(p.get('projected_base_columns',[]))):
                    witnesses.append('earlier_full_base_rows_cover_later_single_table_query')
            if p.get('producer_complete_selection') and p.get('where_conjuncts') and q.get('simple_single_table') and not q.get('limit') and p['tables']==q['tables']:
                if set(p['where_conjuncts'])<=set(q.get('where_conjuncts',[])):
                    if p.get('star_projection') or (not q.get('star_projection') and set(q['columns'])<=set(p.get('projected_base_columns',[]))):
                        witnesses.append('earlier_selection_covers_later_added_conjuncts')
            pairs.append({'producer':p['call_id'],'consumer':q['call_id'],'producer_index':j+1,'consumer_index':i+1,
                'shared_tables':sorted(shared),'shared_columns':sorted(set(p['columns'])&set(q['columns'])),
                'same_filters':sorted(set(p['filters'])&set(q['filters'])),
                'shared_joins':sorted(set(p['joins'])&set(q['joins'])),
                'shared_aggregates':sorted(set(p['aggregates'])&set(q['aggregates'])),
                'range_comparisons':compare_ranges(p.get('simple_ranges',{}),q.get('simple_ranges',{})) if p['tables']==q['tables'] and len(p['tables'])==1 else [],
                'reuse_witnesses':witnesses,'producer_rows':p['row_count'],'consumer_rows':q['row_count'],
                'producer_sql':p['sql'],'consumer_sql':q['sql']})
    return pairs

def atoms(q):return {(q['database'],t) for t in q['tables']}
def fad_atoms(accesses):return {(a['database'],clean(t)) for a in accesses for t in a.get('tables',[]) if clean(t) not in ['*','unknown','?']}
def ratio(n,d):return n/d if d else None
def condition_atoms(text,dialect):
    try:
        tree=sqlglot.parse_one(text,read=dialect)
        for c in tree.find_all(exp.Column):c.set('table',None)
        def split(e):
            if isinstance(e,exp.And):return split(e.this)+split(e.expression)
            return [normalized(e)]
        return set(split(tree))
    except Exception:return {'UNPARSED:'+text}
def audit(run):
    messages=[]
    for s in (run/'kimi.jsonl').read_text().splitlines():
        try:messages.append(json.loads(s))
        except json.JSONDecodeError:pass
    receipts={};mapping={};generation={};flags=[];assistant_turn=0;fad_gen_turn={};last_fad_response=-1
    for idx,m in enumerate(messages):
        if m.get('role')=='assistant':
            assistant_turn+=1
            for tc in m.get('tool_calls',[]):
                f=tc.get('function',{})
                try:a=json.loads(f.get('arguments','{}'))
                except Exception:continue
                cmd=a.get('command','')
                mapping[tc['id']]={'message_index':idx,'assistant_turn':assistant_turn,'name':f.get('name'),'args':a}
                if re.search(r'tool\.py\s+fad\b',cmd):fad_gen_turn[tc['id']]=assistant_turn
                if f.get('name') in ['Write','Edit']:
                    content=str(a.get('content',a.get('new_string','')))
                    if re.search(r'\b(SELECT|WITH|PRAGMA|SHOW|DESCRIBE)\b',content,re.I):generation[idx]=content
                if cmd and not re.search(r'tool\.py\s+(query-db|list-db|fad|python|answer)\b',cmd):
                    flags.append({'kind':'non_adapter_bash_review','index':idx,'command':cmd})
        if m.get('role')=='tool':
            try:
                o=json.loads(m.get('content','').strip()); data=json.loads(o.get('preview','{}'))
            except (ValueError,TypeError):continue
            if isinstance(data,dict) and 'fad_id' in data:
                receipts[data['fad_id']]={'response_index':idx,'response_turn':assistant_turn}
            if isinstance(o,dict) and 'call_id' in o:
                mapping[o['call_id']]=mapping.get(m.get('tool_call_id'),{})
    details={}
    log=run/'tool_calls.jsonl'
    calls=[json.loads(s) for s in log.read_text().splitlines()] if log.exists() else []
    for c in calls:
        if c['tool']!='query-db' or not c.get('fad_id'):continue
        r=receipts.get(c['fad_id']);issued=mapping.get(c['call_id'],{})
        if not issued:
            candidates=[v for v in mapping.values() if 'query-db' in v.get('args',{}).get('command','') and c['fad_id'] in v.get('args',{}).get('command','')]
            if candidates:issued=min(candidates,key=lambda v:v['message_index'])
        ordered=bool(r and issued.get('message_index',-1)>r['response_index'] and issued.get('assistant_turn',-1)>r['response_turn'])
        # Look for the exact SQL emitted in an earlier visible assistant tool argument.
        early=[]
        if r:
            needle=' '.join(c.get('sql','').split())
            for tc in mapping.values():
                if tc.get('message_index',10**9)<=r['response_index']:
                    text=json.dumps(tc.get('args',{}),ensure_ascii=False)
                    try: text=' '.join(str(v) for v in tc.get('args',{}).values())
                    except Exception:pass
                    if needle and needle in ' '.join(text.split()):early.append(tc['message_index'])
        details[c['call_id']]={'separate_assistant_turn':ordered,'exact_sql_seen_before_fad_response':bool(early),'early_indices':sorted(set(early))}
    return {'assistant_turns':assistant_turn,'sql_order_checks':details,'review_flags':flags}

def analyze_run(run):
    meta=json.loads((run/'task_meta.json').read_text())
    calls=[json.loads(s) for s in (run/'tool_calls.jsonl').read_text().splitlines()] if (run/'tool_calls.jsonl').exists() else []
    calls.sort(key=lambda c:c['start_time'])
    sqls=[features(c) for c in calls if 'sql' in c]
    data=[q for q in sqls if not q['metadata']]
    pairs=sql_pairs(data)
    report_path=ROOT/'reports'/f'{meta["group"]}-{meta["task_id"].replace("/","-")}-{meta["run_id"]}.json'
    if report_path.exists():
        sql_dir=run/'sql';sql_dir.mkdir(exist_ok=True)
        for i,q in enumerate(sqls,1):(sql_dir/f'{i:03d}-{q["call_id"]}.sql').write_text(q['sql']+'\n')
    audit_result=audit(run)
    fads=[c for c in calls if c['tool']=='fad' and c['success']]
    fad_details=[]
    for f in fads:
        future=[q for q in sqls if q['tool']=='query-db' and q['start_time']>f['end_time']]
        accesses=f['frontier']['accesses'];pred=fad_atoms(accesses)
        row={'call_id':f['call_id'],'accesses':accesses,'predicted_table_atoms':sorted(pred),'empty':not bool(accesses),
             'future_calls':[q['call_id'] for q in future[:3]],'targets_metadata':bool(future and future[0]['metadata']),
             'has_next_query':bool(future),'next_success':bool(future and future[0]['success'])}
        later_accesses=[a for a in accesses if str(a.get('horizon','1')) in ['2','3']]
        lp=fad_atoms(later_accesses)
        la=set().union(*(atoms(q) for q in future[1:3])) if len(future)>1 else set()
        row['later_prediction_atoms']=sorted(lp)
        row['later_table_precision']=ratio(len(lp&la),len(lp))
        row['later_table_recall']=ratio(len(lp&la),len(la)) if lp else None
        row['later_has_consumer']=len(future)>1
        for h in [1,3]:
            actual=set().union(*(atoms(q) for q in future[:h])) if future else set()
            row[f'table_precision_{h}']=ratio(len(pred&actual),len(pred))
            row[f'table_recall_{h}']=ratio(len(pred&actual),len(actual))
            row[f'unrealized_table_atoms_{h}']=sorted(pred-actual)
        if future:
            q=future[0]
            immediate=[a for a in accesses if str(a.get('horizon',1))=='1']
            ip=fad_atoms(immediate)
            row['immediate_table_precision']=ratio(len(ip&atoms(q)),len(ip))
            row['immediate_table_recall']=ratio(len(ip&atoms(q)),len(atoms(q)))
            relevant=[a for a in immediate if a['database']==q['database'] and (not a['tables'] or set(map(clean,a['tables']))&set(q['tables']))]
            pc={clean(c) for a in relevant for c in a['columns']}
            po={clean(o) for a in relevant for o in a['operations']}
            row['column_precision_1']=ratio(len(pc&set(q['columns'])),len(pc))
            row['operation_precision_1']=ratio(len(po&set(q['operations'])),len(po))
            row['column_recall_1']=ratio(len(pc&set(q['columns'])),len(q['columns']))
            row['operation_recall_1']=ratio(len(po&set(q['operations'])),len(q['operations']))
            pf=set().union(*(condition_atoms(s,q['dialect']) for a in relevant for s in a['filters'])) if relevant else set()
            af=set().union(*(condition_atoms(s,q['dialect']) for s in q['filters']))
            row['filter_exact_precision_1']=ratio(len(pf&af),len(pf))
            row['filter_exact_recall_1']=ratio(len(pf&af),len(af))
            row['predicted_filter_atoms']=sorted(pf)
            row['actual_filter_atoms']=sorted(af)
            row['lead_s']=q['start_time']-f['end_time']
            history=[p for p in data if p['start_time']<f['start_time']]
            hp=atoms(history[-1]) if history else set()
            row['last_query_table_recall_1']=ratio(len(hp&atoms(q)),len(atoms(q)))
            row['last_query_table_precision_1']=ratio(len(hp&atoms(q)),len(hp))
        fad_details.append(row)
    report_path=ROOT/'reports'/f'{meta["group"]}-{meta["task_id"].replace("/","-")}-{meta["run_id"]}.json'
    base=json.loads(report_path.read_text()) if report_path.exists() else meta
    base.update(data_queries=len(data),metadata_queries=sum(q['metadata'] for q in sqls),
        sql_parse_failures=sum(bool(q['parse_error']) for q in sqls),
        successful_data_queries=sum(q['success'] for q in data),
        failed_data_queries=sum(not q['success'] for q in data),
        empty_successful_data_queries=sum(q['success'] and q['row_count']==0 for q in data),
        later_queries_sharing_tables=len({p['consumer'] for p in pairs}),
        later_queries_sharing_table_columns=len({p['consumer'] for p in pairs if p['shared_columns']}),
        later_queries_with_reuse_witness=len({p['consumer'] for p in pairs if p['reuse_witnesses']}),
        exact_repeat_consumers=len({p['consumer'] for p in pairs if 'same_canonical_query' in p['reuse_witnesses']}),
        shared_filter_consumers=len({p['consumer'] for p in pairs if p['same_filters']}),
        shared_join_consumers=len({p['consumer'] for p in pairs if p['shared_joins']}),
        shared_aggregate_consumers=len({p['consumer'] for p in pairs if p['shared_aggregates']}),
        data_query_adapter_ms=sum(q['duration_ms'] for q in data),
        fad_submissions=len(fads),python_calls=sum(c['tool']=='python' for c in calls),
        assistant_turns=audit_result['assistant_turns'])
    result={'summary':base,'queries':sqls,'pairs':pairs,'fads':fad_details,'audit':audit_result}
    if report_path.exists():(run/'analysis.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    return result

def main():
    all_runs=[]
    for meta in sorted((ROOT/'runs').glob('*/*/query*/quick-01/task_meta.json')):
        all_runs.append(analyze_run(meta.parent))
    groups={}
    for g in ['natural','fad']:
        rs=[r for r in all_runs if r['summary']['group']==g]
        summaries=[r['summary'] for r in rs]
        all_fs=[f for r in rs for f in r['fads']]
        fs=[f for f in all_fs if f['has_next_query'] and not f['targets_metadata']]
        stats={'runs':len(rs),'completed':sum('exit_code' in r for r in summaries),
               'passed':sum(r.get('validator_passed',False) for r in summaries)}
        for key in ['data_queries','metadata_queries','failed_data_queries','empty_successful_data_queries','later_queries_sharing_tables','later_queries_sharing_table_columns','later_queries_with_reuse_witness','exact_repeat_consumers','shared_filter_consumers','shared_join_consumers','shared_aggregate_consumers','fad_submissions','python_calls','assistant_turns','data_query_adapter_ms']:
            stats[key]=sum(r[key] for r in summaries)
        for key in ['table_precision_1','table_recall_1','table_precision_3','table_recall_3','immediate_table_precision','immediate_table_recall','column_precision_1','column_recall_1','operation_precision_1','operation_recall_1','filter_exact_precision_1','filter_exact_recall_1','last_query_table_recall_1','later_table_precision','later_table_recall']:
            values=[f[key] for f in fs if f.get(key) is not None]
            stats[key]={'mean':statistics.mean(values) if values else None,'n':len(values)}
        leads=[f['lead_s'] for f in fs if 'lead_s' in f]
        stats['lead_s_median']=statistics.median(leads) if leads else None
        stats['lead_s_min']=min(leads) if leads else None
        stats['lead_s_max']=max(leads) if leads else None
        stats['multi_access_frontiers']=sum(len(f['accesses'])>1 for f in fs)
        stats['scored_data_frontiers']=len(fs)
        stats['empty_data_frontiers']=sum(f['empty'] for f in fs)
        stats['metadata_frontiers']=sum(f['targets_metadata'] for f in all_fs)
        stats['frontiers_without_next_query']=sum(not f['has_next_query'] for f in all_fs)
        stats['frontiers_followed_by_failed_query']=sum(not f['next_success'] for f in fs)
        stats['frontiers_with_later_predictions']=sum(bool(f['later_prediction_atoms']) for f in fs)
        checks=[c for r in rs for c in r['audit']['sql_order_checks'].values()]
        stats['fad_order_checked']=len(checks)
        stats['fad_separate_turn_passed']=sum(c['separate_assistant_turn'] for c in checks)
        stats['sql_early_emission_flags']=sum(c['exact_sql_seen_before_fad_response'] for c in checks)
        groups[g]=stats
    (ROOT/'reports/analysis.json').write_text(json.dumps({'groups':groups,'runs':[r['summary'] for r in all_runs]},indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(groups,indent=2))
if __name__=='__main__':main()
