"""Validate reviewed hypotheses and report opportunity families, not syntax matches.

This is a reproducible audit of a manual catalogue, not an exhaustive optimizer.
No benchmark executions or database changes are performed.
"""
import collections
import json
from pathlib import Path
import sqlglot
from sqlglot import exp
from opportunity_catalog import CANDIDATES

ROOT=Path(__file__).resolve().parents[1]


def validate_candidate(c, runs):
    run=runs[c['group'],c['task']]
    assert c['tier'] in {'A','B'}
    assert len(c['members'])>=2 and c['members']==sorted(set(c['members'])),c['id']
    assert set(c['partial'])<=set(c['members'])
    consumers=[]
    for n in c['members']:
        q=run['queries'][n-1]
        assert q['success'] and not q['metadata'],(c['id'],n)
        assert q['database']==c['database'],(c['id'],n,'different database')
        trees=[t for t in sqlglot.parse(q['sql'],read=q['dialect']) if t is not None]
        tables=set()
        for tree in trees:
            ctes={x.alias_or_name.lower() for x in tree.find_all(exp.CTE)}
            tables|={t.name.lower() for t in tree.find_all(exp.Table) if t.name.lower() not in ctes}
        assert tables & set(c['tables']),(c['id'],n,'no candidate input')
        file=next((run['directory']/'sql').glob(f'{n:03d}-*.sql'))
        assert file.read_text().strip()==q['sql'].strip()
        consumers.append(dict(number=n,call_id=q['call_id'],sql_file=str(file.relative_to(ROOT)),
            sql=q['sql'],tables=sorted(tables),statement_count=len(trees),partial=n in c['partial']))
    return dict(c,consumers=consumers,consumer_count=len(consumers),
                later_count=len(consumers)-1,task_passed=run['summary']['validator_passed'])


def stats(candidates, runs, group, tier=None):
    cs=[c for c in candidates if c['group']==group and (tier is None or c['tier']==tier)]
    covered={(c['task'],n) for c in cs for n in c['members']}
    later={(c['task'],n) for c in cs for n in c['members'][1:]}
    total=sum(sum(q['success'] and not q['metadata'] for q in r['queries'])
              for (g,t),r in runs.items() if g==group)
    return dict(families=len(cs),tasks=len({c['task'] for c in cs}),covered_calls=len(covered),
        covered_fraction=len(covered)/total,later_calls=len(later),
        families_with_two_later=sum(c['later_count']>=2 for c in cs),successful_calls=total)


