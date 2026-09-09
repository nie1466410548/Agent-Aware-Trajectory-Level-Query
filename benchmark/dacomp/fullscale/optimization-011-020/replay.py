"""Execute saved SQLite plans and compare outputs to the archived trajectory."""
import argparse
import json
import sqlite3
from pathlib import Path

from implement import HERE, build_plan, compare, parse, run_query, sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--task', required=True, type=int, choices=range(11, 21))
    parser.add_argument('--candidate', help='Replay the approved subset of one candidate, e.g. C3 or M2')
    parser.add_argument('--database', type=Path, help='Same snapshot at another local path; hash must match')
    args = parser.parse_args()
    task = f'dacomp-{args.task:03}'
    manifest = json.loads((HERE / task / 'manifest.json').read_text())
    path = args.database or Path(manifest['database'])
    if sha(path) != manifest['database_sha256']:
        parser.error('Database differs from the validated snapshot; revalidate before execution')
    plans = {p['id']: p for p in manifest['candidates']}
    qs = manifest['queries']
    if args.candidate:
        if args.candidate not in plans or len(plans[args.candidate].get('safe', [])) < 2:
            parser.error('Candidate has fewer than two approved queries or does not exist')
        selected = [args.candidate]
        qs = {sid: qs[sid] for sid in plans[args.candidate]['safe']}
        assignment = {sid: args.candidate for sid in qs}
    else:
        selected = manifest['combined']['selected']
        assignment = manifest['combined']['assignment']
    db = sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True)
    db.execute('PRAGMA temp_store=MEMORY')
    db.execute('BEGIN')
    built = set()
    all_ok = True
    total_ms = 0
    try:
        for sid, q in qs.items():
            cid = assignment.get(sid)
            dependencies = ([cid] if cid else []) if args.candidate else manifest['combined']['dependencies'][sid]
            for required in dependencies:
                if required not in built:
                    total_ms += build_plan(db, plans[required])
                    built.add(required)
            sql = (plans[cid]['rewrites'][sid] if cid else q['sql']) if args.candidate else manifest['combined']['queries'][sid]
            cols, rows, ms = run_query(db, sql, q.get('parameters'))
            total_ms += ms
            archive = Path(manifest['source_run']) / q['result_file']
            expected = [tuple(json.loads(line)) for line in archive.read_text().splitlines()]
            result = compare(expected, rows, bool(parse(q['sql']).args.get('order')))
            ok = result['ok'] and cols == q['columns']
            all_ok &= ok
            print(f'{task} {sid:4} {cid or "original":8} rows={len(rows):6} '
                  f'ms={ms:9.3f} {"PASS" if ok else "FAIL"}')
        for cid in selected:
            if cid in built:
                db.execute('DROP TABLE ' + plans[cid]['table'])
        db.commit()
    finally:
        db.close()
    unchanged = sha(path) == manifest['database_sha256']
    print(f'queries={len(qs)} verified={all_ok} db_unchanged={unchanged} '
          f'build_and_fetch_ms={total_ms:.3f}')
    if not all_ok or not unchanged:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
