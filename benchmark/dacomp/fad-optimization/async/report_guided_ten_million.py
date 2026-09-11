"""Two-pair guided experiment, written above older results in the same report."""
import argparse
import importlib.util
import json
import statistics
from pathlib import Path

spec=importlib.util.spec_from_file_location('helpers',Path(__file__).with_name('report.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
read=h.read;avg=statistics.mean;safe=h.safe


def fold(title,value,language='json'):
    text=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False,indent=2)
    return ['',f'<details><summary>{title}</summary>','',f'```{language}',text,'```','','</details>']


def object_description(obj):
    p=obj['pattern']
    labels={'Destination':'目的地','Consigned Product':'产品','Profit':'利润',
            'Sales Quantity':'销量','Total Logistics Revenue':'收入',
            'Logistics Unit Price':'物流单价','Discount Amount':'折扣额',
            'Logistics Value-Added Service Revenue':'增值服务收入'}
    def column(expr):
        if expr.startswith("strftime('%Y-%m'"):return '月份'
        return labels.get(expr.strip('"'),expr)
    scope='华南' if p.get('where')=='"Destination" LIKE \'South China%\'' else (p.get('where') or '全部数据')
    if obj['kind']=='index':return scope+'；索引键：'+'、'.join(p['keys'])
    groups='×'.join(column(x) for x in p['groups']) or '不分组'
    metrics=['记录数' if f=='count' and c=='*' else column(c)+{'sum':'求和','avg':'均值','count':'计数','min':'最小值','max':'最大值'}.get(f,f) for f,c in p['aggregations']]
    return scope+'；'+groups+'；'+'、'.join(metrics)


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--output',required=True)
    a=p.parse_args();root=Path(a.run);out=Path(a.output)
    manifest=read(root/'manifest.json');audit=read(root/'AUDIT.json');timing=read(manifest['timing'])
    assert audit['all_passed'] and read(root/'COMPLETE.json')=={'pairs':2,'all_equal':True}
    assert manifest['pairs']==2
    source=Path(timing['source_run']);n=len(timing['calls']);source_summary=read(source/'summary.json')
    review=read(source/'analysis-review.json')
    assert review['sql_calls']==n
    pairs=[]
    for number in (1,2):
        d={'number':number}
        for arm in ('baseline','combined'):
            pdir=root/f'pair-{number:02d}'/arm
            s=read(pdir/'summary.json');t=read(pdir/'timeline.json')
            assert read(pdir/'correctness.json')['all_equal'] and len(t['queries'])==n
            assert abs(s['database_request_seconds']-sum(h.span(q['arrival_ns'],q['response_return_ns']) for q in t['queries']))<1e-6
            builds=[e['object'] for e in t['background'] if e['type']=='build_finished']
            measures=h.measures(s,t)
            measures['all_build_attempt_seconds']=sum(o['build_seconds'] for o in builds)
            d[arm]={'summary':s,'timeline':t,'measures':measures,'builds':builds}
        b,o=(d[k]['summary'] for k in ('baseline','combined'))
        d['saved_seconds']=b['database_request_seconds']-o['database_request_seconds']
        d['saved_percent']=100*d['saved_seconds']/b['database_request_seconds']
        d['saved_with_cleanup_seconds']=d['saved_seconds']+b['tail_cleanup_seconds']-o['tail_cleanup_seconds']
        pairs.append(d)
    metric=lambda arm,k:avg(d[arm]['summary'][k] for d in pairs)
    bg=lambda k:avg(d['combined']['measures'][k] for d in pairs)
    b=metric('baseline','database_request_seconds');o=metric('combined','database_request_seconds')
    pct=(b-o)/b*100
    objects={x['name']:x for d in pairs for x in d['combined']['measures']['objects']}
    names={name:('索引' if x['kind']=='index' else '汇总表')+str(i) for i,(name,x) in enumerate(objects.items(),1)}
    used=lambda d,i:[name for name in objects if name in str(d['combined']['timeline']['queries'][i]['plan'])]
    reused=[c['step'] for i,c in enumerate(timing['calls']) if any(used(d,i) for d in pairs)]
    used_objects={name for d in pairs for i in range(n) for name in used(d,i)}
    counts=[]
    for d in pairs:
        events=[e for e in d['combined']['timeline']['background'] if e['type']=='fad_validated']
        counts.append({'pair':d['number'],'processed_rounds':len(events),'accepted_rounds':sum(e['fad'] is not None for e in events),
                       'nonempty_rounds':sum(bool(e['fad'] and e['fad']['candidates']) for e in events),
                       'accepted_candidates':sum(len(e['fad']['candidates']) for e in events if e['fad'])})
    stats={'source_run':str(source),'database_rows':10000000,'calls':n,
           'business_query_calls':review['business_query_calls'],
           'closing_no_further_access_step':review['closing_no_further_access_step'],
           'successful_source_queries':source_summary['successful_queries'],'formal_pairs':2,
           'primary_metric':'sum_of_database_service_start_to_response_seconds',
           'aggregation':'arithmetic mean of two runs; reduction computed from the two mean service totals',
           'mean_baseline_seconds':b,'mean_fad_seconds':o,'mean_saved_seconds':b-o,'mean_reduction_percent':pct,
           'reused_query_steps':reused,'built_objects':len(objects),'used_objects':len(used_objects),'fad_reception':counts,
           'pairs':[{k:d[k] for k in ('number','saved_seconds','saved_percent','saved_with_cleanup_seconds')} for d in pairs],
           'per_run':[{arm:{'summary':d[arm]['summary'],'measures':d[arm]['measures']} for arm in ('baseline','combined')} for d in pairs]}
    (out.parent/'statistics-async-ten-million-guided.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    sl=f'../async/{source.name}';rl=f'../async/runs/{root.name}'
    lines=['<!-- GUIDED-TEN-MILLION-START -->','## DAComp-006：千万行，SQL分析指导，两对实验','',
           f'**数据库前台累计处理时间，两次平均：普通 {b:.3f} 秒 → 使用FAD {o:.3f} 秒，'+('减少' if pct>=0 else '增加')+f' {abs(pct):.2f}%。**','',
           f'独立新Agent在同一份10,000,000行数据上，根据每次查询结果继续分析，共执行{review["business_query_calls"]}条业务数据查询，最后用Q{review["closing_no_further_access_step"]}的 `SELECT 1` 提交“无后续访问”标记。合计{n}次SQL调用全部成功，均保留在计时中。Agent已提交报告。', '',
           '本次在提示中增加分析步骤要求，把波动统计、贡献分解等计算交给SQL；没有提供旧SQL/FAD、旧数值或结论，也没有设定查询轮数目标。实际查询如何分布，以及分析报告的局限，见下文。', '',
           '### 两对结果','',
           '| 配对 | 普通执行，秒 | 使用FAD，秒 | 节省，秒 | 节省比例 | 加上清理后的节省，秒 |',
           '|---|---:|---:|---:|---:|---:|']
    for d in pairs:
        lines.append(f"| {d['number']} | {d['baseline']['summary']['database_request_seconds']:.3f} | {d['combined']['summary']['database_request_seconds']:.3f} | {d['saved_seconds']:+.3f} | {d['saved_percent']:+.2f}% | {d['saved_with_cleanup_seconds']:+.3f} |")
    lines+=['',f"使用FAD更快：{sum(d['saved_seconds']>0 for d in pairs)}/2对。全部{n*4}次回放与来源结果核对、{n*2}次两组直接比较通过。",'',
            '只累计数据库工具开始处理SQL至结果返回的前台时间，包含解析、快照、匹配/改写、计划检查、执行、结果归档、日志和FAD提交。普通组只执行SQL。后台准备不串行相加，后台与查询同时运行造成的争用已体现在查询实测时间中；末尾清理单列。', '',
            f"来源间隔合计{timing['total_wait_seconds']:.3f}秒，记录后复用；只实际运行查询和后台工作，剩余空闲跳过。后台超过间隔时下一条查询仍按时执行。时间提取依据：{safe(timing['timing_basis'])}；客户端如有并发提交，以原串行MCP服务边界记录间隔，不把排队当作优化空闲窗口。",'',
            '### 实际利用了多少FAD','',
            '| 配对 | 后台处理了多少轮FAD | 其中格式通过 | 其中包含未来访问预测 | 通过的候选访问包数 |',
            '|---|---:|---:|---:|---:|']
    for c in counts:lines.append(f"| {c['pair']} | {c['processed_rounds']}/{n} | {c['accepted_rounds']} | {c['nonempty_rounds']} | {c['accepted_candidates']} |")
    lines+=['','一个候选访问包可以同时描述表、列、过滤、分组和聚合；上表按完整访问包计数。Q26、Q27的FAD各把两个过滤条件直接并列填写，未按Schema写出明确的AND/OR关系，因此未被接收。原始输入和拒绝原因均保留，未根据新轨迹修改接收规则。Q33明确表示没有后续访问，格式通过但没有预测。','',
            f'直接使用提前准备对象的SQL共{len(reused)}/{review["business_query_calls"]}条业务查询：'+('、'.join(f'[Q{q}](#guided-q{q})' for q in reused) or '无')+'。这是实际优化复用数量，不等于FAD每个字段的预测命中率。','',
            f'共准备{len(objects)}个对象，其中{len(used_objects)}个被后续查询使用。主要收益来自产品×月份、目的地×月份的重复聚合：后续SQL读取已准备的汇总数据，继续执行原有的波动统计、贡献分解和排名计算。','',
            '### 前台和后台各花了多少时间','',
            '| 项目（两次平均，秒） | 普通执行 | 使用FAD |','|---|---:|---:|',
            f"| SQL执行及结果归档 | {metric('baseline','query_seconds'):.3f} | {metric('combined','query_seconds'):.3f} |",
            f"| 前台匹配及改写 | 0 | {metric('combined','rewrite_seconds'):.3f} |",
            f"| 前台计划检查及索引保护 | 0 | {metric('combined','plan_seconds'):.3f} |",
            f"| 其他前台处理 | {b-metric('baseline','query_seconds'):.3f} | {o-sum(metric('combined',k) for k in ('query_seconds','rewrite_seconds','plan_seconds')):.3f} |",
            f"| 后台FAD接收和校验 | 0 | {bg('fad_seconds'):.3f} |",
            f"| 后台构建尝试（含失败） | 0 | {bg('all_build_attempt_seconds'):.3f} |",
            f"| 成功构建 | 0 | {bg('build_seconds'):.3f} |",
            f"| 成功构建中与Agent间隔重叠的部分 | 0 | {bg('build_during_wait_seconds'):.3f} |",
            f"| 成功构建中与查询重叠的部分 | 0 | {bg('build_during_query_seconds'):.3f} |",
            f"| 末尾清理和关闭 | {metric('baseline','tail_cleanup_seconds'):.3f} | {metric('combined','tail_cleanup_seconds'):.3f} |",'',
            f"后台决策总时长（含构建及统计）平均{bg('decision_including_build_seconds'):.3f}秒。重叠时间是成功构建时间的子集，不能重复相加。未使用对象和失败尝试均保留成本。",'',
            '### 对象何时准备、后面哪些SQL用了','',
            'v1.5在已有准入和总预算内连续准备合格对象，每个对象提交并准备好匹配规则后即发布。保留12个汇总方向、2个索引、512MiB空间、300秒后台决策和单次120秒上限；不读取未来SQL或未来间隔。', '',
            '| 对象及存储内容 | 依据的FAD | 构建于哪轮之后 | 第1次构建，秒 | 第2次构建，秒 | 实际使用的SQL（次数/2） |',
            '|---|---|---|---:|---:|---|']
    for name,obj in objects.items():
        durations=[]
        for d in pairs:
            matches=[x for x in d['combined']['measures']['objects'] if x['name']==name]
            durations.append(f"{matches[0]['build_seconds']:.3f}" if matches else '未建成')
        uses=[]
        for i,c in enumerate(timing['calls']):
            num=sum(name in used(d,i) for d in pairs)
            if num:uses.append(f"[Q{c['step']}](#guided-q{c['step']})（{num}/2）")
        lines.append(f"| {names[name]}：{safe(object_description(obj))} | "+'、'.join(f'[Q{x}](#guided-q{x})' for x in obj['source_steps'])+f" | Q{obj['created_after']} | {' | '.join(durations)} | "+('、'.join(uses) or '未使用')+' |')
    for name,obj in objects.items():
        lines+=fold(names[name]+'：实际DDL',obj['ddl'],'sql')
        lines+=fold(names[name]+'：匹配规则及空间',{'pattern':obj['pattern'],'matcher':obj.get('matcher'),'allocated_bytes':obj['allocated_bytes']})
    lines+=['','仍有以下明确的未利用机会，下面是对已完成轨迹的事后分析，没有据此回改本批优化动作：','',
            '- Q4已经预测了华南按月份汇总，但该过滤和分组组合只出现一次，被预设的“两轮FAD重复出现才构建”规则挡住。因此Q5、Q6、Q7及后来的Q23、Q24、Q31仍扫描原表。门槛减少无效准备，也漏掉了这个可复用方向。',
            '- 已有产品×月份汇总表，但当前实现只做相同分组和过滤的替换，没有把它再按月份汇总，也没有对汇总表增加产品过滤来服务Q21。Q13、Q15等省份分析使用字符串截取表达式，当前也没有对应的表达式分组及跨层改写能力。',
            '- 后续FAD逐步增加聚合指标，后台重新构建了同一分组的更完整版本；表中保留了未使用的旧版本及其成本。索引准入统计发现华南匹配37.18%的数据，超过预设10%门槛，因此本批没有建立索引。', '',
            '### 每轮查询的等待时间','',
            '| 轮次 | 普通执行，两次平均秒 | FAD优化，两次平均秒 | 节省秒数 | 实际复用对象 |',
            '|---|---:|---:|---:|---|']
    for i,c in enumerate(timing['calls']):
        values=[]
        for arm in ('baseline','combined'):
            values.append(avg(h.span(d[arm]['timeline']['queries'][i]['arrival_ns'],d[arm]['timeline']['queries'][i]['response_return_ns']) for d in pairs))
        values.append(values[0]-values[1])
        labels=sorted({names[x] for d in pairs for x in used(d,i)})
        lines.append(f"| [Q{c['step']}](#guided-q{c['step']}) | "+' | '.join(f'{v:.3f}' for v in values)+' | '+('、'.join(labels) or ('结束标记' if c['step']==review['closing_no_further_access_step'] else '原表'))+' |')
    lines+=['','上表逐条统计SQL开始处理至结果返回，含前台匹配等处理；节省为负表示该条查询变慢。全部行相加即本批主指标。','',
            '### 新Agent实际做了哪些分析','',
            '| 分析内容 | 对应SQL |','|---|---|']
    for stage in review['analysis_stages']:
        lines.append('| '+stage['stage']+' | '+'、'.join(f'[Q{q}](#guided-q{q})' for q in stage['queries'])+' |')
    lines+=['','月度标准差、变异系数、贡献分解和协方差都有对应SQL。异常检查采用分布及贡献聚合，没有逐运单明细查询。', '',
            'Agent原报告仍有一处没有对应SQL的估计：剔除部分省份后，变异系数可能降至5.0%–5.5%。该数值未经验证，不能作为分析结论的证据。数据库结果一致性核对通过，不代表原报告每个分析判断都已通过质量评分。', '',
            '### 每轮SQL、FAD和实际优化对应关系']
    for i,c in enumerate(timing['calls']):
        q=c['step'];raw=c['arguments'].get('future_access');decoded=raw
        if isinstance(raw,str):
            try:decoded=json.loads(raw)
            except ValueError:decoded=None
        lines+=['',f'<a id="guided-q{q}"></a>',f'#### 新轨迹 Q{q}','',
                f"本轮返回后复用的间隔：{(timing['calls'][i+1]['gap_before_seconds'] if i+1<n else timing['final_gap_seconds']):.3f}秒。",'']
        candidates=decoded.get('candidates',[]) if isinstance(decoded,dict) else []
        if candidates:
            lines+=['| 候选 | 本轮预测 |','|---|---|']
            for j,fc in enumerate(candidates,1):
                try:description=h.description(fc)
                except (KeyError,TypeError,ValueError):description=json.dumps(fc,ensure_ascii=False)
                lines.append(f'| {j} | {safe(description)} |')
        else:lines+=['本轮没有候选访问预测；原始输入见下方。']
        lines+=fold('本轮SQL',c['arguments']['sql'],'sql')
        lines+=fold('本轮原始FAD',raw)
        details=[]
        for d in pairs:
            t=d['combined']['timeline'];record=t['queries'][i]
            details.append({'pair':d['number'],'original_status':c['source_status'],
                            'status':record['status'],'executed_sql':record['executed_sql'],
                            'plan':record['plan'],'rewrite_reasons':record['rewrite_reasons'],
                            'used':record['materializations_used'],
                            'background_events':[e for e in t['background'] if e.get('step')==q]})
        lines+=fold('两次实际执行SQL、计划、FAD接收和后台动作',details)
    lines+=['','### 验证范围和资料','',
            '- 77项测试通过。新轨迹先进行独立完整结果验证，正式两对再次与来源结果核对，并在普通/FAD组之间直接比较全部结果。保留NULL、重复行、排序及原有错误；浮点绝对容差1e-7、相对1e-9。',
            '- 每次使用新数据库副本、新进程/连接，相同完整预热、WAL和两个逻辑CPU，随机AB/BA串行。副本位于/tmp的tmpfs；这不是物理磁盘冷缓存测试。数据已逐行验证，由原18,250行复制及固定种子抽样扩展，分类基数没有随行数同步增长。',
            '- 本次分析要求和优化调度都与上一次13轮不同；本批对照固定的是这个新会话的同一轨迹，不把跨批差异单独归因为轮数。',
            '- 来源Agent使用独立会话、工作目录和本地配置/缓存/状态目录，仅开放DB工具。服务端可能复用输入前缀缓存；未计生成额外FAD的模型延时，空闲跳过不重现长期空闲时的缓存老化。',
            '- 只按用户要求做两对，保留两对完整结果；尚未进行官方答案质量评分。', '',
            f'- [Agent报告]({sl}/answer.md)、[完整提示]({sl}/prompt.txt)、[原始SQL/FAD]({sl}/events.jsonl)、[来源总结]({sl}/summary.json)、[分析轨迹核查]({sl}/analysis-review.json)',
            f'- [本批统计](statistics-async-ten-million-guided.json)、[配置]({rl}/manifest.json)、[审计]({rl}/AUDIT.json)',
            '- [预冻结记录](../async/preflight-v15-ten-million-guided/manifest.json)、[分析要求](../async/task6-analysis-requirements.txt)、[计划](../async/PLAN.md)',
            '', '<!-- GUIDED-TEN-MILLION-END -->','']
    text=out.read_text();start='<!-- GUIDED-TEN-MILLION-START -->';end='<!-- GUIDED-TEN-MILLION-END -->'
    if start in text:text=text[:text.index(start)]+text[text.index(end)+len(end):].lstrip('\n')
    heading='# FAD驱动数据库优化验证结果\n\n';assert text.startswith(heading)
    out.write_text(heading+'\n'.join(lines)+text[len(heading):])
    print(json.dumps({k:v for k,v in stats.items() if k not in ('pairs','per_run')},ensure_ascii=False,indent=2))


if __name__=='__main__':main()
