# 指标与证据字典（database_first_v1）

统计单位是单任务的 attempt-01；固定 100 题分母，旧四题不混入。主轨迹是第一次正式会话，不按结果选择。所有官方评分均为未评分。

| 记录 | 字段与口径 |
| --- | --- |
| `sql_journal.jsonl` | request 在执行前 fsync；engine_trace 为 SQLite 实际执行文本；completion 为执行与取回完成。按 execution_id / sql_id 合并，不能三份相加。准备失败可能无 trace，仍算一次尝试。 |
| `sql_events.jsonl` | 每个语句尝试一个最终事件，S1…；任务/批次/调用/父调用/连接/执行 ID、起止时间、SQL 模板与参数、实际引擎文本、类别、状态、结果、计时。中断未完成语句从 journal 检出，不假报成功。 |
| 计数 | 全 SQL 包括 data、metadata、connection_setup、maintenance、unknown。Q1…仅数据 SQL（含失败），附 S↔Q。Python 调用 P1…；Python 内 db.query 只在执行器记一次 SQL。executescript 按完整语句拆分，executemany 按参数组逐次执行。上限拒绝进入 sql_rejections，不计引擎尝试。 |
| 结果 | `columns` 按位置保留重复列名；`results/Sn.rows.jsonl` 每行一个原始行数组，BLOB 使用 `$blob_base64`。SQLite 不提供 SELECT 声明类型时为 null；逐列 observed_types 是实际非静态类型集合。行数仅完整结果可用；受限保存 archived_rows 和不完整标记。流式写入最多 256 MiB。 |
| 时间 | execute_return_ms 是 execute 返回耗时；fetch_ms 是后续取回耗时；execute_fetch_ms 为两者之和，不含逐行编码写盘；encode_write_ms 单独记录；wall_ms 含完整执行归档。没有实测扫描行数，不使用 EXPLAIN 估算冒充。 |
| 基础表 | 作用域解析 CTE/子查询来源；table_references 保留实际表引用次数。访问不同基础表 0/1/2/3/≥4 桶，解析失败另列。未指定 database/schema 时不虚构限定名。 |
| Join | 每个 SELECT 块独立；join_inputs 为该块关系实例数，CTE 输入仍是一个关系，自连接两个输入但基础表可能一张。保存类型、条件、USING、来源别名和块间引用。嵌套复杂关系不支持时记录 unknown，不把各子查询表数相加为 Join。 |
| GROUP BY | 保存每块原始键及解析 SELECT 别名/位置后的表达式、列血缘；最大维度用于 0/1/2/3/≥4 桶，同时完整保存多层维度向量。窗口 PARTITION BY 不计 GROUP BY。 |
| 聚合 | 每个表达式有函数、DISTINCT、FILTER/CASE、指标列、条件列；COUNT(*) 明确 row_count，不虚构列。函数 SQL 数与表达式数分别汇总。窗口函数单列，不计普通聚合。列来源不唯一时记录 unknown；SQL 解析、表血缘、列血缘覆盖分别汇总。 |
| 筛选 | WHERE/HAVING/CASE 独立记录完整表达式及列；不从相同文本直接推导结果依赖或复用。 |
| 完成 | 退出码、错误事件和 answer 提交共同判定。submitted 不是答案验证通过。timeout / quota_interrupted / service_error 等保留；状态和等于 100。 |
| 分布 | 成功数据 SQL 为结构分母；轨迹长度分别报告正常提交与截断/失败，样本量明确。分位数采用排序后 (n−1)p 线性插值。 |

所有实际数据库访问只经 MCP 执行器。Python 在 user/mount/network/PID namespaces 中运行，原库不在其文件系统中，只能通过继承 socket 调用记录执行器；Python sqlite3.connect 另有审计拒绝。运行模型只开放五个 MCP 工具，关闭 shell、文件系统通用工具、委派、检索、skill。源码筛查仅用于计算位置合规线索，不当作运行时完整性证明。Python 沙箱并不保证任意 Python 自行创造的内存数据结构都属于 SQL；本轮记录目标是所供 benchmark 数据库的访问。

