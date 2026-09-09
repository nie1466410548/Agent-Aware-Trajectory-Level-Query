"""Compile and replay task-local SQLite reuse plans. No model/provider calls.

Run with benchmark/dacomp/.venv/bin/python. Source DBs are opened mode=ro;
all materializations live in TEMP on the same connection. No query_only=ON,
which would also prohibit TEMP writes. Original trajectories are never changed.
"""
import argparse
import collections
import hashlib
import json
import math
import re
import sqlite3
import statistics
import time
from pathlib import Path

import sqlglot
from sqlglot import exp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BATCH = 'dsv4flash-db-first-full-01'


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def qi(name):
    return '"' + name.replace('"', '""') + '"'


def parse(sql):
    try:
        return sqlglot.parse_one(sql, read='sqlite')
    except sqlglot.errors.ParseError:
        # SQLite accepts the column named like in SUM(like); sqlglot 30.18
        # interprets it as an operator. Quote only this known column reference
        # for AST inspection; baseline SQL remains byte-for-byte unchanged.
        fixed = re.sub(r'\b(SUM|AVG|MIN|MAX|COUNT)\(\s*like\s*\)',
                       lambda m: m[1] + '("like")', sql, flags=re.I)
        if fixed == sql:
            raise
        return sqlglot.parse_one(fixed, read='sqlite')


def canonical(sql):
    return parse(sql).sql(dialect='sqlite')


def run_query(db, sql, params=()):
    t = time.perf_counter()
    cur = db.execute(sql, params or ())
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    return cols, rows, (time.perf_counter() - t) * 1000


def build_plan(db, plan):
    elapsed = run_query(db, plan['build'])[2]
    for sql in plan.get('indexes', []):
        elapsed += run_query(db, sql)[2]
    return elapsed


def compare(a, b, ordered):
    # Keep the original report's strict unordered-multiset rule. Never silently
    # turn a float mismatch into an accepted exact result.
    if len(a) != len(b):
        return {'ok': False, 'reason': 'row_count', 'original_rows': len(a), 'rewrite_rows': len(b)}
    key = lambda x: json.dumps(x, ensure_ascii=False)
    aa, bb = (a, b) if ordered else (sorted(a, key=key), sorted(b, key=key))
    exact = aa == bb
    tolerant = all(len(x) == len(y) and all(
        u == v or isinstance(u, (float, int)) and isinstance(v, (float, int))
        and math.isclose(u, v, rel_tol=1e-12, abs_tol=1e-9)
        for u, v in zip(x, y)) for x, y in zip(aa, bb))
    result = {'ok': exact or ordered and tolerant, 'exact': exact,
              'comparison': 'ordered_rel1e-12_abs1e-9' if ordered else 'exact_multiset',
              'aligned_numeric_tolerance_only': not exact and tolerant}
    if not result['ok']:
        result['first_difference'] = next(({'original': x, 'rewrite': y}
                                          for x, y in zip(aa, bb) if x != y), None)
    return result


def aliases(sql, names):
    tree = parse(sql)
    if len(tree.selects) != len(names) or any(isinstance(s, exp.Star) for s in tree.selects):
        return sql
    tree.set('expressions', [exp.alias_(s.this.copy() if isinstance(s, exp.Alias) else s.copy(),
                                      name, quoted=True) for s, name in zip(tree.selects, names)])
    return tree.sql(dialect='sqlite', pretty=True)


