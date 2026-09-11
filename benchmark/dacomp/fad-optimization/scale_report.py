"""Append a measured scale to the single task report, retaining original-scale evidence."""
import argparse
import json
import statistics as st
from pathlib import Path
from agent_db_tool.optimization.check import read_records

LABELS={'index':'仅索引','materialization':'仅汇总表','combined':'索引＋汇总表'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--diagnostics',required=True)
    p.add_argument('--data-manifest',required=True);p.add_argument('--output',required=True)
    args=p.parse_args();root=Path(args.run);diag=Path(args.diagnostics);out=Path(args.output)
    assert (root/'COMPLETE.json').exists()
    data=json.loads(Path(args.data_manifest).read_text());summary={};runs={};records={};diagnostics={}
    for mode in LABELS:
        pairs=sorted((root/mode).glob('pair-*'));assert len(pairs)==5
        runs[mode]=[(json.loads((q/'baseline/summary.json').read_text()),json.loads((q/mode/'summary.json').read_text())) for q in pairs]
        records[mode]=[(read_records(q/'baseline'),read_records(q/mode)) for q in pairs]
        diagnostics[mode]=read_records(diag/mode)
        assert all(json.loads((q/'correctness.json').read_text())['all_equal'] for q in pairs)
        rows=[]
        for i,(a,b) in enumerate(runs[mode],1):
            rows.append({'pair':i,'baseline_seconds':a['total_seconds'],'optimized_seconds':b['total_seconds'],
                         'saved_seconds':a['total_seconds']-b['total_seconds'],
                         'saved_percent':(a['total_seconds']-b['total_seconds'])/a['total_seconds']*100})
        summary[mode]={'pairs':rows,'baseline_seconds':st.median(r['baseline_seconds'] for r in rows),
                       'optimized_seconds':st.median(r['optimized_seconds'] for r in rows),
                       'saved_seconds':st.median(r['saved_seconds'] for r in rows),
                       'saved_percent':st.median(r['saved_percent'] for r in rows),
                       'faster_pairs':sum(r['saved_seconds']>0 for r in rows),
                       'saved_min_max_seconds':[min(r['saved_seconds'] for r in rows),max(r['saved_seconds'] for r in rows)]}
    (out.parent/'statistics-million.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    lines=['# FAD驱动数据库优化验证结果','','## DAComp-006：合成1,000,000行','',
           '**比较普通SQL执行与SQL＋FAD优化，所有FAD处理、估计扫描、建对象、改写和清理成本均计入；不调用Agent。**','',
           '按用户要求，每种方式5对独立实验，共15对、30次正式回放。每次均新副本、新进程、新连接、相同完整预热流程，随机AB/BA串行执行。SQL、FAD、对象数量上限、两次预测触发规则和优化预算公式保持不变。', '',
           '### 总耗时与净收益','', '| 优化方式 | 普通执行 | FAD＋优化 | 时间降低比例（负数为变慢） | 优化更快的配对 |','|---|---:|---:|---:|---:|']
    for mode,s in summary.items():lines.append(f"| {LABELS[mode]} | {s['baseline_seconds']:.3f} s | {s['optimized_seconds']:.3f} s | {s['saved_percent']:+.1f}% | {s['faster_pairs']}/5 |")
    positive=[LABELS[m] for m,s in summary.items() if s['saved_seconds']>0]
    lines+=['',('本次中位数出现净收益的方式：'+ '、'.join(positive)+'。' if positive else '**扩大到100万行后，这三种方式的中位数仍没有净收益。**'),
            '总耗时为5次的中位数，比例为5个配对比例的中位数，不能用两个取整后的时间精确复算。5对属于初步观察，以下保留每一对，不给出看似精确的置信区间。','',
            '| 方式 | 配对 | 普通执行 | FAD＋优化 | 净节省 |','|---|---:|---:|---:|---:|']
    for mode,s in summary.items():
        for r in s['pairs']:lines.append(f"| {LABELS[mode]} | {r['pair']} | {r['baseline_seconds']:.3f} s | {r['optimized_seconds']:.3f} s | {r['saved_seconds']:+.3f} s |")
    lines+=['','### 时间花在哪里','','单位秒，均为各自5次的中位数。构建时间包含空间估计所需扫描；各项中位数不一定相加等于总耗时。','',
            '| 时间部分 | 索引：普通 → 优化 | 汇总表：普通 → 优化 | 组合：普通 → 优化 |','|---|---:|---:|---:|']
    for key,label in [('query_seconds','SQL及全部结果归档'),('fad_receive_seconds','FAD解码、校验和列引用汇总'),('rewrite_seconds','编译预检、匹配改写及浮点保护'),('decision_including_build_seconds','决策、估计扫描、构建'),('cleanup_seconds','对象清理'),('common_setup_logging_close_seconds','连接、目录/行数统计、日志及其他开销')]:
        lines.append('| '+label+' | '+' | '.join(f'{st.median(a[key] for a,b in runs[m]):.3f} → {st.median(b[key] for a,b in runs[m]):.3f}' for m in LABELS)+' |')
    lines+=['','这次校验和匹配基本不随行数增长，构建扫描则随数据一起变大。以下分别列出查询节省与构建成本，判断有没有回本：','']
    for mode in LABELS:
        saved=st.median(a['query_seconds']-b['query_seconds'] for a,b in runs[mode])
        built=st.median(b['build_including_estimate_seconds'] for a,b in runs[mode])
        wording=f'查询合计省{saved:.3f}秒' if saved>=0 else f'查询本身反而增加{-saved:.3f}秒'
        lines.append(f'- {LABELS[mode]}：{wording}，构建（含估计扫描）花{built:.3f}秒。')
    small_path=out.parent/'statistics.json'
    if small_path.exists():
        small=json.loads(small_path.read_text())
        lines+=['','固定检查成本和构建成本要分开看。下表是优化组总耗时中的占比：','','| 方式 | FAD校验＋改写检查：小库 → 百万行 | 构建（含估计）：小库 → 百万行 |','|---|---:|---:|']
        for mode in LABELS:
            old=small[mode];oc=old['optimized_components'];ot=old['optimized_total_seconds']
            fixed_small=(oc['fad_receive_seconds']+oc['rewrite_seconds'])/ot*100
            build_small=oc['build_including_estimate_seconds']/ot*100
            fixed_big=st.median((b['fad_receive_seconds']+b['rewrite_seconds'])/b['total_seconds']*100 for a,b in runs[mode])
            build_big=st.median(b['build_including_estimate_seconds']/b['total_seconds']*100 for a,b in runs[mode])
            lines.append(f'| {LABELS[mode]} | {fixed_small:.1f}% → {fixed_big:.1f}% | {build_small:.1f}% → {build_big:.1f}% |')
    lines+=['','仅汇总表模式仍保留那张没有华南过滤、未被后续使用的月度利润表；占用一个名额并产生真实构建成本。没有因提前看到结果而替换策略。索引也不是自动收益：某些查询用了索引但比直接扫描更慢，逐轮表保留这些负结果。','', '### 每个优化动作及后续复用','','下面的构建成本包含估计扫描，不是纯CREATE语句时间。对象没有被使用也照计成本。各对象后续使用轮次来自独立诊断的执行计划，实际执行SQL与正式回放核对。','']
    object_names={}
    for mode in LABELS:
        objects=runs[mode][0][1]['objects'];lines += [f'#### {LABELS[mode]}','','| 对象 | 建立时点 | 构建耗时 | 后续使用SQL |','|---|---|---:|---|']
        for n,obj in enumerate(objects,1):
            name=obj['name'];label=('索引' if obj['kind']=='index' else '汇总表')+str(n);object_names[(mode,name)]=label
            time=st.median(next(o['build_seconds'] for o in b['objects'] if o['name']==name) for a,b in runs[mode])
            used=[r['step'] for r in diagnostics[mode] if any(name in str(x) for x in r['plan'])]
            links='、'.join(f'[Q{q}](#million-q{q})' for q in used) or '**未使用**'
            lines.append(f"| {label} | Q{obj['created_after']}之后 | {time:.3f} s | {links} |")
        for obj in objects:lines+=['',f"**{object_names[(mode,obj['name'])]}实际DDL**",'','```sql',obj['ddl'],'```']
        failures=[(r['step'],a) for r in diagnostics[mode] for a in r['actions'] if a['status'] not in ('built','skipped')]
        for q,a in failures:lines+=['',f"Q{q}之后的构建被拒绝或失败：{a.get('error')}，耗时{a['build_seconds']:.3f}秒（诊断运行）。"]
        lines+=['']
    lines+=['### 数据如何扩容、结果是否一致','',
            f"- 原始18,250行完整复制{data['full_copies']}份，再无放回抽取{data['remainder_rows']:,}行；固定种子{data['seed']}。新增订单只修改运单号，其他业务字段整行保留。", 
            f"- 生成后逐行回读核验{data['business_fields_verified_rows']:,}行。原始53条重复运单号未修复，新增运单号不冲突。华南{data['output_profile']['south_china_rows']:,}行，8种产品、277个目的地、原有日期范围不变。", 
            '- 原始SQL/FAD轨迹不变，仍为30次尝试、29次成功。Q10原有STDEV失败保留；每对均与百万行普通执行结果比较，不能拿小库答案做基准。',
            '- 15对共450条查询对照全部通过；整数/字符串/NULL精确核对，浮点仍采用绝对1e-7、相对1e-9容差，ORDER BY逐行比较，其余保留重复行。未放宽正确性要求。',
            '- 合成数据增加了行数，分组基数没有增长，可能有利于汇总表；不能推论真实业务类别增加时也有相同效果。新库沿用表结构，没有初始索引。',
            '- 生成文件、输入准备、复制和完整预热放在计时外；两组都如此。主实验是预热条件，不声称操作系统冷缓存。', '',
            '### 每轮SQL、FAD和优化后的实际执行','','查询时间单位秒；这些是单条查询时间，总收益仍以包含全部优化成本的任务总耗时为准。','']
    for i,r in enumerate(diagnostics['combined']):
        q=r['step'];lines += [f'<a id="million-q{q}"></a>',f'#### Q{q}','','<details><summary>原SQL</summary>','','```sql',r['sql'],'```','','</details>','',
                              '| 方式 | 普通 → 优化 | 查询使用对象 | 本轮之后新增对象 |','|---|---:|---|---|']
        for mode in LABELS:
            dr=diagnostics[mode][i]
            used=[o['name'] for o in runs[mode][0][1]['objects'] if any(o['name'] in str(x) for x in dr['plan'])]
            use='、'.join(object_names[(mode,x)] for x in used) or '原表'
            if dr['status']!='ok':use='保留STDEV失败'
            added='、'.join(object_names[(mode,a['name'])] for a in dr['actions'] if a['status']=='built') or '无'
            a=st.median(x[i]['query_seconds'] for x,y in records[mode]);b=st.median(y[i]['query_seconds'] for x,y in records[mode])
            lines.append(f'| {LABELS[mode]} | {a:.4f} → {b:.4f} | {use} | {added} |')
        for mode in LABELS:
            dr=diagnostics[mode][i]
            if dr['executed_sql']!=dr['sql']:lines+=['',f'<details><summary>{LABELS[mode]}：实际执行SQL</summary>','','```sql',dr['executed_sql'],'```','','</details>']
        lines+=['','<details><summary>本轮Agent原始FAD</summary>','','```json',json.dumps(r['raw_fad'],ensure_ascii=False,indent=2),'```','','</details>','']
    lines+=['### 额外资源','','| 方式 | 优化对象导致的文件增长＋临时页峰值 | 进程峰值RSS：普通 → 优化 | CPU时间：普通 → 优化 |','|---|---:|---:|---:|']
    for mode in LABELS:
        values=runs[mode]
        extra=max(b['peak_extra_allocated_bytes'] for a,b in values)/1048576
        ra=max(a['peak_rss_kib_process_including_prewarm'] for a,b in values)/1024
        rb=max(b['peak_rss_kib_process_including_prewarm'] for a,b in values)/1024
        ca=st.median(a['cpu_seconds'] for a,b in values);cb=st.median(b['cpu_seconds'] for a,b in values)
        lines.append(f'| {LABELS[mode]} | {extra:.2f} MiB | {ra:.1f} → {rb:.1f} MiB | {ca:.3f} → {cb:.3f} s |')
    lines+=['','RSS包括预热和Python进程，不包含完整操作系统文件缓存；页数也不是排序器临时文件的完整峰值。临时表仍设置temp_store=FILE，不保证每个小汇总表实际写盘。每次的I/O和准备耗时保存在summary.json。','']
    lines+=['### 复现与原始记录','',
            f'- [百万行数据生成清单](../data/synthetic-1000000.manifest.json)',
            f'- [本批环境、输入/代码哈希、随机顺序](../runs/{root.name}/manifest.json)',
            f'- [全部配对完成记录](../runs/{root.name}/COMPLETE.json)',
            f'- [最终审计](../runs/{root.name}/AUDIT.json)',
            '- [每对结果及汇总数字](statistics-million.json)',
            '- [生成器](../scale_data.py)','',
            '下面保留原始18,250行实验，两个规模分开阅读。','']
    old=out.read_text();marker='## DAComp-006：原始18,250行';assert marker in old
    small_section=old[old.index(marker):].replace('尚未运行真实Agent会话，也未扩容。下一步若继续，可按计划做十万行规模敏感性检查，观察扫描收益增长后能否覆盖这些开销；不能把当前负结果改写成已验证提速。','本小节保留原始规模结论；百万行扩容的独立结果已列在上方。真实Agent会话尚未运行。')
    out.write_text('\n'.join(lines)+small_section)
    print(json.dumps({m:{k:v for k,v in s.items() if k!='pairs'} for m,s in summary.items()},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
