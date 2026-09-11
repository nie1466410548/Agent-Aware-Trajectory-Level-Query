# FAD数据库优化实验后端

普通SQL执行 vs SQL＋FAD优化。最新批次为千万行、有分析步骤指导的新Agent会话，按用户要求做两对后台异步对照，见文末v1.5。在线Agent采集入口使用普通SQL后端，正式性能比较使用该新会话实际生成的同一轨迹回放。原始18,250行、百万行及之前千万行结果作为历史批次保留，旧v1错误对照已撤出主要结论。

结果见[单一实验报告](../../benchmark/dacomp/fad-optimization/reports/REPORT.md)，方案见[验证计划](../../FAD驱动数据库优化验证计划.md)。原始18,250行上完成三种优化各20对实验，结果全部一致，但计入全部成本后都变慢。不能把SQL执行时间缩短当作任务提速。

## 文件职责

| 文件 | 职责 |
|---|---|
| backend.py | 两组共用的持久任务连接；Agent只读入口、受控DDL、完整结果归档 |
| patterns.py | 调用v0.2校验；只解一层JSON字符串、汇总明确列引用；结构化FAD转动作 |
| controller.py | 仅接收已到达FAD；两次出现门槛、优先级、对象数量/空间/时间预算、清理 |
| rewrite.py | 精确过滤/分组/指标覆盖后替换单表SELECT层；浮点保护 |
| replay.py | 新副本、规定预热、SQL先执行/FAD后到达、计时与资源记录 |
| check.py | 计时外核对完整结果，包括重复行、排序、NULL及浮点容差 |
| experiment.py | 冻结代码/参数；新进程、随机AB/BA、串行配对、保留失败 |

控制器的输入接口不接收轨迹文件路径或未来事件。离线报告及SQL后续命中分析不参与决策。每轮日志中available_before_query、source_steps、created_after可以核对时间顺序。

## 复现

在仓库根目录执行，Python 3.11；本次SQLite 3.42.0、SQLGlot 30.18.0、jsonschema 4.26.0。其他SQLite版本需重做结果验证。

```bash
benchmark/dacomp/.venv/bin/python -m pip install -r agent_db_tool/optimization/requirements.txt
benchmark/dacomp/.venv/bin/python -m unittest discover -s tests -q
```

先独立运行诊断/结果验证。输出目录必须不存在，防止覆盖已有实验。

```bash
for mode in baseline index materialization combined; do
  benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.replay \
    --database benchmark/dacomp/upstream/dacomp-006/dacomp-006.sqlite \
    --events benchmark/dacomp/tool-prototype/v0.2/runs/dacomp-006-02/events.jsonl \
    --out benchmark/dacomp/fad-optimization/runs/validation-new/$mode \
    --mode "$mode" --diagnostic
done
```

正式配对实验会先核对诊断结果，失败则不开始计时。每次工人的完整结果在计时内归档，配对完成后在计时外再比较。

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.experiment \
  --database benchmark/dacomp/upstream/dacomp-006/dacomp-006.sqlite \
  --events benchmark/dacomp/tool-prototype/v0.2/runs/dacomp-006-02/events.jsonl \
  --validation-root benchmark/dacomp/fad-optimization/runs/validation-new \
  --root benchmark/dacomp/fad-optimization/runs/original-18250-new \
  --pairs 20 --seed 20260910
