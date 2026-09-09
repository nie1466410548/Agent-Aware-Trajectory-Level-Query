"""Render readable implementation notes from independently replayed evidence."""
import json
from pathlib import Path

from implement import HERE, ROOT, BATCH, parse, exp

NOTES = {
11: ('家长教育程度与学生成绩', {
 'C1': '缓存整张学生明细表。后续仍要返回全部 1,000 行，普通表扫描本来就便宜，数据库内再复制一份通常没有收益。',
 'C2': '按家长教育、性别、饮食、网络、活动、学习时间分段等维度联合分组，保存成绩及行为指标的 SUM/COUNT/MIN/MAX，再上卷回答各查询。联合粒度过细：1,000 行仅压到 875 行。'}),
12: ('钻石克拉区间与每克拉价格', {
 'C1': '保存价格、克拉和四档克拉区间；S9、S10 使用该派生明细表。仍是 53,595 行，只省去简单分箱表达式。',
 'C2': '保存价格、克拉、切工、颜色、净度和克拉区间；S16—S18 使用同一份派生明细。不要与 C1 直接互换区间字符串，两者标签不同。',
 'C3': '按切工 × 颜色 × 净度汇总，保存行数、缺失计数、极值和数值统计状态。53,595 行压成 276 行，后续按单维或全局上卷。'}),
13: ('任务负责人的绩效评价', {
 'C1': '缓存任务类型 × 状态的计数结果，S11 读取 S10 的结果；保留结果顺序。',
 'C2': '缓存 S33 的完整计算结果供 S34 使用，避免重复派生指标及分组。',
 'C3': '对 799 条任务一次性计算是否完成、是否按时、质量、工时效率、返工指标，后续负责人评价查询从临时表继续聚合。',
 'C4': '联合维度聚合状态表；先修复输出列名，仍将严格比较不通过的 S14 排除，保留原 SQL。剩余子集可以正确执行，但高维物化不一定划算。'}),
14: ('视频榜单与创作者特征', {
 'C1': '缓存全量 5,200 行榜单，后续十次完整读取仍需扫描、传输。若希望省去重复传输，应在工具层复用已有结果句柄；这不是本包数据库临时表已实现的收益。',
 'C2': '把视频类别、创作者、日期、排名分段等全部合成聚合粒度，保存播放互动等状态。仍有 5,200 行，列数反而增加，不宜因为覆盖 19 条 SQL 就默认启用。'}),
15: ('房屋特征与关注、带看表现', {
 'C1': '保留户型计数的完整结果，第二次相同查询读取临时结果。',
 'C2': '保留楼层计数结果，第二次相同查询读取临时结果。',
 'C3': '缓存 29,975 行原始房源明细，整表再读仍有扫描和输出成本。',
 'C4': '按户型、楼层、装修、朝向、关注量、精选、发布日期联合聚合。修复 S4 等未显式命名的输出列后重验；联合粒度较细。',
 'C5': '物化户型/装修/楼层/朝向均非 NULL 的房源，再执行 S24—S26。29,975 行只排除 3 行，过滤选择性很低。'}),
16: ('中国地表水/地下水与城镇化', {
 'C1': '从供水表保留 China、2005—2018 的 14 行，供明细和供水比例查询使用。',
 'C2': '从经济指标表保留同一地区和年份范围的 14 行，供城镇化及人均 GDP 等查询使用。两个候选来自不同表，不能合并为同一结果。'}),
17: ('产品类别年度利润率与家具类问题定位', {
 'C1': '缓存家具类、数量有效订单的年份/产品/数量/销售/利润投影；S51、S52 复用 S50。',
 'C2': '缓存家具类、数量有效订单的客户/年份/数量投影；S62 复用 S59。',
 'C3': '按年份 × 产品类别保存订单数、销售额、利润、亏损和异常计数，51,289 行汇成 12 行，支持全局、年度和类别上卷。',
 'C4': '先筛出 Home & Furniture 的 10,309 行订单，多个后续诊断查询共用；保留各查询原本的分组、排序和后续条件。',
 'C5': '对家具订单再按折扣、物流、年份、产品、数量、优先级、客户联合聚合，仅压成 10,259 行。S69、S70 浮点求和顺序变化导致严格比较失败，回退原 SQL。',
 'C6': '物化家具类 Beds 订单子集；供明细和销量/折扣/年份等分组使用。',
 'C7': '将 Beds 订单按数量 × 折扣 × 年份聚合，保存数量、销售和利润状态。与 C6 有覆盖交集，按实际收益择一或分配不同查询。',
 'C8': '物化家具类 Umbrellas 订单子集，供三个查询使用。',
 'C9': '将 Umbrellas 订单按数量 × 年份聚合，供两条汇总查询使用。与 C8 有交集。',
 'C10': '物化浏览表中的家具类记录；不是订单表的复用，必须独立建表。',
 'C11': '物化家具类中数量非 NULL 且不是 abc 的订单，多个清洗后分析共用。',
 'C12': '物化家具类 Sofa Covers 订单子集。',
 'C13': '物化家具类且数量、折扣有效的清洗后订单。与 C14 的条件合取项相同、顺序不同；二者是可替代方案，不应重复保存。',
 'C14': '与 C13 是条件顺序不同的同一过滤结果；当前独立保留验证证据，组合计划避免重复部署。',
 'C15': '清洗后的家具订单按年份 × 产品汇总折扣和数量乘折扣的 SUM/COUNT，服务 S65、S66。'}),
18: ('Fashion 类增长与客户群体', {
 'C1': 'customer_information 按客户编号去重，保留完整客户属性，后续与订单聚合做 Join。',
 'C2': 'Fashion 订单按客户编号汇总订单数、销售、利润；后续按客户群分析。',
 'C3': '与 C2 计算相同，只是 sales/profit 的输出顺序不同；在 M2 中统一物化并显式投影回原顺序。',
 'C4': '客户去重后只取性别、客户分层，是 C1 的较窄投影；可由 M1 服务。',
 'C5': 'Fashion 订单按客户求利润，是 C2 的较窄输出；可由 M2 服务。',
 'C6': '客户去重后只取性别，是 C1 的较窄投影；可由 M1 服务。',
 'C7': '客户表按客户编号统计源记录数，再回答人数/重复记录相关查询。不能替换为去重后的 COUNT(*)，否则会丢失原始重复次数。',
 'C8': '物化 Fashion 订单明细子集，服务该类别明细查询。',
 'C9': '物化浏览表 Fashion 子集，和订单表 C8 是不同的数据源。',
 'M1': '合并 C1/C4/C6：客户去重只构建一次，795 行；按各 CTE 的原列顺序显式投影，并给 Customer ID 建普通索引。',
 'M2': '合并 C2/C3/C5：Fashion 订单按客户聚合只构建一次，795 行；显式投影保持列顺序，并给 Customer ID 建普通索引。'}),
19: ('药品库存积压、断供与质量风险', {
 'C1': '缓存 S31 的多表 Join 结果（264 行），S32—S34 读取同一结果，保留原结果顺序。',
 'C2': '药品基本表按来源 × GSP 状态 × 存储条件 × 运输方式联合计数，427 行汇成 36 行，再按单维汇总。',
 'C3': '库存表按库存状态 × 预警状态 × 差异率保存计数和出入库日期极值。428 行仅压到 401 行。'}),
20: ('学生心理健康与成绩、行为因素', {
 'C1': '缓存全部 1,000 行学生记录；第二次取明细仍要读取和返回这些行。',
 'C2': '按心理健康分数、性别、兼职、饮食、家长教育、网络、活动联合聚合，保存行为和成绩统计状态。S5、S16 的全局平均值有浮点末位差异，严格口径下不改写。'}),
}


