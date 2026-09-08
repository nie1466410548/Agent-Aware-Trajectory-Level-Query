"""Run one isolated natural Kimi episode; no automatic retry or paid grading."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('task', choices=['dacomp-006','dacomp-003','dacomp-004','dacomp-005'])
    parser.add_argument('--run-id', default='pilot-01')
    parser.add_argument('--timeout', type=int, default=1200)
    args = parser.parse_args()
    run = ROOT / 'runs' / 'natural' / args.task / args.run_id
    run.mkdir(parents=True, exist_ok=False)
    (run / 'empty-skills').mkdir()
    task = json.loads((ROOT / 'upstream' / args.task / 'task.json').read_text())
    schema = json.loads((ROOT / 'upstream' / args.task / 'schema.json').read_text())
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    meta = {'task_id': args.task, 'run_id': args.run_id, 'group': 'natural', 'model': 'kimi-code/k3',
            'adapter_version': 'dacomp-v1', 'query_attempt_limit': 80, 'timeout_s': args.timeout,
            'upstream_revision': manifest['revision'],
            'database_sha256': next(t['database_sha256'] for t in manifest['tasks'] if t['task_id']==args.task)}
    (run / 'task_meta.json').write_text(json.dumps(meta, indent=2)+'\n')
    tool = f'{ROOT}/.venv/bin/python {ROOT}/tools/tool.py'
    prompt = f'''You are a data analysis agent. Complete the task independently using the supplied SQLite database. Do not delegate or ask the user questions. Finish within {args.timeout//60} minutes and at most 80 database query attempts. Submit the best supported report if you reach a limit.

ORIGINAL TASK:
{task['instruction']}

DATABASE SCHEMA:
{chr(10).join(t['ddl'] for t in schema)}

DATA TOOLS (invoke via Bash):
{tool} list-db
{tool} query-db --sql-file query.sql
{tool} python --file analysis.py
{tool} answer --file report.md

Use Write or Bash to create files in this working directory. All database access must go through list-db or query-db; submit exactly one SQLite statement per query call. Use distinct output aliases. Each response includes a preview and a result_file containing the complete JSON list of row objects. Python can read these result files and your own generated files; available packages include pandas, numpy, scipy, matplotlib and seaborn. Execute analysis Python through the python tool. Choose how to divide computation between SQL and Python naturally. Make any charts needed for your analysis and save them in this directory, referencing them by relative paths in your report.

Use only the task, schema, tools, returned data and files you create. Do not access parent directories, benchmark source, tool implementation, reference reports, evaluation files, prior runs, external websites or credentials. Do not install packages or open a database directly in Python or shell. These are evaluation integrity requirements, not a security sandbox.

When finished, write a Markdown report with data-backed findings and limitations, submit it using the answer tool, and stop. Do not generate future-access predictions. Do not add computations solely to increase the number of queries.
'''
    (run / 'prompt.txt').write_text(prompt)
    (run / 'agent.md').write_text('''---
name: dacomp-natural
description: Solve the supplied analysis task using logged tools.
tools:
  - Bash
  - Read
  - Write
  - Edit
subagents: []
---
Follow the task and logged data-tool protocol. Work within the assigned episode directory. Base conclusions on executed analysis.
''')
    cmd = ['/data/nly/.kimi-code/bin/kimi', '--model', 'kimi-code/k3', '--skills-dir', str(run/'empty-skills'),
           '--agent-file',str(run/'agent.md'),'--prompt',prompt,'--output-format','stream-json']
    start = time.time()
    with (run/'kimi.jsonl').open('w') as out, (run/'kimi.stderr.log').open('w') as err:
        proc = subprocess.Popen(cmd, cwd=run, stdout=out, stderr=err, start_new_session=True,
                                env={**os.environ,'DACOMP_RUN_DIR':str(run),'DACOMP_TASK_ID':args.task})
        (run/'process.json').write_text(json.dumps({'pid':proc.pid,'started_at':start}))
        timeout = False
        try:
            exit_code = proc.wait(timeout=args.timeout)
        except subprocess.TimeoutExpired:
            timeout = True
            os.killpg(proc.pid,signal.SIGTERM)
            try: exit_code=proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid,signal.SIGKILL)
                exit_code=proc.wait()
    calls = [json.loads(l) for l in (run/'tool_calls.jsonl').read_text().splitlines()] if (run/'tool_calls.jsonl').exists() else []
    quota = any(x in (run/'kimi.stderr.log').read_text().lower() for x in ['quota','usage limit','rate limit'])
    summary = {**meta,'exit_code':exit_code,'timed_out':timeout,'quota_error_suspected':quota,
               'duration_s':time.time()-start,'answer_submitted':(run/f'{args.task}.md').exists(),
               'query_attempts':sum(c['tool']=='query-db' for c in calls),
               'query_limit_reached':any(c.get('limit_reached') for c in calls),
               'official_evaluation':'not_run'}
    (run/'run_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary),flush=True)


if __name__=='__main__':
    main()
