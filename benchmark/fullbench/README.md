# Full DAB trajectory study

The five-RQ offline characterization is in [Characterizing SQL Trajectories of Data Analysis Agents](reports/characterization/REPORT.md), with a [task-level CSV](reports/characterization/task-characterization.csv) and [query evidence](reports/characterization/EVIDENCE.md). Reproduce it with `benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/characterize.py`; this command does not invoke the agent or replay workload queries. It reads SQLite schema metadata to resolve hidden rowid columns without expanding them into SELECT *.

This cohort runs the 54 tasks in the pinned upstream README's official 12-dataset benchmark table, once with the natural Kimi agent and once with the cooperative FAD protocol (108 fresh episodes). The repository also contains 50 additional tasks in five datasets not included in that table; a scope clarification was requested. Until changed, this cohort follows the previously discussed official 54-task scope. Exact tasks, sources and data hashes are in `tasks.json`.

- Model: existing authenticated Kimi CLI, `kimi-code/k3`; no hints; fresh run directory and session.
- Three concurrent processes; each episode has a 15-minute wall limit and at most 30 query-db attempts. Completed failed answers are retained without answer-driven retries.
- Existing nine-task results remain under `benchmark/quickcheck/`; this cohort reruns those tasks, rather than mixing old and new adapters.
- PostgreSQL: dedicated `dab-bookreview-pg`, 127.0.0.1:55439, read-only `dab_reader`. SQLite/DuckDB files open read-only. MongoDB: dedicated `dab-full-mongo`, 127.0.0.1:55440; the adapter supports native read operations only and rejects `$out`/`$merge` pipelines. Python runs on host, with prompt restrictions, not an OS sandbox.
- MongoDB requests are retained separately from SQL. They must not be counted as SQL or silently omitted from episode/FAD reporting.
- Every SQL statement in a multi-statement call now has its own saved result. The primary response retains the last statement's result for compatibility; full SQL and all statement result paths remain in the log.
- FAD is an intervention: it can change query choice and adds overhead. It is not passive forecasting of the natural agent. SQL/Mongo receipt order is audited from visible messages.
- The same pinned data and validators are used. Data downloads are hash-checked where the manifest supplies SHA-256; non-manifest files come from the fixed Git tree. No gold or validators are supplied to the agent; validation runs after the episode.

## Live state

`reports/batch-status.json` records queued/active/completed jobs; `reports/batch-process.json` and per-run `process.json` record process IDs. Check live processes as well as status files before resuming an interrupted batch. `reports/batch.log` is the human-readable progress log.

## Artifacts per episode

`runs/GROUP/DATASET/queryN/full-01/` contains task metadata, prompt/profile, `kimi.jsonl`, tool calls, SQL and native Mongo requests, complete results, Python source snapshots and final answer. Analyses are written only after the external validation report exists.

Final reports will use the agreed task-first tables: task, group, validator result, successful SQL, shared table, bound table-column, WHERE conjunct, Join fragment, repeated aggregate expression, GROUP BY and equal result rows. Column definitions are included. Structural matches remain separate from concrete multi-query preparation hypotheses, with consumer SQL evidence and no unmeasured speedup claims. Additional tables cover native Mongo requests, FAD, runtime/rounds, schema/row counts and errors.

## Commands

```bash
python3 benchmark/fullbench/tools/prepare.py --scope core
benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/setup_databases.py
benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/run_batch.py
benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/analyze.py
```

## Instrumentation incident and repair

Natural CRM query7 first attempt left its assigned directory and created alternate metadata/logs under the older pilot tree. It was terminated, archived under `incidents/natural-crmarenapro-query7-attempt1/`, and excluded from the primary cohort. The retained CLI transcript and copied external logs document the deviation. It requires one fresh recovery run after the main batch; this is an instrumentation recovery, not a retry to improve an incorrect answer.

Adapter v2 binds run directory, task and group through launcher environment variables. A read-only smoke test with a conflicting working directory verified that SQL and logs remain bound to the assigned task. Runs already started under v1 are retained and audited; future runs declare `fullbench-v2-bound-run` in metadata. This measurement change and mixed adapter versions must be disclosed in final results.

## Reproducibility records

`reports/source-integrity.json` verifies 259 pinned input/source files (manifest SHA-256/size for large data, Git blob SHA-1 for remaining pinned files). `reports/environment.json` records Python, library, Kimi CLI and container image versions without credentials. The final reports disclose adapter v1/v2 and the one instrumentation recovery.