def extras(task, candidates, qs):
    """018: merge semantically shared customer CTEs despite projection order."""
    if task != 'dacomp-018':
        return []
    byid = {c['candidate_id']: c for c in candidates}
    out = []
    for cid, sources, description in [
        ('M1', ['C1', 'C4', 'C6'], '客户去重一次，按需投影属性；取代三种投影不同的客户 CTE'),
        ('M2', ['C2', 'C3', 'C5'], 'Fashion 订单按客户汇总一次；统一列顺序不同或只取 profit 的 CTE'),
    ]:
        first = byid[sources[0]]
        bodies = {canonical(byid[k]['build_sql']): byid[k] for k in sources}
        rewrites = {}
        for sid, q in qs.items():
            tree = parse(q['sql'])
            changed = False
            for cte in tree.find_all(exp.CTE):
                body = cte.this
                if body.sql(dialect='sqlite') in bodies:
                    names = [s.alias_or_name for s in body.selects]
                    cte.set('this', parse('SELECT ' + ', '.join(qi(n) for n in names) +
                                         ' FROM temp.reuse_candidate'))
                    changed = True
            if changed:
                rewrites[sid] = tree.sql(dialect='sqlite')
        out.append({'candidate_id': cid, 'type': 'merged common subexpression',
                    'existing_result': False, 'build_sql': first['build_sql'],
                    'covered': list(rewrites), 'rewrites': rewrites,
                    'status': 'new', 'reason': description, 'sources': sources})
    return out


def compile_candidate(task, c, qs, out):
    cid = c['candidate_id']
    name = f'reuse_{task[-3:]}_{cid.lower()}'
    table = 'temp.' + qi(name)
    rewrites = {}
    if c['existing_result']:
        producer = qs[c['covered'][0]]
        # Number the source cursor inside SQLite. Explicit cache read order
        # preserves the materialized producer order on this pinned engine/data.
        # ORDER/LIMIT/ties remain validated against every archived consumer.
        names = producer['columns']
        if len({n.lower() for n in names}) != len(names):
            raise ValueError('Duplicate result labels need an explicit positional cache schema')
        ordered = bool(parse(producer['sql']).args.get('order'))
        build = producer['sql'].strip().rstrip(';')
        if ordered:
            build = ('SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (\n' +
                     build + '\n) AS src')
        read = 'SELECT ' + ', '.join(qi(n) for n in names) + ' FROM ' + table
        if ordered:
            read += ' ORDER BY "__reuse_ordinal"'
        rewrites = {sid: read for sid in c['covered']}
    else:
        build = c['build_sql']
        for sid, sql in c['rewrites'].items():
            # AST alias repair preserves all result labels, including unaliased
            # COUNT(*) / expressions for which the old generator lost names.
            rewrites[sid] = aliases(sql.replace('temp.reuse_candidate', table), qs[sid]['columns'])
    build_statement = 'CREATE TEMP TABLE ' + qi(name) + ' AS\n' + build.strip().rstrip(';')
    indexes = []
    if task == 'dacomp-018' and cid in ('M1', 'M2'):
        indexes = ['CREATE INDEX temp.' + qi(name + '_customer') + ' ON ' + qi(name) + '("Customer ID")']
    d = out / cid
    d.mkdir(parents=True, exist_ok=True)
    (d / 'build.sql').write_text('-- Execute once before ' + c['covered'][0] +
                                '; retain this connection for subsequent reads.\n' + build_statement + ';\n' +
                                ''.join(sql + ';\n' for sql in indexes))
    (d / 'cleanup.sql').write_text('DROP TABLE IF EXISTS ' + table + ';\n')
    for sid, sql in rewrites.items():
        (d / (sid + '.sql')).write_text(sql.rstrip(';') + ';\n')
    return {'id': cid, 'type': c['type'], 'source_status': c['status'],
            'source_candidates': c.get('sources', [cid]), 'description': c.get('reason'),
            'table': table, 'build': build_statement, 'indexes': indexes, 'covered': c['covered'],
            'rewrites': rewrites, 'existing_result': c['existing_result'], 'checks': []}


