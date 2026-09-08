# 轨迹内多查询优化机会：重新分析

本版替代之前的结构相似性报告。目标是找出：**在一个任务内，做一次具体准备，可能让哪些后续 SQL 少做重复工作？** 已逐条审阅自然组与 FAD 组的 18 条轨迹；没有重跑 Agent，也没有执行候选物化、索引或性能实验。

## 先读结论

自然组识别出 **5 个公共对象候选，分布在 5/9 个任务，涉及 20/65 次成功数据调用（30.8%）**。另有 3 个较弱的扫描统计准备候选。FAD 组识别出 **6 个公共对象候选，分布在 5/9 个任务，涉及 15/42 次调用（35.7%）**，另有 1 个扫描统计准备候选。

**这些是人工审阅在明确口径下找到的候选，不是已证明的优化数量或可节省成本比例，也不是所有优化机会的穷尽枚举。** 不再以同表、同名列、COUNT(*) 或相似 Join 文本的频次替代优化机会。

## 计数口径

- **A：公共对象候选。** 能指出同一输入上的公共筛选、正确区分连接类型/键的公共 Join、相同派生计算或明确包含的共同窗口，并说明后续 SQL 如何使用。只提出有依据的改写方向，未执行等价性或成本验证。
- **B：扫描统计准备候选。** 同一完整输入需要多项统计，可以考虑一次扫描分别准备所需状态。其证据主要是共享扫描，弱于公共子计算；不把不同分组的同名聚合当作可复用状态。B 单列，不混入 A 的主结论。
- **一个候选是一套共同准备方案，不是查询对。** 同一方案的筛选、Join、派生列可分层准备，按一个候选计数；不同连接语义的准备分开计数。此划分是分析约定，换一种物理设计可能合并或拆分候选，因此原始候选数不是稳定的工作负载属性。
- **涉及 m 次调用**：若在首次使用前准备，可服务这 m 次调用中的全部或部分子计算。**首次使用后还剩 m−1 次**：若等第一次调用时才构建/保留准备对象，可服务的后续次数上限；不是第一次最终结果天然可复用的证明。
- 只算同一任务、同一组、同一数据库内的跨调用机会。Q 编号对应原 sql/NNN 文件，保留元数据编号空档。自然组 65 次成功数据调用含 66 条语句，FAD 组 42 次含 44 条。UNION 分支和一次调用的多条语句不另算未来调用。
- 覆盖率按 (任务, call_id) 去重；一条调用可仅有一个子查询受益。覆盖率不是省掉整条 SQL 的比例。使用完整轨迹事后识别，尚未验证在候选首次出现前 FAD 是否已提供足够信息。

## 两组分别汇总

| 组别 / 类别 | 候选方案 | 涉及任务 / 9 | 涉及成功调用 | 首次使用后剩余调用（去重） | 首次后仍有至少 2 次使用的方案 |
|---|---:|---:|---:|---:|---:|
| natural / A | 5 | 5 | 20/65 (30.8%) | 15 | 4 |
| natural / B | 3 | 2 | 7/65 (10.8%) | 4 | 1 |
| natural / all | 8 | 6 | 27/65 (41.5%) | 19 | 5 |
| fad / A | 6 | 5 | 15/42 (35.7%) | 9 | 3 |
| fad / B | 1 | 1 | 3/42 (7.1%) | 2 | 1 |
| fad / all | 7 | 5 | 18/42 (42.9%) | 11 | 4 |

A+B 合计仅作候选清单规模说明；两组任务相同但轨迹不同，不能用覆盖率差异估计 FAD 的因果效果。

## 按任务看：自然组

