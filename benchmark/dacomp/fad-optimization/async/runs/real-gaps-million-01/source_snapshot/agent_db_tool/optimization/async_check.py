"""Compare replay against the real source results; audit relative time causality."""
import json
from pathlib import Path
import sqlglot
from .check import compare_results
from .replay import DEFAULT_CONFIG


def check(run,timing):
    run=Path(run);t=json.loads(Path(timing).read_text());source=Path(t['source_run'])
    es=[json.loads(l) for l in (source/'events.jsonl').read_text().splitlines()]
    completions={e['request_id']:e['response'] for e in es if e['record']=='completion'}
    timeline=json.loads((run/'timeline.json').read_text());summary=json.loads((run/'summary.json').read_text())
    records=timeline['queries'];checks=[]
    if len(records)!=len(t['calls']):raise ValueError('missing SQL calls')
    objects={e['object']['name']:e['object'] for e in timeline['background'] if e['type']=='object_ready'}
    for r,c in zip(records,t['calls']):
        assert r['sql']==c['arguments']['sql'] and r['step']==c['step']
        original=completions[c['request_id']]
        expected=original['status']=='ok'
        if not expected or r['status']!='ok':
            result={'equal':(r['status']=='ok')==expected and original['error']==r['error'],'reason':r['error']}
        else:
            read=lambda p:[json.loads(l) for l in p.read_text().splitlines()]
            a=read(source/original['result']['result_file']);b=read(run/'results'/f"Q{r['step']}.jsonl")
            parsed=sqlglot.parse_one(r['sql'],read='sqlite')
            result=compare_results(a,b,original['result']['columns'],r['columns'],bool(parsed.args.get('order')),
                                   DEFAULT_CONFIG['absolute_tolerance'],DEFAULT_CONFIG['relative_tolerance'])
        if summary['manifest']['mode']=='baseline':
            assert r['raw_fad'] is None and not r['materializations_used'] and r['rewrite_seconds']==0
        else:
            assert r['raw_fad']==c['arguments']['future_access']
            assert r['fad_delivered_ns']>=r['query_completed_ns']
            for name in r['materializations_used']:
                obj=objects[name]
                assert obj['created_after']<r['step'] and obj['ready_ns']<=r['snapshot_start_ns']
                assert name in r['available_objects']
        checks.append({'step':r['step'],**result})
    for obj in objects.values():
        trigger=next(r for r in records if r['step']==obj['created_after'])
        assert obj['ddl_started_ns']>=trigger['fad_delivered_ns']
        assert obj['commit_return_ns']<=obj['ready_ns']
    if not summary['manifest']['correctness_only']:
        for i,r in enumerate(records):
            anchor=summary['started_ns'] if i==0 else records[i-1]['response_return_ns']
            assert r['arrival_ns']-anchor>=round(t['calls'][i]['gap_before_seconds']*1e9)-1000000
        assert summary['report_ns']-records[-1]['response_return_ns']>=round(t['final_gap_seconds']*1e9)-1000000
        assert summary['task_wall_seconds']>=t['total_wait_seconds']
    assert summary['backend_close']['closed_event'] and not summary['backend_close']['forced_termination']
    result={'all_equal':all(c['equal'] for c in checks),'queries':checks,
            'uncompressed_relative_gaps':not summary['manifest']['correctness_only'],
            'future_only_objects':True,'clean_shutdown':True}
    (run/'correctness.json').write_text(json.dumps(result,indent=2)+'\n')
    return result
