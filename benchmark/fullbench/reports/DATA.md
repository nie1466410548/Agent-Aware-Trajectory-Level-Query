# 数据位置和规模

| 数据集 | 逻辑库 | 引擎 | 表/集合数 | 精确总行/文档数 | 大小 MiB | 位置 |
|---|---|---|---:|---:|---:|---|
| DEPS_DEV_V1 | package_database | sqlite | 1 | 661,372 | 513.91 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_DEPS_DEV_V1/query_dataset/package_query.db` |
| DEPS_DEV_V1 | project_database | duckdb | 2 | 598,372 | 10.51 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_DEPS_DEV_V1/query_dataset/project_query.db` |
| GITHUB_REPOS | metadata_database | sqlite | 3 | 7,051,268 | 540.95 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_GITHUB_REPOS/query_dataset/repo_metadata.db` |
| GITHUB_REPOS | artifacts_database | duckdb | 3 | 566,339 | 344.51 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_GITHUB_REPOS/query_dataset/repo_artifacts.db` |
| PANCANCER_ATLAS | clinical_database | postgres | 1 | 10,761 | 13.92 | `127.0.0.1:55439/pancancer_clinical` |
| PANCANCER_ATLAS | molecular_database | duckdb | 2 | 12,123,762 | 280.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_PANCANCER_ATLAS/query_dataset/pancancer_molecular.db` |
| PATENTS | publication_database | sqlite | 1 | 277,813 | 5169.89 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_PATENTS/query_dataset/patent_publication.db` |
| PATENTS | CPCDefinition_database | postgres | 1 | 260,808 | 126.90 | `127.0.0.1:55439/patent_CPCDefinition` |
| agnews | articles_database | mongo | 1 | 127,600 | 24.40 | `127.0.0.1:55440/articles_db` |
| agnews | metadata_database | sqlite | 2 | 128,594 | 3.86 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_agnews/query_dataset/metadata.db` |
| bookreview | books_database | postgres | 1 | 200 | 8.22 | `127.0.0.1:55439/bookreview_db` |
| bookreview | review_database | sqlite | 1 | 1,833 | 1.04 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_bookreview/query_dataset/review_query.db` |
| crmarenapro | core_crm | sqlite | 3 | 1,199 | 0.18 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_crmarenapro/query_dataset/core_crm.db` |
| crmarenapro | sales_pipeline | duckdb | 6 | 11,394 | 2.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_crmarenapro/query_dataset/sales_pipeline.duckdb` |
| crmarenapro | support | postgres | 6 | 6,499 | 16.33 | `127.0.0.1:55439/crm_support` |
| crmarenapro | products_orders | sqlite | 7 | 1,065 | 0.14 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_crmarenapro/query_dataset/products_orders.db` |
| crmarenapro | activities | duckdb | 3 | 8,870 | 20.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_crmarenapro/query_dataset/activities.duckdb` |
| crmarenapro | territory | sqlite | 2 | 194 | 0.02 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_crmarenapro/query_dataset/territory.db` |
| googlelocal | business_database | postgres | 1 | 79 | 7.51 | `127.0.0.1:55439/googlelocal_db` |
| googlelocal | review_database | sqlite | 1 | 2,000 | 0.56 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_googlelocal/query_dataset/review_query.db` |
| music_brainz_20k | tracks_database | sqlite | 1 | 19,375 | 1.94 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_music_brainz_20k/query_dataset/tracks.db` |
| music_brainz_20k | sales_database | duckdb | 1 | 58,049 | 1.01 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_music_brainz_20k/query_dataset/sales.duckdb` |
| stockindex | indexinfo_database | sqlite | 1 | 14 | 0.01 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_stockindex/query_dataset/indexInfo_query.db` |
| stockindex | indextrade_database | duckdb | 1 | 104,224 | 4.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_stockindex/query_dataset/indextrade_query.db` |
| stockmarket | stockinfo_database | sqlite | 1 | 2,752 | 0.70 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_stockmarket/query_dataset/stockinfo_query.db` |
| stockmarket | stocktrade_database | duckdb | 2753 | 6,473,105 | 920.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_stockmarket/query_dataset/stocktrade_query.db` |
| yelp | businessinfo_database | mongo | 2 | 190 | 0.17 | `127.0.0.1:55440/yelp_db` |
| yelp | user_database | duckdb | 3 | 4,783 | 3.26 | `/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/fullbench/upstream/query_yelp/query_dataset/yelp_user.db` |

文件大小与 PostgreSQL/Mongo 存储大小口径不同，详见 JSON 的 size_kind。Mongo 字段名来自最多 100 个文档抽样，不是完整 schema。

[所有表/集合行数与字段 CSV](tables.csv) · [完整数据清单 JSON](data-inventory.json) · [源文件校验](source-integrity.json) · [环境版本](environment.json)

```bash
benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/inspect_data.py DATASET DATABASE --sql 'SELECT * FROM "TABLE" LIMIT 5'
```

查看工具独立于实验轨迹，SQL 数据库只读连接；Mongo 在此工具中仅列清单。