def num(value):
    return f'{value:.2f}'


def main():
    results = [json.loads((HERE / f'dacomp-{i:03}' / 'manifest.json').read_text()) for i in range(11, 21)]
    summary = []
    for a in results:
        i = int(a['task'][-3:]); title, notes = NOTES[i]
        d = HERE / a['task']; combo = a['combined']
        selected = ', '.join(combo['selected']) or '保留原查询'
        tables = json.loads((Path(a['source_run']) / 'schema.json').read_text())
        lines = [f'# {a["task"]}：{title}', '',
                 f'本次重放 {a["successful_data_sql"]} 条成功数据 SQL。组合方案：**{selected}**。'
                 f'全部查询与历史结果比较通过：**{combo["correct"]}**。', '',
                 '数据：' + '；'.join(f'`{t["name"]}` {t["rows"]:,} 行' for t in tables) + '。', '',
                 f'[原任务报告](../../reports/{BATCH}/tasks/{a["task"]}.md) · [返回十题总览](../README.md)', '',
                 '## 先看应当怎么做', '',
                 f'当前数据上的数据库执行与取回耗时：原始 **{num(combo["baseline_ms"])} ms** → '
                 f'组合方案 **{num(combo["optimized_ms"])} ms**（计入构建及清理）。'
                 '这是本机暖缓存小规模测量，不含模型、Python 分析和网络传输，不是整个 Agent 的加速比。', '',
                 '入口：[完整轨迹 SQL](trajectory.sql)；[执行与验证证据](manifest.json)。', '',
                 '## 每个候选如何实现', '',
                 '下表时间只比较该候选**通过验证的查询子集**。不同候选可能覆盖相同查询，时间或覆盖不能相加。', '',
                 '| 候选 | 实际保存的行数 | 验证通过/原覆盖 | 原查询 ms | 建表及索引 ms | 构建+改写 ms | 组合方案采用 |',
                 '|---|---:|---:|---:|---:|---:|---|']
        for p in a['candidates']:
            perf = p.get('performance', {})
            lines.append(f'| [{p["id"]}](#{p["id"].lower()}) | {p.get("rows", "未知")} | '
                         f'{len(p.get("safe", []))}/{len(p["covered"])} | '
                         f'{num(perf["baseline_ms"]) if perf else "—"} | '
                         f'{num(perf["build_ms"]) if perf else "—"} | '
                         f'{num(perf["total_ms"]) if perf else "—"} | '
                         f'{"是，具体查询见后表" if p["id"] in combo["selected"] else "否"} |')
        for p in a['candidates']:
            cid = p['id']
            lines += ['', f'### {cid}', '', notes[cid], '',
                      f'实现对象：`{p["table"]}`，{p.get("rows", "未知")} 行、{len(p.get("columns", []))} 列。'
                      + ('包含客户编号索引。' if p.get('indexes') else ''), '',
                      '**可改写查询：** ' + ', '.join(f'[{s}]({cid}/{s}.sql)' for s in p.get('safe', [])) + '。', '',
                      f'[建表 SQL]({cid}/build.sql) · [通过验证的完整执行脚本]({cid}/approved.sql) · '
                      f'[清理 SQL]({cid}/cleanup.sql) · [逐查询验证和计时]({cid}/validation.json)', '']
            if p['excluded']:
                for sid in p['excluded']:
                    trial = d / cid / (sid + '.sql')
                    contents = trial.read_text()
                    warning = '-- NOT APPROVED: result comparison failed. Use the original SQL for this query.\n'
                    if not contents.startswith(warning):
                        trial.write_text(warning + contents)
                lines += ['**回退原查询：** ' + ', '.join(p['excluded']) + '。不能执行这些查询对应的试验改写。', '']
                for check in p['checks']:
                    if not check['ok'] or not check['columns_equal']:
                        lines += [f'- {check["sql"]}：' + ('浮点末位差异；本包保留严格无序多重集比较，没有放宽标准。'
                                  if check.get('aligned_numeric_tolerance_only') else '结果或列名比较未通过，详情见验证 JSON。')]
            if p['type'] == 'aggregate MV':
                build = parse(p['build'])
                query = build.expression
                if isinstance(query, exp.Select):
                    dims = query.args.get('group')
                    if dims:
                        lines += ['', '物化粒度：' + '、'.join('`' + x.sql(dialect='sqlite') + '`' for x in dims.expressions) + '。']
            if cid in combo['selected']:
                uses = [s for s, deps in combo['dependencies'].items() if cid in deps]
                lines += ['', '组合方案实际使用：' + ', '.join(uses) + '；在 ' + uses[0] + ' 前构建一次。']
        lines += ['', '## 组合后的执行顺序', '',
                  '只列发生改写的查询；其余成功数据 SQL 原样执行。临时表按第一次使用时构建，任务结束删除。', '',
                  '| SQL | 使用的临时结果 |', '|---|---|']
        for sid, deps in combo['dependencies'].items():
            if deps:
                lines.append(f'| {sid} | {", ".join(deps)} |')
        if not combo['selected']:
            lines.append('| — | 当前测量不支持启用这些候选，完整脚本保留原查询 |')
        if i == 18:
            lines += ['', '客户属性约束：本数据快照逐客户检查 gender、Customer Segment、age、Education Level、'
                      'Marital Status、Region、Country、City，均没有属性冲突（包括 NULL/非 NULL 冲突）。'
                      '原始 `GROUP BY Customer ID` 携带非分组属性只在这种约束下有明确含义；新数据若出现冲突，'
                      '必须先规定选择哪条客户记录，再重新验证，不能任意用 MAX 代替。', '',
                      'M1 和 M2 可在同一 SQL 的不同 CTE 同时使用；组合脚本已做合并改写并验证，收益没有重复累加。']
        lines += ['', '## 执行命令', '', '在仓库根目录运行：', '', '```bash',
                  'benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py '
                  f'--task {i}', '```', '',
                  '若要单独检查某个候选，在命令末尾加 `--candidate C1`（按实际编号替换）。'
                  '该选项只执行验证通过的子集，候选能够执行不代表推荐启用。', '']
        (d / 'README.md').write_text('\n'.join(lines))
        summary.append(f'| [{i:03}]({a["task"]}/README.md) | {title} | {a["successful_data_sql"]} | '
                       f'{selected} | {num(combo["baseline_ms"])} | {num(combo["optimized_ms"])} | '
                       f'{num(combo["speedup"])}× |')
    candidates = [p for a in results for p in a['candidates']]
    total_sql = sum(a['successful_data_sql'] for a in results)
    excluded = [(a['task'], p['id'], p['excluded']) for a in results for p in a['candidates'] if p['excluded']]
    text = [
        '# 011—020：可以实际执行的 SQLite 复用方案', '',
        f'已将十题原报告中的全部候选落实为建表、查询改写、清理 SQL，并补充 018 的两个合并方案。'
        f'共 {len(candidates)} 个方案；组合重放覆盖 {total_sql} 条成功数据 SQL，逐条对照历史结果通过，十个原始数据库哈希保持不变。', '',
        '**建议先看下表，再点具体任务。** 每题的 `trajectory.sql` 是组合后的完整成功查询序列；'
        '`C*/approved.sql` 是单个候选通过验证的查询子集。性能不合算的方案仍保留可执行实现，供检查和后续不同规模实验。', '',
        '## 1. 哪些值得启用', '',
        '| 任务 | 分析场景 | 成功数据 SQL | 组合采用候选 | 原始 ms | 组合后 ms | 数据库阶段比值 |',
        '|---|---|---:|---|---:|---:|---:|', *summary, '',
        '这些比值是暖缓存下的本机诊断测量，不是论文级性能结论。未选候选的任务实际仍执行原 SQL，'
        '前后微小差异是测量波动。候选选择要求预计净节省超过 1 ms 且超过受益子集原耗时的 10%，'
        '避免把极小差异当成部署依据；组合后的实测收益可能更小。', '',
        '## 2. 实现方式：所有共享计算留在数据库里', '',
        '| 原报告机会 | 本次实现 | 后续查询怎么用 |',
        '|---|---|---|',
        '| 完全相同 SQL | 第一次查询时 `CREATE TEMP TABLE ... AS 原查询`；有序结果另外保存顺序编号 | 从临时表读取，保持列名；有序结果按编号读 |',
        '| 公共 CTE | 将 CTE 主体执行一次并保存为临时表 | 替换对应 CTE 的数据来源，其他逻辑保留 |',
        '| 公共单表过滤 | 将过滤后的行保存为临时表 | 后续分组/排序等访问该子集，保留原过滤确保语义 |',
        '| 聚合物化 | 按可覆盖查询的粒度保存 COUNT/SUM/MIN/MAX 及 AVG 的 SUM、非空 COUNT | 通过再次汇总得到原查询结果，不能直接平均平均值 |',
        '| 018 客户共享状态 | 合并投影不同的同类 CTE，并给临时表 Customer ID 建索引 | 同一条 SQL 可同时使用客户维表和客户订单聚合表 |', '',
        'Python 仅负责连接、调度 SQL、抓取结果、比较和计时，没有使用 Pandas 代替数据库过滤/Join/分组。'
        '临时表是本次物化实现，不要求数据库具有正式的 `CREATE MATERIALIZED VIEW` 对象。', '',
        '## 3. 怎样执行', '',
        '在仓库根目录运行（使用现有虚拟环境，不需要模型额度）：', '',
        '```bash',
        '# 执行 018 的组合方案，并逐条核对历史结果',
        'benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 18', '',
        '# 只执行 012 C3 的通过验证子集',
        'benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/replay.py --task 12 --candidate C3', '',
        '# 重新构建、验证和计时十题，再生成报告',
        'benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/implement.py --repeats 5',
        'benchmark/dacomp/.venv/bin/python benchmark/dacomp/fullscale/optimization-011-020/report.py',
        '```', '',
        '也可以在 SQLite 客户端同一连接中直接执行每题 `trajectory.sql`。连接原数据库时使用 URI '
        '`file:/绝对路径/数据库.sqlite?mode=ro`；不要再设置 `PRAGMA query_only=ON`，它会连 TEMP 写入也禁止。'
        '脚本在 `temp` 中建表，`main` 保持只读；同一事务固定快照，结束清理。'
        '换连接后临时表不可用，当前 Agent 工具若每次重连，需要先增加任务级连接管理才能在线接入。', '',
        '## 4. 正确性修复与限制', '',
        '- 修复聚合改写丢失原始输出列名的问题；所有输出包括未显式命名表达式都保留原标签。',
        '- 有 ORDER BY：按行序比较，数值使用原报告相同的相对 1e-12 / 绝对 1e-9 容差。'
        '无 ORDER BY：严格比较多重集，保留重复行，不因浮点末位差异就放宽标准。',
        '- 原始 SQL 首先在当前快照重放并与档案核对，然后才验证改写。'
        '对排序并列项、LIMIT、SQLite 非分组列等行为的结论仅适用于记录的快照和 SQLite 版本，不能推广为任意数据等价。',
        '- AVG 使用 SUM/COUNT 后浮点加法顺序可能变化。以下查询保留原执行，不混入通过验证的覆盖数：',
    ]
    text += [f'  - {task} {cid}：{", ".join(sids)}。' for task, cid, sids in excluded]
    text += ['',
        '每个候选目录中的单条 `S*.sql` 包含试验改写，失败条目便于复核；执行请使用 `approved.sql`、'
        '`replay.py` 或每题组合 `trajectory.sql`，不要批量执行未经筛选的试验 SQL。', '',
        '## 5. 性能口径与研究含义', '',
        '每个候选先预热，再交替测原始/改写顺序五次，取中位数。优化成本包含 CTAS、索引和读取全部结果；'
        '整轨迹另计清理。`temp_store=MEMORY`，不把临时表假定为零成本。原始和改写均使用相同 SQLite 连接与快照。'
        '计时不包括历史档案比较、模型推理、工具网络、JSON 编码以及后续 Python 分析。'
        '没有隔离机器上的其他工作负载，也没有清空 OS 缓存，因此不能声称冷启动或生产环境加速。', '',
        '组合方案按净收益贪心选取，对重叠查询只计一次；不同 CTE 可合并改写。'
        '本次没有对所有可能索引、聚合粒度及候选组合做全局搜索；未入选不等于没有任何优化办法。', '',
        '**构建点仍是离线假设。** 例如从 S3 开始就构建含后续所有维度的 MV，使用了未来 SQL 信息。'
        '本包证明的是当前快照下可执行、可比较的数据库实现；没有证明 Agent 能提前暴露 frontier，'
        '也没有把它们写回在线 Agent 的原始轨迹。', '',
        '## 6. 文件入口', '',
        '| 文件 | 用途 |', '|---|---|',
        '| `dacomp-*/README.md` | 每题候选的业务含义、选用理由及实际查询分配 |',
        '| `dacomp-*/trajectory.sql` | 完整成功数据查询序列，包含构建点和最终清理 |',
        '| `dacomp-*/C*/build.sql`、`M*/build.sql` | 可以直接提交 SQLite 的建表、索引语句 |',
        '| `dacomp-*/C*/approved.sql`、`M*/approved.sql` | 单候选通过验证的完整子集脚本 |',
        '| `dacomp-*/manifest.json` | 原 SQL、所有改写、组合、逐条比较、各轮计时及数据库哈希 |',
        '| `dacomp-*/source-analysis.json` | 冻结的原候选输入，避免其他会话刷新报告影响追溯 |',
        '| `implement.py`、`replay.py`、`report.py` | 可重现的实现、执行入口和报告生成器 |', '',
        '[导出 SQL 文件的独立执行检查](artifact-checks.json) 包含每题查询数、清理结果、数据库哈希检查和 018 客户属性约束证据。', '',
    ]
    (HERE / 'README.md').write_text('\n'.join(text))


if __name__ == '__main__':
    main()
