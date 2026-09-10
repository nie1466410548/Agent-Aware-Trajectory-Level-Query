# DAComp-006：逐轮 FAD 与后续 SQL 人工核对

这里的“支持”仅指实际查询的访问方向支持提示，不代表查询计算或分析结论正确。自然语言评估由人工阅读完成，不是自动语义判定。Q 编号含失败查询；所有后续证据均严格晚于提示所属查询。

FAD 内容取自 [原始请求日志](../runs/hints-006-02/events.jsonl) 的 `arguments.future_access`。原文列保留 Agent 实际填写的 `condition`，不把它改写成更准确的意图。

Q1–Q29 均为 `status=provided`、`coverage=partial_plan`，各含一个候选且 `tables=["sheet1"]`。所有候选均未提供 `filters`、`joins`、`group_by`、`aggregations`、`likelihood` 或 `unresolved`。下表逐轮列出不同的原文、列名和优先级；列名保留原始拼写，包括 Q10/Q11 中的 SQL 引号。“未提供”表示字段缺失，不表示不会访问任何列。Q30 为空提示，单独补列，不计入29份非空 FAD 的统计。

| 提示轮次 | FAD 原文（condition） | FAD 结构化列（columns） | 优先级 | 后续成功 SQL 证据 | 判断 | 解释 |
|---|---|---|---|---|---|---|
| Q1 | Explore date range and destinations in South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q2, Q3 | 部分/组合支持 | Q2检查全表日期和地域概况，Q3列华南目的地；不能认为Q2已完成全部意图。 |
| Q2 | List distinct South China destinations to identify sub-regions/provinces | `sheet1.Destination` | `high` | Q3 | 支持 | 下一轮列出华南目的地。 |
| Q3 | List distinct South China provinces/cities | `sheet1.Destination` | `high` | Q4 | 支持 | 下一轮进一步提取并分组省份。 |
| Q4 | Aggregate monthly South China profit by month | `sheet1.Destination` | `high` | Q5 | 支持但结构字段缺失 | 下一轮按月汇总利润；FAD只声明Destination，缺Date和Profit。 |
| Q5 | Monthly profit by province within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q6 | 支持 | 下一轮按月份、省份汇总利润。 |
| Q6 | Monthly profit by product category within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q12 | 延迟支持 | 先继续省份分析并处理错误；产品月度利润到Q12才发生。 |
| Q7 | Monthly profit by product within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q12 | 延迟支持 | Q7本身失败；预测的产品分析后续确实出现。 |
| Q8 | Monthly profit by product within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q12 | 延迟支持 | Q8本身失败；预测的产品分析后续确实出现。 |
| Q9 | Monthly profit by product within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination` | `high` | Q12 | 延迟支持 | Q10仍在省份分析，Q11仅列产品，Q12按月按产品汇总。 |
| Q10 | Monthly profit by product within South China | `sheet1.Date`、`sheet1.Profit`、`sheet1.Destination`、`sheet1."Consigned Product"` | `high` | Q11, Q12 | 先准备后支持 | Q11列出产品，Q12完成按月产品利润；不能把Q11当作完整聚合命中。 |
| Q11 | Monthly profit by product in South China | `sheet1."Consigned Product"`、`sheet1.Date`、`sheet1.Profit` | `high` | Q12 | 支持 | 下一轮月度产品利润。 |
| Q12 | Monthly profit by customer gender/age in South China | `sheet1.Date`、`sheet1.Profit` | `high` | Q15, Q16 | 延迟支持但结构字段缺失 | 后续性别/年龄分析出现；Q14性别查询失败，Q15/Q16成功。FAD缺性别和年龄列。 |
| Q13 | Monthly profit by customer gender/age in South China | `sheet1.Date`、`sheet1.Profit` | `high` | Q15, Q16 | 支持但结构字段缺失 | 同上；下一次成功Q15只覆盖性别方向。 |
| Q14 | Monthly profit by customer age range in South China | `sheet1.Date`、`sheet1.Profit` | `medium` | Q16 | 延迟支持 | 先修复性别查询，再按年龄组分析。 |
| Q15 | Monthly profit by customer age range in South China | `sheet1.Date`、`sheet1.Profit` | `medium` | Q16 | 支持但结构字段缺失 | 下一轮年龄分析；FAD仍未列Age Range。 |
| Q16 | Monthly profit by customer age range in South China | `sheet1.Date`、`sheet1.Profit` | `medium` | 无 | 仅当前SQL支持 | 年龄分析就是当前Q16，后续没有相应年龄查询。 |
| Q17 | Check if specific cost/revenue components explain instability | 未提供 | `medium` | Q19 | 方向支持 | 下一次成功SQL比较收入和成本组件的波动；仅认定访问方向，不认定因果解释或计算正确。 |
| Q18 | Check discount and cost per unit trends | 未提供 | `low` | Q28 | 延迟支持 | 折扣和单位成本趋势在Q28；Q19是组件波动，不能当作单位经济指标命中。 |
| Q19 | Check discount and cost per unit trends | 未提供 | `low` | Q28 | 延迟支持 | 单位折扣和成本在Q28，不是紧接着的Q20利润/单位。 |
| Q20 | Check product mix by province in South China | 未提供 | `medium` | 无 | 仅当前SQL支持 | 省份×产品交叉统计在当前Q20；后续未再次进行该组合分析。 |
| Q21 | Check product mix shifts in low-profit months | 未提供 | `medium` | Q27 | 部分支持 | Q27查询部分产品的月度利润和数量，未显式限定低利润月份或计算产品份额变化。 |
| Q22 | Monthly profits for Guangxi, Hainan, Henan, Hubei, Hunan provinces | 未提供 | `medium` | Q23, Q24, Q25, Q26 | 部分支持且混入当前访问 | 五省中的广西已在当前Q22查询；其余四省在后续查询。 |
| Q23 | Monthly profits for Hainan, Henan, Hubei, Hunan provinces | 未提供 | `medium` | Q24, Q25, Q26 | 部分支持且混入当前访问 | 海南已在当前Q23查询；后三省后续查询。 |
| Q24 | Monthly profits for Henan, Hubei, Hunan provinces | 未提供 | `medium` | Q25, Q26 | 部分支持且混入当前访问 | 河南已在当前Q24查询；后两省后续查询。 |
| Q25 | Monthly profits for Hubei and Hunan provinces | 未提供 | `medium` | Q26 | 部分支持且混入当前访问 | 湖北已在当前Q25查询；湖南在Q26。 |
| Q26 | Monthly profits for Hunan province | 未提供 | `medium` | 无 | 仅当前SQL支持 | 湖南月度利润就是当前Q26，不能用当前查询计为未来命中。 |
| Q27 | Additional analysis if needed | 未提供 | `low` | 无 | 不可具体检验 | Additional analysis if needed未限定任何具体分析方向。 |
| Q28 | Check monthly unit economics stability | 未提供 | `low` | Q29 | 部分支持 | Q29计算单位利润波动，支持单位经济性的一部分；未检查全部单位收入/成本指标。 |
| Q29 | No further queries expected after this | 未提供 | `low` | Q30 | 结束预期被后续查询否定 | 自然语言说不再查询，但结构状态是provided，且之后确有Q30。 |
| Q30 | 无 condition；`status=no_further_access`，`candidates=[]` | 不适用（空候选集合） | 不适用 | 无 | 与观察到的结束一致 | 此后没有 SQL，Agent 提交了报告；仅是一次终止判断观测。 |
