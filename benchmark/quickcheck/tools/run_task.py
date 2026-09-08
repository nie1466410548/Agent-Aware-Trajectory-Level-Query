"""Launch one fresh Kimi CLI session and validate its submitted answer externally."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('dataset',choices=['bookreview','crmarenapro','stockindex'])
parser.add_argument('task', type=int)
parser.add_argument('group',choices=['natural','fad'])
parser.add_argument('--run-id', default='quick-01')
args = parser.parse_args()
task_id = f'{args.dataset}/query{args.task}'
run = ROOT / 'runs' / args.group / args.dataset / f'query{args.task}' / args.run_id
run.mkdir(parents=True, exist_ok=False)
(run/'empty-skills').mkdir()
meta = {'task_id':task_id,'run_id':args.run_id,'model':'kimi-code/k3','group':args.group,
        'hints':False,'upstream_commit':json.loads((ROOT/'tasks.json').read_text())['commit']}
(run/'task_meta.json').write_text(json.dumps(meta,indent=2))
question = json.loads((ROOT/f'upstream/query_{args.dataset}/query{args.task}/query.json').read_text())
description = (ROOT/f'upstream/query_{args.dataset}/db_description.txt').read_text()
tool = f'{ROOT.parent}/bookreview/.venv/bin/python {ROOT}/tools/tool.py'
prompt = f'''Solve this data analysis task using the supplied databases. Work independently, without asking the user questions. Use at most 30 database calls and finish within 15 minutes. Do not delegate to other agents.

TASK: {question}

DATABASE DESCRIPTION:
{description}

DATA TOOLS (invoke through Bash):
{tool} list-db DATABASE_NAME
{tool} query-db DATABASE_NAME --sql-file query.sql
{tool} python --file analysis.py
{tool} answer --file final.txt

You may also pass --sql with a correctly quoted SQL string instead of --sql-file. Use Bash to create your SQL and Python files in the current directory. All actual database access must use query-db or list-db above. Run analysis Python only through the python tool above. Python can use pandas, pyarrow and the standard library; it can read full query results from the result_file paths returned by the data tools. Those JSON files contain lists of row objects. SQL output is previewed up to 10000 characters; the complete data remains in result_file.

Use only this task description, these tools, and files you create or tool result files in this run directory. Do not inspect parent directories, benchmark source, tool source, validators, gold answers, external websites, user history, or previous sessions. Do not install packages or connect to the databases directly. These restrictions maintain evaluation integrity. Do not optimize for repetition or deliberately split queries: solve the task naturally. DATABASE_NAME is a logical name from the description above, not a physical file name. For DuckDB metadata use information_schema; for SQLite use PRAGMA table_info; for PostgreSQL use information_schema. Do not invoke shell clients directly.

After analysis, write the final answer to final.txt and submit it with the answer tool. Include any requested complete book list. Then stop. If unable to solve, submit your best supported answer and state the limitation. Do not inspect evaluation results.
'''
if args.group=='natural':
    prompt+='\nDo not generate extra future-access predictions.\n'
else:
    prompt+=f'''
FAD GROUP PROTOCOL:
Before EACH query-db call, first publish a short rolling future-access frontier using:
{tool} fad --file frontier.json
The file must be JSON: {{"accesses":[{{"database":"logical name","tables":["table_name"],"columns":["column_name"],"filters":["known condition in SQL-like notation"],"operations":["scan","filter","join","aggregate","sort","limit","metadata"],"horizon":1}}],"unknowns":[]}}
Use only operations that you actually anticipate, not all operations in the example. Describe likely accesses over the next 1-3 data queries. horizon is the expected position (1, 2 or 3); use an empty accesses list when genuinely unknown. Table/column names should be schema-grounded when known, otherwise leave them empty and explain in unknowns. Filters and operations should be concrete enough to help prepare data; do not put complete SQL in the frontier. Include plausible later accesses if known, but do not invent them to fill the frontier.
Crucially, submit FAD and WAIT for its tool response BEFORE writing, emitting, or executing the SQL, including SQL files. After receiving its fresh random fad_id, generate the SQL in a NEW assistant turn and invoke query-db with --fad-id RECEIVED_ID. A receipt permits exactly one query attempt; refresh after each result/error before generating the next SQL. Do not put SQL generation and FAD submission in the same assistant message/tool batch. list-db is exempt. You may revise or drop previous candidates based on results. Continue solving naturally; predictions are not commitments to execute unnecessary queries.
'''
(run/'prompt.txt').write_text(prompt)
profile = '''---
name: dab-quickcheck
description: Solve the supplied data analysis task using the logged data tools.
tools:
  - Bash
  - Read
  - Write
  - Edit
subagents: []
---
You are a data analysis agent. Follow the supplied task and data-tool protocol. Base the answer on executed data operations. Do not access evaluation answers or delegate. Use the run directory for temporary files.
'''
(run/'agent.md').write_text(profile)
cmd=['/data/nly/.kimi-code/bin/kimi','--model','kimi-code/k3',
     '--skills-dir',str(run/'empty-skills'),'--agent-file',str(run/'agent.md'),
     '--prompt',prompt,'--output-format','stream-json']
start=time.time()
with (run/'kimi.jsonl').open('w') as out, (run/'kimi.stderr.log').open('w') as err:
    proc=subprocess.Popen(cmd,cwd=run,stdout=out,stderr=err,start_new_session=True)
    timed_out=False
    try: code=proc.wait(timeout=900)
    except subprocess.TimeoutExpired:
        timed_out=True
        os.killpg(proc.pid,signal.SIGTERM)
        try: code=proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGKILL)
            code=proc.wait()
answer_path=run/'answer.txt'
answer=answer_path.read_text() if answer_path.exists() else ''
spec=importlib.util.spec_from_file_location('validator',ROOT/f'upstream/query_{args.dataset}/query{args.task}/validate.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
passed,reason=module.validate(answer) if answer else (False,'No answer submitted')
calls=[json.loads(s) for s in (run/'tool_calls.jsonl').read_text().splitlines()] if (run/'tool_calls.jsonl').exists() else []
report={**meta,'exit_code':code,'timed_out':timed_out,'duration_s':time.time()-start,
        'answer_submitted':answer_path.exists(),'validator_passed':passed,'validator_reason':reason,
        'tool_calls':len(calls),'sql_calls':sum('sql' in c for c in calls),
        'failed_calls':sum(not c['success'] for c in calls)}
(ROOT/'reports'/f'{args.group}-{args.dataset}-query{args.task}-{args.run_id}.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
