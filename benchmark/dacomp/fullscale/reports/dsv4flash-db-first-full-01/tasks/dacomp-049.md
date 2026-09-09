# dacomp-049

I am an HR professional in the insurance industry. I plan to conduct a competitiveness eva…

运行：已提交。官方未评分。全部 SQL 尝试/成功 19/18；数据 SQL 17/16；Python 13 次。

完整原题：

I am an HR professional in the insurance industry. I plan to conduct a competitiveness evaluation for the following open position within the same industry category. Using a horizontal comparison approach, focusing on core dimensions such as the compensation and benefits system and job requirements, I will analyze our company’s recruiting position relative to similar positions in the industry to identify competitive strengths and weaknesses.
| Job Title | Number of Openings | Company Name | Employment Type | Work Experience Requirement | Foreign Language Requirement | Age Requirement | Gender Requirement | Education Requirement | Work Location | Working Hours | Salary Range | Benefits | Company Address | Company Type | Industry | Job Description |
| PICC Life Insurance Xiamen Haicang and Jimei After-sales Department Establishment Manager | 2 | PICC Life Insurance Company Limited, Xiang'an District Branch, Xiamen City | Full-time | Two years or more of work experience | | 25 to 50 years old | none | Associate degree or above | Haicang District, Xiamen City, Xiang'an District, Xiamen City, Jimei District, Xiamen City | | 30,000 - 50,000 yuan/month (base salary: 24,000 - 30,000 yuan/month + commission) | Commercial insurance, business trip allowance, holiday benefits, professional training, flexible working hours, employee travel, overseas opportunities, no overtime, no probation period | Xindian Town, Xiangwu Village, No. 2 Xiazeng, 3rd Floor (one of the units), Xiang'an District, Xiamen City (361102) | state-owned enterprise | Insurance, Finance/Investment/Securities | Working hours: Monday to Friday, weekends off; except for the morning hours, the rest of the time can be arranged freely. Job requirements: 1. Age 25–50 years old; 2. Associate degree or above; 3. Personal after-tax income over 50,000 yuan in the past year; 4. At least 3 years of experience in the same industry, or at least 1 year of experience as a supervisor in the same industry. Compensation: 1. Full support from company resources; 2. Provide three insurances and one fund (housing provident fund); 3. Four promotion opportunities per year |

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 5004 | 19 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取同类岗位与市场薪资 → Python 解析薪资区间并计算均值、分位数和市场定位 → 岗位建议。

