"""Detailed within-trajectory overlap inventory; no DB queries or episode mutations."""
import collections
import itertools
import json
import sqlite3
from pathlib import Path
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope
from sqlglot.schema import MappingSchema

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = json.loads((ROOT/'reports/data-inventory.json').read_text())
SCHEMAS = {(x['dataset'], x['database']): {
    t['table'].split('.')[-1].strip('"').lower(): {c.lower(): 'UNKNOWN' for c in t['columns']}
    for t in x['tables']} for x in INVENTORY}

# SQLite rowid is addressable but excluded from SELECT *; verify ordinary tables
# against read-only schema metadata rather than inventing visible inventory columns.
for database in INVENTORY:
    if database['engine'] != 'sqlite':
        continue
    key = database['dataset'], database['database']
    schema = {t: dict(cols) for t, cols in SCHEMAS[key].items()}
    visible = {t: set(cols) for t, cols in schema.items()}
    with sqlite3.connect('file:' + database['location'] + '?mode=ro', uri=True) as connection:
        definitions = connection.execute("SELECT name, sql FROM sqlite_master WHERE type='table'").fetchall()
    for table, definition in definitions:
        table = table.lower()
        if table in schema and definition and 'WITHOUT ROWID' not in definition.upper() and 'VIRTUAL TABLE' not in definition.upper():
            for hidden in ['rowid', '_rowid_', 'oid']:
                schema[table].setdefault(hidden, 'BIGINT')
    SCHEMAS[key] = MappingSchema(schema, visible=visible, dialect='sqlite')


def norm(e):
    return e.sql(normalize=True, pretty=False)


def conjuncts(e):
    if isinstance(e, exp.And):
        return conjuncts(e.this) + conjuncts(e.expression)
    return [e]


def enrich(q, dataset, run):
    out = dict(q)
    trees = [t for t in sqlglot.parse(q['sql'], read=q['dialect']) if t is not None]
    out['statement_count'] = len(trees)
    columns = set()
    features = {k: set() for k in ['bound_filters','filter_atoms','bound_joins',
        'bound_aggregates','groups','orders','windows','projections']}
    for tree in trees:
        # No benchmark schema contains case-only-distinct identifiers.
        for ident in tree.find_all(exp.Identifier):
            ident.set('this', ident.this.lower())
            ident.set('quoted', False)
        tree = qualify(tree, dialect=q['dialect'], schema=SCHEMAS[dataset,q['database']],
                       validate_qualify_columns=True)
        for scope in traverse_scope(tree):
            for col in scope.columns:
                source = scope.sources.get(col.table)
                if isinstance(source, exp.Table):
                    columns.add((source.name.lower(), col.name.lower()))
                    col.set('table', exp.to_identifier(source.name.lower()))
        for table in tree.find_all(exp.Table):
            table.set('alias', None)
        features['bound_filters'].update(norm(w.this) for w in tree.find_all(exp.Where))
        features['filter_atoms'].update(norm(c) for w in tree.find_all(exp.Where) for c in conjuncts(w.this))
        for key, kind in [('bound_joins',exp.Join),('bound_aggregates',exp.AggFunc),
                          ('groups',exp.Group),('orders',exp.Order),('windows',exp.Window)]:
            features[key].update(norm(e) for e in tree.find_all(kind))
        features['projections'].update(norm(e.this if isinstance(e, exp.Alias) else e)
            for select in tree.find_all(exp.Select) for e in select.expressions
            if (e.this if isinstance(e, exp.Alias) else e).find(exp.Column))
    out['bound_columns'] = sorted(columns)
    out.update({k: sorted(v) for k,v in features.items()})
    out['output_signature'] = None
    out['output_rows'] = set()
    result = run/'results'/f"{q['call_id']}.json"
    rows = json.loads(result.read_text())
    if rows:
        names = sorted(rows[0])
        out['output_signature'] = names
        out['output_rows'] = {json.dumps([row.get(k) for k in names], sort_keys=True,ensure_ascii=False) for row in rows}
    return out


