# 全量任务：查询重叠与潜在共同优化机会

**进度：108/108 次运行已结束。全量运行已结束。**

正式清单为 12 个数据集、54 个任务，每题自然/FAD 各一次。任务与数据均固定版本，旧 9 题试跑不混入本组。

## 统计规则

依据原始 SQL、执行状态、schema 和保存结果离线比较。只在同一任务、同一组、同一库内比较前后成功数据调用。不使用性能数据证明复用。

| 列 | 具体规则 |
|---|---|
| 验证 | 结束后原始 benchmark 验证器是否通过；未通过不等于 SQL 执行失败。 |
| 成功 SQL | 成功执行的数据查询调用数，排除元数据和失败尝试；多语句仍计一次。 |
| 同表 | 与本任务同组同库的至少一个前序成功查询共享基表。 |
| 同表列 | 共享具体 (基表,列)，按 schema 展开 SELECT *，包含过滤/连接等列；COUNT(*) 不视为所有列。 |
| WHERE 合取项 | 将 WHERE 按 AND 拆分、绑定基表并归一表达式后匹配相同项，保留常量。 |
| Join 片段 | 基表别名归一后相同 Join 节点；不保证左输入、完整中间结果或可复用性。 |
| 聚合表达式 | 相同基表集合中有相同聚合表达式；不要求分组、过滤或输入行相同，不是聚合复用次数。 |
| GROUP BY | 相同基表集合中有相同完整 GROUP BY 结构；不是含分组的调用总数。 |
| 相同结果行 | 同库共享表、输出列名相同时，实际 JSON 行值集合有交集；忽略行序/重复次数，多语句调用排除。 |

运行记录：Kimi 曾返回 5 小时用量额度限制；首批 16 次受影响尝试已单独归档并排除主统计，额度恢复后补跑。正常答题失败仍保留，不因验证结果重跑。详见 [额度中断记录](quota-interruption.json)。


**从“同表”到“相同结果行”均按后续调用去重，列之间不可相加。** 同一后续调用与多个前序匹配也只算一次。若存在无法完整绑定的 SQL，对应任务计数标为 ≥（仅已解析部分），并列出覆盖数。Mongo 原生查询另表记录，不当作 SQL。

## 1. 逐任务查询统计

### DEPS_DEV_V1

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/DEPS_DEV_V1/query1/full-01/analysis.json) | 自然 | ✗ | 8 | 6 | 5 | 5 | 1 | 0 | 0 | 1 | 8/8 |
| [query1](../runs/fad/DEPS_DEV_V1/query1/full-01/analysis.json) | FAD | ✓ | 12 | 10 | 9 | 6 | 2 | 2 | 2 | 3 | 12/12 |
| [query2](../runs/natural/DEPS_DEV_V1/query2/full-01/analysis.json) | 自然 | ✗ | 14 | 11 | 11 | 5 | 0 | 1 | 0 | 0 | 14/14 |
| [query2](../runs/fad/DEPS_DEV_V1/query2/full-01/analysis.json) | FAD | ✗ | 5 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 5/5 |

