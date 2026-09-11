"""Conservative FAD ingestion: explicit normalization and candidate isolation."""
import copy
import json
from agent_db_tool.v02 import references, validate


def receive_object(raw, catalog):
    audit={'errors':[], 'normalizations':[], 'accepted_candidate_indices':[],
           'rejected_candidates':[], 'catalog_check':{}}
    def reject(message):
        audit['errors'].append({'path':'future_access','message':message})
        return None,audit
    try:
        encoded=json.dumps(raw,ensure_ascii=False,allow_nan=False).encode()
    except (TypeError,ValueError,UnicodeError):return reject('Not finite JSON')
    if len(encoded)>16384:return reject('Hint byte limit exceeded')
    if not isinstance(raw,dict):return reject('Expected object')
    if raw.get('status')!='provided':
        fad,errors,check=validate(raw,catalog)
        audit.update(errors=errors,catalog_check=check)
        return fad,audit
    if set(raw)-{'status','coverage','candidates'}:return reject('Unknown envelope fields')
    if raw.get('coverage') not in ('partial_plan','remaining_task'):return reject('Invalid coverage')
    candidates=raw.get('candidates')
    if not isinstance(candidates,list) or not 1<=len(candidates)<=8:return reject('Expected 1..8 candidates')
    accepted=[];checks=[]
    for index,original in enumerate(candidates,1):
        candidate=copy.deepcopy(original)
        notes=[]
        def note(path,before,after):
            notes.append({'candidate':index,'path':path,'before':copy.deepcopy(before),'after':copy.deepcopy(after)})
        def tree(node,path):
            if not isinstance(node,dict):return node
            if node.get('type') in ('and','or') and isinstance(node.get('items'),list):
                node['items']=[tree(x,path+'.items.'+str(i)) for i,x in enumerate(node['items'])]
                if set(node)=={'type','items'} and len(node['items'])==1:
                    child=node['items'][0];note(path,node,child);return child
            value=node.get('value')
            if node.get('type')=='predicate' and isinstance(value,dict) and value.get('status')=='unknown' and 'literal' in value:
                before=copy.deepcopy(value);del value['literal'];note(path+'.value',before,value)
            return node
        def unknown(value):
            if isinstance(value,dict):return value.get('status')=='unknown' or any(unknown(v) for v in value.values())
            return isinstance(value,list) and any(unknown(v) for v in value)
        if isinstance(candidate,dict):
            filters=candidate.get('filters')
            if isinstance(filters,dict) and isinstance(filters.get('items'),list):
                filters['items']=[tree(x,'filters.items.'+str(i)) for i,x in enumerate(filters['items'])]
                if filters.get('status')=='known' and unknown(filters['items']):
                    note('filters.status','known','partial');filters['status']='partial'
            columns=candidate.get('columns')
            if isinstance(columns,dict) and columns.get('status') in ('known','partial') and columns.get('items')==[]:
                refs=[v for _,_,v in references(candidate) if isinstance(v,str)]
                if refs:
                    items=sorted(set(refs));note('columns.items',[],items);columns['items']=items
        value={'status':'provided','coverage':raw['coverage'],'candidates':[candidate]}
        fad,errors,check=validate(value,catalog)
        audit['normalizations'].extend(notes)
        if errors:
            audit['rejected_candidates'].append({'candidate':index,'errors':errors,'catalog_check':check})
        else:
            accepted.append(fad['candidates'][0]);checks.append({'candidate':index,**check})
            audit['accepted_candidate_indices'].append(index)
    audit['catalog_check']={'candidates':checks}
    if not accepted:return reject('No valid candidates')
    result={'status':'provided','coverage':'partial_plan' if audit['rejected_candidates'] else raw['coverage'],'candidates':accepted}
    # Retain global bounds after normalization/column union.
    snapshot,errors,check=validate(result,catalog)
    audit['errors']=errors;audit['final_catalog_check']=check
    return snapshot,audit