def main():
    runs={}
    for path in sorted((ROOT/'runs').glob('*/*/*/quick-01/analysis.json')):
        r=json.loads(path.read_text());r['directory']=path.parent
        runs[r['summary']['group'],r['summary']['task_id']]=r
    assert len(runs)==18
    assert len({c['id'] for c in CANDIDATES})==len(CANDIDATES)
    cs=[validate_candidate(c,runs) for c in CANDIDATES]
    summary={g:{t:stats(cs,runs,g,None if t=='all' else t) for t in ['A','B','all']} for g in ['natural','fad']}
    output=dict(method='manual trajectory review + source/schema-reference checks; not exhaustive, not performance validation',
                summary=summary,candidates=cs)
    (ROOT/'reports/opportunities.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    lines=['# 轨迹内多查询优化机会：重新分析','','本版替代之前的结构相似性报告。目标是找出：**在一个任务内，做一次具体准备，可能让哪些后续 SQL 少做重复工作？** 已逐条审阅自然组与 FAD 组的 18 条轨迹；没有重跑 Agent，也没有执行候选物化、索引或性能实验。', '',
      '## 先读结论', '',
      '自然组识别出 **5 个公共对象候选，分布在 5/9 个任务，涉及 20/65 次成功数据调用（30.8%）**。另有 3 个较弱的扫描统计准备候选。FAD 组识别出 **6 个公共对象候选，分布在 5/9 个任务，涉及 15/42 次调用（35.7%）**，另有 1 个扫描统计准备候选。', '',
      '**这些是人工审阅在明确口径下找到的候选，不是已证明的优化数量或可节省成本比例，也不是所有优化机会的穷尽枚举。** 不再以同表、同名列、COUNT(*) 或相似 Join 文本的频次替代优化机会。', '',
      '## 计数口径', '',
      '- **A：公共对象候选。** 能指出同一输入上的公共筛选、正确区分连接类型/键的公共 Join、相同派生计算或明确包含的共同窗口，并说明后续 SQL 如何使用。只提出有依据的改写方向，未执行等价性或成本验证。',
      '- **B：扫描统计准备候选。** 同一完整输入需要多项统计，可以考虑一次扫描分别准备所需状态。其证据主要是共享扫描，弱于公共子计算；不把不同分组的同名聚合当作可复用状态。B 单列，不混入 A 的主结论。',
      '- **一个候选是一套共同准备方案，不是查询对。** 同一方案的筛选、Join、派生列可分层准备，按一个候选计数；不同连接语义的准备分开计数。此划分是分析约定，换一种物理设计可能合并或拆分候选，因此原始候选数不是稳定的工作负载属性。',
      '- **涉及 m 次调用**：若在首次使用前准备，可服务这 m 次调用中的全部或部分子计算。**首次使用后还剩 m−1 次**：若等第一次调用时才构建/保留准备对象，可服务的后续次数上限；不是第一次最终结果天然可复用的证明。',
      '- 只算同一任务、同一组、同一数据库内的跨调用机会。Q 编号对应原 sql/NNN 文件，保留元数据编号空档。自然组 65 次成功数据调用含 66 条语句，FAD 组 42 次含 44 条。UNION 分支和一次调用的多条语句不另算未来调用。',
      '- 覆盖率按 (任务, call_id) 去重；一条调用可仅有一个子查询受益。覆盖率不是省掉整条 SQL 的比例。使用完整轨迹事后识别，尚未验证在候选首次出现前 FAD 是否已提供足够信息。', '',
      '## 两组分别汇总', '',
      '| 组别 / 类别 | 候选方案 | 涉及任务 / 9 | 涉及成功调用 | 首次使用后剩余调用（去重） | 首次后仍有至少 2 次使用的方案 |',
      '|---|---:|---:|---:|---:|---:|']
    for g in ['natural','fad']:
        for t in ['A','B','all']:
            v=summary[g][t]
            lines.append(f"| {g} / {t} | {v['families']} | {v['tasks']} | {v['covered_calls']}/{v['successful_calls']} ({v['covered_fraction']:.1%}) | {v['later_calls']} | {v['families_with_two_later']} |")
    lines+=['','A+B 合计仅作候选清单规模说明；两组任务相同但轨迹不同，不能用覆盖率差异估计 FAD 的因果效果。','',
      '## 按任务看：自然组', '', '| 任务 | 答案验证 | 成功数据调用 | A 候选 | B 候选 | A 覆盖调用 | 初步判断 |','|---|---|---:|---|---|---:|---|']
    decisions={
      'bookreview/query1':'正则提取重复两次；仅一个额外消费者，表很小。',
      'bookreview/query2':'共同类别筛选覆盖多次探索及最终读取；一次调用仅部分受益。',
      'bookreview/query3':'主要是诊断扫描；未把不同类别 LIKE 写法和样本/全量读取当作强候选。',
      'crmarenapro/query8':'Owner Assignment 子集有六次使用，是较清楚的多消费者候选。',
      'crmarenapro/query12':'五次调用共享原始键 Join，但日期口径不同，结果复用不能直接成立。',
      'crmarenapro/query13':'相同订单窗口和明细 Join 覆盖三次调用；另有商机扫描统计候选。',
      'stockindex/query1':'仅一个业务分析调用；DISTINCT 指数和业务扫描不足以认定具体公共准备。',
      'stockindex/query2':'主要为样本、指数枚举和一次读取；未找到本口径下 A/B 候选。',
      'stockindex/query3':'完整读取后转 Python；同表重访存在，未纳入泛化全表缓存候选。'}
    def links(cs):return '、'.join(f"[{c['id']}](OPPORTUNITY_CASES.md#{c['id'].lower()})" for c in cs) or '—'
    for task in sorted(t for g,t in runs if g=='natural'):
        rr=runs['natural',task];items=[c for c in cs if c['group']=='natural' and c['task']==task]
        ac=[c for c in items if c['tier']=='A'];bc=[c for c in items if c['tier']=='B']
        n=sum(q['success'] and not q['metadata'] for q in rr['queries']);cover=len({m for c in ac for m in c['members']})
        lines.append(f"| {task} | {'通过' if rr['summary']['validator_passed'] else '未通过'} | {n} | {links(ac)} | {links(bc)} | {cover} | {decisions[task]} |")
    lines+=['', '## 按任务看：FAD 组', '', '| 任务 | 答案验证 | 成功数据调用 | A 候选 | B 候选 | A 覆盖调用 |','|---|---|---:|---|---|---:|']
    for task in sorted(t for g,t in runs if g=='fad'):
        rr=runs['fad',task];items=[c for c in cs if c['group']=='fad' and c['task']==task]
        ac=[c for c in items if c['tier']=='A'];bc=[c for c in items if c['tier']=='B']
        n=sum(q['success'] and not q['metadata'] for q in rr['queries']);cover=len({m for c in ac for m in c['members']})
        lines.append(f"| {task} | {'通过' if rr['summary']['validator_passed'] else '未通过'} | {n} | {links(ac)} | {links(bc)} | {cover} |")
    lines+=['', '## 公共对象候选 A：究竟共享什么', '',
      '| ID / 任务 | 准备对象 | 涉及 Q 编号 | 共用调用数 / 首次后剩余 | 可能减少的工作 |',
      '|---|---|---|---:|---|']
    for c in cs:
        if c['tier']!='A':continue
        lines.append(f"| [{c['id']}](OPPORTUNITY_CASES.md#{c['id'].lower()}) / {c['task']} | {c['title']} | {', '.join('Q'+str(n)+('（部分）' if n in c['partial'] else '') for n in c['members'])} | {c['consumer_count']} / {c['later_count']} | {c['uses']} |")
    lines+=['', '## 哪些观察没有算成机会', '', '| 观察 | 本版处理 |', '|---|---|',
      '| 不同表使用同名列或 COUNT(*) | 排除；没有共同输入。 |',
      '| 同表 COUNT(*)，但分组/过滤不同 | 不作为聚合复用；只有能描述共同输入准备时才按相应输入候选计数。 |',
      '| 原始 ID Join 与去 # 后 ID Join | 分为不同准备方案，不能假设键等价。 |',
      '| LEFT JOIN 与 INNER JOIN | 不混用中间结果；可以共享派生键，但外连接语义必须保留。 |',
      '| 样本 LIMIT 后再完整读取 | 样本不能覆盖完整结果；不因同表就计入候选。 |',
      '| 股票原始字符串日期过滤与解析日期过滤 | 不当作相同数据范围。 |',
      '| 先取 2018 数据再做 LAG | 排除这种改写；需要保留窗口前驱行。 |',
      '| 同一调用内三个 UNION 分支 | 不算三次后续 SQL；只计该调用一次。 |',
      '| 泛化“把整张表复制一份”或“给列加索引” | 没有进一步说明共同准备对象/访问模式的，不自动算候选。没有查询计划，未声称索引缺失或无效。 |', '',
      '## 如何理解这次结果', '',
      '自然组公共对象候选主要集中在 CRM，bookreview 有少量文本派生/筛选候选；原自然组三个 stockindex 任务未识别出本口径下的明确公共对象。这比“9/9 都有同表 overlap”更贴近研究问题。未找到并不证明没有任何优化机会。', '',
      '自然组 A 的 5 个候选中，4 个在首次使用后还剩至少两次调用；另一个只有一次额外使用。FAD 组 A 的 6 个候选中有 3 个满足这一点。说明部分轨迹确实包含可以供多条后续查询使用的共同对象，但窗口很短，且首次准备的时机需要额外信息。', '',
      '所有 A 候选均依据实际输入、谓词/键/表达式和具体消费者人工识别；未以实际执行确认输出等价、数据交集大小、缓存有效性或节省成本。数据库较小，物化全量 Join/额外状态可能得不偿失。候选涉及未通过验证的轨迹，不能据此证明正确任务路径也必然需要这些探索。', '',
      '## 可复查产物与复算', '',
      '- [逐候选说明与原始 SQL 链接](OPPORTUNITY_CASES.md)：准备什么、如何使用、边界、部分受益分支。',
      '- [机器可读候选与 SQL 原文](opportunities.json)：包含 Q 编号、call_id、源码位置和覆盖统计。',
      '- [旧结构相似性报告](OVERLAP-structural-v1.md)：仅供历史审计，不再用于估计优化机会。',
      '- [数据规模](DATA.md)、[原始运行及 FAD 统计](TABLES.md)。', '',
      '```bash','benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/opportunity_report.py','```','',
      '实现使用人工审阅的候选目录（tools/opportunity_catalog.py），程序负责校验同库成功调用、输入表、原始 SQL 对应关系，并按任务去重统计。它不是自动发现所有优化机会的检测器。']
    (ROOT/'reports/OPPORTUNITY_METHOD.md').write_text('\n'.join(lines)+'\n')
    detail=['# 潜在优化机会：逐项证据','','所有候选仅为静态分析假设；A 为公共对象、B 为较弱的扫描准备。Q 编号对应原 SQL 文件编号。每项涉及至少两次独立成功数据调用，消费者列表不跨任务。','']
    for c in cs:
        detail += [f"<a id=\"{c['id'].lower()}\"></a>",f"## {c['id']} · {c['group']} · {c['task']} · {c['title']}",'',
          f"类别：{c['tier']}；数据库：`{c['database']}`；任务答案：{'通过' if c['task_passed'] else '未通过'}。",'',
          f"**共同输入证据：** {c['evidence']}",'',f"**一次准备：** {c['prepare']}",'',
          f"**供后续使用：** {c['uses']}",'',f"**约束和不确定性：** {c['constraints']}",'',
          f"涉及 {c['consumer_count']} 次调用；若在首次使用时准备，之后还剩 {c['later_count']} 次潜在使用。",'',
          '| 调用 | 语句数 | 受益范围 | 原始 SQL |','|---|---:|---|---|']
        for q in c['consumers']:
            detail.append(f"| Q{q['number']} | {q['statement_count']} | {'部分子计算' if q['partial'] else '所述公共对象相关部分'} | [SQL](../{q['sql_file']}) |")
        detail+=['']
    (ROOT/'reports/OPPORTUNITY_CASES.md').write_text('\n'.join(detail)+'\n')
    from concise_overlap import write_report
    write_report()
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