```

重算本次报告：

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/space_diagnostic.py
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/report.py \
  --run benchmark/dacomp/fad-optimization/runs/original-18250-v2-sql-only \
  --diagnostics benchmark/dacomp/fad-optimization/runs/validation-02-sql-only \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

## 计时、隔离和证据

数据库副本复制、所有基础表的完整预热读取在计时外；关闭预热连接后开始计时并建立新任务连接。计时涵盖连接/目录、原SQL编译检查、FAD校验、匹配、决策、预算估计扫描、对象构建、SQL及全部结果归档、动作日志、空间检查、对象删除和关闭。每次副本的丢弃属于共同实验准备/处置，建对象从未提前到准备阶段。

对照组只接收SQL，直接执行，不初始化控制器，不解码/校验FAD，不做优化空间检查或清理。EXPLAIN QUERY PLAN预检只在优化组计入；诊断运行额外记录改写后计划，其耗时不进入正式结果。进程启动和导入在计时外，两组完全相同；模型生成FAD的耗时不在本次实验中。

每个正式run保存config.json、manifest.json（哈希、环境、随机顺序）、source_snapshot；各pair包含两组events.jsonl、results/Q*.jsonl、summary.json以及correctness.json。运行结束的COMPLETE.json只在全部对照通过且源数据/代码未变化后生成。数据库副本不保留，原始数据库不修改。

总耗时是实际perf_counter墙钟时间，不是把重叠的分段相加。build_including_estimate_seconds属于decision_including_build_seconds的子集。RSS包含进程预热和库导入；SQLite对象页数不等于排序器临时文件的完整峰值。I/O同时记录OS实际读写和系统调用字节数，主实验为预热条件，不声称冷缓存。

## 首版能力边界

支持单表、确定过滤、列及年/月/日分组、SUM/COUNT/MIN/MAX/AVG。精确过滤/分组复用，不做范围包含、跨粒度roll-up或缺失指标补全；AVG保留原生值及SUM/非NULL COUNT。COUNT DISTINCT、CTE、连接、窗口、HAVING及无法确认的表达式回退原SQL。已有在线v0.2校验器没有被修改，字符串解码只在实验接收模块实施。

索引不强制使用；根据已有FAD过滤键和分组键提案，最多3键、2个对象。首版多表候选不构建连接索引，后续按后端接口扩展。LIKE使用与本次默认语义一致的NOCASE键。汇总表最多2个，每轮最多尝试一个新对象；满额保留，不追看后续SQL来替换。

初次校准发现索引引起的浮点ROUND边界变化，未放宽结果要求。对原先没有索引的表，含ROUND/聚合的当前SQL保守使用NOT INDEXED恢复全表路径；汇总表构建保持原始扫描路径。这个保护针对本次SQLite/目录和已验证轨迹，不宣称对任意SQL、排序并列、原有索引及自定义排序规则提供通用数值等价保证。新数据或新轨迹必须先通过独立结果核查，任何不一致都不应进入有效性能结论。

未来接入实时Agent时复用任务后端和observe_fad/rewrite边界；此次没有修改模型提示或Agent分析路线。扩容生成器及异步回放现已实现，命令见后文；历史SQL驱动对照仍属后续阶段。

空间预算按主库文件增长加临时库页数计量；原库自带687个空闲页，索引复用它们不增加文件长度。报告另用独立空间诊断列出新占用页（两个索引共1180 KiB），两者不能混称。当前原始规模的实际新占用页也低于预算；后续大规模若要限制对象总占用而非新增文件分配，应扩展该预算口径。

回放器在准备阶段提取每组输入：对照仅SQL，优化组SQL＋原始FAD。该操作属于benchmark组装固定输入；数据库计时路径不从含FAD的原始轨迹读取。正确性比较要求SQL完全相同，并检查对照组FAD输入为null、全部优化分段为零。新增回归测试用会抛错的mock替换FAD处理器、控制器、预检和空间检查，确保对照不会调用。


## 百万行、每种方式5对（用户指定）

优化器、执行后端、FAD输入和SQL轨迹不变；只将实验次数下限改为可配置正数。本次以五对作初步观察，旧小库结果仍保留。

```bash
benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/scale_data.py \
  --source benchmark/dacomp/upstream/dacomp-006/dacomp-006.sqlite \
  --out benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --rows 1000000 --seed 20260910
