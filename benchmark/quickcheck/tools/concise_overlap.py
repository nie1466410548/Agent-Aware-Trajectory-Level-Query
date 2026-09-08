"""Readable task-first entry point; technical evidence lives in linked reports."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def write_report():
    raw=json.loads((ROOT/'reports/overlap-detail.json').read_text())
    opp=json.loads((ROOT/'reports/opportunities.json').read_text())
    rows=sorted(raw['runs'],key=lambda r:(r['task'],0 if r['group']=='natural' else 1))
    lines=['# 每个任务有哪些重叠、有哪些潜在优化机会','',
      '第一张表看实际查询中的重复结构；第二张表看其中哪些能提出具体的共同准备方案。只在同一任务、同一组内部比较。','',
      '## 1. 逐任务查询统计','',
      '**从“同表”到“相同结果行”，各列都是存在相应重复的后续调用数，一次调用在一列内只计一次。** 例如“同表=3”表示有 3 次调用访问了本任务此前访问过的表。列之间可以重叠，不能相加。', '',
      '统计依据为已保存的原始 SQL、执行状态、数据库 schema 和查询结果，使用 SQLGlot 离线解析比较；未使用执行计划或性能测量。只比较同一任务、同一组、同一数据库内的前后成功数据调用，排除元数据和失败调用。', '',
      '| 列 | 具体统计规则 |',
      '|---|---|',
      '| 验证 | 运行结束后，原始 benchmark 验证器是否通过。 |',
      '| 成功 SQL | 成功执行的数据查询调用数，不是去重 SQL 数。 |',
      '| 同表 | 后续查询与至少一个前序查询共享基表。 |',
      '| 同表列 | 共享具体的 `(基表, 列)` 引用；依据 schema 展开 `SELECT *`，包括 SELECT、筛选、连接、分组和排序等位置引用的列；`COUNT(*)` 不视为引用所有列。 |',
      '| WHERE 合取项 | 将 WHERE 按 `AND` 拆分、绑定基表并归一表达式后，存在相同条件项；保留常量值，不证明一般谓词语义等价。 |',
      '| Join 片段 | 归一基表别名后，存在相同 Join 语法片段；未验证整个左输入或中间结果相同。 |',
      '| 聚合表达式 | 基表集合相同，且至少一个聚合表达式相同，例如 `COUNT(*)`；不要求分组键或输入行相同。 |',
      '| GROUP BY | 基表集合相同，且至少一个完整 GROUP BY 结构相同；不是只共享一个分组列，也不是含分组的查询总数。 |',
      '| 相同结果行 | 在同库共享基表的查询对中，两次调用输出列名集合相同，实际 JSON 结果中至少有一行值完全相同；忽略行序和重复次数，排除多语句调用。 |', '',
      '一次调用含多条 SQL 时，结构特征取各语句的并集，仍计一次调用；适配器只保存末条返回结果，因此不将此类调用纳入结果行比较。上述规则描述结构或输出匹配，不是语义等价证明，也不是优化机会计数。', '',
      '| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式* | GROUP BY | 相同结果行 |',
      '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    keys=['table_any','column_bound','filter_atom','join_bound','aggregate_bound','group','result_row']
    totals={g:[0]*8 for g in ['natural','fad']}
    for r in rows:
        vals=[r['successful']]+[len({p['consumer'] for p in r['pairs'] if k in p['metrics']}) for k in keys]
        totals[r['group']]=[a+b for a,b in zip(totals[r['group']],vals)]
        link=f"../{r['analysis_path']}"
        lines.append(f"| [{r['task']}]({link}) | {'自然' if r['group']=='natural' else 'FAD'} | {'✓' if r['passed'] else '✗'} | "+' | '.join(map(str,vals))+' |')
    for g in ['natural','fad']:
        lines.append(f"| **合计** | **{'自然' if g=='natural' else 'FAD'}** | **7/9** | "+' | '.join(f'**{v}**' for v in totals[g])+' |')
    lines += ['',
      '*“聚合表达式”只表示相同输入表集合中出现相同表达式，例如 COUNT(*)，**不是聚合计算复用机会**。GROUP BY 列也是“重复相同分组结构”，不是含分组的查询总数。',
      '同表列已绑定到具体基表，并展开 SELECT *。Join 列仅为片段相同，未保证整个输入或连接计算等价。“相同结果行”也不代表能用前序结果替代后序查询。',
      '成功 SQL 的计数单位是工具调用；3 次调用各有两条 SQL。排除失败 SQL 和元数据，保留最终答题失败轨迹中的成功查询。', '',
      '## 2. 哪些重复可以提出具体优化方案','',
      '**“候选数”数的是共同准备对象；“涉及 SQL”数的是可使用这些对象的调用，按任务去重，包含部分子计算受益。** 尚未验证加速。扫描统计准备更弱，单独列出。', '',
      '| 任务 | 组 | 公共对象候选数 | 涉及 SQL / 成功 SQL | 首次使用后仍可用次数 ≥2 的候选数 | 较弱扫描候选数 | 可能共同准备什么 |',
      '|---|---|---:|---:|---:|---:|---|']
    names={
      'N01':'出版年份提取','N02':'文学类别筛选','N03':'评论诊断扫描','N04':'书籍 ID 诊断扫描',
      'N05':'Owner Assignment 历史子集','N06':'原始键商机–合同 Join',
      'N07':'订单窗口＋明细 Join','N08':'商机统计扫描',
      'F01':'Owner Assignment 历史子集','F02':'原始键商机–合同 Join',
      'F03':'去 # 连接键＋Join','F04':'商机诊断扫描','F05':'多窗口订单明细',
      'F06':'股票日期解析＋筛选','F07':'保留 LAG 前驱行的指数窗口'}
    for r in rows:
        cs=[c for c in opp['candidates'] if (c['group'],c['task'])==(r['group'],r['task'])]
        strong=[c for c in cs if c['tier']=='A'];weak=[c for c in cs if c['tier']=='B']
        covered=len({q for c in strong for q in c['members']})
        labels='；'.join(f"[{names[c['id']]}](OPPORTUNITY_CASES.md#{c['id'].lower()})"+('（弱）' if c['tier']=='B' else '') for c in cs) or '本口径未识别'
        lines.append(f"| {r['task']} | {'自然' if r['group']=='natural' else 'FAD'} | {len(strong)} | {covered}/{r['successful']} | {sum(c['later_count']>=2 for c in strong)} | {len(weak)} | {labels} |")
    for g in ['natural','fad']:
        a=opp['summary'][g]['A'];b=opp['summary'][g]['B']
        lines.append(f"| **合计** | **{'自然' if g=='natural' else 'FAD'}** | **{a['families']}** | **{a['covered_calls']}/{a['successful_calls']}** | **{a['families_with_two_later']}** | **{b['families']}** | — |")
    lines += ['',
      '例如自然组 crmarenapro/8：第一张表显示 6 次同表重访；进一步检查后，第二张表识别出 **1 个 Owner Assignment 历史子集候选**，涉及 Q4、Q5、Q6、Q7、Q8、Q10 共 6 次调用。若首次使用时准备，此后还有 5 次潜在使用。不是“有 6 次重访，所以有 6 个优化机会”。', '',
      '自然组 stockindex/3 虽然有 4 次同表重访，但主要是样本、统计和完整读取，随后转 Python；本次没有据此认定具体公共对象候选。', '',
      '**目前的判断：访问重复普遍存在，但能明确说出准备对象的机会主要集中在 CRM。** 这些是完整轨迹事后人工识别的潜在机会，未穷尽所有手段，也未证明当时 FAD 足够、改写等价或有净收益。', '',
      '[逐候选与原始 SQL](OPPORTUNITY_CASES.md) · [候选 JSON](opportunities.json) · [详细口径](OPPORTUNITY_METHOD.md) · [结构统计明细](OVERLAP-structural-v1.md)']
    (ROOT/'reports/OVERLAP.md').write_text('\n'.join(lines)+'\n')
if __name__=='__main__':write_report()
