"""Produce reproducible per-episode SQL/Python inventories; no model calls."""
import json
from pathlib import Path
import sqlglot
from sqlglot import exp

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = ROOT / 'reports'
    report.mkdir(exist_ok=True)
    summaries = []
    for run in sorted((ROOT/'runs'/'natural').glob('*/*')):
        if not (run/'tool_calls.jsonl').exists():
            continue
        events = sorted([json.loads(l) for l in (run/'tool_calls.jsonl').read_text().splitlines()], key=lambda c:c['start_time'])
        task = run.parent.name
        queries = []
        python = []
        for event in events:
            if event['tool']=='python':
                python.append({'id':f'P{len(python)+1}',**event})
            if event['tool']!='query-db':
                continue
            q = {'id':f'Q{len(queries)+1}',**event}
            try:
                tree = sqlglot.parse_one(event['sql'], read='sqlite')
                q['tables'] = sorted({t.name for t in tree.find_all(exp.Table)})
                q['groups'] = [g.sql(dialect='sqlite') for g in tree.find_all(exp.Group)]
                q['predicates'] = [w.sql(dialect='sqlite') for w in tree.find_all(exp.Where)]
                q['aggregates'] = sorted({a.sql(dialect='sqlite') for a in tree.find_all(exp.AggFunc)})
                q['metadata'] = isinstance(tree, exp.Pragma) or any(t.lower().startswith(('sqlite_','pragma_')) for t in q['tables'])
                q['parsed'] = True
            except Exception as exc:
                q.update(parsed=False, parse_error=str(exc), metadata=False)
            queries.append(q)
        summary = json.loads((run/'run_summary.json').read_text()) if (run/'run_summary.json').exists() else {'task_id':task,'running':True}
        summary.update(sql_success=sum(q['success'] for q in queries),
                       metadata_sql=sum(q['success'] and q['metadata'] for q in queries),
                       successful_analysis_sql=sum(q['success'] and not q['metadata'] for q in queries),
                       sql_with_group_by=sum(q['success'] and bool(q.get('groups')) for q in queries),
                       sql_parse_coverage=f"{sum(q['parsed'] for q in queries)}/{len(queries)}",
                       python_calls=len(python),python_success=sum(p['success'] for p in python),
                       sql_execute_fetch_ms=sum(q.get('execute_fetch_ms',0) for q in queries if q['success']))
        dependencies = []
        for p in python:
            for q in queries:
                if q['call_id']+'.json' in p.get('code','') and q['end_time'] < p['start_time']:
                    dependencies.append({'from':q['id'],'to':p['id'],'kind':'SQL result file referenced by Python source'})
        summary['sql_to_python_file_edges'] = len(dependencies)
        summaries.append(summary)
        (report/f'{task}-{run.name}-inventory.json').write_text(json.dumps({'summary':summary,'queries':queries,'python':python,'file_dependencies':dependencies},ensure_ascii=False,indent=2)+'\n')
        lines = [f'# {task} / {run.name} 查询与 Python 清单', '',
                 'Q 编号按该任务 SQL 尝试的开始时间排序，包含错误和元数据查询；P 编号独立。不同任务的 Q 编号不相关。', '',
                 f'[展开 Python 工具后的全部 SQL 轨迹（含 list-db 和连接设置）]({task}-{run.name}-SQL-TRAJECTORY.md)。本页 Q 编号仅对应 query-db 调用，不是全部数据库语句数。', '',
                 'GROUP BY 仅为语法清单，不等于跨查询下钻或复用机会。CTE 名称可能出现在表名清单中。', '']
        lines += ['## 工具时间顺序','', ' → '.join(next((q['id'] for q in queries if q['call_id']==e['call_id']), next((p['id'] for p in python if p['call_id']==e['call_id']),e['tool'])) for e in events), '',
                  'SQL 结果文件在后续 Python 源码中的引用：'+('；'.join(d['from']+' → '+d['to'] for d in dependencies) or '无'), '']
        for q in queries:
            result = (run/'results'/Path(q['result_file']).name).relative_to(report.parent)
            lines += [f"## {q['id']} — {'成功' if q['success'] else '失败'}",'',
                      f"结果行数：{q.get('row_count','—')}；执行并取回：{q.get('execute_fetch_ms',0):.3f} ms；元数据：{q['metadata']}",'',
                      '```sql',q['sql'],'```','',f"[完整结果](../{result})",'']
            if q.get('error'): lines += [q['error'],'']
        for p in python:
            lines += [f"## {p['id']} — Python {'成功' if p['success'] else '失败'}",'',
                      '```python',p.get('code',''),'```','',
                      f"[完整 stdout/stderr](../{(run/'results'/Path(p['result_file']).name).relative_to(report.parent)})",'']
        (report/f'{task}-{run.name}-QUERIES.md').write_text('\n'.join(lines))
        if (run/'run_summary.json').exists():
            # Plain-text export retained for later evaluation; this is not a judge run.
            (run/f'{task}-traj.txt').write_text((run/'kimi.jsonl').read_text())
    (report/'summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))
    from sql_trajectory import main as export_sql_trajectory
    export_sql_trajectory()


if __name__=='__main__':
    main()
