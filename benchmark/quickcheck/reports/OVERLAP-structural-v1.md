> 历史结构相似性统计：以下计数不是优化机会数量。当前分析请看 [OVERLAP.md](OVERLAP.md)。

# 系统性 overlap 清单

本报告基于已保存的 18 条轨迹重新统计，没有重新运行 Agent。仅比较同一运行、同一逻辑数据库内的前后成功数据 SQL；排除元数据和失败尝试。不同任务与不同组不相互配对。

**查询对数**：每个前序→后序组合算一对。**后续查询数**：一条 SQL 即使与多个前序重叠，在该指标中也只算一次。百分比以本组全部成功数据 SQL 为分母；不同指标可交叉，不可相加。任务数是该组出现该类重叠的任务数。

| 统计范围 | 自然组 | FAD 组 |
|---|---:|---:|
| 成功数据 SQL 调用 | 65 | 42 |
| 成功数据 SQL 语句（拆分多语句调用） | 66 | 44 |
| 数据 SQL 尝试（含失败） | 66 | 42 |
| 同库前后查询对（包括不重叠） | 120 | 69 |

计数单位沿用原报告的 SQL 工具调用：3 次成功数据调用各含 2 条 SQL，结构特征取调用内各语句的并集；不统计同一次调用内部的重叠。自然组 65 次成功调用含 66 条语句，FAD 组 42 次含 44 条。多语句调用只保存末条结果，故排除它们的结果行比较。

## 按层次统计

| 重叠定义 | 自然：对数 | 自然：后续 SQL / 65 | 自然：任务 / 9 | FAD：对数 | FAD：后续 SQL / 42 | FAD：任务 / 9 |
|---|---:|---:|---:|---:|---:|---:|
| 共享至少一张基表 | 112 | 44 (67.7%) | 9 | 65 | 25 (59.5%) | 9 |
| 基表集合完全相同（非空） | 79 | 41 (63.1%) | 9 | 55 | 23 (54.8%) | 9 |
| 共享列名（旧口径，未绑定表） | 93 | 37 (56.9%) | 9 | 64 | 25 (59.5%) | 9 |
| 共享基表＋列（展开 SELECT *） | 103 | 41 (63.1%) | 9 | 64 | 25 (59.5%) | 9 |
| 引用的基表＋列集合相同（非空） | 16 | 13 (20.0%) | 7 | 14 | 10 (23.8%) | 7 |
| 前序引用列集合覆盖后序（非空） | 47 | 31 (47.7%) | 8 | 26 | 15 (35.7%) | 7 |
| 共享完整 WHERE（绑定表后） | 8 | 6 (9.2%) | 3 | 5 | 5 (11.9%) | 4 |
| 共享至少一个 WHERE 合取项 | 34 | 14 (21.5%) | 4 | 8 | 7 (16.7%) | 5 |
| 共享 Join 文本片段（旧口径） | 13 | 7 (10.8%) | 3 | 5 | 4 (9.5%) | 2 |
| 共享 Join 片段（基表别名归一） | 13 | 7 (10.8%) | 3 | 5 | 4 (9.5%) | 2 |
| 共享聚合表达式（旧口径） | 20 | 11 (16.9%) | 4 | 35 | 13 (31.0%) | 6 |
| 同基表集合且共享聚合表达式 | 16 | 10 (15.4%) | 4 | 28 | 12 (28.6%) | 6 |
| 同基表集合且共享 GROUP BY | 3 | 2 (3.1%) | 1 | 8 | 5 (11.9%) | 3 |
| 同基表集合、相同 GROUP BY 且共享聚合 | 3 | 2 (3.1%) | 1 | 7 | 4 (9.5%) | 2 |
| 同基表集合且共享含列的投影表达式 | 35 | 24 (36.9%) | 9 | 29 | 18 (42.9%) | 9 |
| 同基表集合且共享 ORDER BY | 4 | 3 (4.6%) | 2 | 10 | 6 (14.3%) | 3 |
| 同基表集合且共享窗口表达式 | 0 | 0 (0.0%) | 0 | 0 | 0 (0.0%) | 0 |
| 简单同列区间兼容（非数据交集证明） | 0 | 0 (0.0%) | 0 | 3 | 3 (7.1%) | 3 |
| 至少一个简单同列区间不相交 | 0 | 0 (0.0%) | 0 | 0 | 0 (0.0%) | 0 |
| 相同输出列名下存在相同结果行 | 4 | 4 (6.2%) | 3 | 3 | 3 (7.1%) | 3 |
| 前序结果集合包含后序非空结果集合 | 0 | 0 (0.0%) | 0 | 1 | 1 (2.4%) | 1 |
| 规范化 SQL 完全相同 | 0 | 0 (0.0%) | 0 | 0 | 0 (0.0%) | 0 |
| 满足已有保守结果复用语法条件 | 0 | 0 (0.0%) | 0 | 0 | 0 (0.0%) | 0 |

