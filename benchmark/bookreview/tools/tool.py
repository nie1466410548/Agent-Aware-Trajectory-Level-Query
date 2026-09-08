"""Logged data tools for the Kimi bookreview pilot. Run from a task directory."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='tool', required=True)
    q = sub.add_parser('query-db')
    q.add_argument('db', choices=['books_database', 'review_database'])
    sql = q.add_mutually_exclusive_group(required=True)
    sql.add_argument('--sql')
    sql.add_argument('--sql-file', type=Path)
    l = sub.add_parser('list-db')
    l.add_argument('db', choices=['books_database', 'review_database'])
    p = sub.add_parser('python')
    p.add_argument('--file', type=Path, required=True)
    a = sub.add_parser('answer')
    a.add_argument('--file', type=Path, required=True)
    args = parser.parse_args()
    run = Path.cwd()
    meta = json.loads((run / 'task_meta.json').read_text())
    call = uuid.uuid4().hex
    results = run / 'results'
    results.mkdir(exist_ok=True)
    log = run / 'tool_calls.jsonl'
    event = {'task_id': meta['task_id'], 'run_id': meta['run_id'],
             'call_id': call, 'tool': args.tool, 'start_time': time.time(),
             'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    start = time.perf_counter()
    try:
        if args.tool in ['query-db', 'list-db']:
            if log.exists() and sum(1 for _ in log.open()) >= 60:
                raise RuntimeError('Pilot limit of 60 tool calls reached; submit current answer.')
            sql = args.sql if args.tool == 'query-db' else None
            if args.tool == 'query-db' and args.sql_file:
                sql = args.sql_file.read_text()
            if args.tool == 'list-db':
                sql = ("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
                       if args.db == 'books_database' else
                       "SELECT name FROM sqlite_master WHERE type='table'")
            event.update(database=args.db, dialect='postgres' if args.db == 'books_database' else 'sqlite', sql=sql)
            if args.db == 'books_database':
                import psycopg2
                conn = psycopg2.connect(host='127.0.0.1', port=55439, user='dab_reader',
                    dbname='bookreview_db', application_name=f"dab:{meta['task_id']}:{call}",
                    options='-c default_transaction_read_only=on -c statement_timeout=600000', connect_timeout=10)
            else:
                db = ROOT / 'upstream/query_dataset/review_query.db'
                conn = sqlite3.connect(db.as_uri() + '?mode=ro', uri=True)
                conn.execute('PRAGMA query_only=ON')
                deadline = time.monotonic() + 600
                conn.set_progress_handler(lambda: int(time.monotonic() > deadline), 10000)
            try:
                cur = conn.cursor()
                execute_start = time.perf_counter()
                cur.execute(sql)
                event['execute_return_ms'] = (time.perf_counter() - execute_start) * 1000
                columns = [d[0] for d in cur.description] if cur.description else []
                rows = cur.fetchall() if cur.description else []
                event['execute_fetch_ms'] = (time.perf_counter() - execute_start) * 1000
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
        stream.write(json.dumps(event, ensure_ascii=False, default=str) + '\n')
    print(json.dumps(output, ensure_ascii=False))

if __name__ == '__main__':
    main()
