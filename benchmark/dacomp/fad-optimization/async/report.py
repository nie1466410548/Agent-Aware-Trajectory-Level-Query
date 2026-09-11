"""Report measured database work and task time reconstructed with recorded idle gaps."""
import argparse
import json
import statistics as st
from pathlib import Path


def read(p): return json.loads(Path(p).read_text())
def med(xs): return st.median(list(xs))
def span(a,b): return (b-a)/1e9

def overlap(a,b,windows):
    return sum(max(0,min(b,y)-max(a,x)) for x,y in windows)/1e9

def measures(summary,timeline):
    waits=[(w['anchor_ns'],w['ended_ns'] if summary['manifest'].get('skip_idle') else w['anchor_ns']+round(w['requested_seconds']*1e9)) for w in timeline['waits']]
    queries=[(q['arrival_ns'],q['response_return_ns']) for q in timeline['queries']]
    work=[];objects=[];closed={}
    fad_time=decision_time=0
    for e in timeline['background']:
        if e['type'] in ('worker_ready','fad_validated','decision'):
            a,b=e['started_ns'],e['ended_ns'];work.append((a,b))
            if e['type']=='fad_validated': fad_time+=span(a,b)
            if e['type']=='decision': decision_time+=span(a,b)
        if e['type']=='object_ready':objects.append(e['object'])
        if e['type']=='worker_closed':
            closed=e;work.append((e['cleanup_started_ns'],e['cleanup_ended_ns']))
    return {'recorded_background_work_seconds':sum(span(a,b) for a,b in work),
            'background_during_wait_seconds':sum(overlap(a,b,waits) for a,b in work),
            'background_during_query_seconds':sum(overlap(a,b,queries) for a,b in work),
            'background_after_report_seconds':sum(overlap(a,b,[(summary['report_ns'],summary['closed_ns'])]) for a,b in work),
            'fad_seconds':fad_time,'decision_including_build_seconds':decision_time,
            'worker_cpu_seconds':closed.get('cpu_seconds',0),'worker_peak_rss_kib':closed.get('peak_rss_kib',0),
            'objects':objects,
            'build_seconds':sum(span(o['build_started_ns'],o['build_ended_ns']) for o in objects),
            'build_during_wait_seconds':sum(overlap(o['build_started_ns'],o['build_ended_ns'],waits) for o in objects),
            'build_during_query_seconds':sum(overlap(o['build_started_ns'],o['build_ended_ns'],queries) for o in objects)}


def safe(s):return str(s).replace('|','&#124;').replace('\n',' ')
def expr(x):
    if x['type']=='time_bucket':return x['column']+'按'+{'month':'月','year':'年','day':'日'}[x['unit']]
    return x['column']

def pred(x):
    if x['type'] in ('and','or'):return '('+(' 且 ' if x['type']=='and' else ' 或 ').join(map(pred,x['items']))+')'
    v=x['value'];val=json.dumps(v['literal'],ensure_ascii=False) if v['status']=='known' else '值未定'
    return x['column']+' '+x['op']+' '+val

