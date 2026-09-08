# Characterizing SQL Trajectories of Data Analysis Agents

54 个任务 × 自然/FAD 两组，共 108 条轨迹；仅使用 full-01 全量实验。所有比较限定同一任务、同一组、同一次运行。答案验证失败的完整轨迹保留；额度中断尝试不混入。此次仅离线分析，没有调用 Agent、重跑数据库或测物化收益。

计数单位以 SQL 工具调用为主，多语句调用另列语句数。SQL 轨迹不等于整个 Agent 轨迹：元数据 SQL、Python、MongoDB 请求和 assistant 轮数分别保留。相邻指实际连续的数据 query-db 请求；过滤掉元数据，但失败或 Mongo 请求会中断有效 SQL 对，不跨过它们拼接。

## RQ1 — Trajectory Structure

| 组 | 任务数 | SQL 尝试总数 | 平均 N_SQL | 中位数 | P90 | 范围 | 成功 SQL | 平均 assistant 轮数 |
|---|---:|---:|---:|---:|---:|---|---:|---:|
| natural | 54 | 323 | 5.98 | 4.5 | 11 | 1–22 | 313 | 11.35 |
| fad | 54 | 262 | 4.85 | 4.0 | 8 | 1–17 | 256 | 22.94 |

这里 Length(T_SQL)=N_SQL（含失败数据 SQL 尝试），不是模型轮数或 SQL 语句数。详表同时记录三者；不能把结束轮数称为成功收敛轮数。

**本节结论：** 当前 workload 以较短的 SQL 轨迹为主，单任务平均约产生 5–6 次数据 SQL 调用。任务内存在跨查询优化的时间窗口，但可供摊销准备成本的后续查询数量有限，因此优化方案需要能在较少的复用次数内收回成本。FAD 组 SQL 较少、assistant 轮数较多只是本次观测，不能据此认定协议提高了效率。

## RQ2 — Cross-query Similarity

RelationOverlap、PredicateOverlap、JoinOverlap 均为对应特征集合的 Jaccard。表名包含逻辑数据库身份；谓词按归一 AST 的 WHERE 合取项严格匹配（基表别名归一，复杂派生列不保证完整血缘）；Join 是归一语法片段，尚非完整 Join 输入等价证明。空并集的 Jaccard 未定义，不算 1；未解析特征也不当作 0。

| 组 | 有效相邻 SQL 对 | Relation 命中 | 平均 Jaccard / n | Predicate 命中 / 可分析对 | 平均 Jaccard / n | Join 命中 / 可分析对 | 平均 Jaccard / n |
|---|---:|---:|---|---|---|---|---|
| natural | 244 | 104/244 | 0.40 / 244 | 24/244 | 0.08 / 201 | 5/244 | 0.13 / 33 |
| fad | 193 | 100/193 | 0.47 / 193 | 25/193 | 0.09 / 172 | 4/193 | 0.11 / 36 |

**本节结论：** 两组约四到五成的有效相邻 SQL 对访问了相同基表，说明任务内存在较明显的访问局部性；相同 WHERE 合取项和 Join 片段的命中则少得多。现有证据支持继续寻找共同扫描或共享子计算，但“访问同表”本身不能证明前序结果可复用，也不能直接作为物化收益。

## RQ3 — Analytical Evolution

先统计 GROUP BY 使用量，再在相同完整基表 FROM/INNER JOIN 输入的前后分组作用域中比较键集合。细化 A⊂B，粗化 B⊂A，sibling 为双方互不包含；相同键单列。分组表达式先解析别名和 GROUP BY 位置引用。两条 SQL 的多个作用域可使其进入不同类别，类别不可直接相加。

| 组 | 含 GROUP BY 的调用 | 涉及任务 | 支持基表输入演化分析的调用 | 同键查询对 | 细化对 | 粗化对 | Sibling 对 | 上述对中筛选发生变化 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| natural | 60 | 33/54 | 58 | 12 | 0 | 0 | 7 | 16 |
| fad | 55 | 35/54 | 49 | 5 | 0 | 0 | 5 | 8 |