def validate(db, plan, qs, archive):
    db.execute('DROP TABLE IF EXISTS ' + plan['table'])
    build_ms = build_plan(db, plan)
    plan['build_ms_validation'] = build_ms
    plan['rows'] = db.execute('SELECT COUNT(*) FROM ' + plan['table']).fetchone()[0]
    plan['columns'] = [r[1] for r in db.execute('PRAGMA temp.table_info(' + plan['table'].split('.', 1)[1] + ')')]
    plan['safe'] = []
    for sid, sql in plan['rewrites'].items():
        q = qs[sid]
        acols, arows = archive[sid]
        cols, rows, ms = run_query(db, sql)
        comparison = compare(arows, rows, bool(parse(q['sql']).args.get('order')))
        check = {'sql': sid, 'columns_equal': cols == acols, **comparison, 'replay_ms': ms}
        if cols != acols:
            check.update(expected_columns=acols, actual_columns=cols)
        if comparison['ok'] and cols == acols:
            plan['safe'].append(sid)
        plan['checks'].append(check)
    plan['excluded'] = [sid for sid in plan['covered'] if sid not in plan['safe']]
    plan['status'] = 'verified' if not plan['excluded'] else 'partial' if len(plan['safe']) >= 2 else 'rejected'
    db.execute('DROP TABLE ' + plan['table'])


def measure_candidate(db, p, qs, repeats):
    safe = p['safe']
    if len(safe) < 2:
        return
    samples = []
    for iteration in range(repeats + 1):
        def original():
            return {sid: run_query(db, qs[sid]['sql'], qs[sid].get('parameters'))[2] for sid in safe}
        def rewritten():
            build_ms = build_plan(db, p)
            times = {sid: run_query(db, p['rewrites'][sid])[2] for sid in safe}
            db.execute('DROP TABLE ' + p['table'])
            return build_ms, times
        if iteration % 2:
            build_ms, new = rewritten(); old = original()
        else:
            old = original(); build_ms, new = rewritten()
        if iteration:
            samples.append({'build_ms': build_ms, 'original_ms': sum(old.values()),
                            'rewrite_ms': sum(new.values()), 'original_by_sql': old, 'rewrite_by_sql': new})
    med = lambda key: statistics.median(s[key] for s in samples)
    old = med('original_ms')
    total = statistics.median(s['build_ms'] + s['rewrite_ms'] for s in samples)
    p['performance'] = {'repeats': repeats, 'samples': samples, 'baseline_ms': old,
                        'build_ms': med('build_ms'), 'reads_ms': med('rewrite_ms'),
                        'total_ms': total, 'saved_ms': old - total, 'speedup': old / total,
                        'original_by_sql': {sid: statistics.median(s['original_by_sql'][sid] for s in samples) for sid in safe},
                        'rewrite_by_sql': {sid: statistics.median(s['rewrite_by_sql'][sid] for s in samples) for sid in safe}}


def choose(plans):
    """Conservative greedy selection, no double counting overlapping consumers.

    Exactly one candidate is used per SQL. All selected builds are charged.
    This is an offline plan, not an online prediction or globally optimal search.
    """
    remaining = [p for p in plans if p.get('performance')]
    assigned = {}
    selected = []
    while remaining:
        choices = []
        for p in remaining:
            perf = p['performance']
            free = [sid for sid in p['safe'] if sid not in assigned and
                    perf['original_by_sql'][sid] > perf['rewrite_by_sql'][sid]]
            gross = sum(perf['original_by_sql'][s] - perf['rewrite_by_sql'][s] for s in free)
            gain = gross - perf['build_ms']
            # Avoid automatically adopting sub-millisecond noise as an optimization.
            if len(free) >= 2 and gain > max(1.0, .1 * sum(perf['original_by_sql'][s] for s in free)):
                choices.append((gain, p, free))
        if not choices:
            break
        _, p, free = max(choices, key=lambda x: x[0])
        selected.append(p['id'])
        assigned.update({s: p['id'] for s in free})
        remaining.remove(p)
    return selected, assigned