LABELS = {
 'table_any':'共享至少一张基表',
 'table_equal':'基表集合完全相同（非空）',
 'column_name':'共享列名（旧口径，未绑定表）',
 'column_bound':'共享基表＋列（展开 SELECT *）',
 'column_equal':'引用的基表＋列集合相同（非空）',
 'column_covered':'前序引用列集合覆盖后序（非空）',
 'where_exact':'共享完整 WHERE（绑定表后）',
 'filter_atom':'共享至少一个 WHERE 合取项',
 'join_literal':'共享 Join 文本片段（旧口径）',
 'join_bound':'共享 Join 片段（基表别名归一）',
 'aggregate_literal':'共享聚合表达式（旧口径）',
 'aggregate_bound':'同基表集合且共享聚合表达式',
 'group':'同基表集合且共享 GROUP BY',
 'aggregate_group':'同基表集合、相同 GROUP BY 且共享聚合',
 'projection':'同基表集合且共享含列的投影表达式',
 'order':'同基表集合且共享 ORDER BY',
 'window':'同基表集合且共享窗口表达式',
 'range_compatible':'简单同列区间兼容（非数据交集证明）',
 'range_disjoint':'至少一个简单同列区间不相交',
 'result_row':'相同输出列名下存在相同结果行',
 'result_subset':'前序结果集合包含后序非空结果集合',
 'sql_exact':'规范化 SQL 完全相同',
 'reuse_witness':'满足已有保守结果复用语法条件',
}


def hits(p,q,old):
    def share(k):return bool(set(p[k]) & set(q[k]))
    pc,qc=set(map(tuple,p['bound_columns'])),set(map(tuple,q['bound_columns']))
    same=bool(p['tables'] and p['tables']==q['tables'])
    output=bool(p['output_signature'] and p['output_signature']==q['output_signature'] and p['statement_count']==q['statement_count']==1)
    ranges=old.get('range_comparisons',[])
    return {
      'table_any':bool(set(p['tables'])&set(q['tables'])), 'table_equal':same,
      'column_name':share('columns'), 'column_bound':bool(pc&qc),
      'column_equal':bool(pc and pc==qc), 'column_covered':bool(qc and qc<=pc),
      'where_exact':share('bound_filters'), 'filter_atom':share('filter_atoms'),
      'join_literal':bool(old.get('shared_joins')), 'join_bound':share('bound_joins'),
      'aggregate_literal':bool(old.get('shared_aggregates')),
      'aggregate_bound':same and share('bound_aggregates'), 'group':same and share('groups'),
      'aggregate_group':same and share('groups') and share('bound_aggregates'),
      'projection':same and share('projections'), 'order':same and share('orders'),
      'window':same and share('windows'),
      'range_compatible':bool(ranges) and all(x['relation']=='compatible_intervals' for x in ranges),
      'range_disjoint':any(x['relation']=='disjoint' for x in ranges),
      'result_row':output and bool(p['output_rows']&q['output_rows']),
      'result_subset':output and bool(q['output_rows']) and q['output_rows']<=p['output_rows'],
      'sql_exact':p.get('canonical')==q.get('canonical'),
      'reuse_witness':bool(old.get('reuse_witnesses')),
    }


