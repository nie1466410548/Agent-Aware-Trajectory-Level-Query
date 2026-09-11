"""Independent post-run audit; no SQL execution inside measured trials."""
import argparse
import json
from pathlib import Path
from agent_db_tool.optimization.async_check import check
from agent_db_tool.optimization.replay import sha, DEFAULT_CONFIG
from agent_db_tool.optimization.check import compare_results
import sqlglot
import sqlite3
from agent_db_tool.optimization.patterns import receive


def read(p):return json.loads(Path(p).read_text())

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();root=Path(a.run)
    manifest=read(root/'manifest.json');timing=read(manifest['timing']);complete=read(root/'COMPLETE.json')
    assert complete['all_equal'] and complete['pairs']==manifest['pairs']
    assert sha(manifest['database'])==manifest['database_sha256']==timing['source_database_sha256']
    assert sha(manifest['timing'])==manifest['timing_sha256']
    source=Path(timing['source_run']);assert read(source/'summary.json')['answer_submitted']
    assert sha(source/'events.jsonl')==timing['source_events_sha256']
    assert sha(source/'agent.jsonl')==timing['source_client_sha256']
    for path,h in manifest['source_hashes'].items():
        assert sha(path)==h and sha(root/'source_snapshot'/path)==h
    db=sqlite3.connect('file:'+manifest['database']+'?mode=ro',uri=True)
    catalog={name:[r[1] for r in db.execute('PRAGMA table_info("'+name.replace('"','""')+'")')] for (name,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()}
    db.close()
    pids=set();runs=[];last_closed=0
    for job in manifest['execution_order']:
        for arm in job['arms']:
            run=root/f"pair-{job['pair']:02d}"/arm;s=read(run/'summary.json');t=read(run/'timeline.json')
            assert s['manifest']['pid'] not in pids;pids.add(s['manifest']['pid'])
            assert s['started_ns']>=last_closed;last_closed=s['closed_ns']
            assert s['manifest']['affinity']==manifest['affinity']
            assert s['manifest']['journal_mode']=='WAL' and s['manifest']['config']==manifest['config']
            assert s['manifest']['timing_sha256']==manifest['timing_sha256']
            assert s['manifest']['database_sha256']==manifest['database_sha256']
            c=check(run,manifest['timing']);assert c['all_equal'] and (c['uncompressed_relative_gaps'] or c.get('reused_idle_gaps'))
            delivered={q['step']:q['fad_delivered_ns'] for q in t['queries']}
            waits=t['waits'];assert len(waits)==len(timing['calls'])+1
            requested=[x['gap_before_seconds'] for x in timing['calls']]+[timing['final_gap_seconds']]
            assert [w['requested_seconds'] for w in waits]==requested
            for q,w in zip(t['queries'],waits):assert w['ended_ns']<=q['arrival_ns']
            objects={e['object']['name']:e['object'] for e in t['background'] if e['type']=='object_ready'}
            by_step={q['step']:q for q in t['queries']}
            for e in t['background']:
                if e['type']=='fad_validated':
                    expected,audit=receive(by_step[e['step']]['raw_fad'],catalog)
                    assert e['fad']==expected and e['audit']==audit
                if e['type'] in ('fad_validated','decision','build_started'):
                    assert e['started_ns']>=delivered[e['step']]
                if e['type']=='object_ready':
                    o=e['object'];assert o['created_after']==e['step']
                    assert all(step<=o['created_after'] for step in o['source_steps'])
            used={}
            for q in t['queries']:
                used[q['step']]=[name for name in objects if name in str(q['plan'])]
                for name in used[q['step']]:
                    obj=objects[name];assert obj['created_after']<q['step']
                    if obj['kind']=='index':
                        assert name in q['snapshot_indexes']
                        # All observed builds in this experiment finished before use.
                        # General SQLite visibility can precede CREATE execute return.
                        assert obj['commit_return_ns']<=q['snapshot_start_ns']
                    else:assert obj['ready_ns']<=q['snapshot_start_ns']
            if arm=='baseline':
                assert not t['background'] and not objects
                assert all(q['raw_fad'] is None and q['plan'] is None and q['executed_sql']==q['sql'] for q in t['queries'])
            runs.append({'pair':job['pair'],'arm':arm,'queries':len(t['queries']),
                         'all_equal':True,'relative_gaps_preserved':True,'idle_gaps_reused':manifest.get('skip_idle',False),'objects_used_by_query':used})
    paired=[]
    for job in manifest['execution_order']:
        pair=root/f"pair-{job['pair']:02d}"
        bt=read(pair/'baseline/timeline.json')['queries'];ot=read(pair/'combined/timeline.json')['queries']
        for b,o in zip(bt,ot):
            assert b['sql']==o['sql'] and b['step']==o['step'] and b['status']==o['status']
            q=b['step']
            rows=lambda arm:[json.loads(line) for line in (pair/arm/'results'/f'Q{q}.jsonl').read_text().splitlines()]
            if b['status']=='ok':
                result=compare_results(rows('baseline'),rows('combined'),b['columns'],o['columns'],
                    bool(sqlglot.parse_one(b['sql'],read='sqlite').args.get('order')),
                    DEFAULT_CONFIG['absolute_tolerance'],DEFAULT_CONFIG['relative_tolerance'])
                assert result['equal'],result
            else:
                assert b['error']==o['error'];result={'equal':True,'reason':'same original error'}
            paired.append({'pair':job['pair'],'step':q,**result})
    result={'paired_query_comparisons':paired,'all_passed':True,'pairs':manifest['pairs'],'replayed_queries_compared_to_source':sum(r['queries'] for r in runs),
            'timing_method':'reconstructed_with_reused_idle_gaps' if manifest.get('skip_idle') else 'full_wall_clock','database_unchanged':True,'source_and_timing_unchanged':True,'code_matches_snapshot':True,
            'distinct_processes':len(pids),'arms_nonoverlapping':True,'baseline_has_no_fad_handling':True,'delivered_fad_matches_audited_reception':True,
            'object_use_follows_originating_fad_and_commit':True,'all_background_workers_closed_cleanly':True,'runs':runs}
    (root/'AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('runs','paired_query_comparisons')},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