### GITHUB_REPOS

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/GITHUB_REPOS/query1/full-01/analysis.json) | 自然 | ✗ | 7 | 5 | 4 | 0 | 0 | 3 | 0 | 0 | 7/7 |
| [query1](../runs/fad/GITHUB_REPOS/query1/full-01/analysis.json) | FAD | ✗ | 6 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 6/6 |
| [query2](../runs/natural/GITHUB_REPOS/query2/full-01/analysis.json) | 自然 | ✓ | 15 | 12 | 12 | 4 | 2 | 2 | 1 | 0 | 15/15 |
| [query2](../runs/fad/GITHUB_REPOS/query2/full-01/analysis.json) | FAD | ✗ | 7 | 4 | 4 | 3 | 0 | 1 | 1 | 0 | 7/7 |
| [query3](../runs/natural/GITHUB_REPOS/query3/full-01/analysis.json) | 自然 | ✓ | 13 | 10 | 10 | 5 | 1 | 4 | 0 | 0 | 13/13 |
| [query3](../runs/fad/GITHUB_REPOS/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 1 | 1 | 0 | 0 | 0 | 4/4 |
| [query4](../runs/natural/GITHUB_REPOS/query4/full-01/analysis.json) | 自然 | ✗ | 6 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 6/6 |
| [query4](../runs/fad/GITHUB_REPOS/query4/full-01/analysis.json) | FAD | ✓ | 5 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 5/5 |

### PANCANCER_ATLAS

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/PANCANCER_ATLAS/query1/full-01/analysis.json) | 自然 | ✗ | 7 | 5 | 4 | 1 | 0 | 3 | 0 | 0 | 7/7 |
| [query1](../runs/fad/PANCANCER_ATLAS/query1/full-01/analysis.json) | FAD | ✗ | 5 | 3 | 3 | 2 | 0 | 1 | 0 | 0 | 5/5 |
| [query2](../runs/natural/PANCANCER_ATLAS/query2/full-01/analysis.json) | 自然 | ✓ | 8 | 6 | 5 | 2 | 0 | 0 | 0 | 2 | 8/8 |
| [query2](../runs/fad/PANCANCER_ATLAS/query2/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 4/4 |
| [query3](../runs/natural/PANCANCER_ATLAS/query3/full-01/analysis.json) | 自然 | ✓ | 7 | 5 | 5 | 3 | 0 | 1 | 0 | 0 | 7/7 |
| [query3](../runs/fad/PANCANCER_ATLAS/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 1 | 0 | 1 | 0 | 0 | 4/4 |

### PATENTS

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/PATENTS/query1/full-01/analysis.json) | 自然 | ✗ | 12 | 10 | 9 | 1 | 0 | 1 | 0 | 1 | 12/12 |
| [query1](../runs/fad/PATENTS/query1/full-01/analysis.json) | FAD | ✗ | 10 | 8 | 7 | 2 | 1 | 3 | 0 | 0 | 10/10 |
| [query2](../runs/natural/PATENTS/query2/full-01/analysis.json) | 自然 | ✗ | 12 | 10 | 9 | 3 | 0 | 5 | 1 | 2 | 12/12 |
| [query2](../runs/fad/PATENTS/query2/full-01/analysis.json) | FAD | ✓ | 8 | 6 | 5 | 1 | 0 | 0 | 0 | 0 | 8/8 |
| [query3](../runs/natural/PATENTS/query3/full-01/analysis.json) | 自然 | ✗ | 5 | 3 | 2 | 0 | 0 | 0 | 0 | 0 | 5/5 |
| [query3](../runs/fad/PATENTS/query3/full-01/analysis.json) | FAD | ✗ | 12 | 10 | 10 | 4 | 0 | 3 | 0 | 0 | 12/12 |

### agnews

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/agnews/query1/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query1](../runs/fad/agnews/query1/full-01/analysis.json) | FAD | ✓ | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query2](../runs/natural/agnews/query2/full-01/analysis.json) | 自然 | ✗ | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query2](../runs/fad/agnews/query2/full-01/analysis.json) | FAD | ✗ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/natural/agnews/query3/full-01/analysis.json) | 自然 | ✗ | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/fad/agnews/query3/full-01/analysis.json) | FAD | ✗ | 3 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 3/3 |
| [query4](../runs/natural/agnews/query4/full-01/analysis.json) | 自然 | ✓ | 4 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query4](../runs/fad/agnews/query4/full-01/analysis.json) | FAD | ✗ | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 0 | 4/4 |

