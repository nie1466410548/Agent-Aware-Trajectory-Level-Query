# 9-task quick feasibility check

This experiment implements the approved quick-check plan: one natural and one FAD run per task, using Kimi CLI 0.41.0 and model `kimi-code/k3`, no hints, fresh sessions, identical base instructions and data tools. The task-specific Kimi profile permits Bash/Read/Write/Edit, disables subagents, and uses an empty skills directory.

## Predeclared tasks

| Dataset | Task IDs | Reason selected from task text |
|---|---|---|
| bookreview | 1, 2, 3 | Known working environment; book metadata and review analysis |
| crmarenapro | 8, 12, 13 | Case assignments, opportunity/contract cycle, order sales; multi-relation metrics |
| stockindex | 1, 2, 3 | Time ranges, volatility, up/down days, investment returns |

Selection occurred before agent execution/overlap inspection. This is a purposive sample, not a random sample of DAB or production traffic. The pinned upstream commit is `b24c8f5586121d4d2f8a5a793ebac530858dd1ab`; `tasks.json` includes data hashes. Original validators are only invoked by the controller after the episode ends.

## Execution and rerun

```bash
python3 benchmark/quickcheck/tools/prepare.py
python3 benchmark/quickcheck/tools/run_batch.py
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/analyze.py
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/report.py
```

The batch uses three independent processes, alternates group order by task, and retains completed reports. It does not silently retry unsuccessful agent answers. Run a new episode with `run_task.py DATASET ID GROUP --run-id NEW_ID`; the main analysis currently targets `quick-01` to preserve the registered cohort. Interrupted directories should be inspected rather than overwritten.

PostgreSQL reuses the dedicated bookreview container at localhost:55439 and the read-only role `dab_reader`. CRM support data is imported into a separate database. SQLite and DuckDB files open read-only. Host Python 3.11.6, pandas 3.0.3, PyArrow 24.0.0, psycopg2-binary 2.9.12, DuckDB 1.3.1, SQLGlot 30.18.0 are used. These are custom Kimi adapter runs, not exact reproduction of the upstream Python 3.12 scaffold. Python runs in the episode working directory on the host. Access restrictions are instructions, not an OS sandbox; review CLI traces for adherence.

Each episode has a 15-minute wall-time limit and a prompt budget of 30 database calls. The adapter limits query-db attempts to 30 and returns complete results by file, with previews capped at 10,000 characters. All starts, ends, SQL, errors, results and Python source are logged. Duration is observational adapter wall time; it includes connection and result processing, excludes process launch, and is not server-only time. Concurrent episodes share host/DB resources and warm caches: duration differences are not causal performance comparisons.

## FAD protocol

Before each query-db call, the agent submits an `accesses` list containing database, tables, columns, filters, operations and horizon (1–3); `unknowns` can state unavailable information. Empty predictions are allowed. The tool returns a fresh random receipt. The agent must wait for the response, generate SQL in a new assistant turn, and cite that receipt. The receipt authorizes one query attempt. list-db is exempt. Metadata query-db calls still require a receipt, but metadata-targeting forecasts are excluded from primary data-access scoring.

Raw CLI message order is audited in addition to tool timestamps. This proves a visible protocol boundary, not that the model had not internally contemplated the SQL. The requirement to announce intentions can influence what it subsequently queries. No claim of counterfactual forecasting or stable cross-model calibration follows from high next-query accuracy.

## Analysis definitions

- Query counts separate metadata (information_schema, PRAGMA, SHOW, etc.), successful data queries, failed attempts and empty results.
- Within-trajectory overlap pairs compare successful data queries in the same logical database. Shared tables, columns, exact WHERE/Join/aggregate strings are structural candidates, not verified physical reuse. Pair counts must not be confused with the fraction of queries: summary uses distinct later consumer queries.
- Canonical equality preserves literal case. Simple result-reuse witnesses require complete single-table producers, compatible projected columns and equal/additional conjuncts; sampling producers are excluded. These conservative witnesses are not exhaustive (e.g. aggregation rollups are not implemented).
- Table atoms are `(logical database, table name)`. FAD precision/recall is set matching against the union of the next 1 or 3 issued query-db statements. Aliases/CTEs are excluded from base table sets. Table names are simplified; manually check ambiguous schemas.
- Column and operation scores compare the forecast entries relevant to the next query's database/tables. Columns use identifier matching, not expression equivalence. Filter scores are exact normalized conjunct matching with qualifiers removed; equivalent ranges/functions can be false negatives. Filter checks do not prove containment.
- Later-frontier scores evaluate only entries explicitly marked horizon 2 or 3 against the second/third query-db statements, excluding the immediately next query. Near episode end, unconsumed predictions count as unfulfilled.
- A last-query-table baseline is a deliberately weak history-only comparator, not a trained predictor or task-aware baseline.
- Lead time is FAD completion to next query submission, including agent generation/tool overhead. It is not measured time saved. Empty/missing predictions and denominators are recorded.
- Primary FAD scores concern issued SQL, including failures; failure counts are reported. Raw per-frontier records allow success-only recomputation. Per-task tables are needed alongside pooled means.

Outputs: `reports/analysis.json`, per-run `analysis.json`, `sql/*.sql`, original `kimi.jsonl`, `tool_calls.jsonl`, complete `results/`, prompts/profiles and external validation reports. Official validators mostly check answer inclusion, so a passing result is not full independent correctness proof.

Tests: `benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/test_analyze.py` checks literal-case preservation, sample/full-result distinction projection compatibility, and disjoint range detection.

## Completed quick-01 results

See [Findings](reports/FINDINGS.md) and [Tables](reports/TABLES.md). All 18 episodes completed; both groups passed 7/9 original validators. Tool result digests and all 146 SQL exports were checked.

Database locations, exact row counts, columns and read-only inspection commands: [DATA.md](reports/DATA.md).

Current multi-query opportunity review: [OVERLAP.md](reports/OVERLAP.md) and [per-candidate SQL evidence](reports/OPPORTUNITY_CASES.md). Recompute with `benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/opportunity_report.py`. The manually reviewed catalogue is `tools/opportunity_catalog.py`; this is not an exhaustive automatic optimizer. The old `overlap_report.py` now writes only `reports/OVERLAP-structural-v1.md`; its structural-match counts must not be interpreted as optimization opportunities.
