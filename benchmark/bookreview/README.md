# Kimi × DAB bookreview pilot

See [PLAN.md](PLAN.md) for environment findings and scope. The original benchmark is [ucbepic/DataAgentBench](https://github.com/ucbepic/DataAgentBench); the pinned revision and verified data hashes are in `upstream/source.json`.

## Files

- `upstream/`: task inputs, original validators/answers (evaluation-side only), and databases.
- `tools/download.py`: pinned download with SHA256 verification, including Git LFS objects.
- `tools/setup_db.py`: one-time import into the dedicated `dab-bookreview-pg` container. Not idempotent; do not rerun against an initialized database.
- `tools/tool.py`: logged database/Python/answer adapter.
- `tools/run_task.py`: fresh Kimi session per task and external validation.
- `tools/summarize.py`: per-call `.sql` files, indexes, and descriptive summary.
- `runs/queryN/RUN/`: prompt, configuration, Kimi JSONL, raw tool log, full results and submitted answer.
- `runs/_smoke/`: initialization checks, excluded from task measurements.
- `reports/`: import log, external validator outcomes, aggregate summary.

## Run

The current instance uses PostgreSQL on `127.0.0.1:55439`, the read-only role `dab_reader`, and read-only SQLite. Kimi CLI reuses the existing user login and model `kimi-code/k3`. Network and Docker access require execution outside Codex's sandbox.

```bash
python3 benchmark/bookreview/tools/run_task.py 1 --run-id another-run
python3 benchmark/bookreview/tools/run_task.py 2 --run-id another-run
python3 benchmark/bookreview/tools/run_task.py 3 --run-id another-run
python3 benchmark/bookreview/tools/summarize.py
```

Run identifiers must be new. Each task has a 15-minute wall-clock limit. Agent sessions use a task-specific profile with data-analysis instructions, no subagents, an empty skills directory, and Bash/file tools. This changes the default coding-agent system prompt and is part of the experimental configuration. The adapter's Python runner uses the project Python 3.11 virtual environment with host pandas/PyArrow, so this is not an exact reproduction of the reference scaffold.

## Metrics and limits

`duration_ms` is adapter wall time, including result handling; `execute_return_ms` and `execute_fetch_ms` are driver-side timings, not isolated server execution time. PostgreSQL buffers results differently from SQLite, so do not directly compare the two timing phases across engines. PostgreSQL also logs statements and durations in the container for later checks.

All tools, including errors and Python code, are logged. Successful query output is a JSON list of row objects; a 10,000-character preview is returned to the model, with the full result available by path. The adapter preserves the original query text. SQL exports include metadata/list-table queries and have a `tool` field in their index to separate those from `query-db` calls.

Exact-repeat counts compare literal SQL plus database identity, only within a run and only among successful calls. They do not establish predicate containment, shared intermediate results, or physically reusable computations. Do not merge separate tasks or repetitions into a single trajectory.

The upstream validators use answer inclusion checks; passing does not establish exact answer-set equality or prove reasoning correctness. Review the trace and computation before stronger claims. The agent is instructed not to read upstream or evaluation files, but the host run is not a filesystem isolation boundary. Preserve and audit CLI tool calls for adherence.

## Container lifecycle

The pilot container is dedicated and contains only benchmark data. Keep it running for further experiments; to release its runtime resources:

```bash
docker stop dab-bookreview-pg
```

Use `docker start dab-bookreview-pg` to resume without reimporting. No existing databases or user Agent configuration are modified by the setup scripts. Kimi itself writes its usual session/log state under the user's Kimi home.