## 按任务分布

以下单元格均为后续查询数；分母为该运行成功数据 SQL 数。列级采用绑定基表并展开星号的新口径；Join 使用基表别名归一，聚合要求同基表集合。

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join | 聚合 | GROUP BY | 相同结果行 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [bookreview/query1](../runs/fad/bookreview/query1/quick-01/analysis.json) | fad | 通过 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 1 |
| [bookreview/query1](../runs/natural/bookreview/query1/quick-01/analysis.json) | natural | 通过 | 5 | 3 | 3 | 0 | 0 | 0 | 0 | 1 |
| [bookreview/query2](../runs/fad/bookreview/query2/quick-01/analysis.json) | fad | 通过 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| [bookreview/query2](../runs/natural/bookreview/query2/quick-01/analysis.json) | natural | 通过 | 7 | 5 | 5 | 3 | 0 | 0 | 0 | 0 |
| [bookreview/query3](../runs/fad/bookreview/query3/quick-01/analysis.json) | fad | 通过 | 5 | 3 | 3 | 0 | 0 | 1 | 0 | 0 |
| [bookreview/query3](../runs/natural/bookreview/query3/quick-01/analysis.json) | natural | 通过 | 9 | 7 | 7 | 0 | 0 | 1 | 0 | 2 |
| [crmarenapro/query12](../runs/fad/crmarenapro/query12/quick-01/analysis.json) | fad | 未通过 | 10 | 8 | 8 | 2 | 3 | 6 | 3 | 1 |
| [crmarenapro/query12](../runs/natural/crmarenapro/query12/quick-01/analysis.json) | natural | 未通过 | 11 | 8 | 8 | 4 | 4 | 3 | 2 | 0 |
| [crmarenapro/query13](../runs/fad/crmarenapro/query13/quick-01/analysis.json) | fad | 通过 | 3 | 2 | 2 | 1 | 1 | 1 | 1 | 0 |
| [crmarenapro/query13](../runs/natural/crmarenapro/query13/quick-01/analysis.json) | natural | 通过 | 12 | 8 | 6 | 2 | 1 | 3 | 0 | 0 |
| [crmarenapro/query8](../runs/fad/crmarenapro/query8/quick-01/analysis.json) | fad | 通过 | 5 | 3 | 3 | 2 | 0 | 1 | 0 | 1 |
| [crmarenapro/query8](../runs/natural/crmarenapro/query8/quick-01/analysis.json) | natural | 未通过 | 8 | 6 | 6 | 5 | 2 | 3 | 0 | 0 |
| [stockindex/query1](../runs/fad/stockindex/query1/quick-01/analysis.json) | fad | 通过 | 6 | 4 | 4 | 1 | 0 | 2 | 1 | 0 |
| [stockindex/query1](../runs/natural/stockindex/query1/quick-01/analysis.json) | natural | 通过 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| [stockindex/query2](../runs/fad/stockindex/query2/quick-01/analysis.json) | fad | 未通过 | 4 | 2 | 2 | 1 | 0 | 1 | 0 | 0 |
| [stockindex/query2](../runs/natural/stockindex/query2/quick-01/analysis.json) | natural | 通过 | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 |
| [stockindex/query3](../runs/fad/stockindex/query3/quick-01/analysis.json) | fad | 通过 | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 |
| [stockindex/query3](../runs/natural/stockindex/query3/quick-01/analysis.json) | natural | 通过 | 6 | 4 | 3 | 0 | 0 | 0 | 0 | 1 |

## 重访的是哪些表

“访问 SQL”按每条 SQL 每张表一次计数；“重访 SQL”扣除本轨迹该表首次访问。同一 SQL 涉及多表可出现在多行，因此不能把各表重访数直接相加得到总重叠查询数。

