# 服务错误停止与恢复入口

批次：`dsv4flash-db-first-full-01`。停止时间：2026-09-08 20:25:25（Asia/Shanghai）。

本轮注册 100 题，已提交 89 题，其中 87 题未触及轨迹上限、033 和 081 为 SQL 调用上限截断提交；提交不代表官方评分通过。087、091、092、093 因服务错误中断且未提交答案。094–100 共 7 题从未派发。旧四题保留在原目录。

092 的模型请求 R22 返回 HTTP 401：服务端连接器数据库尚未达到一致恢复状态，不能接受连接。响应被标为 `auth_error`，但正文并非明确的余额不足；不得据此称额度耗尽。全局停止标记传播到另外三题，停止后的新上游请求数为 0。

- [停止标记](state/parallel-stop.json)、[队列](state/queue.json)、[停止后请求核对](state/service-stop-audit.json)
- [当前可读报告](reports/dsv4flash-db-first-full-01/REPORT.md)
- [原始 R22 响应](runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/provider/R22.response.raw)
- [并行调度器](tools/parallel_run.py)、[离线交付脚本](tools/finalize.py)

## 四个中断检查点

| 任务 | SQL 成功/尝试（含设置、元数据） | Python 调用 | OpenCode session |
|---|---:|---:|---|
| 087 | 22/22 | 11 | `ses_f7f0df37cffesfWzJZKBJvmQ6C` |
| 091 | 32/34 | 3 | `ses_f7f086e6fffezVINxRbVGT5lop` |
| 092 | 38/40 | 0 | `ses_f7f071a97ffeJ8KtAg7sCc9Lci` |
| 093 | 2/2 | 0 | `ses_f7f054163ffeB2MOW1gt5oIPzy` |

每题原始日志、源码、结果和 `run_summary.json` 位于 `runs/dsv4flash-db-first-full-01/<task>/attempt-01/`。隔离的 OpenCode 会话数据库在 `runtime/<task>/`，这是本机恢复缓存，不属于可移植证据索引。请保留，勿清理。

## 用户要求恢复后

先确认服务恢复，再按下面顺序处理；当前不发送付费探测，也不自动重试。不要修改模型、提示或数据版本。

1. 读取队列、停止标记、本文及交接计划，确认无旧调度器和 OpenCode 子进程仍在运行。
2. 对 087、091、092、093，先检查上述本机会话及日志是否支持**同一次主轨迹续接**。当前运行器只支持创建新 attempt-01，不能直接对这些题调用它。续接需要重新绑定 MCP/代理地址、沿用 SQL ID 和工具日志，并先做无模型的恢复验证。未验证前保留中断状态；不能将其改为 pending，不能删除目录或从头重跑。
3. 对从未派发的 094–100，可以恢复并行队列。只有在用户明确要求服务恢复后继续时，归档当前 `queue.json` 和 `parallel-stop.json`，记录恢复事件，再清除队列的 `stop_reason` 和独立停止标记。保持四个中断题及全部已提交题的状态原样。
4. 从仓库根目录运行：

   ```bash
   benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/parallel_run.py --concurrency 4
   ```

   该入口仅派发 pending，存在停止标记时会拒绝启动；不会覆盖已有 attempt。不要同时启动串行运行器。

5. 所有恢复工作结束或再次服务停止后运行：

   ```bash
   benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/finalize.py
   ```

恢复会使当前报告与证据索引过期；保留本次交付快照，并重新生成最终报告、审计及 SHA256 索引。若无法安全续接四个中断会话，应明确报告此限制，不能把重新解题伪装为一次主运行。
