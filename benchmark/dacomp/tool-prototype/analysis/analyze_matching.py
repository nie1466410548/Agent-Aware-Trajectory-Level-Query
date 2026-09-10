"""DAComp-006 observed FAD column matching, without executing data queries.

All targets have step > hint step. Compile successful SQL through SQLite EXPLAIN
and collect SQLITE_READ events, preserving base columns behind aliases/subqueries.
Quoted hint names are normalized only by exact catalog spelling variants.
"""
import json
import sqlite3
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RUN = BASE/'runs/hints-006-02'

def main():
    meta = json.loads((RUN/'task_meta.json').read_text())
    events = [json.loads(s) for s in (RUN/'events.jsonl').read_text().splitlines()]
    requests = [e for e in events if e['record']=='request']
    statuses = {e['request_id']:e['response']['status'] for e in events if e['record']=='completion'}
    db = sqlite3.connect(Path(meta['database_path']).as_uri()+'?mode=ro',uri=True,cached_statements=0)
    features = {}
    for e in requests:
        if statuses[e['request_id']]!='ok':
            continue
        columns, tables = set(),set()
        def auth(action,table,column,*rest):
            if action==sqlite3.SQLITE_READ:
                tables.add(table)
                if column:columns.add(table+'.'+column)
            return sqlite3.SQLITE_OK
        db.set_authorizer(auth)
        db.execute('EXPLAIN '+e['arguments']['sql']).fetchall()
        features[e['step_id']]={'tables':sorted(tables),'columns':sorted(columns)}
    db.close()
    variants={}
    for table, columns in meta['catalog'].items():
        for column in columns:
            canonical=table+'.'+column
            variants[canonical]=canonical
            variants[table+'."'+column.replace('"','""')+'"']=canonical
    comparisons=[]
    fields=Counter()
    for e in requests:
        hint=e['hint_snapshot']
        if hint['status']!='provided':continue
        step=e['step_id']
        targets=[t for t in sorted(features) if t>step]
        assert targets
        cs=hint['candidates']
        for c in cs:fields.update(c.keys())
        raw={v for c in cs for v in c.get('columns',[])}
        predicted={variants.get(v,v) for v in raw}
        actual=set(features[targets[0]]['columns'])
        future=set().union(*(set(features[t]['columns']) for t in targets))
        current=set(features.get(step,{}).get('columns',[]))
        tables={v for c in cs for v in c['tables']}
        full=[t for t in targets if predicted and predicted <= set(features[t]['columns'])]
        comparisons.append({'step':step,'source_status':statuses[e['request_id']],
            'next_successful_step':targets[0], 'condition':cs[0].get('condition'),
            'raw_columns':sorted(raw),'predicted_columns':sorted(predicted),'next_columns':sorted(actual),
            'table_hit_next':tables <= set(features[targets[0]]['tables']),
            'next_hits':sorted(predicted&actual),'next_missing':sorted(actual-predicted),
            'all_columns_next': bool(predicted) and predicted<=actual,
            'all_raw_columns_next':bool(raw) and raw<=actual,
            'all_columns_in_some_future_query':bool(full),
            'first_full_column_hit_step':full[0] if full else None,
            'all_columns_eventually':bool(predicted) and predicted<=future,
            'current_columns':sorted(current),
            'new_vs_current':sorted(predicted-current) if step in features else None})
    named=[x for x in comparisons if x['predicted_columns']]
    def metrics(rows):
        p=sum(len(x['predicted_columns']) for x in rows)
        hits=sum(len(x['next_hits']) for x in rows)
        a=sum(len(x['next_columns']) for x in rows)
        return {'hint_count':len(rows),'predicted_column_occurrences':p,'hit_occurrences':hits,
            'actual_next_column_occurrences':a,'precision':hits/p if p else None,
            'explicit_recall':hits/a if a else None,
            'full_column_next_count':sum(x['all_columns_next'] for x in rows)}
    good=[x for x in named if x['source_status']=='ok']
    baseline_rows=[x for x in comparisons if x['source_status']=='ok']
    baseline_hits=sum(len(set(x['current_columns'])&set(x['next_columns'])) for x in baseline_rows)
    baseline_pred=sum(len(x['current_columns']) for x in baseline_rows)
    baseline_actual=sum(len(x['next_columns']) for x in baseline_rows)
    result={'scope':{'real_agent_tasks':1,'task':'dacomp-006','queries':len(requests),'successful_queries':len(features),
                     'provided_hints':len(comparisons),'column_hints':len(named),'target':'first later successful SQL; source errors retained'},
        'candidate_field_counts':dict(fields), 'named_column_metrics':metrics(named),
        'all_hint_explicit_column_coverage':metrics(comparisons),
        'successful_source_named_metrics':metrics(good),
        'strict_raw_full_next':sum(x['all_raw_columns_next'] for x in named),
        'some_future_full_column_hits':sum(x['all_columns_in_some_future_query'] for x in named),
        'table_next_hits':sum(x['table_hit_next'] for x in comparisons),
        'current_sql_column_baseline':{'source_success_only':True,'pairs':len(baseline_rows),
            'hits':baseline_hits,'predicted':baseline_pred,'actual':baseline_actual,
            'precision':baseline_hits/baseline_pred,'recall':baseline_hits/baseline_actual,
            'fad_same_pairs':metrics(baseline_rows)},
        'sql_features':features,'comparisons':comparisons}
    (BASE/'analysis/matching.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('sql_features','comparisons')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