| 数据集 / 数据库 / 表 | 自然访问 SQL | 自然重访 SQL | FAD 访问 SQL | FAD 重访 SQL |
|---|---:|---:|---:|---:|
| bookreview / books_database / books_info | 13 | 10 | 6 | 3 |
| bookreview / review_database / review | 8 | 5 | 5 | 2 |
| crmarenapro / core_crm / user | 5 | 2 | 1 | 0 |
| crmarenapro / products_orders / order | 6 | 5 | 3 | 2 |
| crmarenapro / products_orders / orderitem | 2 | 1 | 2 | 1 |
| crmarenapro / sales_pipeline / contract | 9 | 7 | 8 | 7 |
| crmarenapro / sales_pipeline / opportunity | 9 | 7 | 9 | 8 |
| crmarenapro / support / case | 2 | 1 | 1 | 0 |
| crmarenapro / support / casehistory__c | 7 | 6 | 4 | 3 |
| stockindex / indexinfo_database / index_info | 5 | 2 | 3 | 0 |
| stockindex / indextrade_database / index_trade | 8 | 5 | 10 | 7 |

## 具体重复列与 Join

发生跨查询重叠的不同基表列：自然组 40 个，FAD 组 30 个。以下为按自然组后续查询数排序的前 20 个；计数按任务＋后续调用去重。

| 基表列（数据集 / 数据库 / 表 / 列） | 自然后续查询数 | FAD 后续查询数 |
|---|---:|---:|
| bookreview / books_database / books_info / book_id | 7 | 3 |
| bookreview / books_database / books_info / details | 6 | 2 |
| crmarenapro / sales_pipeline / contract / companysigneddate | 6 | 5 |
| crmarenapro / sales_pipeline / opportunity / contractid__c | 6 | 8 |
| crmarenapro / support / casehistory__c / createddate | 6 | 3 |
| crmarenapro / support / casehistory__c / field__c | 6 | 3 |
| crmarenapro / support / casehistory__c / newvalue__c | 6 | 2 |
| crmarenapro / support / casehistory__c / oldvalue__c | 6 | 2 |
| crmarenapro / sales_pipeline / contract / id | 5 | 6 |
| crmarenapro / sales_pipeline / opportunity / createddate | 5 | 6 |
| crmarenapro / support / casehistory__c / caseid__c | 5 | 2 |
| stockindex / indextrade_database / index_trade / index | 5 | 6 |
| bookreview / books_database / books_info / categories | 4 | 2 |
| bookreview / review_database / review / purchase_id | 4 | 2 |
| crmarenapro / products_orders / order / effectivedate | 4 | 2 |
| crmarenapro / products_orders / order / ownerid | 4 | 2 |
| crmarenapro / sales_pipeline / opportunity / ownerid | 4 | 5 |
| crmarenapro / products_orders / order / id | 3 | 1 |
| crmarenapro / sales_pipeline / opportunity / closedate | 3 | 2 |
| stockindex / indextrade_database / index_trade / date | 3 | 5 |

所有重复 Join 片段如下；包含对 CTE 的 Join，不能全部解读为可共享的基表 Join。

| 组 / 任务 | 归一化 Join 片段 | 查询对数 |
|---|---|---:|
| fad / crmarenapro/query12 | `JOIN "contract" ON REPLACE(contract."id", '#', '') = REPLACE(opportunity."contractid__c", '#', '')` | 1 |
| fad / crmarenapro/query12 | `JOIN "contract" ON contract."id" = opportunity."contractid__c"` | 3 |
| fad / crmarenapro/query13 | `JOIN "orderitem" ON orderitem."orderid" = order."id"` | 1 |
| natural / crmarenapro/query12 | `JOIN "contract" ON opportunity."contractid__c" = contract."id"` | 10 |
| natural / crmarenapro/query13 | `JOIN "orderitem" ON orderitem."orderid" = order."id"` | 1 |
| natural / crmarenapro/query8 | `JOIN "case" ON case."id" = casehistory__c."caseid__c"` | 1 |
| natural / crmarenapro/query8 | `LEFT JOIN "transfers" ON "t"."agent_id" = "h"."agent_id"` | 1 |

## 实际结果重合案例

结果重合与完整结果可复用分开列出。下表中的“后序被包含”仅为本次结果值集合的包含，不证明 SQL 语义包含。

