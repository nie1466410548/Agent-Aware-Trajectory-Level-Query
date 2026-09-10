"""Offline content review; ignores delivery status, does not alter source logs.
Run from repo root with benchmark/dacomp/.venv/bin/python.
"""
import copy,json,sys
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parents[5]))
from agent_db_tool.matching import decoded_hint,candidate_features,join_matches,key
ROOT=Path(__file__).resolve().parent
FIELDS=('columns','filters','joins','group_by','aggregations')
LABEL={'columns':'列','filters':'过滤','joins':'连接','group_by':'分组','aggregations':'聚合'}

def refs(x):
    if isinstance(x,dict):
        for k,v in x.items():
            if k in ('column','left_column','right_column') and v!='*':yield x,k,v
            else:yield from refs(v)
    elif isinstance(x,list):
        for v in x:yield from refs(v)

def canonical(c,cat):
    c=copy.deepcopy(c);changes=[];unresolved=[];lookup={}
    def forms(s):return [s,'"'+s.replace('"','""')+'"','`'+s.replace('`','``')+'`','['+s+']']
    for t in c['tables']:
        for col in cat.get(t,[]):
            real=t+'.'+col
            for v in forms(col):lookup.setdefault(v.casefold(),set()).add(real)
            for a in forms(t):
                for b in forms(col):lookup.setdefault((a+'.'+b).casefold(),set()).add(real)
    def resolve(s):
        if s=='*':return s
        found=lookup.get(s.casefold(),set())
        if len(found)==1:
            out=next(iter(found))
            if out!=s:changes.append({'raw':s,'resolved':out})
            return out
        unresolved.append(s);return s
    c['columns']['items']=[resolve(s) for s in c['columns']['items']]
    for parent,k,v in refs(c):parent[k]=resolve(v)
    # Collect only existing explicit FAD references, never from SQL.
    c['columns']['items']=sorted(set(c['columns']['items'])|{v for _,_,v in refs(c)})
    return c,changes,unresolved

def brief(t):
    if isinstance(t,str):
        try:t=json.loads(t)
        except ValueError:return t
    if t[0]=='column':return t[1]
    if t[0]=='time_bucket':return t[1]+'按'+{'month':'月','year':'年','day':'日'}[t[2]]
    if t[0]=='predicate':return t[1]+' '+t[2]+' '+json.dumps(t[3],ensure_ascii=False)
    if t[0] in ('inner','left','right','full'):return t[0]+'连接：'+' 且 '.join(a+'='+b for a,b in t[1])
    return t[0].upper()+'('+str(t[1])+')'

def describe(c):
    def predicate(n):
        if n['type'] in ('and','or'):return '('+(' 且 ' if n['type']=='and' else ' 或 ').join(predicate(x) for x in n['items'])+')'
        val=n['value'];v=json.dumps(val.get('literal'),ensure_ascii=False) if val['status']=='known' else '值尚未确定'
        return n['column']+' '+n['op']+' '+v
    text=['读取：'+', '.join(c['columns']['items'])]
    for f in FIELDS[1:]:
        v=c[f];it=v['items']
        if not it:s='未提供（'+v['status']+'）'
        elif f=='group_by':s=' ＋ '.join(x['column']+('按'+{'month':'月','year':'年','day':'日'}[x['unit']] if x['type']=='time_bucket' else '') for x in it)
        elif f=='aggregations':s='、'.join(x['function'].upper()+'('+x['column']+')' for x in it)
        elif f=='filters':s='；'.join(predicate(x) for x in it)
        else:s='；'.join(j['type']+'：'+' 且 '.join(x['left_column']+'='+x['right_column'] for x in j['conditions']) for j in it)
        if it and v['status']=='partial':s+='（只描述了部分）'
        text.append(LABEL[f]+'：'+s)
    return '<br>'.join(text)