```

输出路径存在时拒绝覆盖。生成器逐行回读核对业务字段与来源，新运单号不冲突；同名manifest记录数据哈希、复制次数及补齐部分的原始行序号。

按上文诊断命令，将database换成该百万行数据库、out换成新目录，然后：

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.experiment \
  --database benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --events benchmark/dacomp/tool-prototype/v0.2/runs/dacomp-006-02/events.jsonl \
  --validation-root benchmark/dacomp/fad-optimization/runs/validation-million-01 \
  --root benchmark/dacomp/fad-optimization/runs/synthetic-1000000-v1 \
  --pairs 5
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/audit_run.py \
  --run benchmark/dacomp/fad-optimization/runs/synthetic-1000000-v1 \
  --diagnostics benchmark/dacomp/fad-optimization/runs/validation-million-01
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/scale_report.py \
  --run benchmark/dacomp/fad-optimization/runs/synthetic-1000000-v1 \
  --diagnostics benchmark/dacomp/fad-optimization/runs/validation-million-01 \
  --data-manifest benchmark/dacomp/fad-optimization/data/synthetic-1000000.manifest.json \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

新规模结果放在同一报告中的独立小节，不覆盖原始规模结果。重新生成原始规模报告后，需要再运行scale_report.py恢复两个规模的合并报告。


## 真实间隔异步实验

当前结果：数据库查询处理7.862秒→6.818秒，配对节省13.27%，五对全部更快；本轮固定13轮百万行轨迹。详细计划：[async/PLAN.md](../../benchmark/dacomp/fad-optimization/async/PLAN.md)。使用完整的百万行来源会话source-million-02，13条SQL，等待合计788.051秒；首个超时采集不作为来源。普通组不处理FAD，两组相同相对等待，优化组后台工作与等待重叠，不串行累加成本。

| 文件 | 作用 |
|---|---|
| timing.py | 从客户端工具时间提取初始、相邻、最终报告间隔，并核对服务端request_id |
| async_backend.py | 两组WAL连接、查询快照、后台DDL提交记录与跨连接对象可见性 |
| async_engine.py | 独立后台进程；只接收已经到达的FAD；构建、就绪通知、停止和清理 |
| async_replay.py | SQL返回后锚定固定间隔；支持跳过空闲；分别记录实际与还原时间 |
| async_check.py | 与源会话完整结果比较，审计FAD/对象时间顺序及原始间隔 |
| async_experiment.py | 冻结输入和代码，五对独立串行AB/BA，两个相同逻辑CPU |

下面在仓库根目录执行。输出目录必须不存在。生成原始数据、复制与统一预热在计时外；新建后台进程、请求解码、查询、匹配、构建等实际计时；跳过的空闲单独记录并加回还原任务时间，停止/清理另给总时间。不能将后台各段再次相加冒充延时。

```bash
benchmark/dacomp/.venv/bin/python -c "from agent_db_tool.optimization.timing import extract; extract('benchmark/dacomp/fad-optimization/async/source-million-02', 'benchmark/dacomp/fad-optimization/async/timing-million.json')"

benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_replay \
  --database benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --out benchmark/dacomp/fad-optimization/async/validation-new \
  --mode combined --diagnostic --correctness-only

benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_experiment \
  --database benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --root benchmark/dacomp/fad-optimization/async/runs/reused-gaps-million-new \
  --validation benchmark/dacomp/fad-optimization/async/validation-new --pairs 5 --skip-idle

PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/audit.py \
  --run benchmark/dacomp/fad-optimization/async/runs/reused-gaps-million-new
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/report.py \
  --run benchmark/dacomp/fad-optimization/async/runs/reused-gaps-million-new \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

`correctness-only`只用于计时外验证：去掉等待，并等待后台处理当前FAD以覆盖就绪对象路径，不能将其时间当作实验成绩。正式命令使用`--skip-idle`，后台处理完成后跳过剩余空闲，原始间隔数值复用于还原任务时间；后台未完成且间隔耗尽时，查询仍按时发出。

所有前台查询在各自结果归档、日志完成后记录response_return_ns，下一轮间隔从此开始。原始events.jsonl在该时间戳之前写入，完整时间戳请看timeline.json。后台每项动作记录触发轮次、估计及DDL开始、提交返回与就绪；实际执行计划保留索引使用证据。

异步汇总对象为任务副本内普通表（CREATE TABLE），已提交才可跨连接读取，结束DROP；不是SQLite连接私有TEMP表。查询在构建未完成时继续使用原表。两组WAL与缓存设置一致，共同预热条件下测量，不声称冷缓存或无资源竞争。

实测/tmp为tmpfs内存文件系统。包括旧串行实验在内，这里的数据库副本和WAL虽是文件形式，也不能表述为对物理磁盘的性能测量。进程RSS不包括全部tmpfs和文件缓存，后台CPU/构建时间被等待覆盖仍有资源成本。

报告生成顺序为原始小库report.py、百万行scale_report.py、异步async/report.py；最后一步保留前两节。旧接收器在新来源会话中接受2/13轮FAD，这属于当前实现结果，不能将其当作已充分使用所有原始预测。每轮原始内容和拒收原因一并报告。


