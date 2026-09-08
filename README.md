# Agent-Aware Trajectory-Level Query Processing

Research notes, slides, experiment tooling, and recorded Data Analysis Agent SQL trajectories.

## Start here

- [Five-RQ workload characterization](benchmark/fullbench/reports/characterization/REPORT.md)
- [Task-level characterization CSV](benchmark/fullbench/reports/characterization/task-characterization.csv)
- [Query and materialization evidence](benchmark/fullbench/reports/characterization/EVIDENCE.md)
- [Full benchmark setup and artifacts](benchmark/fullbench/README.md)
- [Task-level overlap report](benchmark/fullbench/reports/OVERLAP.md)
- [Original full-cohort trajectories](benchmark/fullbench/runs/)
- [Archived interrupted attempts](benchmark/fullbench/incidents/)

The full cohort contains 54 DataAgentBench tasks, run once in each of the natural and FAD groups. Earlier pilot and nine-task quickcheck cohorts are kept separately. Reports distinguish structural similarity, static optimization candidates, and measured results; candidate coverage is not a measured speedup.

## Repository contents and large files

Research documents, presentations, code, reports, task definitions, validation materials, SQL/Mongo requests, model transcripts, saved query results, and archived interrupted attempts are included. Large research artifacts use Git LFS. Install Git LFS before cloning, then run `git lfs pull` if the checkout contains pointer files.

Downloaded source databases (`query_dataset/`, SQLite/DuckDB files), Python virtual environments, and caches are excluded. Database source versions, checksums and download locations are retained in the benchmark manifests and preparation tools. See [data locations and sizes](benchmark/fullbench/reports/DATA.md), [task manifest](benchmark/fullbench/tasks.json), and [preparation code](benchmark/fullbench/tools/prepare.py).

Some original logs and scripts contain absolute paths from the experiment host. These are preserved as provenance; adjust environment paths when reproducing the experiments. Saved query outputs are retained even though the original database files are excluded.

Upstream benchmark: [ucbepic/DataAgentBench](https://github.com/ucbepic/DataAgentBench), pinned in the experiment task manifest.