def combined(db, plans, qs, archive, selected, assigned, out, repeats):
    byid = {p['id']: p for p in plans}
    statements = []
    built = set()
    checks = []
    optimized_queries = {}
    dependencies = {}
    for sid, q in qs.items():
        cid = assigned.get(sid)
        sql = byid[cid]['rewrites'][sid] if cid else q['sql']
        needed = [cid] if cid else []
        # If two selected candidates replace different CTEs in the SAME SQL,
        # apply both changes instead of overwriting the first rewrite. Conflicts
        # on the same CTE keep the primary rewrite. Every composition is replayed.
        original_ctes = {c.alias_or_name: c.this.sql(dialect='sqlite') for c in parse(q['sql']).find_all(exp.CTE)}
        tree = parse(sql)
        changed = False
        for other in selected:
            p = byid[other]
            if other == cid or sid not in p['safe'] or 'subexpression' not in p['type']:
                continue
            replacements = {c.alias_or_name: c.this for c in parse(p['rewrites'][sid]).find_all(exp.CTE)
                            if c.this.sql(dialect='sqlite') != original_ctes.get(c.alias_or_name)}
            for cte in tree.find_all(exp.CTE):
                name = cte.alias_or_name
                if name in replacements and cte.this.sql(dialect='sqlite') == original_ctes.get(name):
                    cte.set('this', replacements[name].copy())
                    changed = True
                    if other not in needed:
                        needed.append(other)
        if changed:
            sql = tree.sql(dialect='sqlite', pretty=True)
        optimized_queries[sid] = sql
        dependencies[sid] = needed
        for required in needed:
            if required not in built:
                statements.append((f'BUILD {required} before {sid}', byid[required]['build']))
                statements.extend((f'BUILD INDEX {required} before {sid}', index) for index in byid[required].get('indexes', []))
                built.add(required)
        statements.append((sid, sql))
    # Replay all successful data queries, including untouched fallbacks.
    for label, sql in statements:
        if label.startswith('BUILD'):
            db.execute(sql)
            continue
        cols, rows, _ = run_query(db, sql, qs[label].get('parameters'))
        acols, arows = archive[label]
        check = compare(arows, rows, bool(parse(qs[label]['sql']).args.get('order')))
        checks.append({'sql': label, 'candidate': assigned.get(label), 'columns_equal': cols == acols, **check})
    for cid in selected:
        db.execute('DROP TABLE ' + byid[cid]['table'])
    good = all(c['ok'] and c['columns_equal'] for c in checks)
    samples = []
    for i in range(repeats + 1):
        def old():
            t = time.perf_counter()
            for q in qs.values():
                run_query(db, q['sql'], q.get('parameters'))
            return (time.perf_counter() - t) * 1000
        def new():
            t = time.perf_counter()
            for label, sql in statements:
                run_query(db, sql, qs[label].get('parameters') if label in qs else ())
            for cid in selected:
                db.execute('DROP TABLE ' + byid[cid]['table'])
            return (time.perf_counter() - t) * 1000
        if i % 2:
            n = new(); o = old()
        else:
            o = old(); n = new()
        if i:
            samples.append({'baseline_ms': o, 'optimized_ms': n})
    (out / 'trajectory.sql').write_text(
        '-- Same task, same SQLite connection, immutable main database.\n'
        '-- Successful data SQL only; original failed attempts are not replayed.\n'
        '-- Offline selection; source queries and metadata remain in manifest.json.\n'
        'PRAGMA temp_store=MEMORY;\nBEGIN;\n\n' +
        '\n\n'.join('-- ' + label + '\n' + sql.strip().rstrip(';') + ';' for label, sql in statements) +
        '\n\n' + '\n'.join('DROP TABLE ' + byid[cid]['table'] + ';' for cid in selected) + '\nCOMMIT;\n')
    baseline = statistics.median(s['baseline_ms'] for s in samples)
    optimized = statistics.median(s['optimized_ms'] for s in samples)
    return {'selected': selected, 'assignment': assigned, 'queries': optimized_queries,
            'dependencies': dependencies, 'correct': good, 'checks': checks,
            'samples': samples, 'baseline_ms': baseline, 'optimized_ms': optimized,
            'speedup': baseline / optimized, 'saved_ms': baseline - optimized}