旧接收器批次已完成：`async/runs/real-gaps-million-01`，5对净节省中位数0.468秒（0.059%），含清理后0.391秒；所有130次源结果对照和65个两组直接对照通过，AUDIT.json记录完整审计。该批结果保留在旧统计中，最新报告使用下方接收修复后的结果。


## 2026-09-11：接收修复与复测

`reception.py`作为实验接收层，先规范化明确内容，再独立校验各候选：补齐已明确操作引用的空列列表、展开单分支AND/OR、去掉unknown旁的literal并保留不确定性。一个非法候选不再导致整轮丢弃。不会猜测未来SQL或过滤值，不会删掉AND中无效分支后扩大过滤范围。原始输入保持不变，接收审计保存normalizations、accepted_candidate_indices及rejected_candidates。

严格v0.2在线采集入口保持原样；此次修复用于实验优化器的接收路径。60项测试通过，同一百万行13条SQL独立结果验证通过，13/13轮与41个候选被接受，验证构建2索引、2汇总表。最初的完整等待复测`async/runs/real-gaps-million-02-reception`已停止，不再用于五对统计。当前复测使用下文的间隔复用方式和新目录，SQL/FAD和原始间隔文件不变。


## 固定间隔复用（2026-09-11，按用户更正）

固定的788.051秒间隔已采集，后续不再逐次空等。使用`--skip-idle`：每轮只实际运行数据库查询和后台工作；后台初始化或本轮FAD处理完成后，立即跳过间隔内剩余空闲。若后台工作超过原间隔，下一条查询按原间隔到达，真实保留读写并发。后台优化器仍看不到未来SQL或间隔。

任务时间＝实际经过时间＋跳过的空闲时间。间隔、跳过量、实测查询/构建/清理都分别记录；报告明确这是按固定间隔还原的时间，不能标成完整任务墙钟实测。构建已经消耗的间隔不重复相加。该方法不重现长时间空闲造成的缓存老化或系统活动，采用相同预热条件控制两组初态。

新批次为`reused-gaps-million-01-reception`，5对，验证目录`validation-03-reused-gaps`。61项测试通过，验证13条SQL结果全部一致。此前`real-gaps-million-02-reception`已停止，仅第1对完整、第2对普通组未完成，不当成5对；第1对普通796.002秒、优化797.103秒，保留为完整等待的参照。旧接收器的`real-gaps-million-01`完整5对仍保留。最新结果继续写同一报告。

复测完成：`reused-gaps-million-01-reception`五对全部通过最终审计，130次源结果及65次直接对照一致。每次13/13轮、41个候选接受；配对任务时间增加中位数1.158秒（0.146%）。普通实际回放约7.874秒、优化16.173秒，按固定间隔还原后分别为795.924秒和797.075秒（各列中位数）。详细结果见同一报告。


## 当前复现：WITH聚合复用与索引准入

新增作用域识别后，可以替换WITH内部严格匹配已就绪汇总表的单表聚合，同名CTE不会误当基础表。过滤、分组和指标匹配规则保持严格，递归CTE不处理。索引统一按可能需要回表采取保守准入：首列明确过滤的匹配率须在0～10%，实际计数在后台执行并计时。这并非精确收益模型，也可能拒绝有效的覆盖或分组索引。

最新实测使用同一13轮来源，未改成旧30轮轨迹。主统计database_request_seconds为SQL到达至返回的逐轮耗时之和，包含全部前台处理；后台成本、间隔覆盖和末尾清理另列。

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_replay \
  --database benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --out benchmark/dacomp/fad-optimization/async/validation-cte-new \
  --mode combined --diagnostic --skip-idle
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_experiment \
  --database benchmark/dacomp/fad-optimization/data/synthetic-1000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --root benchmark/dacomp/fad-optimization/async/runs/cte-new \
  --validation benchmark/dacomp/fad-optimization/async/validation-cte-new --pairs 5 --skip-idle
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/audit.py \
  --run benchmark/dacomp/fad-optimization/async/runs/cte-new
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/report.py \
  --run benchmark/dacomp/fad-optimization/async/runs/cte-new \
  --timing benchmark/dacomp/fad-optimization/async/timing-million.json \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

