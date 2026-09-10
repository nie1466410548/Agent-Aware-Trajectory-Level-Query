"""Present predictions beside their SQL evidence, within the existing task sections."""
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[4]))
from agent_db_tool.matching import candidate_features
from sqlglot import Tokenizer,TokenType
OPS=('filters','joins','group_by','aggregations')
LABEL={'columns':'列清单','filters':'过滤','joins':'连接','group_by':'分组','aggregations':'聚合'}

def pretty(sql):
    # Insert display whitespace only, outside string/identifier tokens.
    tokens=Tokenizer(dialect='sqlite').tokenize(sql)
    breaks=set();depth=0
    names={'SELECT','FROM','WHERE','GROUP_BY','ORDER_BY','HAVING','LIMIT','UNION','WITH','JOIN'}
    for t in tokens:
        if t.token_type.name in names and t.start:breaks.add(t.start)
        if t.token_type==TokenType.L_PAREN:depth+=1
        if t.token_type==TokenType.R_PAREN:depth-=1
        if t.token_type==TokenType.COMMA and depth==0:breaks.add(t.end+1)
    out=[];last=0
    for pos in sorted(breaks):out.extend([sql[last:pos].rstrip(),'\n']);last=pos
    out.append(sql[last:].lstrip())
    formatted=''.join(out).strip()
    assert [(t.token_type,t.text) for t in tokens]==[(t.token_type,t.text) for t in Tokenizer(dialect='sqlite').tokenize(formatted)]
    return formatted

def format_fad(c):
    def val(n):
        if n['type'] in ('and','or'):return '('+(' 且 ' if n['type']=='and' else ' 或 ').join(val(x) for x in n['items'])+')'
        v=n['value'];return n['column']+' '+n['op']+' '+(json.dumps(v.get('literal'),ensure_ascii=False) if v['status']=='known' else '值未定')
    lines=['- 表：'+', '.join(c['tables'])+'。','- 列：'+', '.join(c['columns']['items'])+'。']
    for f in OPS:
        obj=c[f];it=obj['items']
        if not it:content={'none':'未声明此操作','unknown':'尚未确定'}.get(obj['status'],'没有具体项')
        elif f=='filters':content='；'.join(val(x) for x in it)
        elif f=='joins':content='；'.join(j['type']+'：'+' 且 '.join(x['left_column']+' = '+x['right_column'] for x in j['conditions']) for j in it)
        elif f=='group_by':content=' ＋ '.join(x['column']+('（按'+{'month':'月','year':'年','day':'日'}[x['unit']]+'）' if x['type']=='time_bucket' else '') for x in it)
        else:content='、'.join(x['function'].upper()+'('+x['column']+')' for x in it)
        if obj['status']=='partial':content+='（部分信息）'
        lines.append('- '+LABEL[f]+'：'+content+'。')
    return '\n'.join(lines)

def evidence(sql,q):return f'**后续实际执行：Q{q}**\n\n```sql\n{pretty(sql)}\n```\n'