### bookreview

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/bookreview/query1/full-01/analysis.json) | 自然 | ✓ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query1](../runs/fad/bookreview/query1/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | 4/4 |
| [query2](../runs/natural/bookreview/query2/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 3/3 |
| [query2](../runs/fad/bookreview/query2/full-01/analysis.json) | FAD | ✓ | 5 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 5/5 |
| [query3](../runs/natural/bookreview/query3/full-01/analysis.json) | 自然 | ✓ | 5 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 5/5 |
| [query3](../runs/fad/bookreview/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 1 | 4/4 |

### crmarenapro

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/crmarenapro/query1/full-01/analysis.json) | 自然 | ✓ | 6 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 6/6 |
| [query1](../runs/fad/crmarenapro/query1/full-01/analysis.json) | FAD | ✓ | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6/6 |
| [query2](../runs/natural/crmarenapro/query2/full-01/analysis.json) | 自然 | ✓ | 9 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 9/9 |
| [query2](../runs/fad/crmarenapro/query2/full-01/analysis.json) | FAD | ✗ | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query3](../runs/natural/crmarenapro/query3/full-01/analysis.json) | 自然 | ✓ | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 7/7 |
| [query3](../runs/fad/crmarenapro/query3/full-01/analysis.json) | FAD | ✓ | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5/5 |
| [query4](../runs/natural/crmarenapro/query4/full-01/analysis.json) | 自然 | ✓ | 10 | 8 | 8 | 3 | 0 | 3 | 2 | 3 | 10/10 |
| [query4](../runs/fad/crmarenapro/query4/full-01/analysis.json) | FAD | ✓ | 9 | 7 | 7 | 2 | 0 | 0 | 0 | 3 | 9/9 |
| [query5](../runs/natural/crmarenapro/query5/full-01/analysis.json) | 自然 | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query5](../runs/fad/crmarenapro/query5/full-01/analysis.json) | FAD | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query6](../runs/natural/crmarenapro/query6/full-01/analysis.json) | 自然 | ✓ | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6/6 |
| [query6](../runs/fad/crmarenapro/query6/full-01/analysis.json) | FAD | ✓ | 9 | 6 | 6 | 1 | 1 | 0 | 0 | 0 | 9/9 |
| [query7](../runs/natural/crmarenapro/query7/full-01/analysis.json) | 自然 | ✓ | 21 | 8 | 8 | 0 | 0 | 0 | 0 | 0 | 21/21 |
| [query7](../runs/fad/crmarenapro/query7/full-01/analysis.json) | FAD | ✗ | 14 | 10 | 10 | 2 | 1 | 0 | 0 | 1 | 14/14 |
| [query8](../runs/natural/crmarenapro/query8/full-01/analysis.json) | 自然 | ✓ | 6 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 6/6 |
| [query8](../runs/fad/crmarenapro/query8/full-01/analysis.json) | FAD | ✓ | 4 | 3 | 3 | 2 | 0 | 0 | 0 | 1 | 4/4 |
| [query9](../runs/natural/crmarenapro/query9/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query9](../runs/fad/crmarenapro/query9/full-01/analysis.json) | FAD | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query10](../runs/natural/crmarenapro/query10/full-01/analysis.json) | 自然 | ✓ | 8 | 6 | 6 | 3 | 1 | 3 | 1 | 0 | 8/8 |
| [query10](../runs/fad/crmarenapro/query10/full-01/analysis.json) | FAD | ✓ | 6 | 4 | 4 | 2 | 0 | 1 | 0 | 1 | 6/6 |
| [query11](../runs/natural/crmarenapro/query11/full-01/analysis.json) | 自然 | ✓ | 6 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 6/6 |
| [query11](../runs/fad/crmarenapro/query11/full-01/analysis.json) | FAD | ✓ | 8 | 5 | 5 | 1 | 1 | 0 | 0 | 0 | 8/8 |
| [query12](../runs/natural/crmarenapro/query12/full-01/analysis.json) | 自然 | ✗ | 9 | 7 | 7 | 3 | 3 | 4 | 3 | 2 | 9/9 |
| [query12](../runs/fad/crmarenapro/query12/full-01/analysis.json) | FAD | ✗ | 3 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 3/3 |
| [query13](../runs/natural/crmarenapro/query13/full-01/analysis.json) | 自然 | ✗ | 9 | 4 | 4 | 0 | 0 | 0 | 0 | 0 | 9/9 |
| [query13](../runs/fad/crmarenapro/query13/full-01/analysis.json) | FAD | ✗ | 4 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 4/4 |

