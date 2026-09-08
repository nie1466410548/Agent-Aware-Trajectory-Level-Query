# Bookreview pilot — environment and execution plan

Checked 2026-09-07 as user `nly` on openEuler 24.03.

## Environment findings

- Host Python 3.11.6; SQLite library 3.42.0; pandas and PyArrow importable.
- No conda, uv, PostgreSQL client/server on PATH, or psycopg2 Python driver.
- Docker client/server 25.0.3 work outside the execution sandbox.
- Existing `postgres:17` image; create a dedicated container, leaving existing services alone.
- Approximately 24 TB free disk and 625 GiB available host memory at inspection time (shared host, not reserved resources).
- Kimi CLI 0.41.0 installed; `kimi doctor` passes. Default configured model `kimi-code/k3`.
- Kimi provider credentials configured; live model connectivity still needs validation.
- Network downloads work through the existing proxy outside the execution sandbox.

## Plan

1. Fetch only bookreview from upstream commit `b24c8f5586121d4d2f8a5a793ebac530858dd1ab`; verify the two data files against the upstream SHA256 manifest.
2. Use a project virtual environment and a dedicated PostgreSQL 17 container. Import books once; expose read-only access for the agent. Open SQLite read-only.
3. Provide Kimi a Bash-based tool adapter for database queries, listing tables, Python execution, and submitting an answer. Persist raw queries, timing, results, errors, and CLI JSONL.
4. Run three independent Kimi sessions, one per task, with no gold answers or validator contents in their supplied context. Use the standard database description without hints for this pilot.
5. Run the original validators separately, summarize correctness and query counts, and retain all successful/failed calls for overlap analysis.

## Pilot interpretation

This is Kimi Code plus a custom logged adapter, not the upstream reference agent. Host Python 3.11 is used instead of upstream Python 3.12. Python executes in a per-run working directory on the host for this pilot, not the upstream Docker sandbox. SQL result previews are limited to 10,000 characters; full results are persisted. Do not report official reference-agent performance or full-benchmark results from this pilot. Existing Kimi login is reused; credentials are never written into the report.

The agent is instructed to use only the adapter and its own run directory; this is a protocol restriction, not an OS security boundary. Query execution uses actual database read-only permissions. Database initialization and validation are excluded from the agent trace. First inspect the trace before treating the sample as valid. Timing is observational, with no cold-cache guarantee.
