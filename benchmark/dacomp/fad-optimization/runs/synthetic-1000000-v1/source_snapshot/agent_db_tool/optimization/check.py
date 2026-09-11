"""Offline full-result comparison. Never imported by the online controller."""
import json
import math
from pathlib import Path
import sqlglot


def read_records(directory):
    return [json.loads(l) for l in (Path(directory) / 'events.jsonl').read_text().splitlines()]


def compare_results(left, right, columns_left, columns_right, ordered, absolute=1e-7, relative=1e-9):
    if columns_left != columns_right:
        return {'equal': False, 'reason': 'column names/order differ'}
    if len(left) != len(right):
        return {'equal': False, 'reason': 'row count differs'}
    max_abs = 0.0
    def eq_row(a, b):
        nonlocal max_abs
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if isinstance(x, float) or isinstance(y, float):
                if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                    return False
                if not math.isclose(x, y, abs_tol=absolute, rel_tol=relative):
                    return False
                max_abs = max(max_abs, abs(x - y))
            elif type(x) is not type(y) or x != y:
                return False
        return True
    if ordered:
        ok = all(eq_row(a, b) for a, b in zip(left, right))
    else:
        # Preserve multiplicity; deterministic bipartite matching of tolerant rows.
        edges = [[j for j, b in enumerate(right) if eq_row(a, b)] for a in left]
        assigned = {}
        def augment(i, seen):
            for j in edges[i]:
                if j not in seen:
                    seen.add(j)
                    if j not in assigned or augment(assigned[j], seen):
                        assigned[j] = i
                        return True
            return False
        ok = all(augment(i, set()) for i in range(len(left)))
    return {'equal': ok, 'reason': None if ok else 'row values/order differ', 'max_absolute_difference': max_abs}


def compare_runs(baseline, optimized, config):
    left, right = read_records(baseline), read_records(optimized)
    if [r['step'] for r in left] != [r['step'] for r in right]:
        raise ValueError('trajectory steps differ')
    checks = []
    for a, b in zip(left, right):
        step = a['step']
        if a['sql'] != b['sql']:
            raise ValueError('SQL trajectory input changed')
        if a['raw_fad'] is not None or a['fad'] is not None or a['actions']:
            raise ValueError('baseline must not receive or process FAD')
        if any(a[k] != 0 for k in ('receive_seconds', 'rewrite_seconds', 'decision_including_build_seconds')):
            raise ValueError('baseline performed FAD/optimization work')
        temporal = all(o in b['available_before_query'] for o in b['materializations_used'])
        if a['status'] != 'ok' or b['status'] != 'ok':
            result = {'equal': a['status'] == b['status'] and a['error'] == b['error'],
                      'reason': a['error'], 'max_absolute_difference': 0}
        else:
            rows = lambda p: [json.loads(l) for l in (Path(p) / 'results' / f'Q{step}.jsonl').read_text().splitlines()]
            tree = sqlglot.parse_one(a['sql'], read='sqlite')
            result = compare_results(rows(baseline), rows(optimized), a['columns'], b['columns'],
                                     bool(tree.args.get('order')), config['absolute_tolerance'], config['relative_tolerance'])
        checks.append({'step': step, 'temporal_ok': temporal, **result})
    return {'all_equal': all(r['equal'] and r['temporal_ok'] for r in checks), 'queries': checks}
