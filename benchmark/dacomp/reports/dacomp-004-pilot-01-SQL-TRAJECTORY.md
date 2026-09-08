# dacomp-004：展开 Python 工具后的 SQL 轨迹

S 编号包含数据 SQL、元数据 SQL 和可据工具源码恢复的连接设置；Q 编号保持原查询清单不变。

**源码恢复的 PRAGMA 并非历史引擎日志，不能与有执行记录的 SQL 混称为实测调用。** SQL 经 Python 工具执行只记一次；Pandas 计算不虚构成 SQL。

有日志的 SQL 尝试：7；成功：7；其中查表元数据：1；额外恢复连接设置：7。

独立 Python 源码检查：1 次；需要进一步核查：0 次。静态检查不能替代运行时数据库追踪。

| 顺序 | 原编号 | 类型 | 来源 | 状态 |
|---|---|---|---|---|
| S1 | list-db | connection_setup | 源码恢复 | 未独立记录 |
| S2 | list-db | metadata | 工具日志 | 成功 |
| S3 | Q1 | connection_setup | 源码恢复 | 未独立记录 |
| S4 | Q1 | query | 工具日志 | 成功 |
| S5 | Q2 | connection_setup | 源码恢复 | 未独立记录 |
| S6 | Q2 | query | 工具日志 | 成功 |
| S7 | Q3 | connection_setup | 源码恢复 | 未独立记录 |
| S8 | Q3 | query | 工具日志 | 成功 |
| S9 | Q4 | connection_setup | 源码恢复 | 未独立记录 |
| S10 | Q4 | query | 工具日志 | 成功 |
| S11 | Q5 | connection_setup | 源码恢复 | 未独立记录 |
| S12 | Q5 | query | 工具日志 | 成功 |
| S13 | Q6 | connection_setup | 源码恢复 | 未独立记录 |
| S14 | Q6 | query | 工具日志 | 成功 |

## S1 · list-db

```sql
PRAGMA query_only=ON
```

## S2 · list-db

```sql
SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/8e62a8fe02fe4164ba71c42c6ca17e95.json)

## S3 · Q1

```sql
PRAGMA query_only=ON
```

## S4 · Q1

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Sales Month") AS n_months, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Customer ID") AS n_customers FROM sheet1;
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/32d2a8253873480d9f1bc86bab3b074d.json)

## S5 · Q2

```sql
PRAGMA query_only=ON
```

## S6 · Q2

```sql
SELECT "Sales Month" AS month, COUNT(*) AS rows, COUNT(DISTINCT "Product Code") AS products, ROUND(SUM("Sales Amount"),2) AS total_sales FROM sheet1 GROUP BY "Sales Month" ORDER BY month;
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/4769620749024d0f83cc505eff3c8911.json)

## S7 · Q3

```sql
PRAGMA query_only=ON
```

## S8 · Q3

```sql
SELECT "Sales Month" AS month, "Product Code" AS product_code, MAX("Specification/Model") AS spec, MAX("Minor Category Name") AS minor_category, MAX("Middle Category Name") AS middle_category, COUNT(*) AS txn_count, COUNT(DISTINCT "Customer ID") AS n_customers, ROUND(SUM("Sales Amount"),2) AS total_sales FROM sheet1 GROUP BY "Sales Month", "Product Code" ORDER BY month, total_sales DESC;
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/2fc1c0146100445081c7fdd47f1937d0.json)

## S9 · Q4

```sql
PRAGMA query_only=ON
```

## S10 · Q4

```sql
SELECT "Product Code" AS product_code, "Sales Month" AS month, COUNT(*) AS repeat_customers FROM (SELECT "Product Code", "Sales Month", "Customer ID", COUNT(*) AS c FROM sheet1 GROUP BY "Product Code", "Sales Month", "Customer ID" HAVING c >= 2) GROUP BY "Product Code", "Sales Month";
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/d0df8843606e406f8156470eed9c0525.json)

## S11 · Q5

```sql
PRAGMA query_only=ON
```

## S12 · Q5

```sql
SELECT "Sales Month" AS month, "Product Code" AS product_code, MAX("Sales Amount") AS max_single_sale FROM sheet1 GROUP BY "Sales Month" ORDER BY month;
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/98002727db954c149289a902ee91f9eb.json)

## S13 · Q6

```sql
PRAGMA query_only=ON
```

## S14 · Q6

```sql
SELECT "Product Code" AS product_code, "Sales Month" AS month, "Is Promotional" AS is_promotional, COUNT(*) AS txn, ROUND(SUM("Sales Amount"),2) AS sales FROM sheet1 WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045') GROUP BY "Product Code", "Sales Month", "Is Promotional" ORDER BY product_code, month, is_promotional;
```

[完整结果](../runs/natural/dacomp-004/pilot-01/results/8622190c07384fefaba73ddaf978ed89.json)
