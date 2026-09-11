"""Conservative single SELECT-layer substitution. No filter containment or roll-up."""
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.scope import traverse_scope
from .backend import quote


def parse_expr(sql):
    return sqlglot.parse_one(sql, read='sqlite')


def canonical(node, table, catalog):
    """Resolve qualified/unqualified base identifiers, preserving expression structure."""
    out = node.copy()
    for col in list(out.find_all(exp.Column)):
        matches = [n for n in catalog[table] if n.casefold() == col.name.casefold()]
        if len(matches) != 1:
            raise ValueError('unresolved base column')
        col.set('table', None)
        col.set('db', None)
        col.set('catalog', None)
        col.set('this', exp.to_identifier(matches[0], quoted=True))
    # Redundant parentheses are safe to strip, no algebraic rewrites.
    out = out.transform(lambda n: n.this.copy() if isinstance(n, exp.Paren) else n)
    return out.sql(dialect='sqlite')


def material_select(pattern):
    fields, replacements = [], {}
    for i, g in enumerate(pattern['groups']):
        name = f'g{i}'
        fields.append(g + ' AS ' + quote(name))
        replacements[g] = quote(name)
    for i, (func, col) in enumerate(pattern['aggregations']):
        name = f'a{i}'
        if func == 'avg':
            # Store AVG itself for exact SQLite semantics; SUM and count retain
            # sufficient statistics for a future roll-up implementation (disabled).
            fields += [f'AVG({col}) AS {quote(name)}',
                       f'SUM({col}) AS {quote(name + "_sum")}',
                       f'COUNT({col}) AS {quote(name + "_count")}']
        else:
            fields.append(f'{func.upper()}({col}) AS {quote(name)}')
        replacements[f'{func.upper()}({col})'] = quote(name)
    sql = 'SELECT ' + ', '.join(fields) + ' FROM ' + quote(pattern['table'])
    if pattern['where']:
        sql += ' WHERE ' + pattern['where']
    if pattern['groups']:
        sql += ' GROUP BY ' + ', '.join(pattern['groups'])
    return sql, replacements


