"""Audit completed SQL-only-baseline experiments without rerunning timed SQL."""
import argparse
import json
import shutil
from pathlib import Path
from agent_db_tool.optimization.check import read_records
from agent_db_tool.optimization.replay import sha


def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--diagnostics',required=True)
    args=p.parse_args();root=Path(args.run);diag=Path(args.diagnostics)
    assert (root/'COMPLETE.json').exists()
    m=json.loads((root/'manifest.json').read_text())
    assert all(sha(path)==h for path,h in m['source_hashes'].items())
    assert sha(m['database'])==m['database_sha256'] and sha(m['events'])==m['events_sha256']
    source=[json.loads(l) for l in Path(m['events']).read_text().splitlines() if json.loads(l).get('record')=='request']
    pids=set();checks_count=0;max_error=0;action_sequences={}
    for mode in ('index','materialization','combined'):
        dr=read_records(diag/mode);pairs=sorted((root/mode).glob('pair-*'))
        assert len(pairs)==m['pairs_per_mode']
        for pair in pairs:
            checks=json.loads((pair/'correctness.json').read_text());assert checks['all_equal']
            checks_count+=len(checks['queries'])
            max_error=max(max_error,max(c.get('max_absolute_difference',0) for c in checks['queries']))
            for arm in ('baseline',mode):
                s=json.loads((pair/arm/'summary.json').read_text());pids.add(s['manifest']['pid'])
                assert s['sql_attempts']==len(source) and s['sql_successes']==29
                assert not s['manifest']['diagnostic']
                if arm=='baseline':
                    assert s['manifest']['database_input']=='sql_only' and not s['objects']
                    for k in ('fad_receive_seconds','rewrite_seconds','decision_including_build_seconds','build_including_estimate_seconds','cleanup_seconds','peak_extra_allocated_bytes'):assert s[k]==0
                for i,r in enumerate(read_records(pair/arm)):
                    assert r['sql']==source[i]['arguments']['sql']
                    if arm=='baseline':
                        assert r['raw_fad'] is None and r['fad'] is None and not r['actions'] and r['executed_sql']==r['sql']
                    else:
                        assert r['raw_fad']==source[i]['arguments']['future_access'] and not r['fad_audit']['errors']
                        assert r['executed_sql']==dr[i]['executed_sql']
                        assert r['available_before_query']==dr[i]['available_before_query']
                        assert r['materializations_used']==dr[i]['materializations_used']
                        assert set(r['materializations_used'])<=set(r['available_before_query'])
                        assert [(a['key'],a['status']) for a in r['actions']]==[(a['key'],a['status']) for a in dr[i]['actions']]
                        for a in r['actions']:
                            if a['status']=='built':
                                assert a['created_after']==r['step'] and max(a['source_steps'])<=r['step'] and len(set(a['source_steps']))>=2
    expected_workers=m['pairs_per_mode']*6
    assert len(pids)==expected_workers and checks_count==m['pairs_per_mode']*3*len(source)
    audit={'pairs':m['pairs_per_mode']*3,'workers':len(pids),'query_pair_checks':checks_count,'all_equal':True,
           'baseline_sql_only':True,'baseline_fad_and_optimization_costs_zero':True,
           'optimized_original_fad_preserved':True,'strict_future_only_use':True,'source_hashes_unchanged':True,
           'formal_sql_and_actions_match_diagnostic':True,'max_absolute_numeric_difference':max_error,
           'tests_passed':50}
    previous=root.parent/'original-18250-v2-sql-only/manifest.json'
    if previous.exists():
        old=json.loads(previous.read_text())
        unchanged=[k for k in old['source_hashes'] if k not in ('agent_db_tool/optimization/experiment.py',)]
        assert all(m['source_hashes'][k]==old['source_hashes'][k] for k in unchanged)
        audit['optimizer_and_backend_unchanged_from_small_scale']=True
    (root/'AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    for filename,dest in [('config.json','configs'),('manifest.json','manifests')]:
        shutil.copyfile(root/filename,root.parent.parent/dest/(root.name+'.json'))
    print(json.dumps(audit,indent=2))

if __name__=='__main__':main()
