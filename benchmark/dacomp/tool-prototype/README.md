# Agent DB Tool v0.1 验证记录

日期：2026-09-09。实现和运行方法见 [Tool README](../../../agent_db_tool/README.md)。

后续已完成同次运行的 [FAD 与后续 SQL 匹配分析](analysis/REPORT.md)。下文保留首次接口验证口径；匹配分析进一步区分了结构化列命中与自然语言意图支持，尚未进行 SQL-only 对照或官方评分。

本目录与原 DAComp 四题自然运行、百题数据库优先运行分开。这里验证的是 SQL 与 future_access 同次提交的接口；不沿用先提交 FAD 回执再生成 SQL 的旧协议。

## 本地与真实数据检查

- `python -m unittest discover -s tests -v`：13 项测试通过。
- 正式 `schema.json` 与设计文档中的 Schema 一致，文档调用示例通过校验。
- [四题联调记录](smoke/local-01/report.json)：006、003、004、005 均通过；使用实际 SQLite 数据，模型调用为 0。
- 覆盖多个同级候选、空提示区别、旧快照清除、SQL 错误、只读访问、超时、结果限制、请求去重、中断后的未知状态、轨迹锁和 MCP 工具发现/调用。

## 真实 Agent 联调

使用本机 OpenCode 1.18.29，模型 `glm-custom/DeepSeek-V4-Flash-0731`，原始 DAComp-006 任务及实际 schema，300 秒运行上限，最多 80 次 SQL 尝试。只提供新 Tool 的查询、结果读取和报告提交入口，没有 Python 或绘图工具。

| 尝试 | 结果 |
|---|---|
| [hints-006-01](runs/hints-006-01/summary.json) | 沙箱内模型服务连接失败；0 次数据库查询，无报告；保留失败记录 |
| [hints-006-02](runs/hints-006-02/summary.json) | 经授权在沙箱外重试；243.62 秒完成，退出码 0，未触及超时，报告已提交 |

第二次尝试的工具行为：

| 指标 | 结果 |
|---|---:|
| SQL 尝试 | 30 |
| SQL 成功 | 26 |
| SQL 错误 | 4 |
| 请求缺少完成记录 | 0 |
| 格式或提示语义校验失败 | 0 |
| provided 提示 | 29 |
| no_further_access 提示 | 1 |
| 同轮多个候选 | 0 |
| catalog 核验通过的提示快照（含空集合） | 28 |
| 含未核验对象的提示快照 | 2 |

4 次 SQL 错误分别为列名歧义以及 SQLite 不支持的 `STDDEV`、`STDDEV_SAMP`。Agent 获得实际错误后继续分析，工具没有自动重复执行 SQL。

2 次未核验对象均为 `sheet1."Consigned Product"`。当前 catalog 校验按实际名称 `sheet1.Consigned Product` 精确匹配，因此额外引号会标记为未核验，不猜测映射、不阻断 SQL。它属于名称表达的适配问题，不能与提示格式错误混计。

## 可以确认与尚不能确认的内容

已确认真实 Agent 能通过原生 MCP 参数生成联合 JSON，执行当前 SQL，读取实际结果，连续更新 future_access，最终提交报告。它不需要先生成 JSON 文件再运行 Bash。

本次所有 provided 提示都只有一个候选，且不少仅包含表、列和简短说明。接口支持多候选已由本地测试验证，但此次真实运行尚未展示 Agent 主动表达多条未来方向的能力。下一轮应考察提示说明与模型选择，不能为得到多候选结果而强迫凑数。

目前未做未来访问匹配评估、SQL-only 对照、性能收益实验或官方模型裁判。因此：

- 字段合法和名称核验通过不等于预测准确。
- 报告提交不等于答案正确或任务通过。
- 这一次运行的耗时/token 不代表提示增量成本。
- 单题结果不能推断所有 DAComp 任务上的表现。

## 可审阅产物

- [逐轮工具统计](runs/hints-006-02/tool-report.json)：包含候选数、状态和模型返回的 token 字段。
- [完整请求与完成日志](runs/hints-006-02/events.jsonl)：请求在 SQL 执行前记录，包含原始 JSON、catalog 检查和真实结果。
- [Agent 消息记录](runs/hints-006-02/agent.jsonl)。
- [最终报告](runs/hints-006-02/answer.md)：未做官方评分。
- [实际任务说明](runs/hints-006-02/prompt.txt)和[数据/协议元信息](runs/hints-006-02/task_meta.json)。

模型用量取自 38 个 step_finish 事件：input 65,039，output 11,138，reasoning 5,067，cache read 497,152，reported total 578,396。这些字段按 provider 原始口径分别保留，不能假定彼此独立相加，也不能全部归因于 future access。

首次联调的 launch 元数据中 `automatic_retries: 0` 指 Runner 不自动重跑任务；OpenCode 对模型连接错误仍进行了内部重试。后续 Runner 已将字段明确为 `automatic_task_retries` 和 `provider_retry_policy`。两次实际尝试均独立保存，没有覆盖或隐去失败记录。
