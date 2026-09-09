"""Scope-aware SQL structure and conservative base-column lineage.
Unresolved references remain explicit unknowns rather than zero counts.
"""
from collections import Counter
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.scope import Scope, traverse_scope

def sql(n): return n.sql(dialect='sqlite') if n is not None else None

def features(text,tables=()):
 try:
    tree=sqlglot.parse_one(text,read='sqlite'); scopes=list(traverse_scope(tree)); ids={id(s):f'B{i+1}' for i,s in enumerate(scopes)}
    schema={t['name'].lower():{c['name'].lower() if isinstance(c,dict) else c.lower() for c in t['columns']} for t in tables}
    schema_names={t['name'].lower():[c['name'] if isinstance(c,dict) else c for c in t['columns']] for t in tables}
    scope_for_expression={id(s.expression):s for s in scopes}
    unknown=[]
    def output_names(source,seen=None):
        seen=set() if seen is None else seen
        if isinstance(source,exp.Table): return schema_names.get(source.name.lower())
        if not isinstance(source,Scope) or id(source) in seen: return None
        seen=seen|{id(source)}; names=[]
        for projection in source.expression.selects:
            if isinstance(projection,exp.Star) or isinstance(projection,exp.Column) and projection.is_star:
                for alias,(_,child) in source.selected_sources.items():
                    if isinstance(projection,exp.Column) and projection.table and alias.lower()!=projection.table.lower(): continue
                    child_names=output_names(child,seen)
                    if child_names is None: return None
                    names+=child_names
            elif projection.alias_or_name: names.append(projection.alias_or_name)
            else: return None
        return names
    def source_tables(source,seen=None):
        seen=set() if seen is None else seen
        if isinstance(source,exp.Table): return [exp.Table(this=source.this.copy(),db=source.args.get('db'),catalog=source.args.get('catalog')).sql(dialect='sqlite')]
        if id(source) in seen: return []
        seen=seen|{id(source)}
        if isinstance(source,Scope):
            used=[v[1] for v in source.selected_sources.values()] or list(source.union_scopes)
            return sorted(set(t for v in used for t in source_tables(v,seen)))
        return []
    def lineage(column,scope,trail=None):
        trail=set() if trail is None else trail
        marker=(id(scope),column.sql())
        if marker in trail: return []
        trail=trail|{marker}; name=column.name.lower(); qualifier=column.table.lower()
        sources={k.lower():v[1] for k,v in scope.selected_sources.items()}
        if qualifier: targets=[sources[qualifier]] if qualifier in sources else []
        else:
            targets=[]
            for s in sources.values():
                if isinstance(s,exp.Table) and (not schema or name in schema.get(s.name.lower(),set())): targets.append(s)
                elif isinstance(s,Scope) and (name in [x.lower() for x in s.expression.named_selects] or '*' in s.expression.named_selects): targets.append(s)
        if not targets and not qualifier:
            alias_expression=next((p.this for p in scope.expression.selects if isinstance(p,exp.Alias) and p.alias.lower()==name),None)
            if alias_expression is not None: return node_columns(alias_expression,scope,trail)
        if len(targets)!=1:
            if not targets and scope.parent: return lineage(column,scope.parent,trail)
            unknown.append({'block':ids.get(id(scope)),'column':sql(column),'reason':'ambiguous_or_missing_source'}); return [{'unknown':sql(column)}]
        target=targets[0]
        if isinstance(target,exp.Table):
            canonical_name=next((n for n in schema_names.get(target.name.lower(),[]) if n.lower()==name),column.name)
            return [{'table':source_tables(target)[0],'column':canonical_name}]
        expressions=target.expression.selects
        indexes=[i for i,x in enumerate(expressions) if x.alias_or_name.lower()==name]
        if not indexes and '*' in target.expression.named_selects:
            unqualified=column.copy(); unqualified.set('table',None)
            return lineage(unqualified,target,trail)
        if not indexes:
            unknown.append({'column':sql(column),'reason':'derived_star_or_missing_output'}); return [{'unknown':sql(column)}]
        output=expressions[indexes[0]]
        if isinstance(target.expression,exp.SetOperation):
            out=[]
            for branch in target.union_scopes:
                if len(branch.expression.selects)>indexes[0]: out+=node_columns(branch.expression.selects[indexes[0]],branch,trail)
            return out
        return node_columns(output,target,trail)
    def node_columns(node,scope,trail=None):
        return [item for c in node.find_all(exp.Column) for item in lineage(c,scope_for_expression.get(id(c.find_ancestor(exp.Select)),scope),trail)]
    blocks=[]; ref=[]
    for scope in scopes:
        expression=scope.expression
        sources=[{'alias':k,'kind':'base' if isinstance(v,exp.Table) else 'derived','block':ids.get(id(v)),'base_tables':source_tables(v)} for k,v in scope.sources.items() if k in scope.selected_sources]
        for k,v in scope.selected_sources.items():
            if isinstance(v[1],exp.Table): ref+=source_tables(v[1])
        block={'id':ids[id(scope)],'parent':ids.get(id(scope.parent)),'kind':type(expression).__name__,'sql':sql(expression),'sources':sources,'joins':[],'group_by':[],'aggregates':[],'windows':[],'filters':[]}
        def own(node): return node.find_ancestor(exp.Select)==expression
        for join in [j for j in expression.find_all(exp.Join) if own(j)]:
            block['joins'].append({'type':(' '.join(filter(None,[join.args.get('method'),join.side,join.kind])) or 'INNER').upper(),'right':sql(join.this),'on':sql(join.args.get('on')),'using':[sql(n) for n in join.args.get('using') or []]})
        block['join_inputs']=len(sources) if block['joins'] else 0
        aliases={e.alias.lower():e.this for e in expression.selects if isinstance(e,exp.Alias)}
        group=expression.args.get('group')
        if group:
            block['group_sets']={k:[sql(n) for n in v] for k,v in group.args.items() if k!='expressions' and isinstance(v,list)}
            for key in group.expressions:
                resolved=key
                if isinstance(key,exp.Literal) and key.is_int and 1<=int(key.this)<=len(expression.selects):
                    resolved=expression.selects[int(key.this)-1]; resolved=resolved.this if isinstance(resolved,exp.Alias) else resolved
                elif isinstance(key,exp.Column) and not key.table:
                    input_name=key.name.lower()
                    input_exists=any(input_name in schema.get(v[1].name.lower(),set()) if isinstance(v[1],exp.Table) else input_name in [n.lower() for n in (output_names(v[1]) or [])] for v in scope.selected_sources.values())
                    resolved=key if input_exists else aliases.get(input_name,key)
                block['group_by'].append({'original':sql(key),'expression':sql(resolved),'columns':node_columns(resolved,scope)})
        aggregate_nodes=list(expression.find_all(exp.AggFunc))+[n for n in expression.find_all(exp.Anonymous) if n.name.upper() in ['TOTAL','JSON_GROUP_ARRAY','JSON_GROUP_OBJECT']]
        for a in aggregate_nodes:
            if not own(a): continue
            if isinstance(a,(exp.Min,exp.Max)) and a.expressions: continue # SQLite multi-argument MIN/MAX are scalar.
            window=a.find_ancestor(exp.Window)
            if window is not None and (window.this is a or isinstance(window.this,exp.Filter) and window.this.this is a): continue
            conditions=[]; metrics=[]
            for c in a.find_all(exp.Column):
                condition=False
                p=c.parent
                while p is not None and p is not a:
                    if isinstance(p,exp.If) and any(c is n for n in p.this.walk()): condition=True
                    if isinstance(p,exp.Filter) and p.expression and any(c is n for n in p.expression.walk()): condition=True
                    p=p.parent
                (conditions if condition else metrics).extend(lineage(c,scope_for_expression.get(id(c.find_ancestor(exp.Select)),scope)))
            filter_node=a.parent if isinstance(a.parent,exp.Filter) else None
            if filter_node and filter_node.expression: conditions+=node_columns(filter_node.expression,scope)
            block['aggregates'].append({'function':a.name.upper() if isinstance(a,exp.Anonymous) else a.sql_name(),'expression':sql(filter_node or a),'distinct':bool(a.find(exp.Distinct)),'metric_columns':metrics,'condition_columns':conditions,'row_count':isinstance(a,exp.Count) and isinstance(a.this,exp.Star)})
        for w in expression.find_all(exp.Window):
            if own(w): block['windows'].append({'expression':sql(w),'function':sql(w.this),'partition_by':[sql(n) for n in w.args.get('partition_by') or []],'order_by':sql(w.args.get('order')),'frame':sql(w.args.get('spec')),'columns':node_columns(w,scope)})
        for kind,klass in [('where',exp.Where),('having',exp.Having),('case',exp.Case)]:
            for f in expression.find_all(klass):
                if own(f): block['filters'].append({'kind':kind,'expression':sql(f),'columns':node_columns(f,scope)})
        references=[{'expression':sql(c),'lineage':lineage(c,scope),'wildcard':False} for c in scope.columns if not c.is_star]
        for projection in expression.selects:
            if isinstance(projection,exp.Star) or isinstance(projection,exp.Column) and projection.is_star:
                for alias,(_,source) in scope.selected_sources.items():
                    if isinstance(projection,exp.Column) and projection.table and projection.table.lower()!=alias.lower(): continue
                    names=output_names(source)
                    if names is None:
                        unknown.append({'block':block['id'],'column':sql(projection),'reason':'wildcard_output_names_unresolved'})
                        references.append({'expression':sql(projection),'lineage':[{'unknown':sql(projection)}],'wildcard':True})
                    else:
                        for name in names:
                            c=exp.column(name,table=alias,quoted=True)
                            references.append({'expression':sql(c),'lineage':lineage(c,scope),'wildcard':True})
        for join in block['joins']:
            for name in join['using']:
                for alias,(_,source) in scope.selected_sources.items():
                    names=output_names(source)
                    if names and name.strip('"').lower() in [n.lower() for n in names]:
                        c=exp.column(name.strip('"'),table=alias,quoted=True)
                        references.append({'expression':sql(c),'lineage':lineage(c,scope),'using_join':True,'wildcard':False})
        block['column_references']=references
        blocks.append(block)
    aggregates=[a for b in blocks for a in b['aggregates']]; funcs=Counter(a['function'] for a in aggregates)
    return {'parsed':True,'canonical_sql':tree.sql(dialect='sqlite',normalize=True),'blocks':blocks,'base_tables':sorted(set(ref)), 'table_references':dict(Counter(ref)),
            'max_join_inputs':max([b['join_inputs'] for b in blocks]+[0]),'join_types':dict(Counter(j['type'] for b in blocks for j in b['joins'])),
            'group_dimensions':[len(b['group_by']) for b in blocks if b['group_by']],'max_group_dimensions':max([len(b['group_by']) for b in blocks]+[0]),
            'aggregate_functions':dict(funcs),'aggregate_expressions':aggregates,'window_count':sum(len(b['windows']) for b in blocks),
            'parse_coverage':True,'table_lineage_coverage':all(s['base_tables'] for b in blocks for s in b['sources']), 'column_lineage_coverage':not unknown,'unknowns':unknown}
 except Exception as e: return {'parsed':False,'error':repr(e),'base_tables':None,'max_join_inputs':None,'max_group_dimensions':None,'aggregate_functions':None,'column_lineage_coverage':False,'table_lineage_coverage':False}