实际已完成目录：validation-04-cte-cost与reused-gaps-million-02-cte-cost。旧失败原始数据不覆盖，statistics-async-million-before-cte-cost.json保留上一批统计。
完成：同一百万行13轮轨迹的五对复测，数据库查询处理耗时中位数7.862秒→6.818秒；配对节省中位数1.044秒（13.27%），5/5对更快。后台构建5.752秒全部被间隔覆盖；加上末尾清理后仍节省0.874秒。64项测试、130次源结果比对及65次两组直接比较通过。


## 原始18,250行的30轮轨迹

原始库与原始dacomp-006-02会话直接对应，不扩容、不重新生成SQL/FAD。间隔文件timing-original-30.json由原客户端记录提取。新批次与13轮百万行批次的优化代码/配置哈希全部一致。

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_replay \
  --database benchmark/dacomp/upstream/dacomp-006/dacomp-006.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-original-30.json \
  --out benchmark/dacomp/fad-optimization/async/validation-original-new \
  --mode combined --diagnostic --skip-idle
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_experiment \
  --database benchmark/dacomp/upstream/dacomp-006/dacomp-006.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-original-30.json \
  --root benchmark/dacomp/fad-optimization/async/runs/original-new \
  --validation benchmark/dacomp/fad-optimization/async/validation-original-new --pairs 5 --skip-idle
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/audit.py \
  --run benchmark/dacomp/fad-optimization/async/runs/original-new
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/report_original_30.py \
  --run benchmark/dacomp/fad-optimization/async/runs/original-new \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

报告生成顺序：先保留/生成百万行小节，再运行report_original_30.py，它在同一个文件加入原始30轮小节。实际完成目录reused-gaps-original-30-v1；统计statistics-async-original-30.json独立保存，不覆盖百万行统计。

原始18,250行、原报告30轮轨迹的五对同策略复测完成：普通查询处理252.5ms，使用FAD459.6ms；配对中位数增加208.2ms（82.6%）。29份有预测FAD、58个候选全部接受，汇总表用于Q13/Q15/Q21；300次来源核对和150次两组直接比较全部通过，Q10原有错误保留。


## 1,000万行与独立新Agent（v1.4）

本批从原18,250行生成`synthetic-10000000.sqlite`，全量回读验证10,000,000行。新会话`source-ten-million-01`独立完成任务六，13条SQL全部成功、13份FAD、47个候选，并提交报告。没有向Agent提供旧轨迹。原始日志及报告在该来源目录中保留。

v1.4将汇总匹配规则在后台预编译，合并同一过滤/分组已收到的聚合指标；最多12个汇总方向，512MiB总预算，单次扫描构建并受SQLite页数限制。只针对明细预测考虑选择性索引；实际计划需回表时保护原表扫描。每轮仍最多一次构建尝试，不承诺所有已预测方向都能及时就绪。68项优化相关测试通过。

本次有客户端调用重叠，但MCP服务串行。`timing.extract`改用原数据库请求/完成的服务时间提取间隔，保留客户端原时间，排队不计作后台空闲窗口；新增3项测试。优化策略已预冻结，补充记录明确只有时间提取改变。

以下命令复用已采集的这条新轨迹；输出目录必须不存在。所有间隔只采集一次，回放跳过剩余空闲，不再等待整段Agent思考时间。

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_replay \
  --database benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-ten-million.json \
  --out benchmark/dacomp/fad-optimization/async/validation-ten-million-new \
  --mode combined --diagnostic --skip-idle
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_experiment \
  --database benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-ten-million.json \
  --root benchmark/dacomp/fad-optimization/async/runs/ten-million-new \
  --validation benchmark/dacomp/fad-optimization/async/validation-ten-million-new --pairs 5 --skip-idle
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/audit.py \
  --run benchmark/dacomp/fad-optimization/async/runs/ten-million-new
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/report_ten_million.py \
  --run benchmark/dacomp/fad-optimization/async/runs/ten-million-new \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

主指标为串行数据库工具开始处理SQL至返回结果的累计时间；不重复计重叠客户端调用的排队等待。前台匹配、改写、日志、结果归档、FAD提交均包含在内。后台准备和末尾清理单列；后台超过已记录间隔时与查询实际并发，其争用保留在实测查询耗时中。