演化不自动等于可复用：筛选不同、Join 不同、DISTINCT/不可合并聚合、Top-K 截断均会改变条件。细粒度到粗粒度需保存足够状态；反方向不能仅从已有粗粒度结果恢复细节。任意两个基表集合相同的查询不算相同输入。CTE/派生输入、外连接、自连接及复杂分组暂未做完整血缘演化识别；因此下表是支持范围内的计数，不能据零断言不存在。

**本节结论：** GROUP BY 在任务中并不少见，但在已覆盖的基表输入范围内，尚未观察到分组键严格包含的细化或粗化；已识别的变化包括同分组键下改变筛选条件，以及少量 sibling exploration。因此目前不支持“Agent 普遍逐级细化分组”的判断。聚合优化仍可围绕同键共享状态、多条件聚合和 sibling 的共同准备展开，但需验证输入语义及成本，且不能将当前零计数推广到未覆盖的复杂输入。

## RQ4 — Result Dependency

在相邻成功 SQL 对中，将后序 WHERE 的直接 column=literal、column IN(literals) 与前序保存的完整结果单元格匹配，保持类型及值；记录结果行号、列名、SQL 文件。仅字符串或数值常量，暂不推导范围谓词、函数转换、Python 派生值、Mongo→SQL、跨多个请求的依赖。多语句生产者排除。

| 组 | 相邻对分母 | 至少一项结果值匹配的对 | 涉及任务 | 新值匹配对* |
|---|---:|---:|---:|---:|
| natural | 244 | 42 | 30 | 24 |
| fad | 193 | 38 | 29 | 26 |

*新值仅指：此前 SQL 的同类谓词中未出现，且任务 prompt 未包含该值文本；不是世界知识新颖性或因果依赖证明。0/1、年份、常见类别等可以偶合；值匹配不证明模型读取并使用了结果。该实验也不能据此证明 future SQL 在 Q1 前不可能知道，或证明方案 novelty。需要结合轨迹人工核对，再用隐藏/扰动结果的对照实验建立更强依赖证据。

人工核对实例：agnews/query2 的 FAD 轨迹先[按 Amy Jones 查作者 ID](../../runs/fad/agnews/query2/full-01/sql/003-fc15464eda3949649d0d46f4187aa5ad.sql)，[结果](../../runs/fad/agnews/query2/full-01/results/fc15464eda3949649d0d46f4187aa5ad.json)为 `author_id=218`，随后[按 author_id=218 查文章](../../runs/fad/agnews/query2/full-01/sql/004-38cd4fc28cc34d239cf6fb5cbc0a4094.sql)。这是明确的“姓名→数据 ID→下一条查询筛选”的轨迹证据；仍不等于反事实意义上证明模型提前无法知道 ID。

**本节结论：** 两组均发现了前序结果值进入后序谓词的匹配，并有“姓名→作者 ID→文章筛选”的具体轨迹实例，支持“部分后续 SQL 参数随查询结果逐步确定”的研究假设。不过，自动值匹配可能包含巧合，尚不能仅凭该统计证明完整 future SQL 提前不可知或证明方案 novelty；更强结论需要逐例核对及结果隐藏／扰动实验。

## RQ5 — Cross-query Optimization Opportunity

ME 在此定义为 materialization candidate（共同准备对象候选）。保留公共筛选、完整公共内连接、标量子表达式、同输入聚合状态；新增同输入但分组键/指标不同的聚合 MV 候选：按分组键并集准备可合并状态，再服务各消费者。计入“可共享的子计算”，不宣称 MV 单独回答完整 SQL。

| 组 | 候选对象组 | 涉及任务 | MV Coverage：调用/成功 SQL | 后续调用覆盖 | Expected Reuse 中位数 | 后续可用≥2 次的对象组 |
|---|---:|---:|---|---:|---:|---:|
| natural | 51 | 22 | 82/313 (26.2%) | 51 | 1 | 17 |
| fad | 42 | 26 | 78/256 (30.5%) | 45 | 1.0 | 8 |

