> 本页保留运行/FAD 数据与历史结构指标。结构相似计数不是优化机会数量；当前多查询机会见 [OVERLAP.md](OVERLAP.md)。

# 九题快速验证：数据表

配置：Kimi CLI 0.41.0 / kimi-code/k3；自然组与 FAD 组各一次；不使用 hints；3 个并发运行进程。
任务按描述预先选取，非随机总体样本。通过指原始 benchmark 验证器通过。

| 任务 | 组别 | 验证 | 数据 SQL | 元数据 SQL | 失败数据 SQL | 空结果 | 重访表的后续 SQL | 复用语法候选 | FAD | 时长/秒 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| [bookreview/query1](../runs/fad/bookreview/query1/quick-01/analysis.json) | fad | 通过 | 3 | 2 | 0 | 0 | 1 | 0 | 3 | 163.6 |
| [bookreview/query1](../runs/natural/bookreview/query1/quick-01/analysis.json) | natural | 通过 | 5 | 2 | 0 | 0 | 3 | 0 | 0 | 132.9 |
| [bookreview/query2](../runs/fad/bookreview/query2/quick-01/analysis.json) | fad | 通过 | 3 | 2 | 0 | 0 | 1 | 0 | 3 | 125.8 |
| [bookreview/query2](../runs/natural/bookreview/query2/quick-01/analysis.json) | natural | 通过 | 7 | 4 | 0 | 2 | 5 | 0 | 0 | 168.1 |
| [bookreview/query3](../runs/fad/bookreview/query3/quick-01/analysis.json) | fad | 通过 | 5 | 2 | 0 | 0 | 3 | 0 | 5 | 164.6 |
| [bookreview/query3](../runs/natural/bookreview/query3/quick-01/analysis.json) | natural | 通过 | 9 | 2 | 0 | 0 | 7 | 0 | 0 | 115.9 |
| [crmarenapro/query12](../runs/fad/crmarenapro/query12/quick-01/analysis.json) | fad | 未通过 | 10 | 0 | 0 | 0 | 8 | 0 | 10 | 331.9 |
| [crmarenapro/query12](../runs/natural/crmarenapro/query12/quick-01/analysis.json) | natural | 未通过 | 11 | 0 | 0 | 0 | 8 | 0 | 0 | 172.9 |
| [crmarenapro/query13](../runs/fad/crmarenapro/query13/quick-01/analysis.json) | fad | 通过 | 3 | 1 | 0 | 0 | 2 | 0 | 3 | 123.0 |
| [crmarenapro/query13](../runs/natural/crmarenapro/query13/quick-01/analysis.json) | natural | 通过 | 13 | 2 | 1 | 0 | 8 | 0 | 0 | 224.8 |
| [crmarenapro/query8](../runs/fad/crmarenapro/query8/quick-01/analysis.json) | fad | 通过 | 5 | 1 | 0 | 0 | 3 | 0 | 5 | 617.1 |
| [crmarenapro/query8](../runs/natural/crmarenapro/query8/quick-01/analysis.json) | natural | 未通过 | 8 | 2 | 0 | 0 | 6 | 0 | 0 | 296.8 |
| [stockindex/query1](../runs/fad/stockindex/query1/quick-01/analysis.json) | fad | 通过 | 6 | 3 | 0 | 0 | 4 | 0 | 7 | 242.5 |
| [stockindex/query1](../runs/natural/stockindex/query1/quick-01/analysis.json) | natural | 通过 | 3 | 3 | 0 | 0 | 1 | 0 | 0 | 72.9 |
| [stockindex/query2](../runs/fad/stockindex/query2/quick-01/analysis.json) | fad | 未通过 | 4 | 3 | 0 | 0 | 2 | 0 | 5 | 166.3 |
| [stockindex/query2](../runs/natural/stockindex/query2/quick-01/analysis.json) | natural | 通过 | 4 | 3 | 0 | 0 | 2 | 0 | 0 | 107.8 |
| [stockindex/query3](../runs/fad/stockindex/query3/quick-01/analysis.json) | fad | 通过 | 3 | 3 | 0 | 0 | 1 | 0 | 4 | 248.8 |
| [stockindex/query3](../runs/natural/stockindex/query3/quick-01/analysis.json) | natural | 通过 | 6 | 3 | 0 | 0 | 4 | 0 | 0 | 195.2 |

## 分组汇总

| 指标 | natural | fad |
|---|---:|---:|
| 运行数 | 9 | 9 |
| 通过数 | 7 | 7 |
| 数据查询数（含失败） | 66 | 42 |
| 元数据查询数 | 21 | 17 |
| 失败数据查询 | 1 | 0 |
| 执行成功但空结果 | 2 | 0 |
| 与前序成功查询共享表的后续查询数 | 44 | 25 |
| 共享表且共享列的后续查询数 | 37 | 25 |
| 存在相同 WHERE 文本的后续查询数 | 5 | 5 |
| 存在相同 Join 片段的后续查询数 | 7 | 4 |
| 存在相同聚合表达式的后续查询数 | 11 | 13 |
| 规范化 SQL 完全相同的后续查询数 | 0 | 0 |
| 满足保守结果复用语法条件的后续查询数 | 0 | 0 |
| 成功提交 FAD 数 | 0 | 45 |
| 适配器 Python 调用数 | 7 | 5 |
| 可见 assistant 消息数 | 103 | 162 |

