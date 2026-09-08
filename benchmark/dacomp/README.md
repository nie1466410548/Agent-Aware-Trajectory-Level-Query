# DAComp-DA 小规模自然轨迹试验

状态：**四题各一次自然运行已完成，均正常提交报告，无预算截断。** 共 27 次 SQL 尝试、26 次成功、18 条含 GROUP BY；官方未评分。未运行 FAD 组或额外重跑。

先读 [五个 RQ 的总报告](reports/REPORT.md)，再按其中的逐题链接查看完整 SQL、Python 和具体复用证据。三个离线候选已经过结果重放核验，尚未做性能收益或 frontier 预测实验。

## 数据与任务

上游：[DAComp-DA](https://huggingface.co/datasets/DAComp/dacomp-da)，固定 revision `2cc22149cdfe16cec41851ccae791c2d2c873bb3`。原题逐字保存在各任务的 `task.json`；数据库大小、SHA-256、表结构和行数保存在 [manifest.json](manifest.json)。

| 顺序 | 任务 | 中文题意概述 | 表数 | 总行数 | 文件大小 |
|---|---|---|---:|---:|---:|
| 1 | dacomp-006 | 华南月度总利润不稳定，哪些方面造成这种不稳定？ | 1 | 18,250 | 7,507,968 B |
| 2 | dacomp-003 | 工业用水占比与经济发展的关系，在全国和各省市是否不同？ | 2 | 1,030 | 200,704 B |
| 3 | dacomp-004 | 找出各月销售额最高的商品，分析其跨月表现及复购率与销售额的关系。 | 1 | 42,816 | 9,310,208 B |
| 4 | dacomp-005 | 识别低利润率订单，比较其多维特征并提出有数据依据的改进方案。 | 1 | 18,250 | 7,507,968 B |

005 和 006 的表数、行数与文件大小相同，但文件哈希和行内容哈希不同，不能视为相同数据库。无论是否共享数据来源，分析单位始终是单个任务的一次运行，不跨任务累计复用。

重新准备数据：`python benchmark/dacomp/tools/prepare.py`。只下载和检查数据，不调用模型。数据库由仓库已有 `.gitignore` 排除。

## 第一轮试验方案

1. 接入现有 Kimi CLI（`kimi-code/k3`），先跑 006，再依次跑其余三个任务；每题一个独立会话、一次自然运行。本轮不设 FAD 组，不重复采样，不扩展全量。
2. 使用原始英文题目和实际 schema，不添加下钻、上卷、增加查询次数或特定分析路线的要求。参考报告、评分规则和历史轨迹不进入 Agent 上下文。
3. 复用原有日志设计，但须实现独立的 DAComp 适配器：原 `fullbench/tools/run_task.py` 绑定 DAB 任务、数据库配置和答案验证器，不能直接运行本 benchmark。
4. 保留 SQL 与 Python 两种计算方式。数据库访问统一经过日志工具；Python 可处理返回的完整结果，不能静默绕过工具直连数据库。该工具限制是本实验的 harness 设置，报告时披露，不声称等同于官方 baseline。
5. 保存完整 Agent 消息、每次 SQL 尝试、SQL 文件、参数、结果文件、执行耗时、错误、Python 源码与输出、最终 Markdown 报告和引用图表。
6. 运行预算在启动前写入运行元数据。触及时间、调用或额度上限的轨迹单独标为截断，不能将其长度当作自然收敛长度。

## 首轮要回答的问题

| 维度 | 判定依据 |
|---|---|
| 轨迹结构 | SQL 尝试、成功 SQL、元数据访问、Python 调用和总运行时长分开统计。 |
| 分组细化 | 同一任务内，在兼容来源和筛选范围上增加分组维度，或沿维度层级从粗到细。 |
| 上卷 | 明确从细粒度转到粗粒度；单条原始表聚合不自动计作跨查询上卷。 |
| 子群分析 | 总体到指定子群的过滤变化，单独统计，不与 GROUP BY 下钻混计。 |
| 结果依赖 | 标明前一步哪个结果参与了后续参数或方向选择；区分题目已指定的依赖与 Agent 自主选择。 |
| 可复用机会 | 检查同任务的来源、过滤、Join、聚合状态和粒度兼容性，逐候选给出受益查询。 |
| 计算载体 | SQL、Pandas groupby/resample、中间结果复用分别记录，避免将 Python 分析误报为 SQL 演化。 |

先做逐任务证据表，再汇总。四题是定向选出的行为试验，不能用于估计所有 Data Agent 任务的发生率；当前数据规模也不能替代实际物化性能实验。

## 评分与验证

DAComp-DA 产出开放式报告，不使用 DAB 的确定性答案通过率。官方评价包括完整性、准确性、结论性、可读性、专业性和可视化，并使用模型裁判，详见 [官方评分说明](https://github.com/ByteDance-Seed/DAComp/blob/main/dacomp-da/evaluation_suite/README.md)。

首轮轨迹分析与官方报告评分分开：未调用官方裁判时只报告“未评分”，不能以成功提交报告代替任务成功。保留报告、轨迹及图表以支持后续按官方格式评分。

## 补充证据

- [InsightBench flag-13](https://github.com/ServiceNow/insight-bench/blob/main/data/notebooks/flag-13.ipynb)：参考 Notebook 含日级聚合、类别细分及日到周汇总；属于参考分析，不是自然 Agent 轨迹。
- [InsightEval 附录 H](https://arxiv.org/html/2511.22884v1#A8)：包含 Agent 生成的经理负载、部门比较、地域分布等问题；这是分析输出证据，不是完整 SQL 执行证据。

这两者先用于解释和核对分析模式，不在首轮额外批量运行。

## 运行与离线复现

原始工具序列、结果文件、Python 源码/输出、最终报告及图表位于 `runs/natural/<task>/pilot-01/`。`kimi.jsonl` 为完整消息记录，`tool_calls.jsonl` 为结构化工具记录，`dacomp-XXX-traj.txt` 为消息的文本副本。原始记录保留运行时绝对路径；离线统计与候选验证脚本按当前仓库位置定位结果文件。

```bash
python3 -m venv benchmark/dacomp/.venv
benchmark/dacomp/.venv/bin/pip install -r benchmark/dacomp/requirements-lock.txt
python3 benchmark/dacomp/tools/prepare.py

# 以下只做离线分析，不调用模型。
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/inventory.py
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/characterize.py
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/verify_view.py benchmark/dacomp/reports/dacomp-006-filter-candidate.json
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/verify_view.py benchmark/dacomp/reports/dacomp-004-aggregate-candidate.json
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/verify_view.py benchmark/dacomp/reports/dacomp-005-aggregate-candidate.json
benchmark/dacomp/.venv/bin/python benchmark/dacomp/tools/audit.py
```

实际 Agent 入口为 `tools/run_task.py`，依赖本机已有 Kimi CLI 与账号。相同任务 / run-id 的目录存在时拒绝覆盖；如将来追加实验，必须显式给新 `--run-id`。`smoke/local` 是工具本地检查，不能混入自然轨迹统计。
