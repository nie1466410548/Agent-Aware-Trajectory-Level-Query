"""Rebuild transparent metrics from the eight preserved episodes. No model calls.

First run agent_db_tool.matching on every episode with the benchmark venv.
Then: python benchmark/dacomp/tool-prototype/v0.2/summarize.py
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ('tables','columns','filters','joins','group_by','aggregations')


def ratio(n, d):
    return f'{n}/{d}（{n/d:.1%}）' if d else '—'


def main():
    data=[]
    for cohort in ('01','02'):
        for task in ('003','004','005','006'):
            p=ROOT/'runs'/f'dacomp-{task}-{cohort}'
            detail=json.loads((p/'matching/detail.json').read_text())
            runtime=json.loads((p/'summary.json').read_text())
            tool=json.loads((p/'tool-report.json').read_text())
            events=[json.loads(s) for s in (p/'events.jsonl').read_text().splitlines()]
            reqs=[e for e in events if e['record']=='request']
            errors=Counter()
            for r in reqs:
                labels=set()
                if isinstance(r['arguments'].get('future_access'),str):labels.add('FAD为字符串')
                for error in r['hint_errors']:
                    msg=error['message'];path=error.get('path','')
                    if 'Missing referenced columns' in msg:labels.add('漏列操作引用列')
                    elif 'Unknown or ambiguous catalog identifier' in msg:labels.add('名称不存在或歧义')
                    elif 'is not of type' in msg and path.endswith('columns'):labels.add('columns类型错误')
                    elif not isinstance(r['arguments'].get('future_access'),str):labels.add('其他结构/状态错误')
                errors.update(labels)
            column_counts=Counter();ever=Counter();latest=Counter();delivered=Counter()
            for q,features in detail['sql_features'].items():
                step=int(q)
                prefixes=[r['step_id'] for r in reqs if r['step_id']<step]
                if not prefixes:continue
                prior=[r for r in detail['rows'] if r['step']<step]
                last=max(prefixes)
                for column in features['columns']:
                    column_counts[column]+=1
                    matching=[r for r in prior if column in r['fields']['columns']['predicted_items']]
                    ever[column]+=bool(matching)
                    latest[column]+=any(r['step']==last for r in matching)
                    delivered[column]+=any(r['step']==last and r['accepted'] for r in matching)
            unsupported=Counter(x['kind'] for q in detail['sql_features'].values() for x in q['unsupported'])
            d={k:v for k,v in detail.items() if k not in ('rows','sql_features','query_coverage')}
            d.update(name=p.name,cohort=cohort,runtime=runtime,error_call_categories=dict(errors),
                     unsupported_expression_occurrences=dict(unsupported),
                     priority_counts=dict(Counter(r['priority'] for r in detail['rows'])),
                     likelihood_counts=dict(Counter(r['likelihood'] or 'omitted' for r in detail['rows'])),
                     high_frequency_columns=[{'column':c,'actual_queries':n,'ever_predicted_queries':ever[c],
                         'latest_predicted_queries':latest[c],'latest_delivered_queries':delivered[c]}
                         for c,n in column_counts.most_common(8)],
                     mean_hint_validation_ms=sum(r.get('hint_validation_ms',0) for r in reqs)/len(reqs),
                     usage={k:tool[k] for k in ('reported_token_sums','cache_read_tokens','cache_write_tokens')})
            data.append(d)
    (ROOT/'metrics.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    lines=['# v0.2完整统计','',
        '01为首轮；02为补充完整调用格式示例后的第二轮。未更换原题、模型、数据库、80次SQL预算或600秒时限。',
        '每个题每个条件只有一次运行；同一候选在多轮重复出现，计数相关，不能当成独立样本。',
        '生成脚本：`summarize.py`；底层逐轮分析：`agent_db_tool/matching.py`。','',
        '## 调用与格式','',
        '| 运行 | SQL成功/尝试 | FAD校验通过/调用 | 接受的非空FAD | 多候选调用 | 原始候选数 | 报告提交 |',
        '|---|---|---|---|---|---|---|']
    for d in data:
        r=d['runtime'];name=d['name']
        lines.append(f"| [{name}](runs/{name}/matching/PER-ROUND.md) | {r['successful_queries']}/{r['query_attempts']} | {ratio(r['query_attempts']-r['invalid_hints'],r['query_attempts'])} | {r['provided_hints']} | {d['multi_candidate_calls']} | {d['candidates']} | {'是' if r['answer_submitted'] else '否'} |")
    for category,title in [('matching','原始内容：已填写字段后来有没有发生'),('accepted_matching','只看数据库接受的候选')]:
        lines+=['',f'## {title}','',
            '分母为有具体项的候选次数，分子为该字段的全部具体项能在某一条严格后续成功SQL中找到的次数。不同字段可命中不同查询；这不是完整候选准确率。',
            'known分组要求同一SQL作用域中完整维度集合一致，partial只要求已填维度包含其中。partial连接允许后续SQL增加等值条件。过滤只比较已知条件单项。','',
            '| 运行 | 表 | 列 | 已知过滤项 | 连接 | 分组 | 聚合 |','|---|---|---|---|---|---|---|']
        for d in data:
            vals=[ratio(d[category][f].get('candidates_hit',0),d[category][f].get('candidates_with_items',0)) for f in FIELDS]
            lines.append('| '+d['name']+' | '+' | '.join(vals)+' |')
    lines+=['','## 实际查询中的操作，有多少曾被提前提到','',
        '每条成功SQL中去重计数各操作单项，排除没有任何此前请求的首条查询。分子为任一更早FAD曾提到的项，包含原始可审核但未接受的内容。',
        '这衡量曾经预见，不表示数据库在执行该SQL之前仍持有这些项。连接覆盖使用包含全部等值条件的完整连接模式，只有部分连接键不算完整覆盖。复杂SQL表达式无法识别的部分不在分母里，限制见下表。','',
        '| 运行 | 列 | 过滤项 | 连接 | 分组维度 | 聚合项 |','|---|---|---|---|---|---|']
    for d in data:
        vals=[ratio(d['coverage'][f].get('ever_predicted',0),d['coverage'][f].get('actual_items',0)) for f in FIELDS[1:]]
        lines.append('| '+d['name']+' | '+' | '.join(vals)+' |')
    lines+=['','## 最近一份有效快照覆盖了多少实际操作','',
        '只使用当前SQL之前的最后一次调用所提交并通过校验的FAD；最后一次无效或空提示会清空快照，不能沿用更早预测。这里仍仅比较操作单项。','',
        '| 运行 | 列 | 过滤项 | 连接 | 分组维度 | 聚合项 |','|---|---|---|---|---|---|']
    for d in data:
        vals=[ratio(d['coverage'][f].get('latest_delivered',0),d['coverage'][f].get('actual_items',0)) for f in FIELDS[1:]]
        lines.append('| '+d['name']+' | '+' | '.join(vals)+' |')
    lines+=['','## 状态与格式错误','']
    for d in data:
        lines += [f"### {d['name']}",'',
            '错误调用分类（可重叠）：'+json.dumps(d['error_call_categories'],ensure_ascii=False),'',
            '| 字段 | known | partial | unknown | none | 未写状态的旧数组 |','|---|---|---|---|---|---|']
        for f in FIELDS[1:]:
            s=d['field_states'][f]
            lines.append('| '+f+' | '+' | '.join(str(s.get(k,0)) for k in ('known','partial','unknown','none','unspecified'))+' |')
    lines+=['','## 高频列是否提前说过','',
        '实际次数为首条查询之后访问该列的成功SQL条数；“曾说过”包括离线可解码的原始内容，“最近有效快照”仅包括数据库实际接受内容。这里只按columns.items统计，joins等操作字段里的引用不自动补算进列清单。','',
        '| 运行 | 高频列 | 实际访问次数 | 曾提前提到 | 上一轮提到 | 最近有效快照提到 |','|---|---|---|---|---|---|']
    for d in data:
        for c in d['high_frequency_columns']:
            lines.append(f"| {d['name']} | {c['column']} | {c['actual_queries']} | {c['ever_predicted_queries']} | {c['latest_predicted_queries']} | {c['latest_delivered_queries']} |")
    lines+=['','## 解析范围与开销','',
        'SQLGlot识别原始列、strftime年/月/日分组、常见简单聚合、已知WHERE条件单项和ON等值连接。CASE分组、聚合后的再聚合、比值、窗口语义、HAVING、复杂条件及连接暂不作完整等价判断。',
        '所有运行SQL解析失败数及具体未支持表达式保存在各运行detail.json。SQLITE_READ列引用不受这些表达式识别限制影响。',
        '耗时为四题并发运行时的观测值，不用于性能比较。token字段按服务原口径保存，可能含重叠项，不能当作FAD增量成本。','',
        '| 运行 | SQL解析失败 | 候选无法分析 | 未支持表达式次数（按类别） | 运行秒数 | 平均提示校验毫秒 |','|---|---|---|---|---|---|']
    for d in data:
        lines.append(f"| {d['name']} | {len(d['parse_errors'])} | {d['unparsed_candidates']} | {json.dumps(d['unsupported_expression_occurrences'],ensure_ascii=False)} | {d['runtime']['duration_s']:.1f} | {d['mean_hint_validation_ms']:.2f} |")
    (ROOT/'METRICS.md').write_text('\n'.join(lines)+'\n')
    print('Wrote',ROOT/'METRICS.md','and metrics.json')


if __name__=='__main__':main()
