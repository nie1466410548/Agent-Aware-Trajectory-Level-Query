# Agent DB Tool 原型

实现 [设计文档](../Agent侧DB%20Tool设计.md) 中的 SQL + future access 联合调用接口。
独立于已有 DAComp/FAD 实验代码，使用 Python、SQLite 与 stdio MCP。

## 当前能力

- `db_query`：执行一条只读 SQLite SQL，同时接收完整的未来访问候选集合。
- `read_result`：分页读取完整查询结果归档；不能读取数据库文件、历史实验或评估材料。
- `submit_answer`：保存 Markdown 报告，关闭任务与提示生命周期。
- `hints` 和 `sql-only` 两种模式共用同一查询后端与返回格式。
- 提示语法和语义错误整体降级，不要求 Agent 重试 SQL；校验结果只写内部日志。
- 进程持有轨迹锁，持久化请求日志；Python/CLI 调用者可用 request_id 去重。
- MCP 传输 ID 不作为持久请求 ID；发生传输错误时不自动重试工具调用。

尚未实现数据库优化动作、预测命中分析、官方报告评分、Python/绘图工具、并发轨迹合并。
因此这是 SQL 与报告工具的接入试验，不能与已有保留 Python 或数据库优先协议的运行直接比较。

## 环境与本地验证

从仓库根目录运行，Python 3.10+，Linux（轨迹锁使用 `fcntl`）。

```bash
python -m pip install -r agent_db_tool/requirements.txt
python -m unittest discover -s tests -v
```

真实 DAComp 四题的确定性联调入口（不调用模型）：

```bash
python -m agent_db_tool.smoke --output /tmp/agent-db-smoke-01
```

输出目录必须不存在。该测试使用人工构造提示，不衡量 Agent 预测能力；检查真实表计数、多个同级候选、错误降级、空提示和报告提交。

## 准备任务与 CLI 调试

```bash
python -m agent_db_tool prepare-dacomp \
  --task dacomp-006 --run /tmp/agent-db-006-01 --mode hints
```

该操作从本地 DAComp 读取原始任务和数据库 schema，记录数据库校验与哈希，创建全新运行目录，不读取参考报告或历史轨迹。数据库不复制到 Agent 工作目录。

创建 `request.json`：

```json
{
  "sql": "SELECT COUNT(*) FROM sheet1",
  "future_access": {"status": "unknown", "candidates": []}
}
```

```bash
python -m agent_db_tool query --run /tmp/agent-db-006-01 \
  --request-file request.json --request-id debug-001
```

CLI 是本地调试入口。Agent 正式接入使用下面的 MCP 工具参数，不需要创建 JSON 文件。

## 接入 Agent

准备目录中的 `mcp-config.json` 给出可合并到 OpenCode 的本地 MCP 配置，使用绝对路径启动脚本。
`prompt.txt` 包含原题、真实 schema 和所选模式的说明；`db_query` 的工具描述也提供提示语义。

手动启动服务器：

```bash
python -m agent_db_tool serve --run /tmp/agent-db-006-01
```

服务器通过 stdin/stdout 接收 MCP JSON-RPC，不是交互式 SQL 控制台。支持版本 `2024-11-05` 与 `2025-03-26`，实现 initialize、initialized、ping、tools/list 和 tools/call；串行处理且不支持运行中异步取消，SQL 有独立执行超时。

已有 OpenCode 和模型账号时，可以在一个**新准备的目录**运行一次真实任务：

```bash
python -m agent_db_tool.run_opencode \
  --run /tmp/agent-db-006-live-01 \
  --config /path/to/existing/opencode.json \
  --model provider/model --cli /path/to/opencode --timeout 600
```

这一步会调用配置的模型服务。Runner 从指定配置读取选定 provider，将其他工具默认禁用，只允许 `agentdb_*`，不把 provider 凭据复制进运行记录。Client 私有运行状态存入单独的 `/tmp/agent-db-opencode-*` 目录。

每个目录只允许一次 live attempt；没有自动任务重跑或官方评分。SQL-only 对照需要另建任务目录，使用 `--mode sql-only`，并保持模型、任务预算、工具能力一致。
模型服务连接错误的内部重试沿用 OpenCode 默认行为；这与 Tool 不自动重复执行 SQL 是两回事。

## 结果与错误语义

`status=ok` 才代表 SQL 成功。`sql_executed=true` 表示已进入执行尝试，不表示执行成功。
语法、权限、超时或结果大小限制均返回 `db_error`；不完整结果显式标记 `result_complete=false`。
进程在请求落盘后中断且没有完成记录时，相同 request_id 返回 `execution_unknown`，不重新执行。

结果以列名数组和行数组保存，保留重复列名；BLOB 编码为 `$blob_base64` 对象。
默认返回至多 12 行且预览约 12000 字符；完整结果以 JSONL 存储，最大 16 MiB。
`read_result` 接受上一次返回的 `next_offset`；调用者不要自行计算非 ASCII 文本的偏移。

对象校验按真实 catalog 中的 `表名.列名` 完整字符串匹配，支持空格等实际列名。
未解析的名称标记为 `unverified`，不会猜测映射或改写 SQL。条件说明不会被执行。

## 目录与审计

| 文件 | 内容 |
|---|---|
| `schema.json` | 原始逻辑 Schema；候选上限由配置同步替换 |
| `validation.py` | 分层校验、条件语义、catalog 核验 |
| `handler.py` | 轨迹锁、请求编号、提示快照、执行与完成日志 |
| `sqlite_adapter.py` | SQL 执行、超时与完整结果归档 |
| `server.py` | MCP 工具发现和调用 |
| `dacomp.py` | 任务准备与 Client 配置生成 |
| `run_opencode.py` | 单次真实 Agent 联调 |

每个运行目录保存 `task_meta.json`、`prompt.txt`、`events.jsonl`、`future_access.json` 和 `results/`。
真实运行额外保存 `agent.jsonl`、`agent.stderr.log`、`summary.json` 及报告。
原始事件包含请求参数和实际后续 SQL，可供下一阶段做匹配分析。当前 summary 只统计接口行为，不给出预测准确率或任务成功率。

`python -m agent_db_tool.report --run RUN_DIRECTORY` 生成 `tool-report.json`，包含逐轮候选数量、提示状态、字段合法性和模型返回的 token 统计。token 字段按服务原始口径分别保留，不把它们相加后声称是提示的增量成本。

实现参考：[MCP stdio](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)、[MCP tools](https://modelcontextprotocol.io/specification/2025-03-26/server/tools)、[OpenCode MCP 接入](https://opencode.ai/docs/mcp-servers/)。
