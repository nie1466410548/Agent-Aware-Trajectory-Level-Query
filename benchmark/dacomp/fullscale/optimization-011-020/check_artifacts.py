"""Execute exported trajectory.sql files, not just the manifest representation."""
import json
import re
import sqlite3
from pathlib import Path

from implement import HERE, compare, dump, parse, sha


def statements(text):
    pending = ''
    for line in text.splitlines(keepends=True):
        pending += line
        if sqlite3.complete_statement(pending):
            yield pending
            pending = ''
    if pending.strip():
        raise ValueError('Incomplete SQL at end of file')


def main():
    checks = []
    for i in range(11, 21):
        task = f'dacomp-{i:03}'
        folder = HERE / task
        manifest = json.loads((folder / 'manifest.json').read_text())
        path = Path(manifest['database'])
        before = sha(path)
        assert before == manifest['database_sha256']
        db = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
        count = 0
        for sql in statements((folder / 'trajectory.sql').read_text()):
            cursor = db.execute(sql)
            if cursor.description is None:
                continue
            match = re.search(r'^-- (S\d+)\s*$', sql, flags=re.M)
            assert match, sql[:120]
            sid = match[1]
            q = manifest['queries'][sid]
            expected = [tuple(json.loads(line)) for line in
                        (Path(manifest['source_run']) / q['result_file']).read_text().splitlines()]
            result = compare(expected, cursor.fetchall(), bool(parse(q['sql']).args.get('order')))
            assert result['ok'], (task, sid, result)
            assert [d[0] for d in cursor.description] == q['columns'], (task, sid, 'columns')
            count += 1
        left = db.execute("SELECT name FROM sqlite_temp_master WHERE type='table'").fetchall()
        assert not left, left
        db.close()
        assert sha(path) == before
        assert count == manifest['successful_data_sql']
        # Check local documentation links before shipping.
        for doc in (folder / 'README.md',):
            for link in re.findall(r'\]\(([^)]+)\)', doc.read_text()):
                if not link.startswith(('#', 'http')):
                    assert (doc.parent / link.split('#')[0]).exists(), (doc, link)
        checks.append({'task': task, 'exported_sql_queries_verified': count,
                       'temp_tables_after_cleanup': 0, 'database_unchanged': True})
        print(task, count, 'exported SQL PASS', flush=True)
    # Document and test the functional dependency used to merge customer CTEs.
    a = json.loads((HERE / 'dacomp-018' / 'manifest.json').read_text())
    db = sqlite3.connect(Path(a['database']).as_uri() + '?mode=ro', uri=True)
    fd = []
    for name in ['gender', 'Customer Segment', 'age', 'Education Level', 'Marital Status', 'Region', 'Country', 'City']:
        col = '"' + name + '"'
        sql = ('SELECT COUNT(*) FROM (SELECT "Customer ID" FROM customer_information GROUP BY "Customer ID" '
               f'HAVING COUNT(DISTINCT {col}) + (COUNT(*)>COUNT({col})) > 1)')
        conflicts = db.execute(sql).fetchone()[0]
        assert conflicts == 0, (name, conflicts)
        fd.append({'column': name, 'conflicting_customer_ids': conflicts, 'sql': sql})
    db.close()
    dump(HERE / 'artifact-checks.json', {'exported_scripts': checks, 'customer_dependency_018': fd,
                                       'source_hashes': {name: sha(HERE / name) for name in
                                                         ['implement.py', 'replay.py', 'report.py', 'check_artifacts.py']}})


if __name__ == '__main__':
    main()