原始模型请求正文及 SSE 响应保存在 provider/；Authorization 从不记录。代理首次 HTTP/网络错误即 latch，之后所有本地重试都不转发上游，运行器终止并保存队列。后台路由模型名仅在响应提供时报告，不能由别名推定。无模型付费探针。

候选筛选：精确完整 SQL、相同自包含 CTE、相同单表完整筛选、可分解单表聚合状态。所有符合方法条件的候选列出；按后续次数、原查询耗时、聚合类型排序，每题最多 3 次正确性验证，每候选 120 秒、原结果最多 32 MiB。不是完备 MV 搜索，不自动为同表查询构建整表副本。

新增物化写入 SQLite TEMP，原数据库 mode=ro。验证保存 build/rewrite、原查询 ID、比较结果。无 ORDER BY 使用精确行多重集（保留重复）；有 ORDER BY 按顺序比较，数值容差 rel=1e-12 / abs=1e-9。unordered 浮点不一致保守标拒绝。NULL、DISTINCT、列名、LIMIT/顺序必须保留。AVG 使用 SUM(x)/COUNT(x)，不能用 COUNT(*) 或均值的均值。已验证覆盖取候选覆盖 SQL 并集/成功数据 SQL，含触发查询；后续复用次数不含首次。

少量性能候选最多 10 个、每题一个，优先覆盖原查询总耗时高者；若实施，每例先正确性、再 5 次交替基线/物化路径串行计时，物化路径每次包含构建，报告暖缓存中位数及范围。未实施的保持未测。离线验证 SQL 属 offline_validation，不计 Agent 轨迹。

Python 计算位置人工判断必须结合源码和输入规模；reason 仅为模型自述。逐题报告标记待核验操作，不能把这些轨迹宣称为已严格合规。依赖边只记录已知接口父调用与文件消费证据；字面值匹配不认定因果。

计时补充：轨迹中的 execute 返回计时包含 SQLite trace callback 的日志写入开销，是记录接口观察的数据库调用时间，并非隔离出来的纯引擎 CPU 时间。离线性能基线与候选均采用同一结果消费方式，不能把两种计时边界直接相减当作在线收益。

分类规范化补充：原执行器对前置注释的语句可能先标 `unknown`。离线统计会忽略前置空白、`--` 与 `/*...*/` 注释后重新判断类别，保留 `recorded_category` 和原始事件不变。`run_summary.json` 的初步数据 SQL 数若有修正，保留 `provisional_data_counts_before_comment_normalization`，正式 CSV/JSON/报告使用规范化后口径；运行日志 END 行是当时初步计数。

失败计时补充：若 `execute()` 抛错而未返回，原始事件的 `execute_fetch_ms=0` 不能解释为零耗时。正式 CSV 将该分项留空，可读表同时显示实际 `wall_ms`（整个失败调用时长）。例如单 SQL 300 秒超时保留为 cancelled，归档不完整，而不是成功的零成本查询。任务自身正常提交与单条 SQL 超时分别记录；整题墙钟/服务中断或查询上限拒绝属于轨迹截断，长度分布另列。

性能边界补充：正式性能测试尚未启动时已确定将临时表 DROP 清理时间计入候选总成本，并单列 teardown_ms；结果比较仍在计时之外。基线与候选均完整取回结果。静态表/列引用与作用域图不是实测物理扫描次数；SQL 中声明的查询结构不代表所有部分都一定被引擎物化。

适配器边界：每次 Python 工具调用使用独立进程，跨调用状态依赖已保存文件；完整结果以行数组归档，列信息在工具返回与 SQL 事件中。重复数据库请求可能受到这种进程和结果读取接口设计影响。观察结果属于本适配器和协议，不能归因为模型本身的固有行为，也不能与旧 Kimi/行对象结果接口做受控因果比较。

并发边界：用户追加授权后，从 021 起使用最多 4 题并发；先前 001–020、061 为串行。模型、提示及数据库工具保持一致，调度与跨任务停止策略独立版本化。原始 SQL 执行时间保留真实竞争条件，不将串行/并发时间直接当受控性能对比。最终构建/复用实验在运行结束后独立串行计时。运行中任务的 SQL/Python 数在汇总表暂不展示，结束后补全。