已冻结批次目录为`reused-gaps-ten-million-v14`，结果继续进入同一`reports/REPORT.md`，统计写`statistics-async-ten-million.json`，保留旧规模的独立记录。副本位于tmpfs，所有组采用相同完整预热；这不是物理磁盘冷缓存实验。

千万行批次完成：reused-gaps-ten-million-v14，五对均加速，普通前台处理100.799秒、使用FAD 94.389秒（各五次中位数）；各对节省5.893～6.868秒，节省比例中位数6.50%。13/13轮FAD、47个候选接受，五个汇总表建成，实际Q8复用一个，Q8的SQL执行中位数7.349秒→0.0067秒。后台构建中位数27.811秒，其中与Agent间隔重叠19.359秒、与查询重叠8.476秒；这些分项独立取中位数，不直接相加。末尾清理0.041秒另列，计入清理后仍五对加速。130次来源结果核对、65次两组直接比较全部通过，10个独立进程，数据/代码/SQL/FAD和使用时序审计通过。结果写入同一reports/REPORT.md，统计statistics-async-ten-million.json。数据保持原分类基数，副本位于tmpfs，此结论只针对本条新轨迹。

## 千万行、SQL分析指导、两对（v1.5）

来源为`source-ten-million-guided-01`：独立新会话，在原有千万行数据上根据返回结果继续分析，32条业务查询及1条结束用的`SELECT 1`，全部成功。没有提供旧轨迹或规定查询次数；波动、贡献及协方差等主要计算有对应SQL。报告中仍有一处剔除省份后的CV估计没有SQL依据，原文保留，实验报告已标注该局限。

v1.5在原准入、空间和时间预算内连续构建合格对象，每个对象提交并准备好匹配规则后独立发布。本轮构建耗时消耗剩余总预算，停止时中断并回滚未完成构建，不再开始下一对象。77项测试通过后，在新Agent启动前冻结代码、预算及提示；冻结记录在`async/preflight-v15-ten-million-guided`。

SQL/FAD和258.701秒来源间隔只采集一次。正式两对采用新副本、新进程、相同预热/WAL/CPU，按FAD→普通、普通→FAD的顺序串行执行；`--skip-idle`跳过剩余空闲，保留真正并发。主指标为逐轮数据库服务开始至结果返回的累计时间，包含全部前台匹配、查询、结果归档及FAD提交；后台准备不串行加进主指标，末尾清理另列。

下面复用本条已采集轨迹重新做两对，验证和运行输出目录必须不存在：

```bash
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_replay \
  --database benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-ten-million-guided.json \
  --out benchmark/dacomp/fad-optimization/async/validation-guided-new \
  --mode combined --diagnostic --skip-idle
benchmark/dacomp/.venv/bin/python -m agent_db_tool.optimization.async_experiment \
  --database benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite \
  --timing benchmark/dacomp/fad-optimization/async/timing-ten-million-guided.json \
  --root benchmark/dacomp/fad-optimization/async/runs/guided-new \
  --validation benchmark/dacomp/fad-optimization/async/validation-guided-new --pairs 2 --skip-idle
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/audit.py \
  --run benchmark/dacomp/fad-optimization/async/runs/guided-new
PYTHONPATH=. benchmark/dacomp/.venv/bin/python benchmark/dacomp/fad-optimization/async/report_guided_ten_million.py \
  --run benchmark/dacomp/fad-optimization/async/runs/guided-new \
  --output benchmark/dacomp/fad-optimization/reports/REPORT.md
```

本批输出`async/runs/reused-gaps-ten-million-guided-v15`，统计为`reports/statistics-async-ten-million-guided.json`；最新小节写入同一`reports/REPORT.md`。提示与调度同时改变，不把跨批差异单独归因于查询轮数。

完成结果：本次验证已完成：有分析步骤指导的千万行独立新Agent生成32条业务查询及1条结束标记SQL，全部成功。正式两对普通/FAD回放均加速，数据库前台累计时间两次平均182.267秒→127.623秒，节省54.644秒（29.98%）。7张汇总表中3张用于后续9条业务查询；31/33轮FAD格式通过，34个候选接受，Q26/Q27过滤关系格式不合要求，原输入保留。77项测试、独立完整验证、132次来源结果核对及66次两组直接比较通过，数据/代码/时序审计通过。