| Build-vs-Reuse 筛查 | 有完整时延记录的候选 | 乐观增量构建预算上界中位数（ms） | 上界不足 100ms 的候选 |
|---|---:|---:|---:|
| natural | 51 | 28.02 | 36 |
| fad | 42 | 33.36 | 27 |

上界采用各候选后续消费者的原始 execute+fetch 耗时之和，假设后续全部计算成本均可消除、MV 查询零成本。这是非常乐观的筛查上界，不是实际构建成本或预期收益；只覆盖已记录的数据库执行与取数计时，受并发/cache 状态影响，不含 JSON 序列化等环节。不同候选重叠，预算不可相加。

Expected Reuse = 已观察轨迹中首次使用后的可用调用数（不是概率期望），不要求连续；同一消费者内多个作用域只算一次。MV Coverage 在任务内去重，再相加；不同候选可能重叠或互为替代，候选组数不能相加解释为独立优化数。

**Build-vs-Reuse：尚无实测净收益。** 每个候选保存消费者已记录的 execute+fetch 时间作为原查询基线，build_ms/reuse_ms 留空。判断式为 `增量构建成本 + 维护/存储成本 < Σ后续查询(原成本 − 使用MV后的成本)`；若构建替代首次查询，应扣除被替代部分。不能把 SQL 总耗时当作可消除的聚合耗时，也不能把 Agent 思考时间算数据库收益。当前缺少 MV 构建及改写查询实测，不能报告加速比或盈亏平衡点。

聚合 MV 须保存完整分组：SUM/COUNT 可再求和，MIN/MAX 可再归并，AVG 保留 SUM 与非 NULL COUNT；不直接平均平均数。不自动支持 COUNT DISTINCT。细粒度并集可能接近基表大小，FILTER/空分组/NULL/类型及每个消费者的 HAVING/LIMIT 必须在改写验证中处理。

**本节结论：** 静态共享计算候选覆盖了两组约四分之一至三成的成功 SQL 调用，但覆盖仅表示其中存在潜在共享子计算。候选首次后的可用次数中位数为 1，乐观增量构建预算上界的中位数也仅为几十毫秒，因此“有机会”尚不足以说明“值得物化”。后续应优先验证原计算较贵、后续复用较多的任务内候选，通过实际构建和查询改写测量净收益。

## 逐任务总表

所有数字均来自本任务本组。R/P/J 是相邻对命中数；演化是全部前后调用对；依赖是相邻值匹配对；这几种分母不可混用。

