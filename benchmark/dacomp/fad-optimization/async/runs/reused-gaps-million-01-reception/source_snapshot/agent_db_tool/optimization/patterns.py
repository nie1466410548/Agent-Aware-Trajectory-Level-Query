"""Compile only explicit, catalog-validated FAD operations into SQL patterns."""
import hashlib
import json

from .reception import receive_object
from .backend import quote


def stable(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def digest(value):
    return hashlib.sha256(stable(value).encode()).hexdigest()[:16]


def receive(raw, catalog):
    decoded = isinstance(raw, str)
    if decoded:
        try:
            raw = json.loads(raw)
        except ValueError as exc:
            return None, {'decoded_string': True, 'errors': [str(exc)]}
    snapshot, audit = receive_object(raw, catalog)
    return snapshot, {'decoded_string': decoded, **audit}


def column_sql(ref, table):
    if ref == '*':
        return '*'
    if not ref.startswith(table + '.'):
        raise ValueError('foreign column')
    return quote(ref[len(table) + 1:])


def group_sql(item, table):
    col = column_sql(item['column'], table)
    if item['type'] == 'column':
        return col
    fmt = {'year': '%Y', 'month': '%Y-%m', 'day': '%Y-%m-%d'}[item['unit']]
    return "strftime('" + fmt + "', " + col + ')'


def literal(value):
    if value is None:
        return 'NULL'
    if isinstance(value, bool):
        return '1' if value else '0'
    if isinstance(value, (int, float)):
        return str(value)
    return "'" + value.replace("'", "''") + "'"


def filter_sql(node, table):
    if node['type'] in ('and', 'or'):
        return '(' + (' ' + node['type'].upper() + ' ').join(filter_sql(n, table) for n in node['items']) + ')'
    if node['value']['status'] != 'known':
        raise ValueError('unknown filter value')
    col, op, val = column_sql(node['column'], table), node['op'], node['value']['literal']
    if op in ('is_null', 'is_not_null'):
        return col + (' IS NULL' if op == 'is_null' else ' IS NOT NULL')
    if op == 'in':
        return col + ' IN (' + ', '.join(literal(v) for v in val) + ')'
    if op == 'between':
        return col + ' BETWEEN ' + literal(val[0]) + ' AND ' + literal(val[1])
    return col + ' ' + {'eq': '=', 'ne': '!=', 'lt': '<', 'le': '<=', 'gt': '>', 'ge': '>=', 'like': 'LIKE'}[op] + ' ' + literal(val)


def material_pattern(candidate):
    if len(candidate['tables']) != 1 or candidate['joins']['status'] != 'none':
        raise ValueError('requires one table without joins')
    if any(candidate[k]['status'] not in ('known', 'none') for k in ('filters', 'group_by', 'aggregations')):
        raise ValueError('incomplete filter/group/aggregate')
    if not candidate['aggregations']['items']:
        raise ValueError('no aggregate')
    table = candidate['tables'][0]
    groups = sorted(set(group_sql(g, table) for g in candidate['group_by']['items']))
    where = ' AND '.join(filter_sql(f, table) for f in candidate['filters']['items'])
    aggs = []
    for a in candidate['aggregations']['items']:
        if a['function'] not in ('sum', 'count', 'min', 'max', 'avg'):
            raise ValueError('unsupported aggregate')
        aggs.append((a['function'], column_sql(a['column'], table)))
    return {'table': table, 'where': where, 'groups': groups, 'aggregations': sorted(set(aggs))}


def index_patterns(candidate):
    if len(candidate['tables']) != 1:
        return []
    table = candidate['tables'][0]
    keys = []
    def predicates(node):
        if node['type'] == 'or':
            return  # No unsupported OR reasoning.
        if node['type'] == 'and':
            for n in node['items']:
                predicates(n)
        elif node['value']['status'] == 'known':
            key = column_sql(node['column'], table)
            if node['op'] == 'like':
                val = node['value']['literal']
                if not isinstance(val, str) or val.startswith(('%', '_')):
                    return
                # Fixed SQLite default case-insensitive LIKE needs NOCASE index.
                key += ' COLLATE NOCASE'
            keys.append(key)
    for f in candidate['filters']['items']:
        predicates(f)
    for j in candidate['joins']['items']:
        for cond in j['conditions']:
            for side in ('left_column', 'right_column'):
                if cond[side].startswith(table + '.'):
                    keys.append(column_sql(cond[side], table))
    keys.extend(group_sql(g, table) for g in candidate['group_by']['items'])
    keys = list(dict.fromkeys(keys))[:3]
    return [{'table': table, 'keys': keys}] if keys else []