### googlelocal

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/googlelocal/query1/full-01/analysis.json) | 自然 | ✓ | 4 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 4/4 |
| [query1](../runs/fad/googlelocal/query1/full-01/analysis.json) | FAD | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query2](../runs/natural/googlelocal/query2/full-01/analysis.json) | 自然 | ✗ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query2](../runs/fad/googlelocal/query2/full-01/analysis.json) | FAD | ✗ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/natural/googlelocal/query3/full-01/analysis.json) | 自然 | ✓ | 4 | 2 | 1 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query3](../runs/fad/googlelocal/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 1 | 0 | 0 | 0 | 1 | 4/4 |
| [query4](../runs/natural/googlelocal/query4/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query4](../runs/fad/googlelocal/query4/full-01/analysis.json) | FAD | ✗ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |

### music_brainz_20k

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/music_brainz_20k/query1/full-01/analysis.json) | 自然 | ✗ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query1](../runs/fad/music_brainz_20k/query1/full-01/analysis.json) | FAD | ✗ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query2](../runs/natural/music_brainz_20k/query2/full-01/analysis.json) | 自然 | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query2](../runs/fad/music_brainz_20k/query2/full-01/analysis.json) | FAD | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query3](../runs/natural/music_brainz_20k/query3/full-01/analysis.json) | 自然 | ✗ | 4 | 2 | 2 | 0 | 0 | 1 | 1 | 1 | 4/4 |
| [query3](../runs/fad/music_brainz_20k/query3/full-01/analysis.json) | FAD | ✗ | 4 | 2 | 2 | 0 | 0 | 1 | 1 | 0 | 4/4 |

### stockindex

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/stockindex/query1/full-01/analysis.json) | 自然 | ✓ | 5 | 3 | 3 | 1 | 0 | 1 | 1 | 0 | 5/5 |
| [query1](../runs/fad/stockindex/query1/full-01/analysis.json) | FAD | ✓ | 5 | 3 | 3 | 1 | 0 | 1 | 0 | 0 | 5/5 |
| [query2](../runs/natural/stockindex/query2/full-01/analysis.json) | 自然 | ✗ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query2](../runs/fad/stockindex/query2/full-01/analysis.json) | FAD | ✗ | 4 | 2 | 2 | 0 | 0 | 1 | 1 | 0 | 4/4 |
| [query3](../runs/natural/stockindex/query3/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/fad/stockindex/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 4/4 |

### stockmarket

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/stockmarket/query1/full-01/analysis.json) | 自然 | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query1](../runs/fad/stockmarket/query1/full-01/analysis.json) | FAD | ✓ | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2/2 |
| [query2](../runs/natural/stockmarket/query2/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query2](../runs/fad/stockmarket/query2/full-01/analysis.json) | FAD | ✓ | 5 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 5/5 |
| [query3](../runs/natural/stockmarket/query3/full-01/analysis.json) | 自然 | ✗ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/fad/stockmarket/query3/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query4](../runs/natural/stockmarket/query4/full-01/analysis.json) | 自然 | ✓ | 3 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 3/3 |
| [query4](../runs/fad/stockmarket/query4/full-01/analysis.json) | FAD | ✗ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 4/4 |
| [query5](../runs/natural/stockmarket/query5/full-01/analysis.json) | 自然 | ✓ | 5 | 3 | 3 | 0 | 0 | 0 | 0 | 0 | 5/5 |
| [query5](../runs/fad/stockmarket/query5/full-01/analysis.json) | FAD | ✓ | 4 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 4/4 |

### yelp

| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [query1](../runs/natural/yelp/query1/full-01/analysis.json) | 自然 | ✓ | 4 | 3 | 3 | 1 | 0 | 2 | 1 | 0 | 4/4 |
| [query1](../runs/fad/yelp/query1/full-01/analysis.json) | FAD | ✓ | 4 | 3 | 3 | 1 | 0 | 2 | 1 | 0 | 4/4 |
| [query2](../runs/natural/yelp/query2/full-01/analysis.json) | 自然 | ✗ | 3 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 3/3 |
| [query2](../runs/fad/yelp/query2/full-01/analysis.json) | FAD | ✓ | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1/1 |
| [query3](../runs/natural/yelp/query3/full-01/analysis.json) | 自然 | ✓ | 3 | 2 | 2 | 1 | 0 | 0 | 0 | 0 | 3/3 |
| [query3](../runs/fad/yelp/query3/full-01/analysis.json) | FAD | ✓ | 4 | 3 | 3 | 1 | 0 | 0 | 0 | 0 | 4/4 |
| [query4](../runs/natural/yelp/query4/full-01/analysis.json) | 自然 | ✓ | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1/1 |
| [query4](../runs/fad/yelp/query4/full-01/analysis.json) | FAD | ✓ | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1/1 |
| [query5](../runs/natural/yelp/query5/full-01/analysis.json) | 自然 | ✓ | 4 | 3 | 3 | 0 | 0 | 2 | 0 | 0 | 4/4 |
| [query5](../runs/fad/yelp/query5/full-01/analysis.json) | FAD | ✓ | 3 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 3/3 |
| [query6](../runs/natural/yelp/query6/full-01/analysis.json) | 自然 | ✓ | 3 | 2 | 2 | 0 | 0 | 1 | 0 | 0 | 3/3 |
| [query6](../runs/fad/yelp/query6/full-01/analysis.json) | FAD | ✓ | 3 | 2 | 2 | 1 | 0 | 1 | 0 | 0 | 3/3 |
| [query7](../runs/natural/yelp/query7/full-01/analysis.json) | 自然 | ✓ | 5 | 3 | 2 | 1 | 0 | 0 | 0 | 0 | 5/5 |
| [query7](../runs/fad/yelp/query7/full-01/analysis.json) | FAD | ✓ | 4 | 3 | 1 | 0 | 0 | 0 | 0 | 1 | 4/4 |

