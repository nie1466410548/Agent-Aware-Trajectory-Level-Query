"""Append original-data 30-call results to the existing report; preserve other runs."""
import argparse
import importlib.util
import json
import statistics as st
from pathlib import Path

spec=importlib.util.spec_from_file_location('report_helpers',Path(__file__).with_name('report.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
read=h.read;med=h.med;span=h.span

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(a.run);out=Path(a.output);manifest=read(root/'manifest.json');timing=read(manifest['timing']);audit=read(root/'AUDIT.json')
    assert audit['all_passed'] and read(root/'COMPLETE.json')['pairs']==5 and len(timing['calls'])==30
    reference=root.parent/'reused-gaps-million-02-cte-cost';old_manifest=read(reference/'manifest.json')
    assert manifest['config']==old_manifest['config'] and manifest['source_hashes']==old_manifest['source_hashes']
    pairs=[]
    for pdir in sorted(root.glob('pair-*')):
        d={}
        for arm in ['baseline','combined']:
            s=read(pdir/arm/'summary.json');t=read(pdir/arm/'timeline.json')
            assert read(pdir/arm/'correctness.json')['all_equal'] and s['query_attempts']==30 and s['query_successes']==29
            assert abs(s['database_request_seconds']-sum(span(q['arrival_ns'],q['response_return_ns']) for q in t['queries']))<1e-6
            d[arm]={'summary':s,'timeline':t,'measures':h.measures(s,t)}
        b,o=[d[x]['summary'] for x in ['baseline','combined']]
        d['saved_seconds']=b['database_request_seconds']-o['database_request_seconds']
        d['saved_percent']=d['saved_seconds']/b['database_request_seconds']*100
        d['saved_including_cleanup_seconds']=d['saved_seconds']+b['tail_cleanup_seconds']-o['tail_cleanup_seconds']
        pairs.append(d)
    assert len(pairs)==5
    metric=lambda arm,key:med(d[arm]['summary'][key] for d in pairs)
    bg=lambda key:med(d['combined']['measures'][key] for d in pairs)
    timeline=pairs[0]['combined']['timeline'];objects=pairs[0]['combined']['measures']['objects']
    vals={e['step']:e for e in timeline['background'] if e['type']=='fad_validated'}
    decisions={e['step']:e for e in timeline['background'] if e['type']=='decision'}
    names={o['name']:('索引' if o['kind']=='index' else '汇总表')+str(i) for i,o in enumerate(objects,1)}
    for d in pairs:
        t=d['combined']['timeline'];vs={e['step']:e for e in t['background'] if e['type']=='fad_validated'}
        assert len(vs)==30 and all(vs[q]['fad']==e['fad'] and vs[q]['audit']==e['audit'] for q,e in vals.items())
        assert {o['name'] for o in d['combined']['measures']['objects']}==set(names)
        for x,y in zip(timeline['queries'],t['queries']):
            assert x['executed_sql']==y['executed_sql'] and x['materializations_used']==y['materializations_used']
    saved=med(d['saved_seconds'] for d in pairs);pct=med(d['saved_percent'] for d in pairs)
    stats={'source_run':timing['source_run'],'database_rows':18250,'calls':30,'successful_queries':29,
           'same_optimizer_code_and_config_as_13_call_run':True,'primary_metric':'sum_of_SQL_arrival_to_response_seconds',
           'baseline_database_seconds':metric('baseline','database_request_seconds'),'fad_database_seconds':metric('combined','database_request_seconds'),
           'median_saved_seconds':saved,'median_saved_percent':pct,'accepted_rounds':30,'nonempty_rounds':29,'accepted_candidates':58,
           'pairs':[{k:v for k,v in d.items() if k not in ('baseline','combined')} for d in pairs],
           'per_run':[{arm:{'summary':d[arm]['summary'],'measures':d[arm]['measures']} for arm in ('baseline','combined')} for d in pairs]}
    (out.parent/'statistics-async-original-30.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    qtime=lambda arm,i:med(d[arm]['timeline']['queries'][i]['query_seconds'] for d in pairs)*1000
    rtime=lambda arm,i:med(span(d[arm]['timeline']['queries'][i]['arrival_ns'],d[arm]['timeline']['queries'][i]['response_return_ns']) for d in pairs)*1000
    lines=['<!-- ORIGINAL-30-START -->','## 原始任务六：18,250行，报告中的30轮轨迹','',
           f"**按相同优化策略实测，这条原始轨迹没有获得更高的净收益：数据库查询处理耗时 {metric('baseline','database_request_seconds')*1000:.1f} ms → {metric('combined','database_request_seconds')*1000:.1f} ms，配对中位数{'增加' if saved<0 else '减少'} {abs(saved)*1000:.1f} ms（{abs(pct):.1f}%）。**",'',
           '数据就是原始dacomp-006.sqlite，18,250行；SQL/FAD就是[原FAD分析报告中任务六](../../tool-prototype/v0.2/trajectory-review/REPORT.md#task-006)的dacomp-006-02会话，30次SQL调用，29次成功。Q10原有错误保留，两组都出现相同错误。没有扩容或重新生成轨迹。', '',
           '本次与上一批13轮百万行实验使用完全相同的优化代码和配置。后台按已到达FAD准备，原客户端间隔358.049秒直接复用，剩余空闲跳过；主指标累计SQL到达至结果返回的时间。后台构建、前台处理和末尾清理分别列出。', '',
           '### 五对结果','',
           '单位ms；净节省=普通−使用FAD，负数表示变慢。','',
           '| 配对 | 普通查询处理 | 使用FAD查询处理 | 净节省 | 净节省比例 | 加清理后的净节省 |','|---|---:|---:|---:|---:|---:|']
    for i,d in enumerate(pairs,1):
        b,o=[d[x]['summary'] for x in ['baseline','combined']]
        lines.append(f"| {i} | {b['database_request_seconds']*1000:.1f} | {o['database_request_seconds']*1000:.1f} | {d['saved_seconds']*1000:+.1f} | {d['saved_percent']:+.1f}% | {d['saved_including_cleanup_seconds']*1000:+.1f} |")
    lines+=['',f"使用FAD更快：{sum(d['saved_seconds']>0 for d in pairs)}/5对。300次回放调用与来源核对、150次两组直接比较全部通过。接受30份FAD，其中29份有预测、1份无后续预测，58个候选全部接受。",'',
            '### 查询确实省了部分工作，前台开销抵消了收益','',
            '| 耗时组成，五次中位数，ms | 普通 | 使用FAD |','|---|---:|---:|',
            f"| SQL执行和结果归档 | {metric('baseline','query_seconds')*1000:.1f} | {metric('combined','query_seconds')*1000:.1f} |",
            f"| 前台匹配、预检、改写 | 0 | {metric('combined','rewrite_seconds')*1000:.1f} |",
            f"| 记录执行计划 | 0 | {metric('combined','plan_seconds')*1000:.1f} |",
            f"| 其余前台处理（快照、提交FAD、日志、返回等） | {med(d['baseline']['summary']['database_request_seconds']-d['baseline']['summary']['query_seconds'] for d in pairs)*1000:.1f} | {med(d['combined']['summary']['database_request_seconds']-sum(d['combined']['summary'][k] for k in ('query_seconds','rewrite_seconds','plan_seconds')) for d in pairs)*1000:.1f} |",
            f"| 任务结束后停止和清理（不在上述主指标中） | {metric('baseline','tail_cleanup_seconds')*1000:.1f} | {metric('combined','tail_cleanup_seconds')*1000:.1f} |",'',
            '各项分别取中位数，列内相加不一定严格等于总时间中位数。其余前台时间由实际时间戳相减得到，没有进一步归因到某个线程或操作。', '',
            '这条轨迹确实有重复访问，华南按月份、产品汇总的结果用于Q13、Q15、Q21。但原始小库的查询只需要几毫秒；当前Python匹配/改写和请求处理也是毫秒级，节省的扫描工作不足以支付前台开销。', '',
            '| 实际复用的SQL | 普通SQL执行，ms | 复用后的SQL执行，ms | 普通整轮处理，ms | 复用后整轮处理，ms |','|---|---:|---:|---:|---:|']
    for i,q in enumerate(timeline['queries']):
        if q['materializations_used']:
            lines.append(f"| [Q{q['step']}](#original30-q{q['step']}) | {qtime('baseline',i):.3f} | {qtime('combined',i):.3f} | {rtime('baseline',i):.3f} | {rtime('combined',i):.3f} |")
    lines+=['','### 实际准备了什么','',
            '| 对象 | 触发FAD | 构建耗时，ms | 后续实际使用 |','|---|---|---:|---|']
    for obj in objects:
        name=obj['name'];used=[q['step'] for q in timeline['queries'] if name in str(q['plan'])]
        build=med(next(o['build_seconds'] for o in d['combined']['measures']['objects'] if o['name']==name) for d in pairs)
        lines.append(f"| {names[name]} | "+'、'.join(f'Q{x}' for x in obj['source_steps'])+f" | {build*1000:.2f} | "+('、'.join(f'[Q{x}](#original30-q{x})' for x in used) or '未使用')+' |')
    lines+=['',f"后台构建合计 {bg('build_seconds')*1000:.2f} ms，其中 {bg('build_during_wait_seconds')*1000:.2f} ms 在Agent间隔内，{bg('build_during_query_seconds')*1000:.2f} ms 与查询重叠。后台接收FAD {bg('fad_seconds')*1000:.2f} ms；这些成本单独保留，没有再次加到前台查询时间。",'',
            '汇总表1统计所有地区的月度利润，没有保留目的地，无法再筛选华南；它未被使用。汇总表2保留华南的月份、产品及利润/销量/收入三个指标，确实用于三条查询。两个固定名额用满后，后来的其他汇总预测没有得到构建机会。', '',
            '当前还要求过滤和分组严格对应、所需聚合已存储。例如Q7多需要Total Logistics Cost求和，而汇总表2没有该指标，所以不能替换。原报告的“候选命中”只要求任意一项被后续使用，并不等于整条查询可由这个候选生成的汇总表替代。', '']
    for obj in objects:lines += [f"**{names[obj['name']]}实际DDL**",'','```sql',obj['ddl'],'```','']
    lines+=['### 逐轮SQL、FAD、实际动作和耗时','',
            '| 轮次 | 普通整轮处理，ms | 使用FAD整轮处理，ms | 实际复用 |','|---|---:|---:|---|']
    for i,q in enumerate(timeline['queries']):
        used=[names[name] for name in q['materializations_used']]
        lines.append(f"| [Q{q['step']}](#original30-q{q['step']}) | {rtime('baseline',i):.3f} | {rtime('combined',i):.3f} | "+('、'.join(used) or ('原有错误' if q['status']!='ok' else '原表'))+' |')
    for i,c in enumerate(timing['calls']):
        q=c['step'];r=timeline['queries'][i];e=vals[q];d=decisions[q]
        lines += ['',f'<a id="original30-q{q}"></a>',f'#### 原始轨迹 Q{q}','',
                  f"查询处理：普通 {rtime('baseline',i):.3f} ms → 使用FAD {rtime('combined',i):.3f} ms。实际复用："+('、'.join(names[n] for n in r['materializations_used']) or '无')+'。','']
        cs=c['arguments']['future_access']['candidates']
        if cs:
            lines+=['| 候选 | 本轮FAD实际预测 |','|---|---|']
            for j,fc in enumerate(cs,1):lines.append(f'| {j}（{fc["priority"]}） | {h.safe(h.description(fc))} |')
        else:lines+=['本轮没有后续访问预测。']
        for title,lang,value in [('原始SQL','sql',r['sql']),('实际执行SQL及执行计划','text',r['executed_sql']+'\n\n'+'\n'.join(' | '.join(map(str,x)) for x in r['plan'])),('原始FAD、接收记录及后台动作','json',json.dumps({'raw':r['raw_fad'],'audit':e['audit'],'fad':e['fad'],'actions':d['actions']},ensure_ascii=False,indent=2))]:
            lines += ['',f'<details><summary>{title}</summary>','',f'```{lang}',value,'```','','</details>']
    lines+=['','### 结论范围与原始证据','',
            '在原始18,250行、30轮轨迹上，当前相同策略没有净提速。它显示了实际汇总复用，也显示出前台开销与对象名额限制。上一实验是百万行、另一条13轮轨迹，两者同时改变数据规模和查询内容，不能把比例差直接归因于SQL轮数或FAD数量。', '',
            '每对全新数据库副本、进程和连接，相同预热、WAL、两个逻辑CPU和随机AB/BA；/tmp为tmpfs。没有修改优化代码或配置去适配本批结果。空闲跳过，间隔沿用原客户端记录，不包含额外生成FAD的模型成本。', '',
            f'- [来源会话](../../tool-prototype/v0.2/runs/dacomp-006-02/summary.json)、[原始SQL/FAD](../../tool-prototype/v0.2/runs/dacomp-006-02/events.jsonl)',
            '- [原始间隔](../async/timing-original-30.json)、[本批统计](statistics-async-original-30.json)',
            f'- [运行配置](../async/runs/{root.name}/manifest.json)、[完成记录](../async/runs/{root.name}/COMPLETE.json)、[审计](../async/runs/{root.name}/AUDIT.json)',
            f'- [第1对完整时间线](../async/runs/{root.name}/pair-01/combined/timeline.json)','',
            '<!-- ORIGINAL-30-END -->','']
    text=out.read_text();start='<!-- ORIGINAL-30-START -->';end='<!-- ORIGINAL-30-END -->'
    if start in text:text=text[:text.index(start)]+text[text.index(end)+len(end):].lstrip('\n')
    heading='# FAD驱动数据库优化验证结果\n\n';assert text.startswith(heading)
    out.write_text(heading+'\n'.join(lines)+text[len(heading):])
    print(json.dumps({k:v for k,v in stats.items() if k not in ('pairs','per_run')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
