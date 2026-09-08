import json
from pathlib import Path
import sqlite3
import subprocess

ROOT = Path(__file__).resolve().parents[1]
command = ['docker', 'exec', '-i', 'dab-bookreview-pg', 'psql', '-X', '-v', 'ON_ERROR_STOP=1', '-U', 'postgres', '-d', 'bookreview_db']
sql = (ROOT / 'upstream/query_dataset/books_info.sql').read_text()
sql += """
CREATE ROLE dab_reader LOGIN;
GRANT CONNECT ON DATABASE bookreview_db TO dab_reader;
GRANT USAGE ON SCHEMA public TO dab_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO dab_reader;
ALTER ROLE dab_reader SET default_transaction_read_only = on;
ANALYZE public.books_info;
SELECT count(*) AS books FROM public.books_info;
"""
proc = subprocess.run(command, input=sql, text=True, capture_output=True)
(ROOT / 'reports/import.log').write_text(proc.stdout + proc.stderr)
if proc.returncode:
    raise RuntimeError('Import failed; inspect reports/import.log')
conn = sqlite3.connect((ROOT / 'upstream/query_dataset/review_query.db').as_uri()+'?mode=ro', uri=True)
print('SQLite integrity:', conn.execute('PRAGMA quick_check').fetchone()[0])
print('Reviews:',conn.execute('SELECT count(*) FROM review').fetchone()[0])
print('PostgreSQL import completed:', proc.stdout.splitlines()[-4:])