rates={d['task']:d for d in json.loads((ROOT/'task-rates.json').read_text())}
text=(ROOT/'REPORT.md').read_text()
for task in ('003','004','005','006'):
    d=json.loads((ROOT/f'dacomp-{task}-02.json').read_text())
    rows={(r['step'],r['candidate']):r for r in d['rows']}
    reqs=[e for x in (ROOT.parent/'runs'/f'dacomp-{task}-02/events.jsonl').read_text().splitlines() if (e:=json.loads(x))['record']=='request']
    reqmap={r['step_id']:r for r in reqs};qs={int(q):s for q,s in d['sql_features'].items()}
    rr={(r['step'],r['candidate']):r for r in rates[task]['candidate_evidence']}
    begin=text.index('## DAComp-'+task+'：');end=text.find('\n<a id="task-',begin)
    if end<0:end=len(text)
    section=text[begin:end]
    # Existing selected examples become adjacent evidence cards, preserving explanation.
    a=section.index('### 1.');b=section.index('### 2.',a)
    old=section[a:b]
    cases=[l for l in old.splitlines() if l.startswith('| Q')]
    destinations={'003':[[7],[6,8]],'004':[[3],[7]],'005':[[2],[5,6,7],[16]],'006':[[3],[4],[7],[30]]}[task]
    selected=['### 1. 预测与后续SQL放在一起看','',
              '每个例子先写FAD预测，下面紧接实际SQL，再解释对应程度。Q编号均属于本题第二轮。','']
    for i,(line,targets) in enumerate(zip(cases,destinations),1):
        c=[x.strip() for x in line.strip('|').split('|')]
        selected += [f'#### 例{i}：{c[0]} → '+ '、'.join('Q'+str(q) for q in targets),'',
                     '**FAD预测：** '+c[1]+'。','',
                     '**实际访问概括：** '+c[2]+'。','']
        for q in targets:selected += [evidence(reqmap[q]['arguments']['sql'],q)]
        selected += ['**对应判断：** '+c[3],'']
    if cases:
        section=section[:a]+'\n'.join(selected)+'\n'+section[b:]
    # Complete appendix: every candidate has its own adjacent SQL evidence.
    a=section.index('### 7.')
    paired=['### 7. 每个候选的FAD与SQL直接对照','',
      '下面按提出预测的轮次排列。每项标题直接写“哪轮候选 → 哪条后续SQL”，展开即可同时看到FAD、实际SQL和对应说明。完整对应的候选选择最早的一条证据；部分对应的候选选择能解释最多已写内容的一条代表SQL，不把部分对应当作完整命中。',
      '这里只排版展示原始SQL，未执行或改写查询。分项可能另有证据，全部编号仍保存在本题复核JSON中。','']
    for req in reqs:
        step=req['step_id'];source_rows=[r for r in d['rows'] if r['step']==step]
        if not source_rows:
            future=[q for q in sorted(qs) if q>step]
            outcome='之后仍有SQL，结束判断不对' if future else '之后没有SQL，与结束判断一致'
            paired += [f'<details><summary>Q{step}：没有候选；{outcome}</summary>','',
              '**原始FAD：** `'+json.dumps(req['arguments']['future_access'],ensure_ascii=False)+'`','']
            if future:paired += [evidence(reqmap[future[0]]['arguments']['sql'],future[0])]
            paired += ['</details>',''];continue
        for r in source_rows:
            stat=rr[(step,r['candidate'])];fields=r['fields'];full=stat['evidence_sql']
            if full:q=full[0]
            else:
                choices=[]
                for q0,act in qs.items():
                    if q0<=step:continue
                    score=0
                    for f in ('columns',*OPS):
                        actual=set().union(*(set(g) for g in act['group_sets'])) if f=='group_by' else set(act[f])
                        score+=len(set(fields[f]['items'])&actual)
                        if fields[f]['items'] and q0 in fields[f]['later_queries']:score+=20 if f!='columns' else 2
                    choices.append((score,-q0,q0))
                q=max(choices)[2] if choices and max(choices)[0] else None
            label={'all_stated_matched':'已写信息全部对应','part_matched':'只对应部分内容','none_matched':'未找到对应内容'}[stat['result']]
            title=f'Q{step}候选{r["candidate"]} → '+(f'Q{q}' if q else '没有后续对应SQL')+'：'+label
            paired += [f'<details><summary>{title}</summary>','',f'**提出预测：Q{step}候选{r["candidate"]}。**','',format_fad(r['fad']),'']
            if q:
                paired += [evidence(reqmap[q]['arguments']['sql'],q), '**逐项对应：**','']
                for f in ('columns',*OPS):
                    if not fields[f]['items']:continue
                    yes=q in fields[f]['later_queries']
                    paired.append('- '+LABEL[f]+'：'+('该SQL包含已写出的这一组信息。' if yes else '该SQL未完整对应这一组信息；不能将其算作整项命中。'))
                if full:paired += ['','**整体判断：** 已写出的列和操作在这条后续SQL中共同对应；未写出的内容不视为已预测。']
                else:paired += ['','**整体判断：** 这是部分内容的代表证据，不能据此将整个候选算成功。相近方向和复杂表达式的人工解释见本题前面的分析。']
            else:
                paired += ['**判断：** 剩余成功SQL中没有找到可作为对应证据的已写内容。']
                future=[n for n in sorted(qs) if n>step]
                if len(future)<=2:
                    for n in future:paired += ['','**剩余实际SQL，供直接核对：**',evidence(reqmap[n]['arguments']['sql'],n)]
            paired += ['', '<details><summary>当前执行的SQL</summary>','',
                       '```sql',pretty(req['arguments']['sql']),'```','','</details>','','</details>','']
    paired += [f'原始记录：[events.jsonl](../runs/dacomp-{task}-02/events.jsonl)；全部分项证据：[本题复核JSON](dacomp-{task}-02.json)。','',
        '本题是在FAD要求下实际生成的轨迹；没有据此声称它与无FAD要求时的路线完全相同。','']
    section=section[:a]+'\n'.join(paired)
    text=text[:begin]+section+text[end:]
(ROOT/'REPORT.md').write_text(text)
print('Updated one report: selected examples and every candidate now have adjacent actual SQL.')
