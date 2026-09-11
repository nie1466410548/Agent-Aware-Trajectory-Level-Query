"""Prepare one new guided episode and freeze policy before any model calls."""
import argparse
import json
import shutil
import sqlite3
import time
from pathlib import Path
from agent_db_tool.dacomp import prepare
from agent_db_tool.handler import dump
from agent_db_tool.optimization.replay import sha, DEFAULT_CONFIG


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--preflight',required=True)
    a=p.parse_args();source=Path(a.source);preflight=Path(a.preflight)
    if source.exists() or preflight.exists():raise ValueError('use fresh paths')
    database=Path('benchmark/dacomp/fad-optimization/data/synthetic-10000000.sqlite').resolve()
    manifest=database.with_suffix('.manifest.json')
    digest=sha(database)
    if digest!='249b99438e16bc4fd750dd52a795e57f29ecd22f97d4a79f25a9478624dd78b6':raise ValueError('unexpected database')
    with sqlite3.connect(database.as_uri()+'?mode=ro',uri=True) as db:
        assert db.execute('PRAGMA quick_check').fetchone()[0]=='ok'
        assert db.execute('SELECT COUNT(*) FROM sheet1').fetchone()[0]==10000000
        catalog={'sheet1':[r[1] for r in db.execute('PRAGMA table_info(sheet1)')]}
    meta=prepare('dacomp-006',source,'benchmark/dacomp',version='0.2')
    assert meta['catalog']==catalog
    meta.update(original_task_database_sha256=meta['database_sha256'],database_path=str(database),database_sha256=digest)
    dump(source/'task_meta.json',meta)
    guidance=Path(__file__).with_name('task6-analysis-requirements.txt')
    prompt=source/'prompt.txt';prompt.write_text(prompt.read_text()+'\n\n'+guidance.read_text())
    dump(source/'collection_meta.json',{
        'rows':10000000,'database_sha256':digest,'data_manifest':str(manifest),
        'source_policy':'independent new Agent; guided analysis; ordinary SQL service without optimization',
        'model':'glm-custom/DeepSeek-V4-Flash-0731','prompt_sha256':sha(prompt),
        'guidance_sha256':sha(guidance),'previous_trajectories_provided':False,
        'analysis_compute_location':'SQL; no Python or model arithmetic for measured statistics',
        'formal_pairs':2,'target_query_count':None})
    freeze(source,preflight,digest)
    print(json.dumps({'source':str(source),'trajectory_id':meta['trajectory_id'],'preflight':str(preflight),'rows':10000000},indent=2))


def freeze(source,preflight,digest):
    assert not (source/'live-launch.json').exists() and not (preflight/'manifest.json').exists()
    guidance=Path(__file__).with_name('task6-analysis-requirements.txt').resolve().relative_to(Path.cwd())
    prompt=source/'prompt.txt'
    paths=sorted(Path('agent_db_tool/optimization').glob('*.py'))
    paths+=sorted(p for p in Path('agent_db_tool').iterdir() if p.is_file())
    paths += [guidance,prompt]
    hashes={str(p):sha(p) for p in paths}
    preflight.mkdir(exist_ok=True)
    for path in paths:
        dest=preflight/'source_snapshot'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,dest)
    shutil.copyfile('/tmp/fad-v15-guided-tests.log',preflight/'tests.log')
    dump(preflight/'manifest.json',{'created_at':time.time(),'source_hashes':hashes,
        'config':DEFAULT_CONFIG,'database_sha256':digest,'formal_pairs':2,
        'unit_tests_passed':77,'new_agent_run':str(source),'new_trajectory_contents_inspected':False,
        'policy_note':'multiple eligible builds within existing budgets; each object published after commit and matcher preparation; no future SQL/gaps; stop and cumulative time budget guarded'})


if __name__=='__main__':main()
