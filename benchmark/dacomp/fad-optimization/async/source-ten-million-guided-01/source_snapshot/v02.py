"""v0.2 contract: intent-derived, structured future access. No prose or SQL inference."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

FIELDS = ('columns', 'filters', 'joins', 'group_by', 'aggregations')


def obj(props, required=None):
    return {'type':'object','additionalProperties':False,'properties':props,
            'required':list(props) if required is None else required}


def build_schema():
    name={'type':'string','minLength':1}
    names={'type':'array','minItems':1,'uniqueItems':True,'items':name}
    scalar={'type':['string','number','boolean','null']}
    value={'anyOf':[
        obj({'status':{'const':'unknown'}}),
        obj({'status':{'const':'known'},'literal':{'anyOf':[scalar,{'type':'array','minItems':1,'items':scalar}]}})]}
    predicate=obj({'type':{'const':'predicate'},'column':name,
        'op':{'enum':['eq','ne','lt','le','gt','ge','in','between','like','is_null','is_not_null']},'value':value})
    defs={'predicate':predicate}
    # Bounded trees make the model-facing schema finite, with no recursive refs.
    prev={'$ref':'#/$defs/predicate'}
    for depth in range(1,4):
        defs[f'filter{depth}']={'anyOf':[{'$ref':'#/$defs/predicate'},
            obj({'type':{'enum':['and','or']},'items':{'type':'array','minItems':2,'maxItems':8,'items':prev}})]}
        prev={'$ref':f'#/$defs/filter{depth}'}
    expr={'anyOf':[obj({'type':{'const':'column'},'column':name}),
        obj({'type':{'const':'time_bucket'},'column':name,'unit':{'enum':['year','month','day']}})]}
    join=obj({'type':{'enum':['inner','left','right','full']},
        'conditions':{'type':'array','minItems':1,'maxItems':8,'items':obj({
            'left_column':name,'op':{'const':'eq'},'right_column':name})}})
    agg=obj({'function':{'enum':['sum','count','avg','min','max','count_distinct']},'column':name})
    def field(item, allow_none=True, max_items=32):
        return obj({'status':{'enum':['known','partial','unknown']+(['none'] if allow_none else [])},
                    'items':{'type':'array','maxItems':max_items,'uniqueItems':True,'items':item}})
    candidate=obj({'tables':names,'columns':field(name), 'filters':field(prev,max_items=1),
                   'joins':field(join),'group_by':field(expr),'aggregations':field(agg),
                   'priority':{'enum':['high','medium','low']},'likelihood':{'enum':['high','medium','low']}},
                  ['tables',*FIELDS,'priority'])
    defs['candidate']=candidate
    defs['futureAccess']=obj({'status':{'enum':['provided','unknown','no_further_access']},
        'coverage':{'enum':['remaining_task','partial_plan']},
        'candidates':{'type':'array','maxItems':8,'items':{'$ref':'#/$defs/candidate'}}},['status','candidates'])
    result=obj({'sql':name,'future_access':{'type':'object', '$ref':'#/$defs/futureAccess',
        'description':'A nested JSON object, never a JSON-encoded string. Candidate columns, filters, joins, group_by and aggregations each require an object with status and items.'}})
    result.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$defs':defs})
    return result


def references(value):
    if isinstance(value,dict):
        for k,v in value.items():
            if k in ('column','left_column','right_column') and v!='*':
                yield value,k,v
            else:
                yield from references(v)
    elif isinstance(value,list):
        for v in value:yield from references(v)


def normalize(hint,catalog):
    """Resolve only unambiguous catalog names and legal identifier quoting."""
    result=copy.deepcopy(hint); changes=[]; errors=[]
    def quote_variants(s):
        return (s,'"'+s.replace('"','""')+'"','`'+s.replace('`','``')+'`','['+s+']')
    def resolve(raw,mapping,path):
        exact=mapping.get(raw,set())
        matches=exact or set().union(*(v for k,v in mapping.items() if k.casefold()==raw.casefold()))
        if len(matches)!=1:
            errors.append({'path':path,'message':'Unknown or ambiguous catalog identifier: '+raw})
            return raw
        canonical=next(iter(matches))
        if canonical!=raw:changes.append({'path':path,'raw':raw,'canonical':canonical})
        return canonical
    table_map={}
    for t in catalog:
        for alias in quote_variants(t):table_map.setdefault(alias,set()).add(t)
    for i,c in enumerate(result['candidates']):
        path=f'future_access.candidates.{i}'
        c['tables']=[resolve(t,table_map,path+'.tables') for t in c['tables']]
        col_map={}
        for t in c['tables']:
            for col in catalog.get(t,[]):
                for a in quote_variants(t):
                    for b in quote_variants(col):col_map.setdefault(a+'.'+b,set()).add(t+'.'+col)
        c['columns']['items']=[resolve(v,col_map,path+'.columns') for v in c['columns']['items']]
        for parent,key,value in references(c):
            parent[key]=resolve(value,col_map,path+'.'+key)
    return result,changes,errors


def validate(value,catalog,max_candidates=8,max_bytes=16384):
    check={'status':'not_applicable','unverified':[],'normalizations':[], 'column_unions':[]}
    def error(path,message):return {'path':path,'message':message}
    try:raw=json.dumps(value,ensure_ascii=False,allow_nan=False).encode()
    except (ValueError,TypeError,UnicodeError):return None,[error('future_access','Not finite JSON')],check
    if len(raw)>max_bytes:return None,[error('future_access','Hint byte limit exceeded')],check
    schema=build_schema();schema['$defs']['futureAccess']['properties']['candidates']['maxItems']=max_candidates
    errs=[error('.'.join(map(str,e.absolute_path)),e.message) for e in Draft202012Validator(schema).iter_errors({'sql':'SELECT 1','future_access':value})]
    if errs:return None,errs,check
    provided=value['status']=='provided'
    if provided and (not value['candidates'] or 'coverage' not in value):
        errs.append(error('future_access','provided requires coverage and nonempty candidates'))
    if not provided and (value['candidates'] or 'coverage' in value):
        errs.append(error('future_access','Empty status requires empty candidates and no coverage'))
    if errs:return None,errs,check
    snapshot,changes,name_errors=normalize(value,catalog)
    check={'status':'unverified' if name_errors else 'verified','unverified':name_errors,'normalizations':changes,'column_unions':[]}
    errs.extend(name_errors)
    # Normalization must not introduce duplicate items.
    errs.extend(error('.'.join(map(str,e.absolute_path)),e.message) for e in Draft202012Validator(schema).iter_errors({'sql':'SELECT 1','future_access':snapshot}))
    def unknown(x):
        if isinstance(x,dict):return x.get('status')=='unknown' or any(unknown(v) for v in x.values())
        return isinstance(x,list) and any(unknown(v) for v in x)
    def filter_check(node,path):
        if node['type'] in ('and','or'):
            for j,item in enumerate(node['items']):filter_check(item,f'{path}.{j}')
            return
        v=node['value'];op=node['op']
        if v['status']=='unknown':
            if op in ('is_null','is_not_null'):errs.append(error(path,'Null tests use known literal null'))
            return
        v=v['literal']
        scalar=lambda x:x is not None and isinstance(x,(str,bool,int,float))
        if op in ('is_null','is_not_null'):valid=v is None
        elif op=='like':valid=isinstance(v,str)
        elif op in ('in','between'):
            valid=isinstance(v,list) and bool(v) and all(scalar(x) for x in v)
            if op=='between':valid=valid and len(v)==2
        else:valid=scalar(v)
        if not valid:errs.append(error(path,'Literal incompatible with '+op))
    for i,c in enumerate(snapshot['candidates']):
        prefix=f'future_access.candidates.{i}'
        for f in FIELDS:
            state=c[f]['status'];items=c[f]['items']
            if (state in ('known','partial')) != bool(items):
                errs.append(error(prefix+'.'+f,'known/partial require items; unknown/none require empty items'))
            if state=='known' and any(unknown(item) for item in items):
                errs.append(error(prefix+'.'+f,'known cannot contain unknown parts'))
        refs={v for _,_,v in references(c)}
        missing=refs-set(c['columns']['items'])
        if missing and not errs:
            before=c['columns']['status']
            c['columns']['items'].extend(sorted(missing))
            if before=='unknown':
                c['columns']['status']='partial'
            elif before=='none':
                c['columns']['status']='partial' if any(c[f]['status'] in ('partial','unknown') for f in FIELDS if f!='columns') else 'known'
            check['column_unions'].append({'candidate':i,'added':sorted(missing),
                'status_before':before,'status_after':c['columns']['status'],
                'source':'explicit_fad_operation_references'})
        if c['columns']['status']=='none':
            aggs=c['aggregations']
            pure_count=aggs['status']=='known' and bool(aggs['items']) and all(a=={'function':'count','column':'*'} for a in aggs['items'])
            if not pure_count or any(c[f]['status']!='none' for f in ('filters','joins','group_by')):
                errs.append(error(prefix+'.columns','none is allowed only for pure COUNT(*) without other column accesses'))
        for j,node in enumerate(c['filters']['items']):filter_check(node,f'{prefix}.filters.{j}')
        for agg in c['aggregations']['items']:
            if agg['column']=='*' and agg['function']!='count':errs.append(error(prefix+'.aggregations','Only count accepts *'))
    # The delivered object must still obey bounds after the deterministic union.
    errs.extend(error('.'.join(map(str,e.absolute_path)),e.message) for e in Draft202012Validator(schema).iter_errors({'sql':'SELECT 1','future_access':snapshot}))
    return (None if errs else snapshot),errs,check


if __name__=='__main__':
    Path(__file__).with_name('schema-v0.2.json').write_text(json.dumps(build_schema(),ensure_ascii=False,indent=2)+'\n')