| 组 / 任务 | 前序 SQL | 后序 SQL | 前序 / 后序行数 | 后序结果集合被包含 |
|---|---|---|---:|---|
| fad / bookreview/query1 | [003](../runs/fad/bookreview/query1/quick-01/sql/003-9d92f5302216413f9d7c0647733d8641.sql) | [005](../runs/fad/bookreview/query1/quick-01/sql/005-db4c3243dfcb40d0a6eff5e2303a3797.sql) | 5 / 200 | 否 |
| fad / crmarenapro/query12 | [002](../runs/fad/crmarenapro/query12/quick-01/sql/002-9e6aa8e4e69a4900aa19221f8f16c2a9.sql) | [009](../runs/fad/crmarenapro/query12/quick-01/sql/009-5d11c21e0e624339b325b42b7a91c8a4.sql) | 1 / 1 | 是 |
| fad / crmarenapro/query8 | [003](../runs/fad/crmarenapro/query8/quick-01/sql/003-2b8e4f5207854706adad96225f32edbf.sql) | [004](../runs/fad/crmarenapro/query8/quick-01/sql/004-a387634c961943e0adab45fbcd5ee7d9.sql) | 39 / 12 | 否 |
| natural / bookreview/query1 | [005](../runs/natural/bookreview/query1/quick-01/sql/005-d57a24858a8b4dedbab82d80f8cce074.sql) | [007](../runs/natural/bookreview/query1/quick-01/sql/007-c59919c876aa4580b6ad31fafb1e3310.sql) | 15 / 200 | 否 |
| natural / bookreview/query3 | [003](../runs/natural/bookreview/query3/quick-01/sql/003-1cf72419649545eb98f8252b21c870ee.sql) | [010](../runs/natural/bookreview/query3/quick-01/sql/010-71b1f3f7c46146d2859d5372e8b93978.sql) | 5 / 25 | 否 |
| natural / bookreview/query3 | [004](../runs/natural/bookreview/query3/quick-01/sql/004-f0f9f5c38dc94606bed5a2d473267155.sql) | [011](../runs/natural/bookreview/query3/quick-01/sql/011-e205ed43cb4a4072b197b1007e3a0e02.sql) | 5 / 329 | 否 |
| natural / stockindex/query3 | [003](../runs/natural/stockindex/query3/quick-01/sql/003-bedc3b3b2ecf47d38bf4377d44187e5f.sql) | [008](../runs/natural/stockindex/query3/quick-01/sql/008-5796b6327168418fb4b7f625a7e37e5d.sql) | 10 / 14 | 否 |

## 口径与解释边界

- 列绑定使用已实测的 schema 和 SQLGlot 作用域，展开 SELECT *；COUNT(*) 不被解释为读取全部列。统计包括 SELECT、WHERE、JOIN、GROUP BY、ORDER BY 等位置引用的基表列，并不等同于输出列或物理读取字节。派生列在内部查询处统计基础依赖；常量输出别名不算基表列。
- 旧列名口径未展开星号、未区分同名列所属表；新口径与旧口径不同，保留两者方便追溯。Join 片段只比较该 JOIN 节点，不证明其左输入、中间结果或谓词下推相同。
- 过滤条件只拆 AND 合取项，保留常量值；未证明一般谓词等价或包含。简单区间沿用原分析器，仅支持单表直接列与字面量比较；不覆盖复杂日期函数/CAST 列表达式。区间兼容不是实际行集合相交的证明。
- 分组、聚合、投影和排序仅为表达式结构重合，输入行可能不同；相同 GROUP BY 加相同聚合仍不足以推出同一聚合结果。基表引用绑定后未实现所有派生关系的代数等价归一。
- 结果重合比较相同输出列名下的实际 JSON 行值，忽略行顺序与重复次数，且限定同库共享表的查询对。统计值碰巧相同也会命中；这不证明底层数据范围相同，也不表示可以省掉查询。
- 前序引用列覆盖后序只说明列需求集合包含，不代表前序输出包含这些列，更不代表其行范围覆盖后序。
- SQL 完全重复和保守复用候选沿用原分析。0 个保守候选不排除一般 Join 中间结果复用或聚合 rollup。物理扫描行/字节 overlap、通用结果包含关系和净性能收益本次尚未测量。

逐查询绑定特征、逐对命中类别及 call_id 见 [overlap-detail.json](overlap-detail.json)。原 SQL 位于各运行目录的 sql/，通过 call_id 可对应查询和完整结果。复算：

```bash
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/overlap_report.py
```
