"""Read-only single-statement SQLite execution with bounded result archives."""
import base64
import json
import sqlite3
import time
from pathlib import Path


def encode(value):
    if isinstance(value, bytes):
        return {'$blob_base64': base64.b64encode(value).decode('ascii')}
    raise TypeError(type(value).__name__)


class SQLiteAdapter:
    def __init__(self, database, timeout=120, preview_rows=12, result_bytes=16*1024*1024):
        self.database = Path(database).resolve(strict=True)
        self.timeout, self.preview_rows, self.result_bytes = timeout, preview_rows, result_bytes

    def connect(self):
        db = sqlite3.connect(self.database.as_uri() + '?mode=ro', uri=True, timeout=min(5, self.timeout))
        db.execute('PRAGMA query_only=ON')
        def auth(action, a, b, *_):
            if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH):
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_FUNCTION and (b or '').lower() in ('load_extension', 'readfile', 'writefile'):
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_PRAGMA:
                if (a or '').lower() not in ('table_info', 'table_xinfo', 'index_info', 'index_list', 'foreign_key_list', 'database_list'):
                    return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        db.set_authorizer(auth)
        return db

    def execute(self, sql, archive):
        start = time.monotonic()
        deadline = start + self.timeout
        rows, columns, count, size = [], [], 0, 0
        begun, complete = False, False
        trace = []
        archive = Path(archive)
        db = None
        try:
            db = self.connect()
            db.set_trace_callback(lambda statement: trace.append(statement))
            db.set_progress_handler(lambda: int(time.monotonic() > deadline), 1000)
            begun = True
            cur = db.execute(sql)
            columns = [item[0] for item in cur.description] if cur.description else []
            with archive.open('w', encoding='utf-8') as out:
                for row in cur:
                    if time.monotonic() > deadline:
                        raise TimeoutError('Query result consumption exceeded deadline')
                    raw = json.dumps(row, ensure_ascii=False, default=encode)
                    size += len((raw + '\n').encode('utf-8'))
                    if size > self.result_bytes:
                        raise OverflowError('Result archive limit exceeded; partial result')
                    out.write(raw + '\n')
                    count += 1
                    # Bound row count AND byte size of the preview.
                    if len(rows) < self.preview_rows and sum(len(json.dumps(r, default=encode)) for r in rows) + len(raw) <= 12000:
                        rows.append(json.loads(raw))
            complete = True
            status, error = 'ok', None
        except (sqlite3.Error, TimeoutError, OverflowError, OSError) as exc:
            status, error = 'db_error', f'{type(exc).__name__}: {exc}'
        finally:
            if db is not None:
                db.close()
        return {
            'status': status, 'sql_executed': begun,
            'result': {'columns': columns, 'rows': rows, 'returned_row_count': len(rows),
                       'row_count': count if complete else None, 'archived_rows': count,
                       'result_complete': complete, 'truncated': not complete or count > len(rows),
                       'result_file': f'results/{archive.name}' if archive.exists() else None},
            'error': error, 'duration_ms': (time.monotonic() - start) * 1000,
            'engine_statements': trace,
        }