| 任务 | 组 | 验证 | SQL尝试/成功 | GROUP BY调用 | 相邻对 | R/P/J命中 | 同键/细化/粗化/sibling | 结果匹配对 | MV覆盖调用 |
|---|---|---|---|---:|---:|---|---|---:|---:|
| DEPS_DEV_V1/query1 | fad | ✓ | 12/12 | 5 | 11 | 6/2/0 | 0/0/0/0 | 0 | 11 |
| DEPS_DEV_V1/query1 | natural | ✗ | 9/8 | 1 | 6 | 3/3/0 | 0/0/0/0 | 1 | 7 |
| DEPS_DEV_V1/query2 | fad | ✗ | 5/5 | 0 | 4 | 1/1/0 | 0/0/0/0 | 1 | 2 |
| DEPS_DEV_V1/query2 | natural | ✗ | 14/14 | 1 | 13 | 5/1/0 | 0/0/0/0 | 5 | 7 |
| GITHUB_REPOS/query1 | fad | ✗ | 6/6 | 1 | 5 | 2/1/0 | 0/0/0/0 | 1 | 2 |
| GITHUB_REPOS/query1 | natural | ✗ | 7/7 | 2 | 6 | 4/0/0 | 0/0/0/0 | 1 | 0 |
| GITHUB_REPOS/query2 | fad | ✗ | 7/7 | 3 | 6 | 2/2/0 | 1/0/0/0 | 1 | 4 |
| GITHUB_REPOS/query2 | natural | ✓ | 15/15 | 4 | 14 | 5/1/0 | 1/0/0/0 | 2 | 7 |
| GITHUB_REPOS/query3 | fad | ✓ | 4/4 | 2 | 3 | 2/1/1 | 0/0/0/0 | 0 | 2 |
| GITHUB_REPOS/query3 | natural | ✓ | 13/13 | 2 | 12 | 7/4/1 | 0/0/0/0 | 3 | 7 |
| GITHUB_REPOS/query4 | fad | ✓ | 5/5 | 2 | 4 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| GITHUB_REPOS/query4 | natural | ✗ | 6/6 | 2 | 5 | 2/0/0 | 0/0/0/0 | 1 | 0 |
| PANCANCER_ATLAS/query1 | fad | ✗ | 5/5 | 2 | 4 | 3/2/0 | 0/0/0/1 | 0 | 3 |
| PANCANCER_ATLAS/query1 | natural | ✗ | 7/7 | 4 | 6 | 5/1/0 | 0/0/0/3 | 0 | 4 |
| PANCANCER_ATLAS/query2 | fad | ✓ | 4/4 | 1 | 3 | 2/1/0 | 0/0/0/0 | 1 | 2 |
| PANCANCER_ATLAS/query2 | natural | ✓ | 8/8 | 1 | 7 | 4/2/0 | 0/0/0/0 | 0 | 3 |
| PANCANCER_ATLAS/query3 | fad | ✓ | 4/4 | 2 | 3 | 1/0/0 | 0/0/0/1 | 0 | 2 |
| PANCANCER_ATLAS/query3 | natural | ✓ | 7/7 | 3 | 6 | 3/1/0 | 0/0/0/1 | 0 | 5 |
| PATENTS/query1 | fad | ✗ | 10/10 | 4 | 9 | 6/0/0 | 0/0/0/0 | 1 | 6 |
| PATENTS/query1 | natural | ✗ | 12/12 | 2 | 11 | 6/0/0 | 0/0/0/0 | 1 | 2 |
| PATENTS/query2 | fad | ✓ | 8/8 | 1 | 7 | 6/1/0 | 0/0/0/0 | 0 | 2 |
| PATENTS/query2 | natural | ✗ | 14/12 | 4 | 10 | 7/3/0 | 1/0/0/2 | 0 | 5 |
| PATENTS/query3 | fad | ✗ | 14/12 | 0 | 10 | 10/3/0 | 0/0/0/0 | 0 | 8 |
| PATENTS/query3 | natural | ✗ | 7/5 | 0 | 3 | 3/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query1 | fad | ✓ | 2/2 | 1 | 0 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query1 | natural | ✓ | 3/3 | 0 | 1 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query2 | fad | ✗ | 3/3 | 0 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| agnews/query2 | natural | ✗ | 3/3 | 0 | 1 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query3 | fad | ✗ | 3/3 | 1 | 0 | 0/0/0 | 0/0/0/0 | 0 | 2 |
| agnews/query3 | natural | ✗ | 3/3 | 0 | 1 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query4 | fad | ✗ | 4/4 | 1 | 2 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| agnews/query4 | natural | ✓ | 4/4 | 0 | 1 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| bookreview/query1 | fad | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| bookreview/query1 | natural | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| bookreview/query2 | fad | ✓ | 5/5 | 1 | 4 | 2/1/0 | 0/0/0/0 | 0 | 2 |
| bookreview/query2 | natural | ✓ | 3/3 | 1 | 2 | 1/1/0 | 0/0/0/0 | 0 | 2 |
| bookreview/query3 | fad | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| bookreview/query3 | natural | ✓ | 5/5 | 1 | 4 | 0/0/0 | 0/0/0/0 | 0 | 2 |
| crmarenapro/query1 | fad | ✓ | 6/6 | 0 | 5 | 2/0/0 | 0/0/0/0 | 1 | 0 |
| crmarenapro/query1 | natural | ✓ | 6/6 | 0 | 5 | 2/0/0 | 0/0/0/0 | 2 | 2 |
| crmarenapro/query10 | fad | ✓ | 6/6 | 2 | 5 | 1/1/0 | 0/0/0/1 | 0 | 3 |
| crmarenapro/query10 | natural | ✓ | 8/8 | 4 | 7 | 4/3/1 | 0/0/0/1 | 1 | 4 |
| crmarenapro/query11 | fad | ✓ | 8/8 | 0 | 7 | 4/1/0 | 0/0/0/0 | 2 | 2 |
| crmarenapro/query11 | natural | ✓ | 6/6 | 0 | 5 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| crmarenapro/query12 | fad | ✗ | 3/3 | 2 | 2 | 1/0/1 | 1/0/0/0 | 1 | 2 |
| crmarenapro/query12 | natural | ✗ | 9/9 | 5 | 8 | 6/0/3 | 4/0/0/0 | 2 | 6 |
| crmarenapro/query13 | fad | ✗ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| crmarenapro/query13 | natural | ✗ | 9/9 | 0 | 8 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query2 | fad | ✗ | 4/4 | 0 | 3 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query2 | natural | ✓ | 9/9 | 0 | 8 | 0/0/0 | 0/0/0/0 | 3 | 0 |
| crmarenapro/query3 | fad | ✓ | 5/5 | 0 | 4 | 0/0/0 | 0/0/0/0 | 2 | 0 |
| crmarenapro/query3 | natural | ✓ | 7/7 | 0 | 6 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| crmarenapro/query4 | fad | ✓ | 9/9 | 0 | 8 | 1/0/0 | 0/0/0/0 | 2 | 3 |
| crmarenapro/query4 | natural | ✓ | 11/10 | 3 | 8 | 3/1/0 | 3/0/0/0 | 0 | 5 |
| crmarenapro/query5 | fad | ✓ | 2/2 | 0 | 1 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query5 | natural | ✓ | 3/2 | 0 | 0 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query6 | fad | ✓ | 9/9 | 0 | 8 | 5/1/1 | 0/0/0/0 | 3 | 2 |
| crmarenapro/query6 | natural | ✓ | 6/6 | 0 | 5 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| crmarenapro/query7 | fad | ✗ | 17/14 | 0 | 13 | 8/1/1 | 0/0/0/0 | 2 | 3 |
| crmarenapro/query7 | natural | ✓ | 22/21 | 0 | 19 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query8 | fad | ✓ | 4/4 | 0 | 3 | 3/2/0 | 0/0/0/0 | 1 | 3 |
| crmarenapro/query8 | natural | ✓ | 6/6 | 1 | 5 | 0/0/0 | 0/0/0/0 | 1 | 2 |
| crmarenapro/query9 | fad | ✓ | 2/2 | 0 | 1 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| crmarenapro/query9 | natural | ✓ | 3/3 | 0 | 2 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| googlelocal/query1 | fad | ✓ | 3/3 | 1 | 2 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| googlelocal/query1 | natural | ✓ | 4/4 | 1 | 3 | 2/1/0 | 0/0/0/0 | 1 | 2 |
| googlelocal/query2 | fad | ✗ | 4/3 | 1 | 1 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| googlelocal/query2 | natural | ✗ | 2/2 | 1 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| googlelocal/query3 | fad | ✓ | 4/4 | 1 | 3 | 2/0/0 | 0/0/0/0 | 0 | 2 |
| googlelocal/query3 | natural | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| googlelocal/query4 | fad | ✗ | 3/3 | 1 | 2 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| googlelocal/query4 | natural | ✓ | 3/3 | 1 | 2 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| music_brainz_20k/query1 | fad | ✗ | 2/2 | 0 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| music_brainz_20k/query1 | natural | ✗ | 2/2 | 1 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| music_brainz_20k/query2 | fad | ✓ | 2/2 | 1 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| music_brainz_20k/query2 | natural | ✓ | 2/2 | 1 | 1 | 0/0/0 | 0/0/0/0 | 1 | 0 |
| music_brainz_20k/query3 | fad | ✗ | 4/4 | 2 | 3 | 0/0/0 | 1/0/0/0 | 1 | 2 |
| music_brainz_20k/query3 | natural | ✗ | 4/4 | 2 | 3 | 0/0/0 | 1/0/0/0 | 1 | 2 |
| stockindex/query1 | fad | ✓ | 5/5 | 2 | 4 | 3/0/0 | 0/0/0/1 | 1 | 2 |
| stockindex/query1 | natural | ✓ | 5/5 | 2 | 4 | 3/0/0 | 1/0/0/0 | 2 | 2 |
| stockindex/query2 | fad | ✗ | 4/4 | 2 | 3 | 2/0/0 | 1/0/0/0 | 1 | 0 |
| stockindex/query2 | natural | ✗ | 4/4 | 0 | 3 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| stockindex/query3 | fad | ✓ | 4/4 | 2 | 3 | 2/0/0 | 0/0/0/1 | 0 | 2 |
| stockindex/query3 | natural | ✓ | 3/3 | 1 | 2 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| stockmarket/query1 | fad | ✓ | 2/2 | 0 | 1 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| stockmarket/query1 | natural | ✓ | 2/2 | 0 | 1 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| stockmarket/query2 | fad | ✓ | 5/5 | 1 | 4 | 1/2/0 | 0/0/0/0 | 1 | 0 |
| stockmarket/query2 | natural | ✓ | 4/3 | 0 | 1 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| stockmarket/query3 | fad | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 2 | 0 |
| stockmarket/query3 | natural | ✗ | 3/3 | 1 | 2 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| stockmarket/query4 | fad | ✗ | 4/4 | 0 | 3 | 2/0/0 | 0/0/0/0 | 1 | 0 |
| stockmarket/query4 | natural | ✓ | 3/3 | 0 | 2 | 1/0/0 | 0/0/0/0 | 1 | 0 |
| stockmarket/query5 | fad | ✓ | 4/4 | 1 | 3 | 1/0/0 | 0/0/0/0 | 2 | 0 |
| stockmarket/query5 | natural | ✓ | 6/5 | 1 | 3 | 2/0/0 | 0/0/0/0 | 1 | 0 |
| yelp/query1 | fad | ✓ | 4/4 | 2 | 3 | 3/1/0 | 1/0/0/0 | 2 | 2 |
| yelp/query1 | natural | ✓ | 4/4 | 2 | 3 | 3/1/0 | 1/0/0/0 | 1 | 2 |
| yelp/query2 | fad | ✓ | 1/1 | 0 | 0 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query2 | natural | ✗ | 3/3 | 1 | 2 | 2/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query3 | fad | ✓ | 4/4 | 0 | 2 | 2/1/0 | 0/0/0/0 | 0 | 2 |
| yelp/query3 | natural | ✓ | 3/3 | 0 | 2 | 2/1/0 | 0/0/0/0 | 0 | 2 |
| yelp/query4 | fad | ✓ | 1/1 | 1 | 0 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query4 | natural | ✓ | 1/1 | 1 | 0 | 0/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query5 | fad | ✓ | 3/3 | 1 | 2 | 2/0/0 | 0/0/0/0 | 1 | 0 |
| yelp/query5 | natural | ✓ | 4/4 | 0 | 3 | 3/0/0 | 0/0/0/0 | 1 | 0 |
| yelp/query6 | fad | ✓ | 3/3 | 1 | 1 | 1/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query6 | natural | ✓ | 3/3 | 1 | 2 | 2/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query7 | fad | ✓ | 4/4 | 0 | 3 | 2/0/0 | 0/0/0/0 | 0 | 0 |
| yelp/query7 | natural | ✓ | 5/5 | 0 | 2 | 0/0/0 | 0/0/0/0 | 0 | 2 |

分析异常记录 1 条，详见 [analysis-issues.json](analysis-issues.json)。不完整结构绑定不影响原始 SQL 执行成功的计数。

[逐任务 CSV](task-characterization.csv) · [相邻对](adjacent-pairs.json) · [分组演化](group-evolution.json) · [结果值依赖证据](result-dependencies.json) · [物化候选](materialization-candidates.json) · [可读实例与原始 SQL](EVIDENCE.md)
