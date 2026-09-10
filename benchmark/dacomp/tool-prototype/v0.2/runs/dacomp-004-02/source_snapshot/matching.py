"""Offline FAD-vs-later-SQL audit. Requires sqlglot; never queries an LLM.

SQLITE_READ supplies logical base-column references; SQLGlot scopes supply grouping,
simple aggregates, predicate atoms and equijoins. Unsupported expressions remain
explicit. Field matches are NOT full-query equivalence or correctness judgments.
"""
import argparse
import copy
import json
import sqlite3
from collections import Counter
from pathlib import Path

import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import Scope, traverse_scope

FIELDS=('columns','filters','joins','group_by','aggregations')

def records(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def key(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def literal(x):
    if isinstance(x,exp.Null):return None
    if isinstance(x,exp.Boolean):return bool(x.this)
    if isinstance(x,exp.Literal):return x.this if x.is_string else float(x.this)
    if isinstance(x,exp.Neg):return -literal(x.this)
    raise ValueError('non-literal')
def normvalue(v):
    if isinstance(v,bool) or v is None:return v
    if isinstance(v,(int,float)):return float(v)
    if isinstance(v,list):return [normvalue(x) for x in v]
    return v

def local_nodes(root):
    yield root
    for child in root.iter_expressions():
        if isinstance(child,(exp.Select,exp.Subquery,exp.Union)):continue
        yield from local_nodes(child)


def sql_features(sql,catalog):
    lookup={(t.casefold(),c.casefold()):t+'.'+c for t,cols in catalog.items() for c in cols}
    typed={t:{c:'UNKNOWN' for c in cols} for t,cols in catalog.items()}
    tree=qualify(sqlglot.parse_one(sql,read='sqlite'),dialect='sqlite',schema=typed,validate_qualify_columns=False)
    scopes=list(traverse_scope(tree)); unsupported=[]
    def deref(node,scope,depth=0):
        if depth>10:return node,scope
        if isinstance(node,exp.Paren):return deref(node.this,scope,depth+1)
        if not isinstance(node,exp.Column):return node,scope
        source=scope.sources.get(node.table)
        if isinstance(source,Scope):
            for selection in source.expression.selects:
                if selection.alias_or_name.casefold()==node.name.casefold():
                    return deref(selection.this if isinstance(selection,exp.Alias) else selection,source,depth+1)
        return node,scope
    def column(node,scope):
        node,scope=deref(node,scope)
        if not isinstance(node,exp.Column):return None
        source=scope.sources.get(node.table)
        if isinstance(source,exp.Table):return lookup.get((source.name.casefold(),node.name.casefold()))
        return None
    def group(node,scope):
        node,scope=deref(node,scope)
        c=column(node,scope)
        if c:return ('column',c)
        if isinstance(node,exp.TimeToStr):
            fmt=node.args.get('format');fmt=fmt.this if isinstance(fmt,exp.Literal) else None
            unit={'%Y':'year','%Y-%m':'month','%Y-%m-%d':'day'}.get(fmt)
            operand=node.this
            while isinstance(operand,(exp.Cast,exp.TsOrDsToTimestamp,exp.TsOrDsToDate)):
                operand=operand.this
            c=column(operand,scope)
            if c and unit:return ('time_bucket',c,unit)
        return ('unsupported',node.sql(dialect='sqlite'))
    def atom(node,scope):
        if isinstance(node,exp.Not) and isinstance(node.this,exp.Is) and isinstance(node.this.expression,exp.Null):
            c=column(node.this.this,scope)
            return ('predicate',c,'is_not_null',None) if c else None
        if isinstance(node,exp.Is) and isinstance(node.expression,exp.Null):
            c=column(node.this,scope)
            return ('predicate',c,'is_null',None) if c else None
        if isinstance(node,(exp.In,exp.Between)):
            c=column(node.this,scope)
            if not c:return None
            try:
                vals=[literal(v) for v in node.expressions] if isinstance(node,exp.In) else [literal(node.args['low']),literal(node.args['high'])]
                if isinstance(node,exp.In):vals=sorted(vals,key=key)
                return ('predicate',c,'in' if isinstance(node,exp.In) else 'between',vals)
            except (ValueError,TypeError):return None
        ops={exp.EQ:'eq',exp.NEQ:'ne',exp.LT:'lt',exp.LTE:'le',exp.GT:'gt',exp.GTE:'ge',exp.Like:'like'}
        op=ops.get(type(node))
        if op:
            c=column(node.this,scope)
            try:
                if c:return ('predicate',c,op,literal(node.expression))
                c=column(node.expression,scope)
                if c and op!='like':return ('predicate',c,{'lt':'gt','le':'ge','gt':'lt','ge':'le'}.get(op,op),literal(node.this))
            except (ValueError,TypeError):pass
        return None
    groups=[];aggregates=set();filters=set();joins=set();scope_rows=[]
    for scope in scopes:
        root=scope.expression
        if not isinstance(root,exp.Select):continue
        g=root.args.get('group')
        gs=sorted({key(group(v,scope)) for v in g.expressions}) if g else []
        if g:groups.append(gs)
        for token in gs:
            if json.loads(token)[0]=='unsupported':unsupported.append({'kind':'group_by','sql':json.loads(token)[1]})
        local_aggs=set()
        for node in local_nodes(root):
            if isinstance(node,exp.AggFunc):
                fn={exp.Sum:'sum',exp.Count:'count',exp.Avg:'avg',exp.Min:'min',exp.Max:'max'}.get(type(node))
                operand=node.this
                if isinstance(operand,exp.Distinct):
                    if fn=='count' and len(operand.expressions)==1:
                        fn='count_distinct';operand=operand.expressions[0]
                    else:fn=None
                c=column(operand,scope) if operand is not None else None
                if fn=='count' and (isinstance(operand,exp.Star) or isinstance(operand,exp.Literal) and operand.this is not None):c='*'
                if fn and c:local_aggs.add(key((fn,c)))
                else:unsupported.append({'kind':'aggregations','sql':node.sql(dialect='sqlite')})
        aggregates.update(local_aggs)
        # WHERE predicates only: HAVING operates on aggregates, not base filters.
        where=root.args.get('where')
        if where:
            def predicates(n):
                if isinstance(n,(exp.And,exp.Or,exp.Paren)):
                    for child in n.iter_expressions():yield from predicates(child)
                else:yield n
            for n in predicates(where.this):
                a=atom(n,scope)
                if a:filters.add(key(a))
                else:unsupported.append({'kind':'filters','sql':n.sql(dialect='sqlite')})
        for j in root.args.get('joins',[]):
            on=j.args.get('on');pairs=[]
            jt=(j.args.get('side') or j.args.get('kind') or 'inner').lower()
            def equalities(n):
                if isinstance(n,(exp.And,exp.Paren)):
                    for child in n.iter_expressions():yield from equalities(child)
                else:yield n
            if on:
                valid=True
                for n in equalities(on):
                    if not isinstance(n,exp.EQ):valid=False;break
                    left=column(n.this,scope);right=column(n.expression,scope)
                    if not left or not right:valid=False;break
                    pairs.append(sorted([left,right]) if jt=='inner' else [left,right])
                if valid and pairs:joins.add(key((jt,sorted(pairs))))
                else:unsupported.append({'kind':'joins','sql':j.sql(dialect='sqlite')})
        scope_rows.append({'group_by':gs,'aggregations':sorted(local_aggs)})
    return {'group_sets':groups,'aggregations':sorted(aggregates),'filters':sorted(filters),'joins':sorted(joins),
            'scopes':scope_rows,'unsupported':unsupported}


def candidate_features(c,catalog):
    aliases={}
    for t,cols in catalog.items():
        for col in cols:
            canonical=t+'.'+col
            for a in (t,'"'+t.replace('"','""')+'"'):
                for b in (col,'"'+col.replace('"','""')+'"'):
                    aliases[(a+'.'+b).casefold()]=canonical
    def col(x):return aliases.get(x.casefold(),x)
    fs={};fs['columns']={col(x) for x in c['columns']['items']}
    fs['group_by']={key(('time_bucket',col(x['column']),x['unit'])) if x['type']=='time_bucket' else key(('column',col(x['column']))) for x in c['group_by']['items']}
    fs['aggregations']={key((x['function'],col(x['column']) if x['column']!='*' else '*')) for x in c['aggregations']['items']}
    fs['filters']=set();unknown_values=0
    def filt(x):
        nonlocal unknown_values
        if x['type'] in ('and','or'):
            for item in x['items']:filt(item)
        elif x['value']['status']=='known':
            v=normvalue(x['value']['literal'])
            if x['op']=='in':v=sorted(v,key=key)
            fs['filters'].add(key(('predicate',col(x['column']),x['op'],v)))
        else:unknown_values+=1
    for x in c['filters']['items']:filt(x)
    fs['joins']=set()
    for j in c['joins']['items']:
        pairs=[]
        for cond in j['conditions']:
            pair=[col(cond['left_column']),col(cond['right_column'])]
            pairs.append(sorted(pair) if j['type']=='inner' else pair)
        fs['joins'].add(key((j['type'],sorted(pairs))))
    fs['unknown_filter_values']=unknown_values
    return fs


def decoded_hint(raw):
    """Offline visibility only: never changes delivered snapshot or acceptance.

    Recover explicitly written data from a JSON string and legacy column arrays;
    never invent a missing column, filter, group, aggregate or known status.
    """
    notes=[]
    if isinstance(raw,str):
        try:raw=json.loads(raw);notes.append('JSON string decoded for offline inspection only')
        except ValueError:return {},['unparseable string']
    if not isinstance(raw,dict):return {},['not an object']
    raw=copy.deepcopy(raw)
    for c in raw.get('candidates',[]):
        if not isinstance(c,dict):continue
        for f in FIELDS:
            v=c.get(f)
            if isinstance(v,list):
                c[f]={'status':'unspecified','items':v}
                notes.append(f+' legacy array: status not inferred')
            elif isinstance(v,dict) and 'items' not in v and v.get('status') in ('none','unknown'):
                v['items']=[]
                notes.append(f+' empty content shown from explicit none/unknown status')
    return raw,notes


def analyze(run):
    run=Path(run);meta=json.loads((run/'task_meta.json').read_text());events=records(run/'events.jsonl')
    reqs=[e for e in events if e['record']=='request'];ends={e['request_id']:e for e in events if e['record']=='completion'}
    catalog=meta['catalog'];qs={};parse_errors=[]
    db=sqlite3.connect(Path(meta['database_path']).as_uri()+'?mode=ro',uri=True,cached_statements=0)
    for e in reqs:
        if ends.get(e['request_id'],{}).get('response',{}).get('status')!='ok':continue
        cols=set();tables=set()
        def auth(action,t,c,*_):
            if action==sqlite3.SQLITE_READ:
                tables.add(t)
                if c:cols.add(t+'.'+c)
            return sqlite3.SQLITE_OK
        db.set_authorizer(auth)
        db.execute('EXPLAIN '+e['arguments']['sql']).fetchall()
        try:f=sql_features(e['arguments']['sql'],catalog)
        except Exception as exc:
            f={'group_sets':[],'aggregations':[],'filters':[],'joins':[],'unsupported':[],'scopes':[]}
            parse_errors.append({'step':e['step_id'],'error':str(exc)})
        f.update(columns=sorted(cols),tables=sorted(tables),sql=e['arguments']['sql'])
        qs[e['step_id']]=f
    db.close()
    rows=[];states={f:Counter() for f in FIELDS};filled_calls={f:set() for f in FIELDS}
    totals={f:Counter() for f in FIELDS};raw_candidates=0;invalid=0;unparsed=0;multi=0
    for e in reqs:
        h,decoding=decoded_hint(e['arguments'].get('future_access'));cs=h.get('candidates',[])
        raw_candidates+=len(cs);invalid+=bool(e['hint_errors']);multi+=len(cs)>1
        for index,c in enumerate(cs):
            try:pred=candidate_features(c,catalog)
            except (KeyError,TypeError,AttributeError):unparsed+=1;continue
            future=[q for q in sorted(qs) if q>e['step_id']]
            r={'step':e['step_id'],'candidate':index+1,'accepted':not bool(e['hint_errors']), 'fad':c,'fields':{},'offline_decoding':decoding,
               'priority':c.get('priority'),'likelihood':c.get('likelihood')}
            for f in FIELDS:
                state=c[f]['status'];states[f][state]+=1
                values=pred[f]
                if values:filled_calls[f].add(e['step_id'])
                matches=[]
                for q in future:
                    if f=='group_by':
                        yes=any(values==set(g) if state=='known' else values<=set(g) for g in qs[q]['group_sets'])
                    else:yes=values <= set(qs[q][f])
                    if values and yes:matches.append(q)
                token_hits={v for v in values if any(v in (set().union(*(set(g) for g in qs[q]['group_sets'])) if f=='group_by' else set(qs[q][f])) for q in future)}
                r['fields'][f]={'status':state,'specified':len(values),'matches':matches,'first_hit':matches[0] if matches else None,
                    'matched_items':len(token_hits),'unmatched_items':sorted(values-token_hits),
                    'predicted_items':sorted(values)}
                if values:
                    totals[f]['candidates_with_items']+=1;totals[f]['candidates_hit']+=bool(matches)
                    totals[f]['items']+=len(values);totals[f]['items_ever_hit']+=len(token_hits)
                    if matches:
                        totals[f]['first_hit_lag_sum']+=matches[0]-e['step_id']
                        totals[f]['next_success_hit']+=bool(future) and matches[0]==future[0]
            rows.append(r)
    # Per-successful-query coverage, counting tokens distinctly within each query.
    # Ever-before and active/latest-prefix are separate measurements.
    coverage={f:Counter() for f in FIELDS};query_coverage=[]
    for q,feat in sorted(qs.items()):
        prior=[r for r in rows if r['step']<q]
        prefixes=[e['step_id'] for e in reqs if e['step_id']<q]
        if not prefixes:continue
        last=max(prefixes);item={'step':q,'fields':{}}
        for f in FIELDS:
            actual=set().union(*(set(g) for g in feat['group_sets'])) if f=='group_by' else set(feat[f])
            before=set().union(*(set(r['fields'][f]['predicted_items']) for r in prior)) if prior else set()
            latest=set().union(*(set(r['fields'][f]['predicted_items']) for r in prior if r['step']==last))
            accepted=set().union(*(set(r['fields'][f]['predicted_items']) for r in prior if r['step']==last and r['accepted']))
            coverage[f]['actual_items']+=len(actual);coverage[f]['ever_predicted']+=len(actual&before)
            coverage[f]['latest_predicted']+=len(actual&latest);coverage[f]['latest_delivered']+=len(actual&accepted)
            item['fields'][f]={'actual':sorted(actual),'never_predicted':sorted(actual-before)}
        query_coverage.append(item)
    result={'task':meta['task_id'],'run':str(run),'query_attempts':len(reqs),'successful_queries':len(qs),
        'provided_hints':sum(decoded_hint(e['arguments'].get('future_access'))[0].get('status')=='provided' for e in reqs),
        'candidates':raw_candidates,'multi_candidate_calls':multi,'invalid_hint_calls':invalid,'unparsed_candidates':unparsed,
        'field_states':{f:dict(v) for f,v in states.items()},'calls_with_specified_fields':{f:len(v) for f,v in filled_calls.items()},
        'matching':{f:dict(v) for f,v in totals.items()},'coverage':{f:dict(v) for f,v in coverage.items()},
        'parse_errors':parse_errors,'rows':rows,'sql_features':qs,'query_coverage':query_coverage,
        'notes':['All matches use strictly later successful SQL; source failed-query hints retained.',
                 'Generated parseable candidates include rejected hints; accepted flag and latest_delivered distinguish usability.',
                 'JSON strings/legacy arrays decoded offline only; no semantic content or known status is inferred.',
                 'Grouping known matches full dimensions within one SQL scope; partial uses subset.',
                 'Aggregates and filter atoms match individually; filter AND/OR structure and full-query equivalence are NOT scored.',
                 'Unsupported SQL expressions are listed, so feature coverage is conditional on recognized expressions.',
                 'Repeated predictions and fields are correlated; no statistical significance or performance benefit claimed.']}
    out=run/'matching';out.mkdir(exist_ok=True)
    (out/'detail.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    summary={k:v for k,v in result.items() if k not in ('rows','sql_features','query_coverage')}
    (out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    lines=[f"# {meta['task_id']}：逐轮FAD和后续SQL",'',
        '仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。',
        '', '| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |',
        '|---|---|---|---|---|---|']
    def hits(x):
        if not x['specified']:return '没有提供具体项（'+x['status']+'）'
        return ', '.join('Q'+str(q) for q in x['matches']) or '未发现对应查询'
    for r in rows:
        c=r['fad'];pieces=[]
        for f in FIELDS:
            pieces.append(f+': '+key(c[f]))
        pieces.append('priority: '+str(c.get('priority')))
        if c.get('likelihood'):pieces.append('likelihood: '+c['likelihood'])
        content='<br>'.join(pieces).replace('|','\\|')
        lines.append(f"| Q{r['step']} / {r['candidate']} | {'是' if r['accepted'] else '否，见原始错误'} | {content} | {hits(r['fields']['group_by'])} | {hits(r['fields']['aggregations'])} | {hits(r['fields']['filters'])} |")
    lines+=['','## 实际SQL','']
    for e in reqs:
        status=ends.get(e['request_id'],{}).get('response',{}).get('status','unknown')
        lines += [f"### Q{e['step_id']}（{status}）",'','```sql',e['arguments']['sql'],'```','']
    (out/'PER-ROUND.md').write_text('\n'.join(lines))
    return summary


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args()
    print(json.dumps(analyze(a.run),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