## 2. 可提出具体准备方案的候选

自动候选采用比上表更严格的规则：同一基表上的相同筛选；完全相同基表输入/键/类型的内连接；同一基表列的相同非平凡派生表达式；或 FROM、WHERE、GROUP BY 全部相同的聚合状态。不同输入/分组的 COUNT 不算聚合复用。Mongo 仅识别相同集合的非空原生筛选。

以下数的是候选对象组，同一种对象、相同输入和相同消费者集合中的多个表达式合并。不同种类可能是同一优化的替代方案，**不能把各类之和当成互不重复的优化数量**。覆盖调用按任务去重，可仅有部分子计算受益。尚未测加速、改写等价和 FAD 当时是否能提前给出信息。

| 任务 | 组 | 公共筛选 | 公共内连接 | 派生计算 | 同输入聚合状态 | Mongo 筛选 | 涉及调用（去重） | 首次后仍有至少 2 次使用的对象组 | 证据 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| DEPS_DEV_V1/query1 | FAD | 2 | 0 | 3 | 0 | 0 | 11 | 2 | [C0001](OPPORTUNITY_CASES.md#c0001) [C0002](OPPORTUNITY_CASES.md#c0002) [C0003](OPPORTUNITY_CASES.md#c0003) [C0004](OPPORTUNITY_CASES.md#c0004) [C0005](OPPORTUNITY_CASES.md#c0005) |
| DEPS_DEV_V1/query1 | 自然 | 2 | 0 | 1 | 0 | 0 | 7 | 1 | [C0041](OPPORTUNITY_CASES.md#c0041) [C0042](OPPORTUNITY_CASES.md#c0042) [C0043](OPPORTUNITY_CASES.md#c0043) |
| DEPS_DEV_V1/query2 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0006](OPPORTUNITY_CASES.md#c0006) |
| DEPS_DEV_V1/query2 | 自然 | 4 | 0 | 0 | 0 | 0 | 7 | 2 | [C0044](OPPORTUNITY_CASES.md#c0044) [C0045](OPPORTUNITY_CASES.md#c0045) [C0046](OPPORTUNITY_CASES.md#c0046) [C0047](OPPORTUNITY_CASES.md#c0047) |
| GITHUB_REPOS/query1 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0007](OPPORTUNITY_CASES.md#c0007) |
| GITHUB_REPOS/query1 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| GITHUB_REPOS/query2 | FAD | 1 | 0 | 1 | 0 | 0 | 4 | 1 | [C0008](OPPORTUNITY_CASES.md#c0008) [C0009](OPPORTUNITY_CASES.md#c0009) |
| GITHUB_REPOS/query2 | 自然 | 3 | 1 | 1 | 0 | 0 | 7 | 3 | [C0048](OPPORTUNITY_CASES.md#c0048) [C0049](OPPORTUNITY_CASES.md#c0049) [C0050](OPPORTUNITY_CASES.md#c0050) [C0051](OPPORTUNITY_CASES.md#c0051) [C0052](OPPORTUNITY_CASES.md#c0052) |
| GITHUB_REPOS/query3 | FAD | 2 | 1 | 0 | 0 | 0 | 2 | 0 | [C0010](OPPORTUNITY_CASES.md#c0010) [C0011](OPPORTUNITY_CASES.md#c0011) [C0012](OPPORTUNITY_CASES.md#c0012) |
| GITHUB_REPOS/query3 | 自然 | 4 | 1 | 0 | 0 | 0 | 7 | 2 | [C0053](OPPORTUNITY_CASES.md#c0053) [C0054](OPPORTUNITY_CASES.md#c0054) [C0055](OPPORTUNITY_CASES.md#c0055) [C0056](OPPORTUNITY_CASES.md#c0056) [C0057](OPPORTUNITY_CASES.md#c0057) |
| GITHUB_REPOS/query4 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| GITHUB_REPOS/query4 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| PANCANCER_ATLAS/query1 | FAD | 2 | 0 | 0 | 0 | 0 | 3 | 1 | [C0013](OPPORTUNITY_CASES.md#c0013) [C0014](OPPORTUNITY_CASES.md#c0014) |
| PANCANCER_ATLAS/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0058](OPPORTUNITY_CASES.md#c0058) |
| PANCANCER_ATLAS/query2 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0015](OPPORTUNITY_CASES.md#c0015) |
| PANCANCER_ATLAS/query2 | 自然 | 1 | 0 | 0 | 0 | 0 | 3 | 1 | [C0059](OPPORTUNITY_CASES.md#c0059) |
| PANCANCER_ATLAS/query3 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0016](OPPORTUNITY_CASES.md#c0016) |
| PANCANCER_ATLAS/query3 | 自然 | 2 | 0 | 0 | 0 | 0 | 5 | 1 | [C0060](OPPORTUNITY_CASES.md#c0060) [C0061](OPPORTUNITY_CASES.md#c0061) |
| PATENTS/query1 | FAD | 1 | 0 | 1 | 1 | 0 | 6 | 0 | [C0017](OPPORTUNITY_CASES.md#c0017) [C0018](OPPORTUNITY_CASES.md#c0018) [C0019](OPPORTUNITY_CASES.md#c0019) |
| PATENTS/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0062](OPPORTUNITY_CASES.md#c0062) |
| PATENTS/query2 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0020](OPPORTUNITY_CASES.md#c0020) |
| PATENTS/query2 | 自然 | 3 | 0 | 0 | 0 | 0 | 5 | 2 | [C0063](OPPORTUNITY_CASES.md#c0063) [C0064](OPPORTUNITY_CASES.md#c0064) [C0065](OPPORTUNITY_CASES.md#c0065) |
| PATENTS/query3 | FAD | 3 | 0 | 0 | 1 | 0 | 8 | 1 | [C0021](OPPORTUNITY_CASES.md#c0021) [C0022](OPPORTUNITY_CASES.md#c0022) [C0023](OPPORTUNITY_CASES.md#c0023) [C0024](OPPORTUNITY_CASES.md#c0024) |
| PATENTS/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query1 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query3 | FAD | 1 | 0 | 1 | 0 | 1 | 4 | 0 | [C0025](OPPORTUNITY_CASES.md#c0025) [C0026](OPPORTUNITY_CASES.md#c0026) [C0089](OPPORTUNITY_CASES.md#c0089) |
| agnews/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query4 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| agnews/query4 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| bookreview/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| bookreview/query1 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| bookreview/query2 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0027](OPPORTUNITY_CASES.md#c0027) |
| bookreview/query2 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0066](OPPORTUNITY_CASES.md#c0066) |
| bookreview/query3 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| bookreview/query3 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0067](OPPORTUNITY_CASES.md#c0067) |
| crmarenapro/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0068](OPPORTUNITY_CASES.md#c0068) |
| crmarenapro/query10 | FAD | 1 | 0 | 0 | 0 | 0 | 3 | 1 | [C0028](OPPORTUNITY_CASES.md#c0028) |
| crmarenapro/query10 | 自然 | 2 | 0 | 1 | 0 | 0 | 4 | 2 | [C0069](OPPORTUNITY_CASES.md#c0069) [C0070](OPPORTUNITY_CASES.md#c0070) [C0071](OPPORTUNITY_CASES.md#c0071) |
| crmarenapro/query11 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0029](OPPORTUNITY_CASES.md#c0029) |
| crmarenapro/query11 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query12 | FAD | 0 | 1 | 0 | 0 | 0 | 2 | 0 | [C0030](OPPORTUNITY_CASES.md#c0030) |
| crmarenapro/query12 | 自然 | 2 | 2 | 2 | 0 | 0 | 6 | 2 | [C0072](OPPORTUNITY_CASES.md#c0072) [C0073](OPPORTUNITY_CASES.md#c0073) [C0074](OPPORTUNITY_CASES.md#c0074) [C0075](OPPORTUNITY_CASES.md#c0075) [C0076](OPPORTUNITY_CASES.md#c0076) [C0077](OPPORTUNITY_CASES.md#c0077) |
| crmarenapro/query13 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query13 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query3 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query4 | FAD | 1 | 0 | 0 | 0 | 0 | 3 | 1 | [C0031](OPPORTUNITY_CASES.md#c0031) |
| crmarenapro/query4 | 自然 | 3 | 0 | 1 | 0 | 0 | 5 | 1 | [C0078](OPPORTUNITY_CASES.md#c0078) [C0079](OPPORTUNITY_CASES.md#c0079) [C0080](OPPORTUNITY_CASES.md#c0080) [C0081](OPPORTUNITY_CASES.md#c0081) |
| crmarenapro/query5 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query5 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query6 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0032](OPPORTUNITY_CASES.md#c0032) |
| crmarenapro/query6 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query7 | FAD | 2 | 0 | 0 | 0 | 0 | 3 | 0 | [C0033](OPPORTUNITY_CASES.md#c0033) [C0034](OPPORTUNITY_CASES.md#c0034) |
| crmarenapro/query7 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query8 | FAD | 1 | 0 | 0 | 0 | 0 | 3 | 1 | [C0035](OPPORTUNITY_CASES.md#c0035) |
| crmarenapro/query8 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0082](OPPORTUNITY_CASES.md#c0082) |
| crmarenapro/query9 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| crmarenapro/query9 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0083](OPPORTUNITY_CASES.md#c0083) |
| googlelocal/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query3 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0036](OPPORTUNITY_CASES.md#c0036) |
| googlelocal/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query4 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| googlelocal/query4 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| music_brainz_20k/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| music_brainz_20k/query1 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| music_brainz_20k/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| music_brainz_20k/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| music_brainz_20k/query3 | FAD | 0 | 0 | 0 | 1 | 0 | 2 | 0 | [C0037](OPPORTUNITY_CASES.md#c0037) |
| music_brainz_20k/query3 | 自然 | 0 | 0 | 0 | 1 | 0 | 2 | 0 | [C0084](OPPORTUNITY_CASES.md#c0084) |
| stockindex/query1 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0038](OPPORTUNITY_CASES.md#c0038) |
| stockindex/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0085](OPPORTUNITY_CASES.md#c0085) |
| stockindex/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockindex/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockindex/query3 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockindex/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query1 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query1 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query3 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query3 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query4 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query4 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query5 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| stockmarket/query5 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query1 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0039](OPPORTUNITY_CASES.md#c0039) |
| yelp/query1 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0086](OPPORTUNITY_CASES.md#c0086) |
| yelp/query2 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query2 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query3 | FAD | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0040](OPPORTUNITY_CASES.md#c0040) |
| yelp/query3 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0087](OPPORTUNITY_CASES.md#c0087) |
| yelp/query4 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query4 | 自然 | 0 | 0 | 0 | 0 | 1 | 2 | 0 | [C0090](OPPORTUNITY_CASES.md#c0090) |
| yelp/query5 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query5 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query6 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query6 | 自然 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query7 | FAD | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 未识别 |
| yelp/query7 | 自然 | 1 | 0 | 0 | 0 | 0 | 2 | 0 | [C0088](OPPORTUNITY_CASES.md#c0088) |

候选只是在支持的 SQL 作用域内保守提取，不是所有优化机会的穷尽枚举；外连接、自连接、复杂派生输入等未自动合并。泛化全表缓存、任意索引建议和单纯同名函数不计入。

[运行轮数及耗时](RUNS.md) · [MongoDB 调用](MONGO.md) · [FAD 统计](FAD.md) · [数据位置与规模](DATA.md) · [错误及解析覆盖](ERRORS.md) · [机器可读结构明细](overlap-detail.json) · [候选原文](opportunities.json)