def description(c):
    pieces=[]
    for name,label,render in [('columns','补充列',str),('filters','过滤',pred),('group_by','分组',expr),
                              ('aggregations','聚合',lambda x:x['function'].upper()+'('+x['column']+')'),
                              ('joins','连接',lambda x:json.dumps(x,ensure_ascii=False))]:
        f=c[name];items='、'.join(render(x) for x in f['items'])
        pieces.append(label+'：'+(items or {'none':'无','unknown':'未定','known':'空列表（标成known）','partial':'空列表（标成partial）'}[f['status']])+
                      ('（不完整）' if f['status']=='partial' else ''))
    return '；'.join(pieces)

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--timing',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();root=Path(a.run);out=Path(a.output);manifest=read(root/'manifest.json');timing=read(a.timing)
    assert read(root/'COMPLETE.json')['all_equal'] and read(root/'AUDIT.json')['all_passed']
    paths=sorted(root.glob('pair-*'));assert len(paths)==manifest['pairs']==5
    data=[]
    for pair,path in enumerate(paths,1):
        r={'pair':pair}
        for arm in ('baseline','combined'):
            s=read(path/arm/'summary.json');t=read(path/arm/'timeline.json')
            assert read(path/arm/'correctness.json')['all_equal'] and s['manifest']['skip_idle']
            measured=sum(span(q['arrival_ns'],q['response_return_ns']) for q in t['queries'])
            assert abs(measured-s['database_request_seconds'])<1e-6
            r[arm]={'summary':s,'timeline':t,'measures':measures(s,t)}
        b,o=[r[x]['summary'] for x in ('baseline','combined')]
        r.update(saved_seconds=b['database_request_seconds']-o['database_request_seconds'],
                 saved_percent=(b['database_request_seconds']-o['database_request_seconds'])/b['database_request_seconds']*100,
                 saved_including_cleanup_seconds=b['database_request_seconds']+b['tail_cleanup_seconds']-o['database_request_seconds']-o['tail_cleanup_seconds'])
        data.append(r)
    metric=lambda arm,key:med(r[arm]['summary'][key] for r in data)
    bgmetric=lambda key:med(r['combined']['measures'][key] for r in data)
    saved=med(r['saved_seconds'] for r in data);pct=med(r['saved_percent'] for r in data)
    t=data[0]['combined']['timeline'];objects=data[0]['combined']['measures']['objects']
    validations={e['step']:e for e in t['background'] if e['type']=='fad_validated'}
    decisions={e['step']:e for e in t['background'] if e['type']=='decision'}
    names={};counts={}
    for o in objects:
        label='索引' if o['kind']=='index' else '汇总表';counts[label]=counts.get(label,0)+1;names[o['name']]=label+str(counts[label])
    for r in data:
        rt=r['combined']['timeline']
        assert {o['name'] for o in r['combined']['measures']['objects']}==set(names)
        es={e['step']:e for e in rt['background'] if e['type']=='fad_validated'}
        assert es.keys()==validations.keys()
        assert all(es[q]['fad']==e['fad'] and es[q]['audit']==e['audit'] for q,e in validations.items())
        for x,y in zip(t['queries'],rt['queries']):
            assert x['executed_sql']==y['executed_sql']
            assert {n for n in names if n in str(x['plan'])}=={n for n in names if n in str(y['plan'])}
    accepted=sum(e['fad'] is not None for e in validations.values())
    candidates=sum(len(e['fad']['candidates']) for e in validations.values() if e['fad'])
    stats={'primary_metric':'sum_of_SQL_arrival_to_response_seconds','accepted_fad_rounds':accepted,'accepted_candidates':candidates,
           'baseline_database_seconds':metric('baseline','database_request_seconds'),'fad_database_seconds':metric('combined','database_request_seconds'),
           'median_saved_seconds':saved,'median_saved_percent':pct,'source_wait_seconds':timing['total_wait_seconds'],
           'pairs':[{k:v for k,v in r.items() if k not in ('baseline','combined')} for r in data],
           'per_run':[{arm:{'summary':r[arm]['summary'],'measures':r[arm]['measures']} for arm in ('baseline','combined')} for r in data]}
    (out.parent/'statistics-async-million.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    n=len(timing['calls']);runlink=f'../async/runs/{root.name}'
    lines=['# FAD驱动数据库优化验证结果','','<!-- ASYNC-START -->','## DAComp-006：百万行，固定13轮SQL/FAD','',
           f"**数据库查询处理耗时：普通 {metric('baseline','database_request_seconds'):.3f} 秒 → 使用FAD {metric('combined','database_request_seconds'):.3f} 秒；五对配对结果的中位数{'节省' if saved>=0 else '增加'} {abs(saved):.3f} 秒（{abs(pct):.2f}%）。**",'',
           '主指标只累计每条SQL到达至结果返回的时间，包含快照、匹配/改写、查询、结果归档、日志和提交FAD的前台开销。后台校验、统计、构建及末尾清理单独报告；被Agent间隔覆盖的部分不重复扣除。', '',
           '本次沿用上一批失败实验的同一条13轮轨迹，没有重新调用Agent。固定间隔788.051秒复用，后台工作实际执行，结束后跳过剩余空闲。若构建未结束而间隔到期，下一条查询仍按时到达，保留实际并发。', '',
           '| 轨迹 | 来源 | SQL调用数 | 与本次关系 |','|---|---|---:|---|',
           '| 最早的FAD预测分析 | [dacomp-006-02](../../tool-prototype/v0.2/runs/dacomp-006-02/summary.json) | 30（29成功） | 原18,250行数据；下方旧串行实验沿用它 |',
           '| 本次与上一批失败实验 | [source-million-02](../async/source-million-02/summary.json) | 13（全部成功） | 百万行独立会话；两批输入完全相同 |','',
           f'**每次接受{accepted}/{n}轮FAD，共{candidates}个候选；所有130次回放查询与来源完整结果一致，65次两组直接比较一致。**','',
           '### 五对数据库耗时','',
           '单位秒。节省比例按每对普通耗时作分母；中位数先配对相减再计算。', '',
           '| 配对 | 普通查询处理 | 使用FAD的查询处理 | 节省 | 节省比例 | 加上末尾清理后的节省 |','|---|---:|---:|---:|---:|---:|']
    for r in data:
        b,o=[r[x]['summary'] for x in ('baseline','combined')]
        lines.append(f"| {r['pair']} | {b['database_request_seconds']:.3f} | {o['database_request_seconds']:.3f} | {r['saved_seconds']:+.3f} | {r['saved_percent']:+.2f}% | {r['saved_including_cleanup_seconds']:+.3f} |")
    lines+=['',f"使用FAD更快：{sum(r['saved_seconds']>0 for r in data)}/5对。节省范围 {min(r['saved_seconds'] for r in data):+.3f}～{max(r['saved_seconds'] for r in data):+.3f} 秒。",'',
            '### 收益具体来自哪里','',
            '本次改动：按SQL作用域匹配WITH内部的单表聚合，使提前建好的汇总表可以用于外层分析；同时对非覆盖索引检查首列过滤的真实匹配行数。没有明确首列过滤、零匹配或匹配超过全表10%的索引不建。10%为固定保守规则，不是精确收益预测。', '',
            '构建依然只看已收到的FAD及当前数据，不看未来SQL。同一方向在不同轮出现两次才可构建；最多两张汇总表、两个索引，每轮最多一次DDL尝试。拒绝索引后，同轮其余满足条件的汇总表仍可进入构建。', '',
            '| SQL | 普通查询，秒 | 使用FAD查询，秒 | 实际使用对象 |','|---|---:|---:|---|']
    for i,q in enumerate(t['queries']):
        bs=med(r['baseline']['timeline']['queries'][i]['query_seconds'] for r in data)
        os=med(r['combined']['timeline']['queries'][i]['query_seconds'] for r in data)
        used=[names[name] for name in names if name in str(q['plan'])]
        lines.append(f"| [Q{q['step']}](#async-q{q['step']}) | {bs:.4f} | {os:.4f} | {'、'.join(used) or '原表'} |")
    lines+=['','上表是查询执行与结果归档；主表还包含前台匹配等处理，因此不直接等于上表逐项相加。','',
            '### 每个准备动作：耗时与实际复用','',
            '单位秒，分别取五次中位数。构建全程包括空间估计扫描和CREATE；索引是否准入的过滤计数另列，避免遗漏。','',
            '| 对象 | 触发FAD轮次 | 估计及CREATE前处理 | CREATE至提交 | 构建全程 | 实际使用 |','|---|---|---:|---:|---:|---|']
    for obj in objects:
        name=obj['name'];os=[next(o for o in r['combined']['measures']['objects'] if o['name']==name) for r in data]
        used=[q['step'] for q in t['queries'] if name in str(q['plan'])]
        lines.append(f"| {names[name]} | "+'、'.join(f'[Q{s}](#async-q{s})' for s in obj['source_steps'])+
                     f" | {med(span(o['build_started_ns'],o['ddl_started_ns']) for o in os):.3f} | {med(span(o['ddl_started_ns'],o['commit_return_ns']) for o in os):.3f} | {med(span(o['build_started_ns'],o['build_ended_ns']) for o in os):.3f} | "+('、'.join(f'[Q{s}](#async-q{s})' for s in used) or '未使用')+' |')
    assessment_times=[]
    for r in data:
        assessment_times.append(sum(a.get('index_assessment',{}).get('seconds',0) for e in r['combined']['timeline']['background'] if e['type']=='decision' for a in e['actions'] if a['status']!='skipped'))
    lines+=['',f"后台FAD接收/校验 {bgmetric('fad_seconds'):.3f} 秒；索引准入检查 {med(assessment_times):.3f} 秒；实际对象构建 {bgmetric('build_seconds'):.3f} 秒。前台匹配/改写 {metric('combined','rewrite_seconds'):.3f} 秒，记录计划 {metric('combined','plan_seconds'):.3f} 秒，均已计入主指标。",'',
            f"构建与Agent间隔重叠 {bgmetric('build_during_wait_seconds'):.3f} 秒，与查询处理重叠 {bgmetric('build_during_query_seconds'):.3f} 秒。末尾停止/清理：普通 {metric('baseline','tail_cleanup_seconds'):.3f} 秒、使用FAD {metric('combined','tail_cleanup_seconds'):.3f} 秒；加上清理后节省的配对中位数 {med(r['saved_including_cleanup_seconds'] for r in data):+.3f} 秒。",'',
            '后台成本虽然没有重复计入查询等待，仍真实消耗资源。未被采用的索引也保留构建、空间和清理成本，不算作有效收益。', '',
            '本次拦住的宽范围索引：首列条件Destination LIKE South China%匹配371,782/1,000,000行（37.18%），超过10%准入线；纯月份索引没有明确的首列筛选条件，也不再盲目构建。不是按Q编号禁用某条SQL的索引。','']
    for obj in objects:
        name=obj['name'];used=[q['step'] for q in t['queries'] if name in str(q['plan'])]
        lines += [f'**{names[name]}**','',f"在Q{obj['created_after']}后由已到达FAD触发；后续使用："+('、'.join(f'Q{s}' for s in used) or '无')+'。','',
                  '```sql',obj['ddl'],'```','',f"主库新增分配页 {obj['allocated_bytes']/1024:.1f} KiB，不含WAL及排序临时空间。",'']
    lines+=['### 每轮SQL、FAD与执行证据','']
    for i,c in enumerate(timing['calls']):
        q=c['step'];r=t['queries'][i];e=validations[q];d=decisions[q]
        gap=timing['calls'][i+1]['gap_before_seconds'] if i+1<n else timing['final_gap_seconds']
        used=[names[name] for name in names if name in str(r['plan'])]
        built=[names[x['name']] for x in d['actions'] if x['status']=='built']
        lines += [f'<a id="async-q{q}"></a>',f'#### Q{q}','',
                  f"查询使用：{'、'.join(used) or '原表'}。本轮FAD触发新建：{'、'.join(built) or '无'}。本轮后复用间隔：{gap:.3f}秒。",'']
        if 'preserve original rounding scan order' in r['rewrite_reasons']:
            lines+=['当前舍入保护为SQL加入NOT INDEXED，保持原表浮点累加顺序。这也会放弃可能的索引收益，属于尚存的保守限制。','']
        lines+=['| 候选 | 本轮FAD实际预测 |','|---|---|']
        for j,fc in enumerate(c['arguments']['future_access']['candidates'],1):
            lines.append(f'| {j}（{fc["priority"]}） | {safe(description(fc))} |')
        for title,lang,value in [
            ('原始SQL','sql',c['arguments']['sql']),
            ('实际执行SQL与计划','text',r['executed_sql']+'\n\n'+'\n'.join(' | '.join(map(str,x)) for x in r['plan'])),
            ('原始FAD、接收记录与后台决策','json',json.dumps({'original_fad':c['arguments']['future_access'],'reception':{'audit':e['audit'],'fad':e['fad']},'decisions':d['actions']},ensure_ascii=False,indent=2))]:
            lines += [f'<details><summary>{title}</summary>','',f'```{lang}',value,'```','','</details>','']
    previous=read(out.parent/'statistics-async-million-before-cte-cost.json')
    lines+=['### 上一批失败结果保留','',
            f"上一批在相同13轮输入上，查询执行与结果归档中位数为普通7.870秒、使用FAD8.930秒；加上前台开销后的任务时间配对中位数增加1.158秒。新批次重新建立独立普通对照，不复用旧查询耗时。旧原始记录和[完整统计](statistics-async-million-before-cte-cost.json)保留。",'',
            '本次同时调整索引准入与CTE改写；这是整个修复的对照结果，不是只改其中一个功能的消融实验。每轮实际执行SQL、对象来源和计划可直接核对。', '',
            '### 控制条件与适用范围','',
            '- 每次全新数据库副本、进程和连接；相同预热、WAL、缓存与两个逻辑CPU；五对随机AB/BA串行执行，两组互不并发。普通组只处理SQL，不解码FAD或启动优化器。',
            '- 背景进程只接收已到达的FAD；没有未来SQL、未来间隔或离线匹配结果。对象提交完成后才可用，原始输入和数据哈希不变。',
            '- 64项测试通过，包括CTE作用域/同名遮蔽、聚合结果、索引筛选准入和后台未提交时查询继续执行；独立13条语义验证及正式130条源结果比对、65条直接对照均通过。',
            '- 修复基于这条轨迹暴露的问题；正收益仅证明当前轨迹上的可行性，不能替代未见任务上的验证。10%准入门槛仍是启发式；已建而未用的索引、两张汇总表数量上限和舍入保护仍限制收益。',
            '- 固定间隔仅复用数值，空闲跳过；不重现模型/其他工具的CPU、I/O竞争及长时间空闲对缓存和频率的影响。本次不计额外生成FAD的模型延时。',
            '- 数据为原18,250行复制扩到百万行，新增运单号唯一，其他业务字段保留；分组基数未同比增大。数据库副本位于/tmp的tmpfs，属于内存文件系统上的SQLite实验，不是物理磁盘性能结果。',
            '- 异步汇总表是副本中的任务级普通表，以便跨连接共享，任务末尾删除。所有后台进程正常关闭；浮点结果按绝对1e-7、相对1e-9核对，完整列名、行数、重复行、NULL和排序保留。','',
            '### 复现与原始记录','',
            f'- [本批配置](../async/runs/{root.name}/manifest.json)、[完成记录](../async/runs/{root.name}/COMPLETE.json)、[审计](../async/runs/{root.name}/AUDIT.json)',
            '- [来源SQL/FAD](../async/source-million-02/events.jsonl)、[客户端事件](../async/source-million-02/agent.jsonl)、[间隔清单](../async/timing-million.json)',
            '- [五对统计](statistics-async-million.json)、[实验计划](../async/PLAN.md)、[复现命令](../../../../agent_db_tool/optimization/README.md)',
            f'- [第1对完整时间线]({runlink}/pair-01/combined/timeline.json)（其余配对在同级目录）','',
            '<!-- ASYNC-END -->','','## 以下为旧串行成本诊断','',
            '**下方旧实验使用30轮来源，构建串行阻塞；只能说明串行执行时的成本，不能代表当前后台准备的查询延时。**','']
    old=out.read_text();marker='## DAComp-006：合成1,000,000行';assert marker in old
    out.write_text('\n'.join(lines)+old[old.index(marker):])
    print(json.dumps({k:v for k,v in stats.items() if k not in ('pairs','per_run')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