def main():
    runs=[]
    for path in sorted((ROOT/'runs').glob('*/*/*/quick-01/analysis.json')):
        a=json.loads(path.read_text());summary=a['summary'];dataset=summary['task_id'].split('/')[0]
        qs=[enrich(q,dataset,path.parent) for q in a['queries'] if q['success'] and not q['metadata']]
        old={(p['producer'],p['consumer']):p for p in a['pairs']}
        pairs=[];eligible=0
        for p,q in itertools.combinations(qs,2):
            if p['database']!=q['database']:continue
            eligible+=1
            if not(set(p['tables'])&set(q['tables'])):continue
            h=hits(p,q,old[p['call_id'],q['call_id']])
            pairs.append({'producer':p['call_id'],'consumer':q['call_id'], 'database':q['database'],
                'metrics':[k for k,v in h.items() if v], 'shared_tables':sorted(set(p['tables'])&set(q['tables'])),
                'shared_bound_columns':sorted(set(map(tuple,p['bound_columns']))&set(map(tuple,q['bound_columns']))),
                'shared_filter_atoms':sorted(set(p['filter_atoms'])&set(q['filter_atoms'])),
                'shared_joins':sorted(set(p['bound_joins'])&set(q['bound_joins']))})
        runs.append({'group':summary['group'],'task':summary['task_id'], 'passed':summary['validator_passed'],
            'successful':len(qs),'attempted':summary['data_queries'],'eligible_pairs':eligible,
            'pairs':pairs,'queries':[{k:v for k,v in q.items() if k!='output_rows'} for q in qs],
            'analysis_path':str(path.relative_to(ROOT))})
    def aggregate(rs):
        result={}
        for k in LABELS:
            matched=[(i,p) for i,r in enumerate(rs) for p in r['pairs'] if k in p['metrics']]
            result[k]={'pairs':len(matched), 'consumers':len({(i,p['consumer']) for i,p in matched}),
                       'tasks':len({i for i,p in matched})}
        return result
    groups={g:aggregate([r for r in runs if r['group']==g]) for g in ['natural','fad']}
    report={'definitions':LABELS,'groups':groups,'runs':runs}
    (ROOT/'reports/overlap-detail.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    lines=['> 历史结构相似性统计，不代表优化机会；当前报告见 [OVERLAP.md](OVERLAP.md)。', '', '# 系统性 overlap 清单','','本报告基于已保存的 18 条轨迹重新统计，没有重新运行 Agent。仅比较同一运行、同一逻辑数据库内的前后成功数据 SQL；排除元数据和失败尝试。不同任务与不同组不相互配对。',
      '', '**查询对数**：每个前序→后序组合算一对。**后续查询数**：一条 SQL 即使与多个前序重叠，在该指标中也只算一次。百分比以本组全部成功数据 SQL 为分母；不同指标可交叉，不可相加。任务数是该组出现该类重叠的任务数。', '',
      '| 统计范围 | 自然组 | FAD 组 |','|---|---:|---:|']
    for label,fn in [('成功数据 SQL 调用',lambda rs:sum(r['successful'] for r in rs)),('成功数据 SQL 语句（拆分多语句调用）',lambda rs:sum(q['statement_count'] for r in rs for q in r['queries'])),('数据 SQL 尝试（含失败）',lambda rs:sum(r['attempted'] for r in rs)),('同库前后查询对（包括不重叠）',lambda rs:sum(r['eligible_pairs'] for r in rs))]:
        lines.append('| '+label+' | '+' | '.join(str(fn([r for r in runs if r['group']==g])) for g in groups)+' |')
    lines+=['','计数单位沿用原报告的 SQL 工具调用：3 次成功数据调用各含 2 条 SQL，结构特征取调用内各语句的并集；不统计同一次调用内部的重叠。自然组 65 次成功调用含 66 条语句，FAD 组 42 次含 44 条。多语句调用只保存末条结果，故排除它们的结果行比较。', '', '## 按层次统计','', '| 重叠定义 | 自然：对数 | 自然：后续 SQL / 65 | 自然：任务 / 9 | FAD：对数 | FAD：后续 SQL / 42 | FAD：任务 / 9 |','|---|---:|---:|---:|---:|---:|---:|']
    for k,label in LABELS.items():
        vals=[]
        for g,n in [('natural',65),('fad',42)]:
            v=groups[g][k];vals += [str(v['pairs']),f"{v['consumers']} ({v['consumers']/n:.1%})",str(v['tasks'])]
        lines.append('| '+label+' | '+' | '.join(vals)+' |')
    lines+=['','## 按任务分布','', '以下单元格均为后续查询数；分母为该运行成功数据 SQL 数。列级采用绑定基表并展开星号的新口径；Join 使用基表别名归一，聚合要求同基表集合。','', '| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join | 聚合 | GROUP BY | 相同结果行 |','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in sorted(runs,key=lambda r:(r['task'],r['group'])):
        m=aggregate([r]);vals=[str(m[k]['consumers']) for k in ['table_any','column_bound','filter_atom','join_bound','aggregate_bound','group','result_row']]
        lines.append(f"| [{r['task']}](../{r['analysis_path']}) | {r['group']} | {'通过' if r['passed'] else '未通过'} | {r['successful']} | "+' | '.join(vals)+' |')
    lines+=['','## 重访的是哪些表','', '“访问 SQL”按每条 SQL 每张表一次计数；“重访 SQL”扣除本轨迹该表首次访问。同一 SQL 涉及多表可出现在多行，因此不能把各表重访数直接相加得到总重叠查询数。', '', '| 数据集 / 数据库 / 表 | 自然访问 SQL | 自然重访 SQL | FAD 访问 SQL | FAD 重访 SQL |','|---|---:|---:|---:|---:|']
    table_stats=collections.defaultdict(lambda:collections.Counter())
    for r in runs:
        seen=set()
        for q in r['queries']:
            for t in q['tables']:
                key=(r['task'].split('/')[0],q['database'],t)
                table_stats[key][r['group']+'_access']+=1
                if key in seen:table_stats[key][r['group']+'_revisit']+=1
                seen.add(key)
    for key,v in sorted(table_stats.items()):lines.append('| '+' / '.join(key)+' | '+' | '.join(str(v[g+'_'+m]) for g in ['natural','fad'] for m in ['access','revisit'])+' |')
    columns=collections.defaultdict(lambda:collections.defaultdict(set))
    joins=collections.defaultdict(lambda:collections.Counter())
    for r in runs:
        for pair in r['pairs']:
            for table,col in pair['shared_bound_columns']:
                key=(r['task'].split('/')[0],pair['database'],table,col)
                columns[key][r['group']].add((r['task'],pair['consumer']))
            for join in pair['shared_joins']:
                joins[(r['group'],r['task'],join)]['pairs']+=1
    lines += ['', '## 具体重复列与 Join', '',
        f"发生跨查询重叠的不同基表列：自然组 {sum(bool(v['natural']) for v in columns.values())} 个，FAD 组 {sum(bool(v['fad']) for v in columns.values())} 个。以下为按自然组后续查询数排序的前 20 个；计数按任务＋后续调用去重。", '',
        '| 基表列（数据集 / 数据库 / 表 / 列） | 自然后续查询数 | FAD 后续查询数 |',
        '|---|---:|---:|']
    for key,v in sorted(columns.items(),key=lambda kv:(-len(kv[1]['natural']),kv[0]))[:20]:
        lines.append('| '+' / '.join(key)+' | '+str(len(v['natural']))+' | '+str(len(v['fad']))+' |')
    lines += ['', '所有重复 Join 片段如下；包含对 CTE 的 Join，不能全部解读为可共享的基表 Join。', '',
        '| 组 / 任务 | 归一化 Join 片段 | 查询对数 |','|---|---|---:|']
    for (group,task,join),v in sorted(joins.items()):
        lines.append(f"| {group} / {task} | `{join}` | {v['pairs']} |")
    lines += ['', '## 实际结果重合案例', '',
        '结果重合与完整结果可复用分开列出。下表中的“后序被包含”仅为本次结果值集合的包含，不证明 SQL 语义包含。', '',
        '| 组 / 任务 | 前序 SQL | 后序 SQL | 前序 / 后序行数 | 后序结果集合被包含 |',
        '|---|---|---|---:|---|']
    for r in runs:
        qs={q['call_id']:q for q in r['queries']}
        directory=(ROOT/r['analysis_path']).parent
        for pair in r['pairs']:
            if 'result_row' not in pair['metrics']:continue
            p,q=qs[pair['producer']],qs[pair['consumer']]
            links=[]
            for query in [p,q]:
                file=next((directory/'sql').glob('*-'+query['call_id']+'.sql'))
                links.append(f"[{file.name.split('-')[0]}](../{file.relative_to(ROOT)})")
            lines.append(f"| {r['group']} / {r['task']} | {links[0]} | {links[1]} | {p['row_count']} / {q['row_count']} | {'是' if 'result_subset' in pair['metrics'] else '否'} |")
    lines+=['','## 口径与解释边界','',
      '- 列绑定使用已实测的 schema 和 SQLGlot 作用域，展开 SELECT *；COUNT(*) 不被解释为读取全部列。统计包括 SELECT、WHERE、JOIN、GROUP BY、ORDER BY 等位置引用的基表列，并不等同于输出列或物理读取字节。派生列在内部查询处统计基础依赖；常量输出别名不算基表列。',
      '- 旧列名口径未展开星号、未区分同名列所属表；新口径与旧口径不同，保留两者方便追溯。Join 片段只比较该 JOIN 节点，不证明其左输入、中间结果或谓词下推相同。',
      '- 过滤条件只拆 AND 合取项，保留常量值；未证明一般谓词等价或包含。简单区间沿用原分析器，仅支持单表直接列与字面量比较；不覆盖复杂日期函数/CAST 列表达式。区间兼容不是实际行集合相交的证明。',
      '- 分组、聚合、投影和排序仅为表达式结构重合，输入行可能不同；相同 GROUP BY 加相同聚合仍不足以推出同一聚合结果。基表引用绑定后未实现所有派生关系的代数等价归一。',
      '- 结果重合比较相同输出列名下的实际 JSON 行值，忽略行顺序与重复次数，且限定同库共享表的查询对。统计值碰巧相同也会命中；这不证明底层数据范围相同，也不表示可以省掉查询。',
      '- 前序引用列覆盖后序只说明列需求集合包含，不代表前序输出包含这些列，更不代表其行范围覆盖后序。',
      '- SQL 完全重复和保守复用候选沿用原分析。0 个保守候选不排除一般 Join 中间结果复用或聚合 rollup。物理扫描行/字节 overlap、通用结果包含关系和净性能收益本次尚未测量。',
      '', '逐查询绑定特征、逐对命中类别及 call_id 见 [overlap-detail.json](overlap-detail.json)。原 SQL 位于各运行目录的 sql/，通过 call_id 可对应查询和完整结果。复算：', '', '```bash','benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/overlap_report.py','```']
    (ROOT/'reports/OVERLAP-structural-v1.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(groups,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
