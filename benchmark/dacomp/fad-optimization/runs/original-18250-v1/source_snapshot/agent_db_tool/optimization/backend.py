"""One connection per task, with a read-only query boundary and trusted DDL."""
import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

from agent_db_tool.sqlite_adapter import encode


def quote(name):
    return '"' + name.replace('"', '""') + '"'


class TaskBackend:
    def __init__(self, database, query_seconds=120):
        self.database = Path(database)
        self.db = sqlite3.connect(database, cached_statements=0, isolation_level=None)
        self.query_seconds = query_seconds
        for pragma in ('journal_mode=DELETE', 'synchronous=FULL', 'temp_store=FILE',
                       'cache_size=-8192', 'automatic_index=ON', 'foreign_keys=ON'):
            self.db.execute('PRAGMA ' + pragma)
        self.catalog = {
            t: [r[1] for r in self.db.execute('PRAGMA table_info(' + quote(t) + ')')]
            for (t,) in self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()
        }
        self.base_pages = self.db.execute('PRAGMA main.page_count').fetchone()[0]
        self.page_size = self.db.execute('PRAGMA page_size').fetchone()[0]
        self.guard()

    def guard(self):
        self.db.execute('PRAGMA query_only=ON')
        allowed = {sqlite3.SQLITE_SELECT, sqlite3.SQLITE_READ,
                   sqlite3.SQLITE_FUNCTION, sqlite3.SQLITE_RECURSIVE}
        def auth(action, a, b, *_):
            if action not in allowed:
                return sqlite3.SQLITE_DENY
            if action == sqlite3.SQLITE_FUNCTION and (b or '').lower() in (
                    'load_extension', 'readfile', 'writefile'):
                return sqlite3.SQLITE_DENY
            return sqlite3.SQLITE_OK
        self.db.set_authorizer(auth)

    @contextmanager
    def trusted(self):
        self.db.set_authorizer(None)
        self.db.execute('PRAGMA query_only=OFF')
        try:
            yield self.db
        finally:
            self.db.set_progress_handler(None, 0)
            self.guard()

    def prewarm(self):
        # Read every base column/row using this same documented procedure in all arms.
        for table in self.catalog:
            for _ in self.db.execute('SELECT * FROM ' + quote(table)):
                pass

    def space(self):
        with self.trusted() as db:
            main = db.execute('PRAGMA main.page_count').fetchone()[0]
            temp = db.execute('PRAGMA temp.page_count').fetchone()[0]
        return max(0, main - self.base_pages) * self.page_size + temp * self.page_size

    def execute(self, sql, archive):
        start = time.perf_counter()
        self.db.set_progress_handler(lambda: int(time.perf_counter() - start > self.query_seconds), 1000)
        columns, count, error = [], 0, None
        try:
            cur = self.db.execute(sql)
            columns = [x[0] for x in cur.description] if cur.description else []
            with Path(archive).open('w') as out:
                for row in cur:
                    if time.perf_counter() - start > self.query_seconds:
                        raise TimeoutError('query timeout while consuming results')
                    out.write(json.dumps(row, ensure_ascii=False, default=encode) + '\n')
                    count += 1
        except (sqlite3.Error, TimeoutError) as exc:
            error = f'{type(exc).__name__}: {exc}'
        finally:
            self.db.set_progress_handler(None, 0)
        return {'status': 'error' if error else 'ok', 'error': error,
                'columns': columns, 'row_count': count,
                'query_seconds': time.perf_counter() - start}

    def explain(self, sql):
        try:
            return [list(r) for r in self.db.execute('EXPLAIN QUERY PLAN ' + sql)]
        except sqlite3.Error as exc:
            return [['error', str(exc)]]

    def close(self):
        self.db.close()
