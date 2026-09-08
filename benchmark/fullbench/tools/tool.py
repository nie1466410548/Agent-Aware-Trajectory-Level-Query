"""Logged data tools for the Kimi bookreview pilot. Run from a task directory."""
import argparse
import os
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import uuid
import yaml
import fcntl

ROOT = Path(__file__).resolve().parents[1]

def execute_mongo(client, request):
    from pymongo import MongoClient
    def check(value):
        if isinstance(value,dict):
            if any(k in {'$out','$merge'} for k in value):raise ValueError('MongoDB writes are disabled')
            for v in value.values():check(v)
        elif isinstance(value,list):
            for v in value:check(v)
    check(request)
    with MongoClient('mongodb://127.0.0.1:55440',serverSelectionTimeoutMS=10000) as conn:
        db=conn[client['db_name']]
        op=request.get('operation');name=request.get('collection')
        if op=='list':return [{'collection':n} for n in db.list_collection_names()]
        if not isinstance(name,str):raise ValueError('collection is required')
        coll=db[name]
        if op=='find':
            cur=coll.find(request.get('filter',{}),request.get('projection')).max_time_ms(600000)
            if request.get('sort'):cur=cur.sort([tuple(x) for x in request['sort']])
            if request.get('limit'):cur=cur.limit(int(request['limit']))
            return list(cur)
        if op=='aggregate':return list(coll.aggregate(request['pipeline'],maxTimeMS=600000))
        if op=='count_documents':return [{'count':coll.count_documents(request.get('filter',{}),maxTimeMS=600000)}]
        if op=='distinct':return [{'value':v} for v in coll.distinct(request['field'],request.get('filter',{}),maxTimeMS=600000)]
        raise ValueError('Allowed operations: find, aggregate, count_documents, distinct')

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='tool', required=True)
    q = sub.add_parser('query-db')
    q.add_argument('db')
    q.add_argument('--fad-id')
    sql = q.add_mutually_exclusive_group(required=True)
    sql.add_argument('--sql')
    sql.add_argument('--sql-file', type=Path)
    sql.add_argument('--mongo-file', type=Path)
    l = sub.add_parser('list-db')
    l.add_argument('db')
    f = sub.add_parser('fad')
    f.add_argument('--file', type=Path, required=True)
    p = sub.add_parser('python')
    p.add_argument('--file', type=Path, required=True)
    a = sub.add_parser('answer')
    a.add_argument('--file', type=Path, required=True)
    args = parser.parse_args()
    run = Path(os.environ.get('DAB_RUN_DIR',str(Path.cwd()))).resolve()
    if not run.is_relative_to(ROOT/'runs') and not run.is_relative_to(ROOT/'smoke'):
        raise RuntimeError('Use the assigned episode directory; task logs cannot be redirected')
    meta = json.loads((run / 'task_meta.json').read_text())
    dataset = meta['task_id'].split('/')[0]
    expected_task=os.environ.get('DAB_TASK_ID')
    expected_group=os.environ.get('DAB_GROUP')
    if expected_task and (meta['task_id']!=expected_task or meta['group']!=expected_group):
        raise RuntimeError('Episode identity mismatch')
    data_root = ROOT / 'upstream' / ('query_' + dataset)
    config = yaml.safe_load((data_root/'db_config.yaml').read_text())['db_clients']
    call = uuid.uuid4().hex
    results = run / 'results'
    results.mkdir(exist_ok=True)
    log = run / 'tool_calls.jsonl'
    event = {'task_id': meta['task_id'], 'run_id': meta['run_id'],
             'call_id': call, 'tool': args.tool, 'start_time': time.time(),
             'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    start = time.perf_counter()
    try:
        if args.tool == 'fad':
            if meta['group'] != 'fad':
                raise ValueError('FAD is disabled in the natural group')
            forecast = json.loads(args.file.read_text())
            if not isinstance(forecast, dict) or not isinstance(forecast.get('accesses'), list):
                raise ValueError('Expected {"accesses": [...]}')
            for access in forecast['accesses']:
                if access.get('database') not in config:raise ValueError('Unknown database')
                for field in ['tables','columns','filters','operations']:
                    if not isinstance(access.get(field),list):raise ValueError('Each access needs lists: tables, columns, filters, operations')
            event['frontier']=forecast
            data={'fad_id':call, 'accepted':True, 'instruction':'Now generate the next SQL in a NEW assistant turn; cite this fad_id. Do not reuse after one query attempt.'}
        elif args.tool in ['query-db', 'list-db']:
            previous=[json.loads(s) for s in log.read_text().splitlines()] if log.exists() else []
            if sum(c['tool']=='query-db' for c in previous) >= 30:
                raise RuntimeError('Limit of 30 query attempts reached; submit current answer.')
            client = config[args.db]
            dialect = client['db_type']
            sql = args.sql if args.tool == 'query-db' else None
            if args.tool == 'query-db' and args.sql_file:
                sql = args.sql_file.read_text()
            if args.tool == 'list-db':
                sql = ("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                       if dialect in ['postgres','duckdb'] else
                       "SELECT name FROM sqlite_master WHERE type='table'")
                if dialect=='duckdb':sql="SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog')"
            event.update(database=args.db, dialect=dialect, sql=sql, fad_id=getattr(args,'fad_id',None))
            if meta['group']=='fad' and args.tool=='query-db':
                fads=[c for c in previous if c['tool']=='fad' and c['success']]
                if not fads or args.fad_id!=fads[-1]['call_id']:
                    raise ValueError('Submit a new FAD first and cite the returned fad_id')
                if any(c.get('fad_id')==args.fad_id for c in previous):
                    raise ValueError('FAD receipt already used; refresh before generating another SQL')
                event['fad_lead_s']=event['start_time']-fads[-1]['end_time']
            if dialect == 'mongo':
                event.pop('sql',None)
                request={'operation':'list'} if args.tool=='list-db' else json.loads(args.mongo_file.read_text()) if args.mongo_file else json.loads(args.sql)
                event['mongo_request']=request
                data=execute_mongo(client,request)
                event.update(row_count=len(data),columns=sorted(set().union(*(set(x) for x in data))) if data else [])
            else:
                if dialect == 'postgres':
                    import psycopg2
                    conn = psycopg2.connect(host='127.0.0.1', port=55439, user='dab_reader',
                        dbname=client['db_name'], application_name=f"dab:{meta['task_id']}:{call}"[:63],
                        options='-c default_transaction_read_only=on -c statement_timeout=600000', connect_timeout=10)
                elif dialect == 'duckdb':
                    import duckdb
                    conn=duckdb.connect(str(data_root/client['db_path']),read_only=True,config={'threads':2,'memory_limit':'1GB','enable_external_access':'false'})
                else:
                    db = data_root/client['db_path']
                    conn = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)
                    conn.execute('PRAGMA query_only=ON')
                    deadline = time.monotonic() + 600
                    conn.set_progress_handler(lambda: int(time.monotonic() > deadline), 10000)
                try:
                    cur = conn.cursor()
                    execute_start = time.perf_counter()
                    import sqlparse
                    statement_results=[]
                    event['statement_results']=statement_results
                    execute_total=0.0;fetch_total=0.0
                    for index,statement in enumerate(sqlparse.split(sql),1):
                        statement_start=time.perf_counter()
                        cur.execute(statement)
                        execute_total+=(time.perf_counter()-statement_start)*1000
                        cols=[d[0] for d in cur.description] if cur.description else []
                        values=cur.fetchall() if cur.description else []
                        fetch_total+=(time.perf_counter()-statement_start)*1000
                        payload=[dict(zip(cols,row)) for row in values]
                        raw_statement=json.dumps(payload,ensure_ascii=False,default=str).encode()
                        statement_file=results/(call+f'-statement-{index}.json')
                        statement_file.write_bytes(raw_statement)
                        statement_results.append({'sql':statement,'columns':cols,'row_count':len(values),'result_file':str(statement_file),'result_sha256':hashlib.sha256(raw_statement).hexdigest()})
                    event['statement_results']=statement_results
                    event['execute_return_ms'] = execute_total
                    columns = [d[0] for d in cur.description] if cur.description else []
                    rows = values
                    event['execute_fetch_ms'] = fetch_total
                    data = [dict(zip(columns, row)) for row in rows]
                    event.update(columns=columns, row_count=len(rows))
                finally:
                    conn.close()
        elif args.tool == 'python':
            event['code'] = args.file.read_text()
            code_path = results / (call + '.py')
            code_path.write_text(event['code'])
            proc = subprocess.run([sys.executable, str(code_path)], cwd=run,
                                  text=True, capture_output=True, timeout=600)
            data = {'stdout': proc.stdout, 'stderr': proc.stderr, 'returncode': proc.returncode}
            event['success'] = proc.returncode == 0
        else:
            answer = args.file.read_text()
            (run / 'answer.txt').write_text(answer)
            data = {'submitted': True, 'answer': answer}
        raw = json.dumps(data, ensure_ascii=False, default=str).encode()
        path = results / (call + '.json')
        path.write_bytes(raw)
        event.update(result_file=str(path), result_bytes=len(raw), result_sha256=hashlib.sha256(raw).hexdigest())
        event.setdefault('success', True)
        output = {'call_id': call, 'success': event['success'], 'result_file': str(path),
                  'row_count': event.get('row_count'), 'preview': raw.decode()[:10000],
                  'truncated': len(raw.decode()) > 10000}
    except Exception as exc:
        event.update(success=False, error=f'{type(exc).__name__}: {exc}')
        output = {'call_id': call, 'success': False, 'error': event['error']}
    event.update(end_time=time.time(), duration_ms=(time.perf_counter()-start)*1000)
    with log.open('a') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX)
        stream.write(json.dumps(event, ensure_ascii=False, default=str) + '\n')
        stream.flush()
        fcntl.flock(stream,fcntl.LOCK_UN)
    print(json.dumps(output, ensure_ascii=False))

if __name__ == '__main__':
    main()