def process(i, repeats):
    task = f'dacomp-{i:03}'
    out = HERE / task
    out.mkdir(exist_ok=True)
    run = ROOT / 'runs' / BATCH / task / 'attempt-01'
    source = ROOT / 'reports' / BATCH / 'tasks' / (task + '.analysis.json')
    # Freeze analysis input because another session may regenerate reports.
    frozen = out / 'source-analysis.json'
    if not frozen.exists():
        frozen.write_bytes(source.read_bytes())
    analysis = json.loads(frozen.read_text())
    meta = json.loads((run / 'task_meta.json').read_text())
    dbpath = Path(meta['database_path'])
    qs = {q['sql_id']: q for q in map(json.loads, (run / 'sql_events.jsonl').read_text().splitlines())
          if q['category'] in ('data', 'unknown') and q['status'] == 'success'
          and isinstance(parse(q['sql']), exp.Query)}
    qs = dict(sorted(qs.items(), key=lambda x: int(x[0][1:])))
    archive = {sid: (q['columns'], [tuple(json.loads(l)) for l in (run / q['result_file']).read_text().splitlines()])
               for sid, q in qs.items()}
    before = sha(dbpath)
    if before != meta['database_sha256']:
        raise RuntimeError('Database hash differs from recorded snapshot: ' + task)
    db = sqlite3.connect(dbpath.resolve().as_uri() + '?mode=ro', uri=True)
    db.execute('PRAGMA temp_store=MEMORY')
    # A transaction pins the snapshot across builds and consumers.
    db.execute('BEGIN')
    baseline_checks = []
    for sid, q in qs.items():
        cols, rows, _ = run_query(db, q['sql'], q.get('parameters'))
        acols, arows = archive[sid]
        comp = compare(arows, rows, bool(parse(q['sql']).args.get('order')))
        baseline_checks.append({'sql': sid, 'columns_equal': cols == acols, **comp})
    if not all(c['ok'] and c['columns_equal'] for c in baseline_checks):
        dump(out / 'baseline-failure.json', baseline_checks)
        raise RuntimeError('Original SQL no longer reproduces archive: ' + task)
    plans = []
    for c in analysis['candidates'] + extras(task, analysis['candidates'], qs):
        p = compile_candidate(task, c, qs, out)
        try:
            validate(db, p, qs, archive)
            measure_candidate(db, p, qs, repeats)
        except Exception as e:
            p.update(status='error', error=repr(e))
            db.execute('DROP TABLE IF EXISTS ' + p['table'])
        plans.append(p)
        print(task, p['id'], p['status'], len(p.get('safe', [])), '/', len(p['covered']),
              'speedup', round(p.get('performance', {}).get('speedup', 0), 2), flush=True)
        dump(out / p['id'] / 'validation.json', p)
        (out / p['id'] / 'approved.sql').write_text(
            '-- Approved subset only. Other queries must run their original SQL.\n' +
            (p['build'] + ';\n' + ''.join(sql + ';\n' for sql in p['indexes']) + '\n' +
             '\n\n'.join('-- ' + sid + '\n' + p['rewrites'][sid] + ';' for sid in p.get('safe', [])) +
             '\n\nDROP TABLE ' + p['table'] + ';\n' if len(p.get('safe', [])) >= 2 else '-- No executable reuse plan approved.\n'))
    selected, assigned = choose(plans)
    combo = combined(db, plans, qs, archive, selected, assigned, out, repeats)
    db.close()
    after = sha(dbpath)
    result = {'task': task, 'database': str(dbpath), 'database_sha256': before,
              'database_unchanged': before == after, 'sqlite_version': sqlite3.sqlite_version,
              'sqlglot_version': sqlglot.__version__, 'temp_store': 'MEMORY',
              'successful_data_sql': len(qs), 'source_analysis_sha256': sha(frozen),
              'created_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'baseline_checks': baseline_checks, 'candidates': plans, 'combined': combo,
              'source_run': str(run), 'queries': qs}
    dump(out / 'manifest.json', result)
    if not combo['correct'] or before != after:
        raise RuntimeError('Combined plan validation failed: ' + task)
    print(task, 'COMBINED', selected, round(combo['baseline_ms'], 2), round(combo['optimized_ms'], 2), flush=True)
    return result


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--tasks', nargs='+', type=int, default=list(range(11, 21)))
    ap.add_argument('--repeats', type=int, default=5)
    args = ap.parse_args()
    if args.repeats < 3:
        ap.error('Use at least three measured repetitions')
    for task_id in args.tasks:
        process(task_id, args.repeats)
