"""Untimed, independent replay to distinguish reused SQLite pages from file growth."""
import json
import shutil
import sqlite3
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATABASE = ROOT.parent / 'upstream/dacomp-006/dacomp-006.sqlite'


def main():
    results = {}
    for mode in ('index', 'materialization', 'combined'):
        records = [json.loads(l) for l in (ROOT / 'runs/validation-02-sql-only' / mode / 'events.jsonl').read_text().splitlines()]
        with tempfile.TemporaryDirectory(prefix='fad-space-') as scratch:
            database = Path(scratch) / 'task.sqlite'
            shutil.copyfile(DATABASE, database)
            db = sqlite3.connect(database, isolation_level=None)
            db.execute('PRAGMA temp_store=FILE')
            def pages(schema):
                size = db.execute(f'PRAGMA {schema}.page_size').fetchone()[0]
                count = db.execute(f'PRAGMA {schema}.page_count').fetchone()[0]
                free = db.execute(f'PRAGMA {schema}.freelist_count').fetchone()[0]
                return {'file_bytes': size * count, 'used_bytes': size * (count - free), 'free_bytes': size * free}
            initial = pages('main')
            objects = []
            for r in records:
                try:
                    db.execute(r['executed_sql']).fetchall()
                except sqlite3.Error:
                    pass  # Original Q10; this diagnostic is not correctness evidence.
                for a in r['actions']:
                    if a['status'] != 'built':
                        continue
                    schema = 'main' if a['kind'] == 'index' else 'temp'
                    before = pages(schema)
                    db.execute(a['ddl'])
                    after = pages(schema)
                    objects.append({'name': a['name'], 'created_after': r['step'], 'kind': a['kind'],
                                    'used_page_growth_bytes': after['used_bytes'] - before['used_bytes'],
                                    'file_growth_bytes': after['file_bytes'] - before['file_bytes']})
            results[mode] = {'initial_main': initial, 'objects': objects, 'final_main': pages('main'), 'final_temp': pages('temp')}
            db.close()
    (ROOT / 'reports/space-diagnostic.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
