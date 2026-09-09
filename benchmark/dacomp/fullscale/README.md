# DAComp-DA 全量执行

独立批次 `dsv4flash-db-first-full-01`，模型 `glm-custom/DeepSeek-V4-Flash-0731`，数据库内优先协议。旧四题及旧实现保留。

[可读报告](reports/dsv4flash-db-first-full-01/REPORT.md) · [指标口径](reports/dsv4flash-db-first-full-01/METRICS.md) · [任务清单](manifests/tasks.jsonl) · [执行队列](state/queue.json)

当前因 092 的服务端 HTTP 401 连接器数据库恢复错误停止：89 题提交（其中 2 题截断）、4 题中断、7 题未派发。错误不是明确的余额不足。接续此检查点请先读 [恢复说明](RECOVERY.md)，不要重新执行下面的首次准备/验收命令。

从仓库根目录运行：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/prepare.py
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/test_local.py
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/run.py --preflight
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/run.py --acceptance
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/audit.py --acceptance
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/run.py --continue-full
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/report.py
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/audit.py
```

前三条不调用模型。005、多表题、061 是正式主轨迹，验收后不重跑。运行器拒绝覆盖现有 attempt；每题完成即更新队列和报告。工具实现、协议、依赖快照与哈希保存在 attempt 内，原始提示和模型请求正文可检查上下文隔离。

额度/服务中断时 `state/queue.json.stop_reason` 和当前 attempt 的 `provider/stop.json` 保留原始原因；不自动清除、续接或重跑。补充服务端额度并由用户要求恢复后，先核查当前 session 能否用同一隔离配置续接（必须重建 relay 地址，原始日志保留）；不能直接重复 `run --acceptance` 新建同题会话。未开始任务可在记录恢复授权后清除 stop_reason，从 pending 队列继续。当前中断题若不能续接，保留其主轨迹中断状态，任何额外 attempt 都须明确记录原因，不能替换主轨迹或挑最好结果。报告生成和审计始终可离线执行。

本批次不设金额预算、预留额度或估价，不调用 FAD 组或官方模型裁判。30 分钟/题、120 次 SQL、300 秒/SQL、180 秒/Python、256 MiB/单结果是卡死与结果体积限制。

OpenCode 适配依据本机 1.18.29 的 `run --help`、`debug config/agent/skill` 和 [官方配置文档](https://opencode.ai/docs/config/)、[Agent 文档](https://opencode.ai/docs/agents/)。实际出站请求与工具清单另在本批次 provider 证据核验；`--pure` 本身不是隔离保证。命名空间挂载只向 Python 暴露本题工作目录、结果和依赖，不暴露原库、研究文档、历史轨迹或凭据。

队列全部结束或服务中断、且当前模型进程已退出后，离线交付入口：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/finalize.py
```

此入口不调用模型。早期候选若缺少分 phase 的离线 SQL 日志，仅重放原先已选的同一批最多 3 个候选来补齐证据，保留 `*.analysis.initial.json`；不增加代表候选数量、不重跑 Agent。之后按既定规则最多选择 10 个案例做五次暖缓存构建/复用计时，并重建依赖、查询对、哈希和链接审计。`answers/` 是规范化本地图片/附件链接并明确标记缺失附件的可读副本；原始回答不改写。`code_versions/` 保存分析源码版本，`evidence_index.json` 可逐文件复核。

### 用户授权的并发切换

2026-09-08 用户要求加快串行实验，切换为 4 个独立任务并发。001–020 与 061 共 21 题已在串行阶段提交；020 正常结束、报告落盘后停止旧调度器，不中断或重跑任何主运行。后续使用 `tools/parallel_run.py --concurrency 4`，仍为同一模型、同一数据库内优先提示与工具协议，每题一次主运行。

并发队列只有一个写入者，并使用 `state/dispatch.lock` 排斥第二个并发调度器。`current_tasks` 保存当前全部任务；`current_task` 仅兼容旧入口。每个任务独立 OpenCode/relay/工具服务、工作目录和数据库只读连接。`state/parallel-stop.json` 为跨任务首个错误闩锁；所有 relay 在接收后续请求时检查，已通过入口检查的请求可能仍在途。错误一旦出现，停止派发，活动 worker 终止其模型及 Python 子进程并补齐取消记录。不会自动清除闩锁或恢复额度中断任务。

启动命令：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/tools/parallel_run.py --concurrency 4
```

状态与恢复证据：`state/queue.json`、`state/parallel-stop.json`（若发生错误）、`state/parallel-run.log`、`state/dacomp-XXX.worker.log`，以及各题原 attempt。不要同时启动旧 `run.py --continue-full`。服务恢复并获用户继续授权后，先核对活动进程、各题 summary 和部分轨迹；当前工具只自动领取 `pending`，不会把中断题伪装为未开始，也不会重跑已提交题。

`tools/test_parallel.py` 使用本机假服务/假 worker，验证跨题额度闩锁只允许第一次上游请求、并行重叠、队列闭合与不重复领取；没有调用真实模型。运行中轨迹不参与报告解析，避免读到半条日志；每题结束后统一审计。并发期间的原始 SQL 耗时可能受资源竞争影响，最终代表性性能实验仍在所有模型任务退出后串行执行。
