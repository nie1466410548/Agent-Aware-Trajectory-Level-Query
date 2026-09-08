"""Export SQL behind Python tools as one trajectory, without double counting.

Historical connection setup is reconstructed only for the audited v1 adapter;
it is explicitly distinguished from recorded statements. No model calls.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1_TOOL_SHA = '0ccdc4aa86ce9c8f659fe9212b99e1ec731a10696f81296ab5e5c1ff0f097d5d'
ACCESS = re.compile(r'\b(?:sqlite3|duckdb|psycopg2|read_sql\w*|executescript|executemany|execute|connect|subprocess|__import__|importlib)\b')


def export(run, known_v1):
    events=sorted(map(json.loads,(run/'tool_calls.jsonl').read_text().splitlines()),key=lambda x:x['start_time'])
    statements=[]; python=[]; q=0
    for event in events:
        if event['tool']=='python':
            code=event.get('code','')
            python.append({'id':f'P{len(python)+1}','call_id':event['call_id'],
                           'source_available':bool(code),'database_access_review_flags':sorted(set(ACCESS.findall(code)))})
        if event['tool'] not in ['query-db','list-db'] or 'sql' not in event:
            continue
        if event['tool']=='query-db': q+=1
        reference=f'Q{q}' if event['tool']=='query-db' else 'list-db'
        common={'call_id':event['call_id'],'tool':event['tool'],'database':event['database'],
                'call_start_time':event['start_time'],'query_reference':reference}
        # In these v1 runs every successful call and the known SQL prepare error
        # reached the connection setup. Other failures must not be guessed.
        reached=event['success'] or event.get('error')=='OperationalError: misuse of aggregate function AVG()'
        if known_v1 and reached and not event.get('limit_reached'):
            statements.append({**common,'sql':'PRAGMA query_only=ON','category':'connection_setup',
                               'evidence':'reconstructed_from_audited_v1_adapter','success':None,
                               'note':'Runs before the logged statement; no separate execution timestamp or duration was recorded.'})
        statements.append({**common,'sql':event['sql'],'category':'metadata' if event['tool']=='list-db' else 'query',
                           'evidence':'tool_calls.jsonl','success':event['success'],
                           'result_file':str((run/'results'/Path(event['result_file']).name).relative_to(ROOT)),
                           'execute_fetch_ms':event.get('execute_fetch_ms'),'error':event.get('error')})
    for i,s in enumerate(statements,1):s['id']=f'S{i}'
    summary={'task_id':run.parent.name,'run_id':run.name,
             'recorded_sql_attempts':sum(s['evidence']=='tool_calls.jsonl' for s in statements),
             'recorded_sql_success':sum(s['success'] is True for s in statements),
             'recorded_metadata_sql':sum(s['category']=='metadata' for s in statements),
             'query_db_attempts':q,'reconstructed_setup_sql':sum(s['category']=='connection_setup' for s in statements),
             'python_calls_reviewed':len(python),
             'python_calls_requiring_review':sum(not p['source_available'] or bool(p['database_access_review_flags']) for p in python)}
    return {'summary':summary,'statements':statements,'python_review':python,
            'limitations':'S is an expanded SQL sequence, Q retains original query-db numbering. Setup entries are source reconstruction, not historical engine trace. Python source scanning is not proof of runtime completeness; flagged or missing source requires review. Pandas operations are not translated into invented SQL.'}


def main():
    known=hashlib.sha256((ROOT/'tools/tool.py').read_bytes()).hexdigest()==V1_TOOL_SHA
    summaries=[]
    for run in sorted((ROOT/'runs/natural').glob('*/*')):
        if not (run/'tool_calls.jsonl').exists():continue
        data=export(run,known); summary=data['summary']; summaries.append(summary)
        stem=f'{run.parent.name}-{run.name}-SQL-TRAJECTORY'
        (ROOT/'reports'/f'{stem}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        lines=[f'# {run.parent.name}：展开 Python 工具后的 SQL 轨迹','',
               'S 编号包含数据 SQL、元数据 SQL 和可据工具源码恢复的连接设置；Q 编号保持原查询清单不变。', '',
               '**源码恢复的 PRAGMA 并非历史引擎日志，不能与有执行记录的 SQL 混称为实测调用。** SQL 经 Python 工具执行只记一次；Pandas 计算不虚构成 SQL。','',
               f"有日志的 SQL 尝试：{summary['recorded_sql_attempts']}；成功：{summary['recorded_sql_success']}；其中查表元数据：{summary['recorded_metadata_sql']}；额外恢复连接设置：{summary['reconstructed_setup_sql']}。",'',
               f"独立 Python 源码检查：{summary['python_calls_reviewed']} 次；需要进一步核查：{summary['python_calls_requiring_review']} 次。静态检查不能替代运行时数据库追踪。",'',
               '| 顺序 | 原编号 | 类型 | 来源 | 状态 |','|---|---|---|---|---|']
        for s in data['statements']:
            lines.append(f"| {s['id']} | {s['query_reference']} | {s['category']} | {'工具日志' if s['evidence']=='tool_calls.jsonl' else '源码恢复'} | {'成功' if s['success'] is True else '失败' if s['success'] is False else '未独立记录'} |")
        for s in data['statements']:
            lines += ['',f"## {s['id']} · {s['query_reference']}",'','```sql',s['sql'],'```']
            if s.get('result_file'):lines += ['',f"[完整结果](../{s['result_file']})"]
            if s.get('error'):lines += ['',s['error']]
        (ROOT/'reports'/f'{stem}.md').write_text('\n'.join(lines)+'\n')
    (ROOT/'reports/sql-trajectory-summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))


if __name__=='__main__':main()