注意：不同结构指标可以重叠，不能相加。同表/同 Join 片段均为候选，不表示已验证物理复用或净收益。

## FAD 预测统计

以下为各前瞻点的宏平均；分母 n 为有定义的前瞻点数。元数据目标已分离；针对已发出 SQL 的结构评分包含失败 SQL。

| 指标 | 平均值 | n |
|---|---:|---:|
| 整个 frontier 对下一条 SQL 的表精度 | 82.1% | 42 |
| 下一条 SQL 的表覆盖率 | 100.0% | 42 |
| 仅 horizon=1 条目的下一条表精度 | 98.4% | 42 |
| 仅 horizon=1 条目的下一条表覆盖率 | 100.0% | 42 |
| 整个 frontier 对后续最多三条 SQL 的表精度 | 95.2% | 42 |
| 后续最多三条 SQL 的表覆盖率 | 92.5% | 42 |
| 下一条 SQL 的列精度 | 85.0% | 42 |
| 下一条 SQL 的列覆盖率 | 90.9% | 39 |
| 下一条 SQL 的操作精度 | 93.7% | 42 |
| 下一条 SQL 的操作覆盖率 | 89.3% | 42 |
| 过滤条件精确合取项匹配精度 | 28.6% | 21 |
| 过滤条件精确合取项匹配覆盖率 | 29.0% | 20 |
| horizon 2/3 条目对第 2/3 条 SQL 的表精度 | 82.4% | 17 |
| horizon 2/3 条目对第 2/3 条 SQL 的表覆盖率 | 76.5% | 17 |
| 弱基线：上一条查询表集合覆盖下一条 | 47.6% | 42 |

- 数据目标 FAD：42；元数据目标：3；之后无查询：0。
- 明确包含 horizon 2/3 预测的数据 frontier：17。
- 下一条查询失败的数据 frontier：0。
- SQL 独立后续 assistant turn 时序检查：45/45；提前出现相同 SQL 的检查标记：0。
- FAD 完成到 SQL 提交的时间差：中位数 8.27 秒，范围 5.22–17.26 秒。
- 时间差包括模型生成与工具开销，不能等同于可隐藏的物化时间或实测加速。
- frontier 内含多个候选时，下一条表精度较低可以是正常分支/远期预测，不能全部解释为错误。第 2/3 条的独立指标更接近 rolling 能力。
- 过滤指标是严格文本结构匹配，SQL 等价条件可能被判未匹配；未测概率校准。

## FAD 按任务分布

| 任务 | 数据 frontier 数 | horizon=1 表覆盖 | 第 2/3 条表精度 | 有远期预测的 frontier 数 |
|---|---:|---:|---:|---:|
| bookreview/query1 | 3 | 100.0% | 100.0% | 2 |
| bookreview/query2 | 3 | 100.0% | 100.0% | 2 |
| bookreview/query3 | 5 | 100.0% | 100.0% | 2 |
| crmarenapro/query12 | 10 | 100.0% | 0.0% | 1 |
| crmarenapro/query13 | 3 | 100.0% | 100.0% | 1 |
| crmarenapro/query8 | 5 | 100.0% | 33.3% | 3 |
| stockindex/query1 | 6 | 100.0% | 100.0% | 3 |
| stockindex/query2 | 4 | 100.0% | 100.0% | 1 |
| stockindex/query3 | 3 | 100.0% | 100.0% | 2 |

## 两组运行变化

| 任务 | natural 秒 | fad 秒 | 数据 SQL natural → fad | 验证 natural → fad |
|---|---:|---:|---|---|
| bookreview/query1 | 132.9 | 163.6 | 5 → 3 | True → True |
| bookreview/query2 | 168.1 | 125.8 | 7 → 3 | True → True |
| bookreview/query3 | 115.9 | 164.6 | 9 → 5 | True → True |
| crmarenapro/query12 | 172.9 | 331.9 | 11 → 10 | False → False |
| crmarenapro/query13 | 224.8 | 123.0 | 13 → 3 | True → True |
| crmarenapro/query8 | 296.8 | 617.1 | 8 → 5 | False → True |
| stockindex/query1 | 72.9 | 242.5 | 3 → 6 | True → True |
| stockindex/query2 | 107.8 | 166.3 | 4 → 4 | True → False |
| stockindex/query3 | 195.2 | 248.8 | 6 → 3 | True → True |

同题两组是不同的随机轨迹，样本各一次，运行时长受共享资源与服务波动影响。这里仅描述变化，不估计 FAD 的因果开销或收益。

详细方法、约束及复跑方法见 [README](../README.md)。结论与案例见 [FINDINGS](FINDINGS.md)。
