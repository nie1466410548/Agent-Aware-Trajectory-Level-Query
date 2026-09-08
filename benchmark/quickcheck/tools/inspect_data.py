"""Read-only database inspection, independent of benchmark trajectory logs."""
import argparse
import json
from pathlib import Path
import sqlite3
import yaml

ROOT = Path(__file__).resolve().parents[1]

def quote(name):
    return '"' + name.replace('"', '""') + '"'

def connect(dataset, database):
    root = ROOT / 'upstream' / ('query_' + dataset)
    cfg = yaml.safe_load((root / 'db_config.yaml').read_text())['db_clients'][database]
    if cfg['db_type'] == 'postgres':
        import psycopg2
        conn = psycopg2.connect(host='127.0.0.1', port=55439, user='dab_reader',
            dbname=cfg['db_name'], options='-c default_transaction_read_only=on -c statement_timeout=60000')
    elif cfg['db_type'] == 'duckdb':
        import duckdb
        conn = duckdb.connect(str(root / cfg['db_path']), read_only=True,
            config={'enable_external_access': 'false', 'threads': 2})
    else:
        conn = sqlite3.connect((root / cfg['db_path']).as_uri() + '?mode=ro', uri=True)
        conn.execute('PRAGMA query_only=ON')
    return conn, cfg, root

def inspect(dataset, database, sql=None):
    conn, cfg, root = connect(dataset, database)
    try:
        cur = conn.cursor()
        if sql:
            cur.execute(sql)
            columns = [c[0] for c in cur.description] if cur.description else []
            return {'columns': columns, 'rows': cur.fetchall()}
        if cfg['db_type'] == 'sqlite':
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
            tables = [(None, x[0]) for x in cur.fetchall()]
        else:
            cur.execute("SELECT table_schema, table_name FROM information_schema.tables WHERE table_type='BASE TABLE' AND table_schema NOT IN ('information_schema','pg_catalog') ORDER BY 1,2")
            tables = cur.fetchall()
        info = []
        for schema, name in tables:
            qualified = (quote(schema) + '.' if schema else '') + quote(name)
            cur.execute('SELECT COUNT(*) FROM ' + qualified)
            count = cur.fetchone()[0]
            cur.execute('SELECT * FROM ' + qualified + ' LIMIT 0')
            info.append({'table': qualified, 'rows': count, 'columns': [c[0] for c in cur.description]})
        if cfg['db_type'] == 'postgres':
            cur.execute('SELECT pg_database_size(current_database())')
            size = cur.fetchone()[0]
            location = '127.0.0.1:55439/' + cfg['db_name']
            size_kind = 'PostgreSQL database bytes (includes system catalogs)'
        else:
            path = root / cfg['db_path']
            size = path.stat().st_size
            location = str(path)
            size_kind = 'database file bytes'
        return {'dataset': dataset, 'database': database, 'engine': cfg['db_type'],
            'location': location, 'bytes': size, 'size_kind': size_kind, 'tables': info}
    finally:
        conn.close()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('dataset', nargs='?', choices=['bookreview', 'crmarenapro', 'stockindex'])
    p.add_argument('database', nargs='?')
    p.add_argument('--sql', help='Read-only SQL; include LIMIT for preview')
    a = p.parse_args()
    if a.sql and not (a.dataset and a.database):
        p.error('--sql requires dataset and database')
    rows = []
    for dataset in ([a.dataset] if a.dataset else ['bookreview', 'crmarenapro', 'stockindex']):
        config = yaml.safe_load((ROOT / 'upstream' / ('query_' + dataset) / 'db_config.yaml').read_text())['db_clients']
        for db in ([a.database] if a.database else config):
            rows.append(inspect(dataset, db, a.sql))
    print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))

if __name__ == '__main__':
    main()