def run(name):
    p=ROOT.parent/'runs'/name
    d=json.loads((p/'matching/detail.json').read_text());cat=json.loads((p/'task_meta.json').read_text())['catalog']
    events=[json.loads(x) for x in (p/'events.jsonl').read_text().splitlines()]
    requests=[r for r in events if r['record']=='request']
    qs={int(q):f for q,f in d['sql_features'].items()};rows=[];empty=[];stats={f:Counter() for f in FIELDS}
    for req in requests:
        h,notes=decoded_hint(req['arguments']['future_access']);cs=h.get('candidates',[])
        if not cs:empty.append({'step':req['step_id'],'status':h.get('status')})
        for i,raw in enumerate(cs,1):
            c,changes,unknown=canonical(raw,cat);pred=candidate_features(c,cat)
            r={'step':req['step_id'],'candidate':i,'fad':c,'name_resolution':changes,'unresolved_names':unknown,'fields':{}}
            for f in FIELDS:
                values=pred[f];state=c[f]['status'];hits=[]
                for q,act in qs.items():
                    if q<=r['step'] or not values:continue
                    if f=='group_by':yes=any(values==set(g) if state=='known' else values<=set(g) for g in act['group_sets'])
                    elif f=='joins':yes=all(any(join_matches(v,a,state=='partial') for a in act['joins']) for v in values)
                    else:yes=values<=set(act[f])
                    if yes:hits.append(q)
                r['fields'][f]={'items':sorted(values),'later_queries':hits}
                if values:stats[f]['stated']+=1;stats[f]['later_occurred']+=bool(hits)
            rows.append(r)
    coverage={f:Counter() for f in FIELDS};cols=Counter();predcols=Counter();nevercols=Counter();unpredicted=[]
    for q,act in qs.items():
        prior=[r for r in rows if r['step']<q]
        if not any(r['step_id']<q for r in requests):continue
        missed={}
        for f in FIELDS:
            actual=set().union(*(set(g) for g in act['group_sets'])) if f=='group_by' else set(act[f])
            predicted=set().union(*(set(r['fields'][f]['items']) for r in prior))
            coverage[f]['actual']+=len(actual);coverage[f]['mentioned_before']+=len(actual&predicted)
            missed[f]=sorted(actual-predicted)
            if f=='columns':
                cols.update(actual);predcols.update(actual&predicted);nevercols.update(actual-predicted)
        unpredicted.append({'step':q,'not_mentioned_before':missed})
    out={'run':name,'successful_queries':len(qs),'candidate_count':len(rows),'counts':stats,'coverage':coverage,'rows':rows,'empty_fad':empty,
         'actual_without_prior_prediction':unpredicted,'frequent_columns':[{'column':c,'queries':n,'mentioned_before':predcols[c]} for c,n in cols.most_common()],
         'sql_features':qs}
    (ROOT/(name+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    lines=['# '+name+'：每个候选到底预测了什么','',
        '只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。',
        '下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。','',
        '| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |','|---|---|---|']
    for req in requests:
        rr=[r for r in rows if r['step']==req['step_id']]
        if not rr:
            h,_=decoded_hint(req['arguments']['future_access'])
            lines.append(f"| Q{req['step_id']} | 没有候选：{h.get('status')} | — |")
        for r in rr:
            evidence=[]
            for f in FIELDS:
                v=r['fields'][f]
                if not v['items']:continue
                hits=v['later_queries']
                evidence.append(LABEL[f]+'：'+('、'.join('Q'+str(q) for q in hits) if hits else '后续未找到全部所述项同时出现'))
            lines.append(f"| Q{r['step']} / 候选{r['candidate']} | {describe(r['fad']).replace('|','&#124;')} | {'<br>'.join(evidence)} |")
    lines+=['','## 实际SQL（保留失败轮次，失败SQL不作为发生证据）','']
    for req in requests:
        q=req['step_id'];lines += [f'### Q{q}（'+('成功' if q in qs else '失败')+'）','','```sql',req['arguments']['sql'],'```','']
    (ROOT/(name+'.md')).write_text('\n'.join(lines))
    return {k:v for k,v in out.items() if k not in ('rows','sql_features','actual_without_prior_prediction')}

if __name__=='__main__':
    allruns=[run(f'dacomp-{n}-{v}') for v in ('01','02') for n in ('003','004','005','006')]
    (ROOT/'summary.json').write_text(json.dumps(allruns,ensure_ascii=False,indent=2)+'\n')
    for r in allruns:
        print(r['run'],dict(r['counts']['group_by']),dict(r['counts']['aggregations']),'column coverage',dict(r['coverage']['columns']))