数据库大小：317,820,928 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 4.69 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.373 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 0 | 5.414 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 6.731 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 6.034 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | [] | 27 | 6.244 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | [] | 27 | 6.468 |
| [S10/Q8](#s10) | failed | ["sheet1"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.218 ms |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | [] | [] | 12 | 6.355 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | [] | [] | 29 | 6.409 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 5.93 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | [] | [] | 11 | 5.446 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | [] | [] | 9 | 6.193 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 6.097 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(\"Salary Range\")", "COUNT(\"Benefits\")", "COUNT(\"Education Requirement\")", "COUNT(\"Work Experience Requirement\")", "COUNT(\"Age Requirement\")"] | 1 | 5.012 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | [] | [] | 16 | 6.241 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | [] | [] | 4119 | 6.605 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 从归档薪资明细计算均值、最小最大值及阈值占比；这些可在 SQL 中计算。中位数、分位数与图表另行保留，不把所有 Python 统计都判为违规。 [证据](../reviews/dacomp-049.json)。

P1：Parse salary strings into numeric ranges using regex (SQLite has no regex), then compute salary statistics for the 16 genuine insurance peer jobs and the full Xiamen market for context; also tabulate education/experience/age/benefit/company-type distributions. These are statistical/data-cleaning steps outside SQL's capability.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Check where the recorded result archives live so the peer-set and salary-column rows can be loaded for parsing.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Parse salary strings into numeric ranges with regex (SQLite has no regex support), then compute salary summary statistics for the 16 insurance peer jobs and the full Xiamen market salary column for context; save parsed frames for charting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Check column names of the peer-set results file to identify the correct salary column name.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Inspect the JSON Lines structure of the peer-set archive to see how rows are encoded.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Parse salary strings into numeric ranges with regex (not supported by SQLite), compute peer vs market salary statistics, and persist parsed frames for charting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Tabulate education, experience, age, company-type, and benefit-penetration distributions across the 16 insurance peer jobs. This is descriptive statistics outside SQL's capability for textual analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Create three charts (salary comparison, education distribution, benefit coverage) from the parsed peer data — visualization must be done in Python rather than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P9：Create three visualizations (salary comparison bar chart, education distribution bar chart, benefit coverage chart) from the parsed peer data — visualizations must be done in Python, not SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P10：Create the work directory for saving figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Generate three visualizations (salary comparison, education distribution, benefit coverage) from the parsed peer data — visualizations must be done in Python, not SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P12：Generate a market-context histogram showing where the target salary range falls within the overall Xiamen wage distribution, and print the finalized peer comparison table for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Print the finalized peer list to include in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S3", "S17"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S7", "S8", "S9", "S11"] | 3 | 27 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S16", "S18"] | 1 | 16 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：8/16 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-049.analysis.json)。

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S8](#s8), [S9](#s9), [S11](#s11) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%'
```

受益查询 S7 的改写示例：

```sql
SELECT COUNT(*) AS insurance_rows FROM temp.reuse_candidate AS sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%'
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S17](#s17) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, COUNT("Salary Range") AS __a1, COUNT("Benefits") AS __a2, COUNT("Education Requirement") AS __a3, COUNT("Work Experience Requirement") AS __a4, COUNT("Age Requirement") AS __a5 FROM "sheet1" 
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S16](#s16), [S18](#s18) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%') AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')
```

受益查询 S16 的改写示例：

```sql
SELECT COUNT(*) AS peer_count FROM temp.reuse_candidate AS sheet1 WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%') AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S16 | True | True | exact_multiset |
| S18 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-049.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `1da9424d975f471090dadabbb885f0e8`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `1da9424d975f471090dadabbb885f0e8`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`8c9ad6fdec530f5865b919eec34d33bfdb0c4ad756e9b8790f38b123d074eca9`。

## S3

类别 `data`；来源 `query_db`；调用 `ca2b52623d314153acf3015f36ef533a`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`5d387a829e4fe0c7eaa6ebc80e70c1343652a06c417c1ab2cecba011646bd441`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `6eb7e396583f43498f6a084c8318a4ed`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Industry", "Salary Range" FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`dc2a369503feb87ea66fd789dc918258c582bc1b85b76b27371cc8837dc0fc8c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `7e5c37222fa446e4a287898a1bb45989`；状态 `success`。

```sql
SELECT * FROM sheet1 WHERE "Job Title" LIKE '%PICC%' OR "Company Name" LIKE '%PICC%' OR "Job Title" LIKE '%保险%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `d93ad92fd5f2444f99f4d2e0d4aac460`；状态 `success`。

```sql
SELECT DISTINCT "Industry" FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%' OR "Industry" LIKE '%insurance%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`3315f0337285f6ba72ce36f61b68c201603b535bca41ece803a569edc5ac027f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `e9992f35c22b46c38fd680a2278b85b8`；状态 `success`。

```sql
SELECT COUNT(*) AS insurance_rows FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`6fd2826852b6d410507b6e2c2cc4d4fd153d08ececb1ab25543dc5ccfebdff6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `7ddf202e35174f62ad155a68971d920a`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement" FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%' LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`faf519782e6d10b07d7e5ca559a6f51fd66e9a46a994ee20678fecf6789880d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `8e4f8eff85f64b579fb4050a3e5c543b`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description" FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%' ORDER BY "Job Title"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`df2e782ce267d182ed858e364cf7d9b8a7bed37a4617374ec27ab141e446f9ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `fca15ad786c44ae9a28c5653467b76b1`；状态 `failed`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description" FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%' ORDER BY "Job Title" OFFSET 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S10.parameters.json)。

错误：`OperationalError('near "OFFSET": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `84726839ffca499393181357c86ae935`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description" FROM sheet1 WHERE "Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%' ORDER BY "Job Title" LIMIT 30 OFFSET 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`008c57a49df4fb848d5a80bce585a04665b0bc7da4b624f0eae800de57fe5a7b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `35bbd83962f642de8e768c44be4268a4`；状态 `success`。

```sql
SELECT "Job Title" FROM sheet1 WHERE "Job Title" LIKE '%After-sales%' OR "Job Title" LIKE '%售后%' OR "Job Title" LIKE '%Establishment%' OR "Job Title" LIKE '%经理%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`14e245ddb12e1ecf2d727aeacf741cea58eed6ef2a355cc96ee116cd3c86c837`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `cc72e5c801b34dd4bb72dce6a07ea6ac`；状态 `success`。

```sql
SELECT "Job Title", "Company Name" FROM sheet1 WHERE "Company Name" LIKE '%人保%' OR "Company Name" LIKE '%PICC%' OR "Company Name" LIKE '%人寿%' OR "Company Name" LIKE '%Life Insurance%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ebfa5152c9d5c14b337acc76d781c6b6ec8676df0acb4b051c38c092c85a0de7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `4bd57da88d204ac5951a38614cd89d6a`；状态 `success`。

```sql
SELECT * FROM (
  SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description"
  FROM sheet1 
  WHERE ("Industry" LIKE '%保险%' OR "Industry" = 'Insurance')
    AND "Industry" NOT LIKE '1800%'
    AND "Industry" NOT LIKE '1. Holiday%'
    AND "Industry" NOT LIKE 'Join Ctrip%'
    AND "Industry" NOT LIKE 'Other industries%'
    AND "Industry" NOT LIKE 'Internet/E-commerce%'
) AS insurance_jobs
ORDER BY "Job Title"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`46cc0ba77dc83a3f71e25ff1be4350ef1c399c62bb6e7475d25fbd40b2899fb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "insurance_jobs", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `a681ef02a34d45768a5baa91ef0abc8e`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Employment Type", "Work Location" FROM sheet1 WHERE "Industry" LIKE 'Finance/Investment/Securities, Insurance' OR "Industry" LIKE 'Insurance, Finance/Investment/Securities' OR "Job Title" LIKE '%Product Planning%' OR "Job Title" LIKE '%Training Management%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`252ba92faed4b7717a4d1c6e5050fa40df76f8f312fb62c1c0aefa00c73aa230`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `da3a97d400c946449e38c72f832c40f1`；状态 `success`。

```sql
SELECT COUNT(*) AS peer_count FROM sheet1
WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%')
  AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`76d0d491e38a3c6487fe171f0b93a52fe1be5462423fdcbbbe1ddfe980abff5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `54350ccb6d874b76b8616537cace287d`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT("Salary Range") AS sal_nonnull, COUNT("Benefits") AS ben_nonnull, COUNT("Education Requirement") AS edu_nonnull, COUNT("Work Experience Requirement") AS exp_nonnull, COUNT("Age Requirement") AS age_nonnull FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`4d6caf740d42b459ce65d2ec6ca2a651647724cf2e296e0aca1d1b197fc59d2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT("Salary Range") | [{"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B1 | COUNT("Benefits") | [{"table": "sheet1", "column": "Benefits"}] | [] | False |
| B1 | COUNT("Education Requirement") | [{"table": "sheet1", "column": "Education Requirement"}] | [] | False |
| B1 | COUNT("Work Experience Requirement") | [{"table": "sheet1", "column": "Work Experience Requirement"}] | [] | False |
| B1 | COUNT("Age Requirement") | [{"table": "sheet1", "column": "Age Requirement"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `0d9ec502aa9643de83cb33255fe50d0e`；状态 `success`。

```sql
SELECT "Job Title", "Company Name", "Company Type", "Industry", "Salary Range", "Benefits", "Education Requirement", "Work Experience Requirement", "Age Requirement", "Gender Requirement", "Employment Type", "Work Location", "Job Description" FROM sheet1
WHERE ("Industry" LIKE '%保险%' OR "Industry" LIKE '%Insurance%')
  AND ("Company Name" LIKE '%保险%' OR "Company Name" LIKE '%Insurance%' OR "Company Name" LIKE '%Life%')
ORDER BY "Job Title"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`49edab400d9979ed6d91524528e0bfe332bfe2804c724cd0e027e556a2755e93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `62c1197f524249dabc494ac0455dcd23`；状态 `success`。

```sql
SELECT "Salary Range" FROM sheet1 WHERE "Salary Range" IS NOT NULL AND "Salary Range" != ''
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-049/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`ac9cf0046403eea613250dd2b023c3349cd57c7ff25c0da51f88ae8c4ab3f4ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

