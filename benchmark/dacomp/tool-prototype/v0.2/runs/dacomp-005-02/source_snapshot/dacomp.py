"""Prepare a fresh DAComp episode without copying gold reports or prior traces."""
import hashlib
import json
import sqlite3
import sys
import time
import uuid
from pathlib import Path

from .handler import dump
from .validation import ROOT


def prepare(task, run, benchmark, mode='hints', max_candidates=8, version='0.1'):
    if version not in ('0.1', '0.2'):
        raise ValueError('Unsupported schema version')
    benchmark, run = Path(benchmark).resolve(), Path(run).resolve()
    if not task.startswith('dacomp-') or len(task) != 10 or not task[7:].isdigit():
        raise ValueError('Expected dacomp-NNN')
    source = benchmark / 'upstream' / task
    database = (source / f'{task}.sqlite').resolve(strict=True)
    question = json.loads((source / 'task.json').read_text())['instruction']
    catalog, ddls = {}, []
    conn = sqlite3.connect(database.as_uri() + '?mode=ro', uri=True)
    try:
        check = conn.execute('PRAGMA quick_check').fetchone()[0]
        if check != 'ok':
            raise ValueError('Database quick_check failed')
        for name, ddl in conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
            catalog[name] = [r[1] for r in conn.execute('SELECT * FROM pragma_table_info(?)', (name,))]
            ddls.append(ddl)
    finally:
        conn.close()
    if mode not in ('hints', 'sql-only') or not 1 <= max_candidates <= 64:
        raise ValueError('Invalid mode or max_candidates (1..64)')
    digest = hashlib.sha256()
    with database.open('rb') as dbfile:
        for block in iter(lambda: dbfile.read(1024*1024), b''):
            digest.update(block)
    # Refuse overwrite; don't put task databases or evaluator files in the workspace.
    run.mkdir(parents=True, exist_ok=False)
    meta = {'schema_version': version, 'trajectory_id': uuid.uuid4().hex, 'task_id': task,
            'mode': mode, 'created_at': time.time(), 'database_path': str(database),
            'database_sha256': digest.hexdigest(), 'catalog': catalog,
            'max_candidates': max_candidates, 'query_attempt_limit': 80,
            'sql_timeout_s': 120, 'result_limit_bytes': 16*1024*1024,
            'official_evaluation': 'not_run', 'harness': f'agent-db-tool-v{version}-sql-report-only',
            'source_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ROOT.iterdir()) if p.is_file()}}
    dump(run / 'task_meta.json', meta)
    snapshot = run / 'source_snapshot'
    snapshot.mkdir()
    for p in ROOT.iterdir():
        if p.is_file():
            (snapshot/p.name).write_bytes(p.read_bytes())
    (run / 'workspace').mkdir()
    prompt = ('Complete the following data analysis task using only the supplied DB tools. '
              'Use db_query for all database access, read_result to inspect full results, '
              'and submit_answer to submit a Markdown report. Stop after submission. '
              'Base conclusions on actual results. Do not add queries merely to lengthen the trajectory. '
              'You have at most 80 SQL attempts. This prototype provides SQL and report submission, '
              'but no Python or figure generation; state any resulting limitations.\n\n'
              'TASK:\n' + question + '\n\nDATABASE SCHEMA:\n' + '\n'.join(ddls))
    if mode == 'hints':
        filename = 'instructions-v0.2.md' if version == '0.2' else 'instructions.md'
        prompt += '\n\n' + (ROOT / filename).read_text().replace('{max_candidates}', str(max_candidates))
    else:
        prompt += '\n\nDo not generate future-access predictions.\n'
    (run / 'prompt.txt').write_text(prompt)
    # This snippet contains no provider credentials; merge it in the chosen Agent client.
    dump(run / 'mcp-config.json', {'mcp': {'agentdb': {'type': 'local',
        'command': [sys.executable, str(ROOT / 'entry.py'), 'serve', '--run', str(run)],
        'enabled': True, 'timeout': 130000}}})
    return meta
