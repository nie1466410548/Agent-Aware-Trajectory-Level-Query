"""WAL connections for one task; writer-owned tables are visible after commit."""
import sqlite3
import time
from pathlib import Path
from .backend import TaskBackend, quote


class WriterConnection:
    def __init__(self, connection, stop):
        self.connection, self.stop = connection, stop
        self.commits = {}

    def __getattr__(self, key):
        return getattr(self.connection, key)

    def set_progress_handler(self, callback, n):
        if callback is None:
            self.connection.set_progress_handler(None, 0)
        else:
            self.connection.set_progress_handler(lambda: int(self.stop.is_set()) or callback(), n)

    def execute(self, sql, *args):
        ddl = sql.replace('CREATE TEMP TABLE ', 'CREATE TABLE ', 1) if sql.startswith('CREATE TEMP TABLE ') else sql
        if ddl.startswith(('CREATE INDEX ', 'CREATE TABLE ')):
            start=time.monotonic_ns()
            cur=self.connection.execute(ddl,*args)
            self.commits[sql]={'commit_return_ns':time.monotonic_ns(),'ddl_started_ns':start,'actual_ddl':ddl}
            return cur
        return self.connection.execute(sql,*args)


class AsyncBackend(TaskBackend):
    materialization_schema = 'main'
    def __init__(self, database, query_seconds=120, stop=None):
        self.database=Path(database);self.query_seconds=query_seconds
        self.db=sqlite3.connect(database,cached_statements=0,isolation_level=None,timeout=5)
        if self.db.execute('PRAGMA journal_mode').fetchone()[0].lower()!='wal':
            assert self.db.execute('PRAGMA journal_mode=WAL').fetchone()[0].lower()=='wal'
        for pragma in ('synchronous=FULL','temp_store=FILE','cache_size=-8192','automatic_index=ON','foreign_keys=ON'):
            self.db.execute('PRAGMA '+pragma)
        self.catalog={t:[r[1] for r in self.db.execute('PRAGMA table_info('+quote(t)+')')]
                      for (t,) in self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'fad_%'").fetchall()}
        self.base_pages=self.db.execute('PRAGMA main.page_count').fetchone()[0]
        self.page_size=self.db.execute('PRAGMA page_size').fetchone()[0]
        self.originally_unindexed={t for t in self.catalog if not any(not r[1].startswith('fad_i_') for r in self.db.execute('PRAGMA index_list('+quote(t)+')'))}
        if stop is not None:self.db=WriterConnection(self.db,stop)
        self.guard()

    def begin_snapshot(self):
        start=time.monotonic_ns()
        with self.trusted() as db:
            db.execute('BEGIN')
            entries=db.execute('SELECT type,name FROM sqlite_master').fetchall()
            self.snapshot_indexes=[name for kind,name in entries if kind=='index']
        return start,time.monotonic_ns()

    def end_snapshot(self):
        with self.trusted() as db:db.execute('COMMIT')
