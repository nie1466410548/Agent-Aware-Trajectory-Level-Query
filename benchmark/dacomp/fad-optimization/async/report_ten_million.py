"""Render new ten-million-row results into the one report, retaining prior sections."""
import argparse
import importlib.util
import json
from pathlib import Path
spec=importlib.util.spec_from_file_location('report_helpers',Path(__file__).with_name('report.py'))
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
read=h.read;med=h.med;span=h.span


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    root=Path(a.run);out=Path(a.output);manifest=read(root/'manifest.json');timing=read(manifest['timing']);audit=read(root/'AUDIT.json')
    assert audit['all_passed'] and read(root/'COMPLETE.json')['pairs']==5
    profile=read(Path(manifest['database']).with_suffix('.manifest.json'));assert profile['output_profile']['rows']==10000000
    source=Path(timing['source_run']);n=len(timing['calls']);success=sum(c['source_status']=='ok' for c in timing['calls'])
    pairs=[]
    for pdir in sorted(root.glob('pair-*')):
        d={}
        for arm in ['baseline','combined']:
            s=read(pdir/arm/'summary.json');t=read(pdir/arm/'timeline.json')
            assert read(pdir/arm/'correctness.json')['all_equal'] and s['query_attempts']==n and s['query_successes']==success
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
    names={};counts={}
    for o in objects:
        kind='索引' if o['kind']=='index' else '汇总表';counts[kind]=counts.get(kind,0)+1;names[o['name']]=kind+str(counts[kind])
    for d in pairs:
        t=d['combined']['timeline'];vs={e['step']:e for e in t['background'] if e['type']=='fad_validated'}
        assert vs.keys()==vals.keys()
        assert all(vs[q]['fad']==e['fad'] and vs[q]['audit']==e['audit'] for q,e in vals.items())
    # Availability may vary when builds overlap queries; don't assume all five
    # use identical objects or rewrites. Each SQL's actual plan is retained.
    all_objects={o['name']:o for d in pairs for o in d['combined']['measures']['objects']}
    for name,o in all_objects.items():
        if name not in names:
            kind='索引' if o['kind']=='index' else '汇总表';counts[kind]=counts.get(kind,0)+1;names[name]=kind+str(counts[kind])
    reused_steps=[q['step'] for i,q in enumerate(timeline['queries']) if any(
        name in str(d['combined']['timeline']['queries'][i]['plan']) for name in all_objects for d in pairs)]
    accepted=sum(e['fad'] is not None for e in vals.values())
    nonempty=sum(bool(e['fad'] and e['fad']['candidates']) for e in vals.values())
    candidate_count=sum(len(e['fad']['candidates']) for e in vals.values() if e['fad'])
    saved=med(d['saved_seconds'] for d in pairs);pct=med(d['saved_percent'] for d in pairs)
    stats={'source_run':timing['source_run'],'database_rows':10000000,'calls':n,'successful_queries':success,
           'primary_metric':'sum_of_SQL_arrival_to_response_seconds','accepted_rounds':accepted,'nonempty_rounds':nonempty,'accepted_candidates':candidate_count,
           'baseline_database_seconds':metric('baseline','database_request_seconds'),'fad_database_seconds':metric('combined','database_request_seconds'),
           'median_saved_seconds':saved,'median_saved_percent':pct,
           'pairs':[{k:v for k,v in d.items() if k not in ('baseline','combined')} for d in pairs],
           'per_run':[{arm:{'summary':d[arm]['summary'],'measures':d[arm]['measures']} for arm in ('baseline','combined')} for d in pairs]}
    (out.parent/'statistics-async-ten-million.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n')
    qt=lambda arm,i:med(d[arm]['timeline']['queries'][i]['query_seconds'] for d in pairs)
    rt=lambda arm,i:med(span(d[arm]['timeline']['queries'][i]['arrival_ns'],d[arm]['timeline']['queries'][i]['response_return_ns']) for d in pairs)
    source_link=f'../async/{source.name}';run_link=f'../async/runs/{root.name}'
    lines=['<!-- TEN-MILLION-START -->','## DAComp-006：1,000万行，独立新Agent轨迹','',
           f"**Agent等待数据库的累计时间：普通 {metric('baseline','database_request_seconds'):.3f} 秒 → 使用FAD {metric('combined','database_request_seconds'):.3f} 秒（两组各五次中位数）。每对节省 {min(d['saved_seconds'] for d in pairs):+.3f}～{max(d['saved_seconds'] for d in pairs):+.3f} 秒，节省比例中位数 {pct:+.2f}%。**",'',
           f"直接复用的典型查询：[Q8](#ten-million-q8)按城市、月份汇总订单数和利润，SQL执行由{qt('baseline',7):.3f}秒降至{qt('combined',7):.4f}秒，{timeline['queries'][7]['row_count']}行结果一致。整条任务的收益按全部{n}条SQL累计计算。",'',
           f'数据库从原18,250行扩为10,000,000行；独立新会话实际生成{n}次SQL调用，{success}次成功。没有沿用旧30轮或13轮SQL。两组固定回放这一次生成的相同SQL/FAD，调用间隔合计{timing["total_wait_seconds"]:.3f}秒，记录后复用，剩余空闲直接跳过。', '',
           '主指标为每条SQL开始被数据库工具处理至结果返回的累计时间，包含解析、快照、匹配/改写、SQL执行、结果归档、日志和FAD提交的前台开销。后台准备单独计时，已经被Agent间隔覆盖的工作不重复扣除；构建超过间隔时，下一条查询仍按时到达，并发争用由实际查询计时体现。末尾清理另列。', '',
           '本次Agent曾并发提交Q8～Q10、Q11～Q12，原MCP工具实际串行处理。间隔取数据库请求/完成日志中的服务边界，排队的查询紧接上一条执行，间隔仅约3～7毫秒。原始客户端时间戳保留，不把排队时间变成后台优化窗口，也不把重叠调用的排队等待重复相加。优化策略冻结后只补充了这一时间提取兼容处理；策略和预算未改。', '',
           '### 五对数据库等待时间','',
           '单位秒。节省=普通−使用FAD，比例以各对普通耗时为分母；先配对计算，再取中位数。','',
           '| 配对 | 普通执行 | 使用FAD | 节省 | 节省比例 | 加清理后的节省 |','|---|---:|---:|---:|---:|---:|']
    for i,d in enumerate(pairs,1):
        b,o=[d[x]['summary'] for x in ['baseline','combined']]
        lines.append(f"| {i} | {b['database_request_seconds']:.3f} | {o['database_request_seconds']:.3f} | {d['saved_seconds']:+.3f} | {d['saved_percent']:+.2f}% | {d['saved_including_cleanup_seconds']:+.3f} |")
    lines+=['',f"使用FAD更快：{sum(d['saved_seconds']>0 for d in pairs)}/5对；节省范围{min(d['saved_seconds'] for d in pairs):+.3f}～{max(d['saved_seconds'] for d in pairs):+.3f}秒。{n*10}次来源结果核对和{n*5}次两组直接比较全部通过。",'',
            f'每次收到{n}份FAD；{accepted}份通过接收，{nonempty}份包含候选，共接受{candidate_count}个候选。实际直接使用提前准备对象的SQL为'+('、'.join(f'[Q{x}](#ten-million-q{x})' for x in reused_steps) or '无')+f'，共{len(reused_steps)}/{n}条。这是数据库实际复用数量，与FAD单项预测命中率不是同一个指标。','',
            '### 时间花在哪里','',
            '| 耗时组成（五次中位数，秒） | 普通 | 使用FAD |','|---|---:|---:|',
            f"| SQL执行与结果归档 | {metric('baseline','query_seconds'):.3f} | {metric('combined','query_seconds'):.3f} |",
            f"| 前台匹配、原SQL必要预检及改写 | 0 | {metric('combined','rewrite_seconds'):.3f} |",
            f"| 实际计划检查及索引保护 | 0 | {metric('combined','plan_seconds'):.3f} |",
            f"| 其他前台处理 | {med(d['baseline']['summary']['database_request_seconds']-d['baseline']['summary']['query_seconds'] for d in pairs):.3f} | {med(d['combined']['summary']['database_request_seconds']-sum(d['combined']['summary'][k] for k in ('query_seconds','rewrite_seconds','plan_seconds')) for d in pairs):.3f} |",
            f"| 后台FAD接收、校验 | 0 | {bg('fad_seconds'):.3f} |",
            f"| 后台实际对象构建 | 0 | {bg('build_seconds'):.3f} |",
            f"| 构建中与Agent间隔重叠的部分 | 0 | {bg('build_during_wait_seconds'):.3f} |",
            f"| 构建中与查询处理重叠的部分 | 0 | {bg('build_during_query_seconds'):.3f} |",
            f"| 末尾停止、清理及关闭 | {metric('baseline','tail_cleanup_seconds'):.3f} | {metric('combined','tail_cleanup_seconds'):.3f} |",'',
            '构建重叠两行是构建耗时的子集，不能与整列相加。后台决策总时长（包含构建、统计等）中位数为'+f"{bg('decision_including_build_seconds'):.3f}秒。各项独立取中位数，分项相加不一定等于总时间中位数。",'',
            '### 本次优化实现','',
            '在查看新轨迹内容之前冻结了v1.4策略：汇总匹配规则后台预编译；相同过滤和分组的已收到聚合指标合并准备，增补版本不占新的方向名额；最多12个汇总方向，仍受512MiB总空间和时间预算约束。汇总表直接一次扫描构建，以SQLite页数上限保护空间，省去此前重复的聚合估计扫描。', '',
            '聚合预测准备汇总表。明细预测才尝试含明确投影列的索引，首列过滤匹配比例须在0～10%；重复过滤统计缓存。当前查询计划如果选择需要大量回表的FAD索引，则回退原表；既有浮点舍入保护保留。所有动作来自已到达的FAD和当前数据库统计，优化器不接收未来SQL或未来间隔。', '',
            '### 每个对象的触发、准备时间和实际使用','',
            '只统计实际建成次数；同一对象在不同配对的就绪时机会变化。构建和使用次数按五次使用FAD回放统计。','',
            '| 对象 | 依据的FAD轮次 | 构建于哪轮之后 | 建成次数 | 构建耗时中位数，秒 | 实际使用的查询（采用次数/5） |','|---|---|---|---:|---:|---|']
    for name,obj in all_objects.items():
        os=[o for d in pairs for o in d['combined']['measures']['objects'] if o['name']==name]
        uses=[]
        for i,q in enumerate(timeline['queries']):
            count=sum(name in str(d['combined']['timeline']['queries'][i]['plan']) for d in pairs)
            if count:uses.append(f"[Q{q['step']}](#ten-million-q{q['step']})（{count}/5）")
        lines.append(f"| {names[name]} | "+'、'.join(f'Q{x}' for x in obj['source_steps'])+f" | Q{obj['created_after']} | {len(os)} | {med(o['build_seconds'] for o in os):.3f} | "+('、'.join(uses) or '未使用')+' |')
    for name,obj in all_objects.items():
        lines+=['',f"<details><summary>{names[name]}：实际DDL和匹配规则</summary>",'','```sql',obj['ddl'],'```','',
                '```json',json.dumps({'pattern':obj['pattern'],'matcher':obj.get('matcher'),'created_after':obj['created_after'],'source_steps':obj['source_steps'],'allocated_bytes':obj['allocated_bytes']},ensure_ascii=False,indent=2),'```','','</details>']
    lines+=['','未使用或未及时就绪的对象也计入后台资源与清理，不算作复用收益。','',
            '### 每轮SQL与前台等待时间','',
            '| 轮次 | 普通整轮处理，秒 | 使用FAD整轮处理，秒 | 普通SQL执行，秒 | 使用FAD的SQL执行，秒 | 实际复用对象 |','|---|---:|---:|---:|---:|---|']
    for i,q in enumerate(timeline['queries']):
        used=sorted({names[name] for name in all_objects if any(name in str(d['combined']['timeline']['queries'][i]['plan']) for d in pairs)})
        lines.append(f"| [Q{q['step']}](#ten-million-q{q['step']}) | {rt('baseline',i):.3f} | {rt('combined',i):.3f} | {qt('baseline',i):.3f} | {qt('combined',i):.3f} | "+('、'.join(used) or '原表/原有错误')+' |')
    if source.name=='source-ten-million-01' and n==13:
        lines+=['','### 为什么有预测，却没有全部转成加速','',
                '这次47个候选中，同一预测会随多轮SQL重复更新。建出的对象数量和实际提速的查询数量，不能与47直接等同。下面区分预测本身缺的信息和当前优化器的限制。','',
                '| 查询 | 本次没有复用的具体原因 |','|---|---|',
                '| Q1～Q3 | 起初没有更早的可用对象；Q1/Q2的过滤范围仍为unknown。 |',
                '| Q4（月度收支） | Q1/Q2预测了月度指标，但华南过滤值未定；本版只为过滤条件完整的预测建汇总表。 |',
                '| Q5（产品收支） | 已建产品汇总表缺少实际SQL中的运费、仓储费和其他运营成本三个SUM。不能用不完整结果替代整条查询。 |',
                '| Q6（月×产品利润） | 预测已给出，但每轮最多构建一个对象，排在其他方向后面；对应对象到Q6结束后才构建。这是当前调度限制。 |',
                '| Q7（全表区域×月） | 实际按Destination截取的区域分组、访问全表；已有预测主要是华南完整Destination分组。 |',
                '| Q9（月×产品收支） | 同分组的已建汇总表缺少销量、收入、成本的SUM；产品维度的另一个表没有月份，不能补齐。 |',
                '| Q10（月度量价） | 月度方向缺少完整、可构建的预测，所需销量和单价聚合也未在该方向完整给出。 |',
                '| Q11/Q12（年龄、性别×月） | FAD只写了年龄/性别分组，实际SQL还加了月份；已有表已丢掉月度信息。 |',
                '| Q13（省份条件聚合） | 实际SUM(CASE WHEN …)没有对应的提前汇总规则，本版也不支持从城市汇总安全转换这种条件聚合。 |','',
                'Q8的过滤、月份和城市分组、COUNT(*)、SUM(Profit)与提前准备的对象一致，所以能直接读取小汇总表。未利用对象的构建和清理仍保留在统计中；Q6错过的机会也没有被记为收益。']
    for i,c in enumerate(timing['calls']):
        q=c['step'];r=timeline['queries'][i];e=vals[q];d=decisions[q]
        gap=timing['calls'][i+1]['gap_before_seconds'] if i+1<n else timing['final_gap_seconds']
        lines+=['',f'<a id="ten-million-q{q}"></a>',f'#### 千万行 Q{q}','',
                f"整轮等待：普通{rt('baseline',i):.3f}秒→使用FAD {rt('combined',i):.3f}秒。本轮后复用间隔{gap:.3f}秒。",'']
        raw=c['arguments'].get('future_access');decoded=json.loads(raw) if isinstance(raw,str) else raw
        cs=decoded.get('candidates',[]) if isinstance(decoded,dict) else []
        if cs:
            lines+=['| 候选 | 本轮实际预测 |','|---|---|']
            for j,fc in enumerate(cs,1):lines.append(f'| {j}（{fc["priority"]}） | {h.safe(h.description(fc))} |')
        else:lines+=['本轮未提供候选访问预测。']
        plans=[{'pair':j,'executed_sql':x['combined']['timeline']['queries'][i]['executed_sql'],'plan':x['combined']['timeline']['queries'][i]['plan'],'used':x['combined']['timeline']['queries'][i]['materializations_used']} for j,x in enumerate(pairs,1)]
        for title,lang,value in [('原始SQL','sql',r['sql']),('各对实际SQL和执行计划','json',json.dumps(plans,ensure_ascii=False,indent=2)),('原始FAD、接收与后台动作（第1对）','json',json.dumps({'raw':raw,'audit':e['audit'],'fad':e['fad'],'actions':d['actions']},ensure_ascii=False,indent=2))]:
            lines+=['',f'<details><summary>{title}</summary>','',f'```{lang}',value,'```','','</details>']
    lines+=['','### 独立性、正确性和适用范围','',
            f'- [新来源会话]({source_link}/summary.json)使用独立进程、Session ID、工作目录及本地配置/数据/缓存/状态目录。模型为{timing["model"]}；没有给Agent旧SQL/FAD或报告。采集时仅正常执行SQL，未启用数据库优化。',
            '- 数据逐行校验血缘：547份完整复制和17,250行固定种子抽样，新增运单号唯一，原有53个重复运单号保留。行数增长，日期范围、产品和目的地类别未同比增长；这是扩容可行性实验。',
            '- 两组每次新数据库副本、新进程/连接，相同完整预热、WAL与缓存设置，两个相同逻辑CPU，随机AB/BA串行。副本位于/tmp的tmpfs；不代表物理磁盘或冷缓存结果。',
            f'- 优化相关68项测试和新增3项排队调用时间测试通过；新轨迹独立验证和正式{n*10}次来源核对、{n*5}次两组直接比较通过。核对NULL、重复行和排序；浮点绝对1e-7、相对1e-9。',
            '- 原始SQL、FAD、客户端间隔、数据和代码哈希冻结。后台对象提交后才可见；索引及汇总表的实际使用均有计划和时间戳证据。',
            '- 主结论只针对这条新轨迹。之前18,250行30轮和百万行13轮是不同来源，本次优化实现也升级，不能把跨批时间差解释成单纯的数据规模收益。',
            '- 未计额外生成FAD的模型延时；服务端可能复用输入前缀缓存。复用的间隔包含模型服务、客户端和其他工具活动，只模拟时间，不复现模型资源竞争；空闲跳过不重现长期空闲的缓存老化。',
            '- 后台工作被覆盖仍有资源成本；本报告记录所有已建对象及未复用情况。只用五对进行初步验证，不据此声称所有任务都能提速。','',
            f'- [数据生成和逐行校验](../data/synthetic-10000000.manifest.json)、[新SQL/FAD]({source_link}/events.jsonl)、[客户端事件]({source_link}/agent.jsonl)',
            f'- [固定间隔](../async/{Path(manifest["timing"]).name})、[本批统计](statistics-async-ten-million.json)、[正式配置]({run_link}/manifest.json)、[审计]({run_link}/AUDIT.json)',
            '- [策略预冻结记录](../async/preflight-v14-ten-million/manifest.json)、[串行服务时间提取补充记录](../async/preflight-v14-ten-million-queued-service/manifest.json)、[实验计划](../async/PLAN.md)','',
            '<!-- TEN-MILLION-END -->','']
    text=out.read_text();start='<!-- TEN-MILLION-START -->';end='<!-- TEN-MILLION-END -->'
    if start in text:text=text[:text.index(start)]+text[text.index(end)+len(end):].lstrip('\n')
    heading='# FAD驱动数据库优化验证结果\n\n';assert text.startswith(heading)
    out.write_text(heading+'\n'.join(lines)+text[len(heading):])
    print(json.dumps({k:v for k,v in stats.items() if k not in ('pairs','per_run')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
