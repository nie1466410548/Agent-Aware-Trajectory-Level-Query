"""Offline, within-episode adjacent-query characterization. No model calls.

These are syntactic signals, not a materialized-view equivalence test.
"""
import json
from pathlib import Path
import sqlglot
from sqlglot import exp

ROOT = Path(__file__).resolve().parents[1]


def features(sql):
    tree = sqlglot.parse_one(sql, read='sqlite')
    ctes = {c.alias_or_name.lower() for c in tree.find_all(exp.CTE)}
    relations = {t.name.lower() for t in tree.find_all(exp.Table)} - ctes
    aliases = {t.alias_or_name.lower(): t.name.lower() for t in tree.find_all(exp.Table)}
    def canonical(node):
        node = node.copy()
        for col in node.find_all(exp.Column):
            if col.table and col.table.lower() in aliases:
                col.set('table', exp.to_identifier(aliases[col.table.lower()]))
        return node.sql(dialect='sqlite', normalize=True)
    columns = set()
    for col in tree.find_all(exp.Column):
        scope = col.find_ancestor(exp.Select)
        output_aliases = {e.alias.lower() for e in scope.expressions if isinstance(e, exp.Alias)} if scope else set()
        # References to computed output names are not additional base columns.
        if not col.table and col.name.lower() in output_aliases and not col.find_ancestor(exp.Alias):
            continue
        relation = aliases.get(col.table.lower()) if col.table else (next(iter(relations)) if len(relations)==1 else None)
        if relation in relations:
            columns.add(f'{relation}.{col.name.lower()}')
    predicates = set()
    for where in tree.find_all(exp.Where):
        predicates.update(canonical(term) for term in where.this.flatten() if term is not None) if isinstance(where.this, exp.And) else predicates.add(canonical(where.this))
    joins = {canonical(j) for j in tree.find_all(exp.Join)}
    # Resolve SELECT aliases only within their own SELECT scope.
    groups = set()
    for select in tree.find_all(exp.Select):
        aliases_select = {e.alias.lower(): e.this for e in select.expressions if isinstance(e, exp.Alias)}
        group = select.args.get('group')
        if group:
            keys = []
            for key in group.expressions:
                resolved = aliases_select.get(key.name.lower(), key) if isinstance(key, exp.Column) and not key.table else key
                keys.append(canonical(resolved))
            groups.add(tuple(sorted(keys)))
    return {'relations':relations, 'columns':columns, 'predicates':predicates,
            'joins':joins, 'aggregates':{canonical(a) for a in tree.find_all(exp.AggFunc)},
            'groups':groups, 'exact_sql':canonical(tree)}


def main():
    summaries = []
    for path in sorted((ROOT/'reports').glob('*-inventory.json')):
        inventory = json.loads(path.read_text())
        queries = [q for q in inventory['queries'] if q['success'] and not q['metadata']]
        pairs = []
        for left, right in zip(queries, queries[1:]):
            pair = {'from':left['id'], 'to':right['id']}
            try:
                a, b = features(left['sql']), features(right['sql'])
                for name in ['relations','columns','predicates','joins','aggregates','groups']:
                    # Shared expression alone is only a signal; require some shared base relation.
                    pair[name] = sorted(a[name] & b[name]) if a['relations'] & b['relations'] else []
                pair['same_sql'] = a['exact_sql']==b['exact_sql']
                pair['analyzed'] = True
            except Exception as exc:
                pair.update(analyzed=False,error=str(exc))
            pairs.append(pair)
        summary = {'task_id':inventory['summary']['task_id'], 'adjacent_pairs':len(pairs),
                   'analyzed_pairs':sum(p['analyzed'] for p in pairs)}
        for name in ['relations','columns','predicates','joins','aggregates','groups','same_sql']:
            summary[name] = sum(bool(p.get(name)) for p in pairs)
        summaries.append(summary)
        output = {'definition':'Adjacent successful non-metadata SQL within one episode; exact syntax after limited alias normalization. Not MV coverage. Shared aggregate/group syntax requires shared base relation but does not verify filters or join equivalence.',
                  'summary':summary,'pairs':pairs}
        path.with_name(path.name.replace('-inventory.json','-adjacent.json')).write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'reports'/'adjacent-summary.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(summaries,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