| 任务 | 答案验证 | 成功数据调用 | A 候选 | B 候选 | A 覆盖调用 | 初步判断 |
|---|---|---:|---|---|---:|---|
| bookreview/query1 | 通过 | 5 | [N01](OPPORTUNITY_CASES.md#n01) | — | 2 | 正则提取重复两次；仅一个额外消费者，表很小。 |
| bookreview/query2 | 通过 | 7 | [N02](OPPORTUNITY_CASES.md#n02) | — | 4 | 共同类别筛选覆盖多次探索及最终读取；一次调用仅部分受益。 |
| bookreview/query3 | 通过 | 9 | — | [N03](OPPORTUNITY_CASES.md#n03)、[N04](OPPORTUNITY_CASES.md#n04) | 0 | 主要是诊断扫描；未把不同类别 LIKE 写法和样本/全量读取当作强候选。 |
| crmarenapro/query12 | 未通过 | 11 | [N06](OPPORTUNITY_CASES.md#n06) | — | 5 | 五次调用共享原始键 Join，但日期口径不同，结果复用不能直接成立。 |
| crmarenapro/query13 | 通过 | 12 | [N07](OPPORTUNITY_CASES.md#n07) | [N08](OPPORTUNITY_CASES.md#n08) | 3 | 相同订单窗口和明细 Join 覆盖三次调用；另有商机扫描统计候选。 |
| crmarenapro/query8 | 未通过 | 8 | [N05](OPPORTUNITY_CASES.md#n05) | — | 6 | Owner Assignment 子集有六次使用，是较清楚的多消费者候选。 |
| stockindex/query1 | 通过 | 3 | — | — | 0 | 仅一个业务分析调用；DISTINCT 指数和业务扫描不足以认定具体公共准备。 |
| stockindex/query2 | 通过 | 4 | — | — | 0 | 主要为样本、指数枚举和一次读取；未找到本口径下 A/B 候选。 |
| stockindex/query3 | 通过 | 6 | — | — | 0 | 完整读取后转 Python；同表重访存在，未纳入泛化全表缓存候选。 |

## 按任务看：FAD 组

| 任务 | 答案验证 | 成功数据调用 | A 候选 | B 候选 | A 覆盖调用 |
|---|---|---:|---|---|---:|
| bookreview/query1 | 通过 | 3 | — | — | 0 |
| bookreview/query2 | 通过 | 3 | — | — | 0 |
| bookreview/query3 | 通过 | 5 | — | — | 0 |
| crmarenapro/query12 | 未通过 | 10 | [F02](OPPORTUNITY_CASES.md#f02)、[F03](OPPORTUNITY_CASES.md#f03) | [F04](OPPORTUNITY_CASES.md#f04) | 6 |
| crmarenapro/query13 | 通过 | 3 | [F05](OPPORTUNITY_CASES.md#f05) | — | 2 |
| crmarenapro/query8 | 通过 | 5 | [F01](OPPORTUNITY_CASES.md#f01) | — | 3 |
| stockindex/query1 | 通过 | 6 | [F06](OPPORTUNITY_CASES.md#f06) | — | 2 |
| stockindex/query2 | 未通过 | 4 | [F07](OPPORTUNITY_CASES.md#f07) | — | 2 |
| stockindex/query3 | 通过 | 3 | — | — | 0 |

## 公共对象候选 A：究竟共享什么

| ID / 任务 | 准备对象 | 涉及 Q 编号 | 共用调用数 / 首次后剩余 | 可能减少的工作 |
|---|---|---|---:|---|
| [N01](OPPORTUNITY_CASES.md#n01) / bookreview/query1 | 出版年份正则提取 | Q4, Q5 | 2 / 1 | Q4 从派生列计算非空数量；Q5 用派生列 IS NULL 筛选原始记录。 |
| [N02](OPPORTUNITY_CASES.md#n02) / bookreview/query2 | 文学类别筛选与布尔标记 | Q5, Q6（部分）, Q7, Q8 | 4 / 3 | Q5/Q7/Q8 使用类别子集，保留各自 LIMIT、英语条件及投影；Q6 的 lit_fic 与 lit_fic_english 使用该子集，total 仍需全表总数。 |
| [N05](OPPORTUNITY_CASES.md#n05) / crmarenapro/query8 | Owner Assignment 历史子集 | Q4, Q5, Q6, Q7, Q8, Q10 | 6 / 5 | Q4/Q7 在此基础上继续连接 Case；Q5/Q6/Q10 的 CTE 从子集读取后保留各自窗口、分组与 Join；Q8 继续过滤 oldvalue。 |
| [N06](OPPORTUNITY_CASES.md#n06) / crmarenapro/query12 | 原始 ID 的 Opportunity–Contract 公共 Join | Q3, Q4, Q5, Q8（部分）, Q10 | 5 / 4 | Q3/Q4/Q5/Q10 在公共 Join 上保留各自日期条件与聚合/投影；Q8 仅 apr_close_with_contract 子查询可使用它。 |
| [N07](OPPORTUNITY_CASES.md#n07) / crmarenapro/query13 | 同一订单窗口及订单明细 Join | Q11, Q13, Q14 | 3 / 2 | Q13 用订单子集；Q11/Q14 用明细 Join 分别按原始 OwnerId、去 # 后 OwnerId 聚合。 |
| [F01](OPPORTUNITY_CASES.md#f01) / crmarenapro/query8 | Owner Assignment 历史子集 | Q3, Q4, Q6 | 3 / 2 | Q3/Q6 施加同一日期窗口；Q4 单独施加 oldvalue 非空；保留不同排序和聚合。 |
| [F02](OPPORTUNITY_CASES.md#f02) / crmarenapro/query12 | 原始 ID 的 Opportunity–Contract Join | Q1, Q2, Q5 | 3 / 2 | Q1/Q2 分别按创建和签署日期筛选聚合；Q5 按关闭日期筛选后返回明细。 |
| [F03](OPPORTUNITY_CASES.md#f03) / crmarenapro/query12 | 去 # 的连接键与归一化 Join | Q7（部分）, Q8, Q9 | 3 / 2 | Q7 的 c2 LEFT JOIN 分支使用预计算键/访问结构，保留外连接；Q8/Q9 可用归一键 INNER JOIN 明细。 |
| [F05](OPPORTUNITY_CASES.md#f05) / crmarenapro/query13 | 多个销售时间窗口的共同明细 | Q3, Q4 | 2 / 1 | Q3 保留滚动窗口筛选；Q4 三个 UNION ALL 分支分别筛选各自窗口后分组。 |
| [F06](OPPORTUNITY_CASES.md#f06) / stockindex/query1 | 股票日期解析及共同分析输入 | Q8, Q9 | 2 / 1 | Q8 从该输入计算 close 分母波动率及日期统计；Q9 计算 open/mid 等其他波动指标。 |
| [F07](OPPORTUNITY_CASES.md#f07) / stockindex/query2 | 北美指数窗口输入 | Q6, Q7 | 2 / 1 | Q6 再筛 2018 下界后比较 Open/Close；Q7 在宽窗口上先算 LAG，再筛 2018。 |

## 哪些观察没有算成机会

| 观察 | 本版处理 |
|---|---|
| 不同表使用同名列或 COUNT(*) | 排除；没有共同输入。 |
| 同表 COUNT(*)，但分组/过滤不同 | 不作为聚合复用；只有能描述共同输入准备时才按相应输入候选计数。 |
| 原始 ID Join 与去 # 后 ID Join | 分为不同准备方案，不能假设键等价。 |
| LEFT JOIN 与 INNER JOIN | 不混用中间结果；可以共享派生键，但外连接语义必须保留。 |
| 样本 LIMIT 后再完整读取 | 样本不能覆盖完整结果；不因同表就计入候选。 |
| 股票原始字符串日期过滤与解析日期过滤 | 不当作相同数据范围。 |
| 先取 2018 数据再做 LAG | 排除这种改写；需要保留窗口前驱行。 |
| 同一调用内三个 UNION 分支 | 不算三次后续 SQL；只计该调用一次。 |
| 泛化“把整张表复制一份”或“给列加索引” | 没有进一步说明共同准备对象/访问模式的，不自动算候选。没有查询计划，未声称索引缺失或无效。 |

## 如何理解这次结果

自然组公共对象候选主要集中在 CRM，bookreview 有少量文本派生/筛选候选；原自然组三个 stockindex 任务未识别出本口径下的明确公共对象。这比“9/9 都有同表 overlap”更贴近研究问题。未找到并不证明没有任何优化机会。

自然组 A 的 5 个候选中，4 个在首次使用后还剩至少两次调用；另一个只有一次额外使用。FAD 组 A 的 6 个候选中有 3 个满足这一点。说明部分轨迹确实包含可以供多条后续查询使用的共同对象，但窗口很短，且首次准备的时机需要额外信息。

所有 A 候选均依据实际输入、谓词/键/表达式和具体消费者人工识别；未以实际执行确认输出等价、数据交集大小、缓存有效性或节省成本。数据库较小，物化全量 Join/额外状态可能得不偿失。候选涉及未通过验证的轨迹，不能据此证明正确任务路径也必然需要这些探索。

## 可复查产物与复算

- [逐候选说明与原始 SQL 链接](OPPORTUNITY_CASES.md)：准备什么、如何使用、边界、部分受益分支。
- [机器可读候选与 SQL 原文](opportunities.json)：包含 Q 编号、call_id、源码位置和覆盖统计。
- [旧结构相似性报告](OVERLAP-structural-v1.md)：仅供历史审计，不再用于估计优化机会。
- [数据规模](DATA.md)、[原始运行及 FAD 统计](TABLES.md)。

```bash
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/opportunity_report.py
```

实现使用人工审阅的候选目录（tools/opportunity_catalog.py），程序负责校验同库成功调用、输入表、原始 SQL 对应关系，并按任务去重统计。它不是自动发现所有优化机会的检测器。
