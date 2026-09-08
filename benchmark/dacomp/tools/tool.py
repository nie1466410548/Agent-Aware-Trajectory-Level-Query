"""Logged SQLite/Python tools for a single DAComp episode."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
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
    query = sub.add_parser('query-db')
    group = query.add_mutually_exclusive_group(required=True)
    group.add_argument('--sql')
    group.add_argument('--sql-file', type=Path)
    sub.add_parser('list-db')
    for name in ['python', 'answer']:
        sub.add_parser(name).add_argument('--file', type=Path, required=True)
    args = parser.parse_args()
    run = Path(os.environ['DACOMP_RUN_DIR']).resolve()
    if not (run.is_relative_to(ROOT / 'runs') or run.is_relative_to(ROOT / 'smoke')):
        raise ValueError('Invalid episode directory')
    meta = json.loads((run / 'task_meta.json').read_text())
    if meta['task_id'] != os.environ['DACOMP_TASK_ID']:
        raise ValueError('Task identity mismatch')
    task = meta['task_id']
    database = ROOT / 'upstream' / task / f'{task}.sqlite'
    call = uuid.uuid4().hex
    results = run / 'results'
    results.mkdir(exist_ok=True)
    event = {'task_id': task, 'run_id': meta['run_id'], 'call_id': call,
             'tool': args.tool, 'start_time': time.time(),
             'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    start = time.perf_counter()
    try:
        if args.tool in ['query-db', 'list-db']:
            sql = (args.sql_file.read_text() if args.sql_file else args.sql) if args.tool == 'query-db' else "SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name"
            event.update(sql=sql, database=task, dialect='sqlite')
            # Reserve an attempt atomically; rejected writes/errors count as attempts.
            if args.tool == 'query-db':
                with (run / 'query-count.txt').open('a+') as count:
                    fcntl.flock(count, fcntl.LOCK_EX)
                    count.seek(0)
                    attempts = len(count.readlines())
                    if attempts >= meta['query_attempt_limit']:
                        event['limit_reached'] = True
                        raise RuntimeError('Query budget reached; submit your supported findings')
                    count.write(call + '\n')
                    count.flush()
            (results / f'{call}.sql').write_text(sql)
            with sqlite3.connect(database.resolve().as_uri() + '?mode=ro', uri=True) as db:
                db.execute('PRAGMA query_only=ON')
                # Block attaching unlogged databases and changing any database state.
                denied = {sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH}
                db.set_authorizer(lambda action, *unused: sqlite3.SQLITE_DENY if action in denied else sqlite3.SQLITE_OK)
                query_start = time.perf_counter()
                db.set_progress_handler(lambda: int(time.perf_counter() - query_start > 120), 10000)
                cur = db.execute(sql)  # exactly one statement per logged call
                event['execute_return_ms'] = (time.perf_counter() - query_start) * 1000
                columns = [d[0] for d in cur.description] if cur.description else []
                rows = cur.fetchall()
                event['execute_fetch_ms'] = (time.perf_counter() - query_start) * 1000
                event.update(columns=columns, row_count=len(rows))
                # Preserve duplicate column names in a parallel raw representation.
                raw_rows = {'columns': columns, 'rows': rows}
                (results / f'{call}-rows.json').write_text(json.dumps(raw_rows, ensure_ascii=False, default=str))
                data = [dict(zip(columns, row)) for row in rows]
                if len(set(columns)) != len(columns):
                    event['duplicate_columns'] = True
        elif args.tool == 'python':
            event['code'] = args.file.read_text()
            code_path = results / f'{call}.py'
            code_path.write_text(event['code'])
            try:
                proc = subprocess.run([sys.executable, str(code_path)], cwd=run,
                    env={**os.environ, 'MPLBACKEND': 'Agg'}, capture_output=True, text=True, timeout=180)
                data = {'stdout': proc.stdout, 'stderr': proc.stderr, 'returncode': proc.returncode}
                event['success'] = proc.returncode == 0
            except subprocess.TimeoutExpired as exc:
                data = {'stdout': str(exc.stdout or ''), 'stderr': str(exc.stderr or ''), 'timed_out': True}
                event['success'] = False
        else:
            answer = args.file.read_text()
            if not answer.strip():
                raise ValueError('Empty report')
            (run / f'{task}.md').write_text(answer)
            data = {'submitted': True, 'report_file': str(run / f'{task}.md')}
        event.setdefault('success', True)
    except Exception as exc:
        event.update(success=False, error=f'{type(exc).__name__}: {exc}')
        data = {'error': event['error']}
    raw = json.dumps(data, ensure_ascii=False, default=str)
    result_file = results / f'{call}.json'
    result_file.write_text(raw)
    event.update(result_file=str(result_file), result_sha256=hashlib.sha256(raw.encode()).hexdigest(),
                 end_time=time.time(), duration_ms=(time.perf_counter()-start)*1000)
    with (run / 'tool_calls.jsonl').open('a') as log:
        fcntl.flock(log, fcntl.LOCK_EX)
        log.write(json.dumps(event, ensure_ascii=False) + '\n')
        log.flush()
    print(json.dumps({'call_id': call, 'success': event['success'], 'result_file': str(result_file),
                      'row_count': event.get('row_count'), 'preview': raw[:10000], 'truncated': len(raw)>10000}, ensure_ascii=False))


if __name__ == '__main__':
    main()
