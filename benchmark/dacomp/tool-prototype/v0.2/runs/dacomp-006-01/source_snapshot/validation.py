"""Shared schema and layered validation. Hints never become executable SQL."""
import copy
import json
import math
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).parent


def schema(max_candidates=8, hints=True, version='0.1'):
    if version not in ('0.1', '0.2'):
        raise ValueError('Unsupported schema version')
    filename = 'schema-v0.2.json' if version == '0.2' else 'schema.json'
    result = json.loads((ROOT / filename).read_text())
    result['$defs']['futureAccess']['properties']['candidates']['maxItems'] = max_candidates
    if not hints:
        result['required'] = ['sql']
        result['properties'].pop('future_access')
        result.pop('$defs')
    return result


def execution_errors(args, hints=True):
    if not isinstance(args, dict):
        return [{'path': '', 'message': 'Expected an object'}]
    errors = []
    allowed = {'sql', 'future_access'} if hints else {'sql'}
    if set(args) - allowed:
        errors.append({'path': '', 'message': 'Unknown execution fields'})
    if not isinstance(args.get('sql'), str) or not args['sql'].strip():
        errors.append({'path': 'sql', 'message': 'SQL must be a nonempty string'})
    return errors


def validate_hint(value, max_candidates=8, max_bytes=16384):
    """Return a snapshot (or None) and errors; discard the entire invalid hint."""
    try:
        raw = json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')
    except (ValueError, TypeError, UnicodeError):
        return None, [{'path': 'future_access', 'message': 'Not a finite JSON value'}]
    if len(raw) > max_bytes:
        return None, [{'path': 'future_access', 'message': 'Hint byte limit exceeded'}]
    validator = Draft202012Validator(schema(max_candidates))
    errors = [
        {'path': '.'.join(map(str, e.absolute_path)), 'message': e.message}
        for e in validator.iter_errors({'sql': 'SELECT 1', 'future_access': value})
    ]
    if errors:
        return None, errors
    for index, candidate in enumerate(value['candidates']):
        prefix = f'future_access.candidates.{index}'
        for j, item in enumerate(candidate.get('filters', [])):
            op, val = item['op'], item['value']
            scalar = lambda x: isinstance(x, (str, bool, int, float)) and not (isinstance(x, float) and not math.isfinite(x))
            if op in ('is_null', 'is_not_null'):
                valid = val is None
            elif op in ('in', 'between'):
                valid = isinstance(val, list) and bool(val) and all(scalar(x) for x in val)
                if op == 'between':
                    valid = valid and len(val) == 2
            else:
                valid = scalar(val)
            if not valid:
                errors.append({'path': f'{prefix}.filters.{j}', 'message': 'Value incompatible with operator'})
        for j, item in enumerate(candidate.get('aggregations', [])):
            if item['column'] == '*' and item['function'] != 'count':
                errors.append({'path': f'{prefix}.aggregations.{j}', 'message': '* only supported for count'})
    return (None if errors else copy.deepcopy(value)), errors


def catalog_check(hint, catalog):
    """Exact names, no splitting on dots/spaces or SQL parsing of hint text."""
    if hint is None:
        return {'status': 'not_applicable', 'unverified': []}
    unresolved = []
    for i, candidate in enumerate(hint['candidates']):
        tables = candidate['tables']
        for table in tables:
            if table not in catalog:
                unresolved.append({'candidate': i, 'object': table})
        allowed = {f'{table}.{column}' for table in tables for column in catalog.get(table, [])}
        refs = candidate.get('columns', []) + candidate.get('group_by', [])
        refs += [f['column'] for f in candidate.get('filters', [])]
        refs += [j[k] for j in candidate.get('joins', []) for k in ('left_column', 'right_column')]
        refs += [a['column'] for a in candidate.get('aggregations', []) if a['column'] != '*']
        for ref in refs:
            if ref not in allowed:
                unresolved.append({'candidate': i, 'object': ref})
    return {'status': 'unverified' if unresolved else 'verified', 'unverified': unresolved}
