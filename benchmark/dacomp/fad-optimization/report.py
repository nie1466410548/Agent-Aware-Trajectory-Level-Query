"""Render one task-local performance report from completed paired runs."""
import argparse
import json
import random
import statistics as st
from pathlib import Path

from agent_db_tool.optimization.check import read_records

LABELS = {'index': '仅建索引', 'materialization': '仅建汇总表', 'combined': '索引＋汇总表'}


def median(xs):
    return st.median(xs)


def ci(xs, seed=20260910):
    rng = random.Random(seed)
    samples = sorted(median(rng.choices(xs, k=len(xs))) for _ in range(10000))
    return [samples[249], samples[9749]]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', required=True)
    parser.add_argument('--diagnostics', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    root, diag, out = Path(args.run), Path(args.diagnostics), Path(args.output)
    assert (root / 'COMPLETE.json').exists(), 'only report completed experiments'
    out.parent.mkdir(parents=True, exist_ok=True)
    space_data = json.loads((out.parent / 'space-diagnostic.json').read_text())
    stats, records, pair_summaries = {}, {}, {}
    for mode in LABELS:
        pairs = sorted((root / mode).glob('pair-*'))
        values = [(json.loads((p / 'baseline' / 'summary.json').read_text()), json.loads((p / mode / 'summary.json').read_text())) for p in pairs]
        assert len(values) >= 20
        assert all(json.loads((p / 'correctness.json').read_text())['all_equal'] for p in pairs)
        pair_summaries[mode] = values
        records[mode] = [(read_records(p / 'baseline'), read_records(p / mode)) for p in pairs]
        delta = [a['total_seconds'] - b['total_seconds'] for a, b in values]
        stats[mode] = {'pairs': len(values),
                       'baseline_total_seconds': median([a['total_seconds'] for a, b in values]),
                       'optimized_total_seconds': median([b['total_seconds'] for a, b in values]),
                       'paired_savings_seconds': median(delta), 'paired_savings_95_ci': ci(delta),
                       'paired_savings_min_max': [min(delta), max(delta)],
                       'paired_savings_percent': median([(a['total_seconds'] - b['total_seconds']) / a['total_seconds'] * 100 for a, b in values]),
                       'paired_speedup': median([a['total_seconds'] / b['total_seconds'] for a, b in values]),
                       'pairs_faster': sum(d > 0 for d in delta),
                       'baseline_components': {k: median([a[k] for a, b in values]) for k in ('query_seconds', 'fad_receive_seconds', 'rewrite_seconds', 'decision_including_build_seconds', 'cleanup_seconds', 'common_setup_logging_close_seconds')},
                       'optimized_components': {k: median([b[k] for a, b in values]) for k in ('query_seconds', 'fad_receive_seconds', 'rewrite_seconds', 'decision_including_build_seconds', 'build_including_estimate_seconds', 'cleanup_seconds', 'common_setup_logging_close_seconds')},
                       'query_saved_seconds': median([a['query_seconds'] - b['query_seconds'] for a, b in values]),
                       'peak_extra_bytes': max(b['peak_extra_allocated_bytes'] for a, b in values),
                       'optimized_cpu_seconds': median([b['cpu_seconds'] for a, b in values]),
                       'baseline_cpu_seconds': median([a['cpu_seconds'] for a, b in values]),
                       'optimized_peak_rss_kib': max(b['peak_rss_kib_process_including_prewarm'] for a, b in values),
                       'baseline_peak_rss_kib': max(a['peak_rss_kib_process_including_prewarm'] for a, b in values),
                       'baseline_io_bytes': {k: median([a['io_delta'][k] for a, b in values]) for k in ('read_bytes', 'write_bytes', 'rchar', 'wchar')},
                       'optimized_io_bytes': {k: median([b['io_delta'][k] for a, b in values]) for k in ('read_bytes', 'write_bytes', 'rchar', 'wchar')}}
    (out.parent / 'statistics.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n')
    lines = ['# FAD驱动数据库优化验证结果', '', '## DAComp-006：原始18,250行', '',
             '**本次实现没有获得数据库端净收益。三种方式都加快了一部分SQL，但全部优化成本计入后，整段轨迹耗时增加。**', '',
             '输入为已保存的006轨迹：30次SQL尝试，29次成功；Q10原本调用SQLite不支持的STDEV，两组保留同一失败。这里没有调用Agent，不含模型生成FAD的延时。**对照组只接收SQL并正常执行，完全不接收或处理FAD，也不创建优化控制器。优化组接收SQL＋FAD，承担FAD处理和优化的全部成本。**', '',
             '本报告已按用户纠正的对照重新实测。旧的“两组都处理FAD”结果已撤出主要结论；本次数字来自全新的120次回放，不是从旧耗时中扣减校验时间。', '',
             '### 整个任务到底快了多少', '',
             '每种方式各20对独立实验，共60对、120次回放。下表总耗时为20次的中位数；“增加比例”为每对相对变化的中位数。单位毫秒。', '',
             '| 数据库处理方式 | 对照组总耗时 | 优化组总耗时 | 耗时增加比例 | 比对照快的实验 |',
             '|---|---:|---:|---:|---:|']
    for mode, s in stats.items():
        lines.append(f"| {LABELS[mode]} | {s['baseline_total_seconds']*1000:.1f} | {s['optimized_total_seconds']*1000:.1f} | {-s['paired_savings_percent']:.1f}% | {s['pairs_faster']}/{s['pairs']} |")
    lines += ['', '配对净节省 = 同一对的对照耗时 − 优化耗时，负数表示变慢。95%区间采用固定种子的10,000次配对重采样，保留每对关联，不把120次当作互不相关的样本：', '',
              '| 方式 | 配对净节省中位数 | 95%区间 | 最小～最大 | 加速倍数（小于1为变慢） |', '|---|---:|---:|---:|---:|']
    for mode, s in stats.items():
        lo, hi = s['paired_savings_95_ci']; mn, mx = s['paired_savings_min_max']
        lines.append(f"| {LABELS[mode]} | {s['paired_savings_seconds']*1000:.1f} ms | [{lo*1000:.1f}, {hi*1000:.1f}] ms | [{mn*1000:.1f}, {mx*1000:.1f}] ms | {s['paired_speedup']:.3f}× |")
    lines += ['', '### 时间花在哪里', '',
              '以下按每种方式各自的20对结果计算中位数。各分段中位数不一定精确加成总耗时。SQL时间包含完整结果读取和逐行写入结果文件；“决策及构建”已经包含估计扫描、建对象和失败尝试，不要再次加上对象表中的构建时间。', '',
              '| 时间部分（ms） | 索引：对照 → 优化 | 汇总表：对照 → 优化 | 组合：对照 → 优化 |', '|---|---:|---:|---:|']
    for key, label in [('query_seconds', 'SQL执行与完整结果归档'), ('fad_receive_seconds', 'FAD解码、格式/目录校验及列引用汇总'), ('rewrite_seconds', 'SQL编译检查、匹配改写及浮点保护'), ('decision_including_build_seconds', '优化决策、估计扫描与对象构建'), ('cleanup_seconds', '清理优化对象'), ('common_setup_logging_close_seconds', '连接初始化、必要日志与关闭（优化组另含空间检查）')]:
        lines.append('| ' + label + ' | ' + ' | '.join(f"{stats[m]['baseline_components'][key]*1000:.1f} → {stats[m]['optimized_components'][key]*1000:.1f}" for m in LABELS) + ' |')
    lines += ['']
    for mode, s in stats.items():
        lines.append(f"- {LABELS[mode]}：SQL本身合计省约 **{s['query_saved_seconds']*1000:.1f} ms**，但任务总耗时增加约 **{-s['paired_savings_seconds']*1000:.1f} ms**。")
    lines += ['', '这里最明显的限制是：原始数据很小，单条SQL通常只需几毫秒；本次Python原型逐轮做SQL解析、结构匹配及保守检查，成本超过省下的扫描时间。这个结果说明当前实现和策略在该规模不划算，不能据此声称FAD没有预测价值，也不能用单条查询加速代替任务净收益。', '',
              '### 结果是否一致、实验是否独立', '',
              '- 先用独立诊断副本验证，再开始正式计时；正式实验结束后再次逐条核对所有结果。60对全部通过，29条成功查询的列名、列顺序、行数、重复行和数值一致；Q10失败状态和错误也一致。',
              '- 有ORDER BY时逐行比较，否则比较保留重复行的多重集合。浮点绝对容差1e-7、相对容差1e-9；没有放宽到容忍整数位变化。',
              '- 每次新数据库副本、新进程、新任务连接，预热完整基础表后关闭预热连接，再开始计时。两组都如此。这是统一预热实验，不是操作系统冷缓存实验。',
              '- 60对顺序及每对AB/BA顺序由固定种子随机生成，串行执行，计时进程固定到同一逻辑CPU。对象每次重新构建，优化时间不跨实验摊销。共享机器不声称独占。',
              '- 对象只能在本轮SQL结束后由本轮已到达FAD触发，不能用于本轮SQL。控制器不读取未来SQL或离线命中分析；每轮日志保存查询前可用对象。',
              '- 下载/复制/预热属于共同准备，计时外单列；优化所需统计扫描、建表/建索引、检查、归档与清理全部计时。没有异步工作或虚构的Agent思考空档。', '',
              '**校准中的失败也保留了：** 初次索引运行在Q13、Q15将一个ROUND结果从40455变成40454。原因是索引改变浮点累加顺序。正式版本对当前SQL含ROUND和聚合、且基础表原先无索引的情况恢复全表读取；汇总表构建也保持该读取路径。这个保护没有按Q编号特判，成本和牺牲的索引机会都反映在正式结果里。Q10曾被SQL解析器重印函数名导致错误文本变化，现优化组先检查原SQL，原本失败的SQL保持原样执行；对照组直接执行原SQL，保留数据库原生错误。', '',
              '### 哪些FAD建出了对象，后来谁用了', '',
              '下表构建时间包含为估计空间所做的扫描。占用空间是独立诊断测得的已使用页增长（包含页管理开销），不是文件长度增长；两个索引合计使用1180 KiB，但复用了原库空闲页，主库文件没有变大。实际使用依据独立诊断运行的EXPLAIN QUERY PLAN；汇总表还必须在实际执行SQL中出现。正式运行逐轮改写、可用对象及结果均与诊断核对。', '']
    diag_records = {m: read_records(diag / m) for m in LABELS}
    object_labels = {}
    for mode in LABELS:
        objects = pair_summaries[mode][0][1]['objects']
        lines += [f'#### {LABELS[mode]}', '', '| 对象 | 哪轮FAD促成构建 | 构建耗时 | 后续实际使用SQL | 占用空间 |', '|---|---|---:|---|---:|']
        for n, obj in enumerate(objects, 1):
            name = obj['name']; label = ('索引' if obj['kind'] == 'index' else '汇总表') + str(n)
            object_labels[(mode, name)] = label
            use = [r['step'] for r in diag_records[mode] if any(name in str(x) for x in r['plan'])]
            build_ms = median([o['build_seconds']*1000 for a, b in pair_summaries[mode] for o in b['objects'] if o['name'] == name])
            trigger = '、'.join('Q'+str(q) for q in obj['source_steps']) + f"；Q{obj['created_after']}结束后建立"
            links = '、'.join(f'[Q{q}](#q{q})' for q in use) or '**未使用**'
            occupied = next(o['used_page_growth_bytes'] for o in space_data[mode]['objects'] if o['name'] == name)
            lines.append(f"| {label} | {trigger} | {build_ms:.1f} ms | {links} | {occupied/1024:.0f} KiB |")
        for obj in objects:
            lines += ['', f"**{object_labels[(mode, obj['name'])]}：FAD中明确的访问内容与实际DDL**", '', '```sql', obj['ddl'], '```']
        lines += ['']
    lines += ['未使用的典型对象是“无过滤的月度利润汇总表”：Q1/Q2预测了该模式，但后续月度查询实际加了华南过滤，且常要求更多指标。首版不猜过滤范围、不补未预测指标，因此不能复用。仅汇总表模式下它占去一个名额，仍完整承担构建成本。其余候选因为没有再次出现、已有对象达到数量上限，或所需指标未被覆盖，没有继续构建；详细原因在逐轮日志中。', '',
              '组合模式每轮也只建一个对象，因此前两次先建索引，随后建出的两个汇总表与“仅汇总表”模式不同。这是同一选择规则的结果，不是人为给组合模式另选后续查询。', '',
              '### 每轮SQL：用了什么，快了多少', '',
              '每轮列出原SQL、该轮FAD、执行前已有对象的实际使用、该轮结束后的新动作。查询耗时只比较本条SQL；整段任务是否划算以上面的总耗时为准。单位毫秒，中位数来自每种方式各自的20对实验。', '']
    original = read_records(diag / 'combined')
    for i, raw in enumerate(original):
        q = raw['step']
        lines += [f'<a id="q{q}"></a>', f'#### Q{q}', '', '<details><summary>原SQL</summary>', '', '```sql', raw['sql'], '```', '', '</details>', '',
                  '| 方式 | 本条SQL：对照 → 优化 | 查询时实际使用对象 | 本轮SQL之后的构建动作 |', '|---|---:|---|---|']
        for mode in LABELS:
            r = diag_records[mode][i]
            times_a = [a[i]['query_seconds']*1000 for a, b in records[mode]]
            times_b = [b[i]['query_seconds']*1000 for a, b in records[mode]]
            used = [obj['name'] for obj in pair_summaries[mode][0][1]['objects'] if any(obj['name'] in str(x) for x in r['plan'])]
            use_text = '、'.join(object_labels[(mode, n)] for n in used) or '原表'
            if r['status'] != 'ok':
                use_text = '保留原始失败：STDEV不受支持'
            actions = [a for a in r['actions'] if a['status'] != 'skipped']
            action_text = '；'.join(('建立' + object_labels[(mode, a['name'])]) if a['status']=='built' else '构建被拒绝/失败：'+a['error'] for a in actions) or '无新对象'
            lines.append(f'| {LABELS[mode]} | {median(times_a):.2f} → {median(times_b):.2f} | {use_text} | {action_text} |')
        for mode in LABELS:
            r = diag_records[mode][i]
            if r['materializations_used']:
                lines += ['', f'<details><summary>{LABELS[mode]}：实际改写后SQL</summary>', '', '```sql', r['executed_sql'], '```', '', '</details>']
        if any('preserve original full scan' in reason for m in LABELS for reason in diag_records[m][i]['rewrite_rejections']):
            lines += ['', '本轮索引路径触发浮点保护，对原先无索引的基础表使用NOT INDEXED；具体执行SQL保存在该轮事件中。']
        lines += ['', '<details><summary>本轮Agent原始FAD</summary>', '', '```json', json.dumps(raw['raw_fad'], ensure_ascii=False, indent=2), '```', '', '</details>', '']
    lines += ['### 额外资源与测量边界', '', '| 方式 | 新占用页 | 主库文件增长＋临时库页数 | 进程峰值RSS：对照 → 优化 | CPU时间：对照 → 优化 |', '|---|---:|---:|---:|---:|']
    for mode, s in stats.items():
        occupied = sum(o['used_page_growth_bytes'] for o in space_data[mode]['objects'])
        lines.append(f"| {LABELS[mode]} | {occupied/1024:.0f} KiB | {s['peak_extra_bytes']/1024:.0f} KiB | {s['baseline_peak_rss_kib']/1024:.1f} → {s['optimized_peak_rss_kib']/1024:.1f} MiB | {s['baseline_cpu_seconds']*1000:.1f} → {s['optimized_cpu_seconds']*1000:.1f} ms |")
    lines += ['', '原库自带687个空闲页，共2,813,952字节，索引复用它们，所以文件不增长并不表示索引不占空间。新占用页在独立副本重放动作测量，未混入正式计时；具体记录见space-diagnostic.json。当前预算监控主库文件增长与临时库页数，新占用的空闲页另列；本次实际使用也低于7,507,968字节上限。RSS为整个进程峰值，包含Python库和计时前预热。这些数据不是排序器临时文件的完整峰值。各次进程I/O（read_bytes/write_bytes及rchar/wchar）和准备时间保存在summary.json；完整环境、顺序、数据/代码哈希保存在manifest.json。', '',
              '### 当前结论与后续范围', '',
              'A—E的小型固定轨迹验证已经完成：预测可以促成真实复用，但当前Python实现与选择规则在18,250行上没有净收益。尚未运行真实Agent会话，也未扩容。下一步若继续，可按计划做十万行规模敏感性检查，观察扫描收益增长后能否覆盖这些开销；不能把当前负结果改写成已验证提速。', '',
              f'- [正式实验清单、固定顺序与代码快照](../runs/{root.name}/manifest.json)',
              f'- [60对实验全部通过的完成记录](../runs/{root.name}/COMPLETE.json)',
              '- [可重算的汇总数字](statistics.json)',
              '- [独立的对象占用空间诊断](space-diagnostic.json)',
              f'- [最终1800条查询对照与输入、时间顺序审计](../runs/{root.name}/AUDIT.json)',
              '- [实现与复现方式](../../../../../../agent_db_tool/optimization/README.md)',
              '- [校准失败记录](../runs/calibration-01/index/correctness.json)', '']
    # Report lives benchmark/dacomp/fad-optimization/reports: four parents to repo.
    lines = [x.replace('../../../../../../agent_db_tool/', '../../../../agent_db_tool/') for x in lines]
    out.write_text('\n'.join(lines))
    print(json.dumps({m: {k: s[k] for k in ('baseline_total_seconds','optimized_total_seconds','paired_savings_percent','paired_savings_95_ci')} for m,s in stats.items()}, indent=2))


if __name__ == '__main__':
    main()