def rewrite(sql, objects, catalog):
    materials = [o for o in objects if o['kind'] == 'materialization']
    if not materials:
        return sql, [], []
    try:
        statements = sqlglot.parse(sql, read='sqlite')
        if len(statements) != 1 or statements[0] is None:
            return sql, [], ['not a single SQL statement']
        tree = statements[0]
    except sqlglot.errors.ParseError:
        return sql, [], ['parser rejected SQL']
    if any(w.args.get('recursive') for w in tree.find_all(exp.With)):
        return sql, [], ['recursive CTE unsupported']
    used, reasons = [], []
    # Leaf layers only; replacement keeps other query layers and aliases intact.
    # Resolve names by scope: a CTE named like a base table is not that table.
    try:
        scopes = list(traverse_scope(tree))
    except (ValueError, sqlglot.errors.OptimizeError):
        return sql, [], ['unresolved query scope']
    for scope in scopes:
        select = scope.expression
        if not isinstance(select, exp.Select):
            continue
        source = select.args.get('from_')
        if not source or not isinstance(source.this, exp.Table):
            continue
        try:
            resolved = scope.selected_sources
        except sqlglot.errors.OptimizeError:
            continue
        if len(resolved) != 1 or not isinstance(next(iter(resolved.values()))[1], exp.Table):
            continue
        table = next((t for t in catalog if t.casefold() == source.this.name.casefold()), None)
        if table is None:
            continue
        if source.this.args.get('db') or source.this.args.get('catalog'):
            continue
        if any(select.args.get(k) for k in ('joins', 'having', 'qualify', 'windows', 'distinct', 'with_')):
            continue
        if any(select.find_all(exp.Window)) or any(select.find_all(exp.Subquery)):
            continue
        if not select.args.get('group') and not any(select.find_all(exp.AggFunc)):
            continue
        qualifiers = {source.this.name.casefold(), source.this.alias_or_name.casefold()}
        if any(c.table and c.table.casefold() not in qualifiers for c in select.find_all(exp.Column)):
            continue
        aliases = {e.alias: e.this for e in select.expressions if isinstance(e, exp.Alias)}
        base_names = {c.casefold() for c in catalog[table]}
        def resolve_group(e):
            if isinstance(e, exp.Literal) and e.is_int:
                i = int(e.this) - 1
                if not 0 <= i < len(select.expressions):
                    raise ValueError('bad group ordinal')
                e = select.expressions[i]
                return e.this if isinstance(e, exp.Alias) else e
            if isinstance(e, exp.Column) and not e.table and e.name.casefold() not in base_names and e.name in aliases:
                return aliases[e.name]
            return e
        try:
            groups = sorted(set(canonical(resolve_group(e), table, catalog)
                                for e in (select.args['group'].expressions if select.args.get('group') else [])))
            where = canonical(select.args['where'].this, table, catalog) if select.args.get('where') else ''
        except ValueError:
            continue
        for obj in materials:
            p = obj['pattern']
            if p['table'] != table:
                continue
            try:
                pg = sorted(set(canonical(parse_expr(g), table, catalog) for g in p['groups']))
                pw = canonical(parse_expr(p['where']), table, catalog) if p['where'] else ''
                if pg != groups or pw != where:
                    continue
                mapping = {canonical(parse_expr(k), table, catalog): parse_expr(v)
                           for k, v in obj['replacements'].items()}
                def convert(node, allow_alias=False):
                    if allow_alias and isinstance(node, exp.Column) and not node.table and node.name in aliases:
                        return node.copy()
                    try:
                        key = canonical(node, table, catalog)
                    except ValueError:
                        key = None
                    if key in mapping:
                        return mapping[key].copy()
                    if isinstance(node, exp.Column):
                        if allow_alias and not node.table and node.name in aliases:
                            return node.copy()
                        raise ValueError('uncovered column')
                    if isinstance(node, (exp.AggFunc, exp.Star, exp.Subquery, exp.Window)):
                        raise ValueError('uncovered aggregate or unsafe expression')
                    # Only proven scalar operations; volatile/user functions fall back.
                    if isinstance(node, exp.Func) and not isinstance(node, (exp.Round, exp.Nullif, exp.Coalesce, exp.Abs)):
                        raise ValueError('unsupported scalar function')
                    result = node.copy()
                    for k, v in node.args.items():
                        if isinstance(v, exp.Expression):
                            result.set(k, convert(v, allow_alias))
                        elif isinstance(v, list):
                            result.set(k, [convert(x, allow_alias) if isinstance(x, exp.Expression) else x for x in v])
                    return result
                projections = []
                for e in select.expressions:
                    if isinstance(e, exp.Alias):
                        projections.append(exp.alias_(convert(e.this), e.alias, quoted=True))
                    elif isinstance(e, exp.Column):
                        projections.append(exp.alias_(convert(e), e.name, quoted=True))
                    else:
                        raise ValueError('unaliased expression label cannot be preserved')
                replacement = select.copy()
                replacement.set('expressions', projections)
                replacement.set('from_', exp.From(this=exp.to_table(obj['name'], quoted=True)))
                replacement.set('where', None)
                replacement.set('group', None)
                if select.args.get('order'):
                    replacement.set('order', convert(select.args['order'], allow_alias=True))
                select.replace(replacement)
                if select is tree:
                    tree = replacement
                used.append(obj['name'])
                break
            except (ValueError, sqlglot.errors.ParseError) as exc:
                reasons.append(obj['name'] + ': ' + str(exc))
    return (tree.sql(dialect='sqlite') if used else sql), sorted(set(used)), sorted(set(reasons))


def preserve_rounding_scan_order(sql, tables_without_original_indexes):
    """Conservative fallback for ROUND over aggregates on originally unindexed data.

    NOT INDEXED restores the original full-table access path; it never disables
    a pre-existing user index. Only the current SQL is inspected, no Q numbers.
    """
    if 'round' not in sql.casefold():
        return sql, False
    try:
        tree = sqlglot.parse_one(sql, read='sqlite')
    except sqlglot.errors.ParseError:
        return sql, False
    if not any(tree.find_all(exp.Round)) or not any(tree.find_all(exp.AggFunc)):
        return sql, False
    if any(tree.find_all(exp.With)):
        return sql, False
    changed = False
    for table in tree.find_all(exp.Table):
        if table.name in tables_without_original_indexes and not table.args.get('db'):
            table.set('indexed', False)
            changed = True
    return (tree.sql(dialect='sqlite') if changed else sql), changed
