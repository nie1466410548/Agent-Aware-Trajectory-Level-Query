# dacomp-005：展开 Python 工具后的 SQL 轨迹

S 编号包含数据 SQL、元数据 SQL 和可据工具源码恢复的连接设置；Q 编号保持原查询清单不变。

**源码恢复的 PRAGMA 并非历史引擎日志，不能与有执行记录的 SQL 混称为实测调用。** SQL 经 Python 工具执行只记一次；Pandas 计算不虚构成 SQL。

有日志的 SQL 尝试：12；成功：11；其中查表元数据：1；额外恢复连接设置：12。

独立 Python 源码检查：1 次；需要进一步核查：0 次。静态检查不能替代运行时数据库追踪。

| 顺序 | 原编号 | 类型 | 来源 | 状态 |
|---|---|---|---|---|
| S1 | list-db | connection_setup | 源码恢复 | 未独立记录 |
| S2 | list-db | metadata | 工具日志 | 成功 |
| S3 | Q1 | connection_setup | 源码恢复 | 未独立记录 |
| S4 | Q1 | query | 工具日志 | 失败 |
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
| S15 | Q7 | connection_setup | 源码恢复 | 未独立记录 |
| S16 | Q7 | query | 工具日志 | 成功 |
| S17 | Q8 | connection_setup | 源码恢复 | 未独立记录 |
| S18 | Q8 | query | 工具日志 | 成功 |
| S19 | Q9 | connection_setup | 源码恢复 | 未独立记录 |
| S20 | Q9 | query | 工具日志 | 成功 |
| S21 | Q10 | connection_setup | 源码恢复 | 未独立记录 |
| S22 | Q10 | query | 工具日志 | 成功 |
| S23 | Q11 | connection_setup | 源码恢复 | 未独立记录 |
| S24 | Q11 | query | 工具日志 | 成功 |

## S1 · list-db

```sql
PRAGMA query_only=ON
```

## S2 · list-db

```sql
SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/1cce93f116e047f4aa4c59ae5a41d13a.json)

## S3 · Q1

```sql
PRAGMA query_only=ON
```

## S4 · Q1

```sql
SELECT COUNT(*) AS n_orders,
AVG("Profit Margin") AS avg_margin,
AVG("Profit Margin")*0.5 AS low_margin_threshold,
SUM(CASE WHEN "Profit Margin" < AVG("Profit Margin")*0.5 THEN 1 ELSE 0 END) AS dummy_check,
MIN("Profit Margin") AS min_margin, MAX("Profit Margin") AS max_margin,
MIN("Date") AS min_date, MAX("Date") AS max_date
FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/4a15592a1b6449f4b4ffd3d258a7f7b7.json)

OperationalError: misuse of aggregate function AVG()

## S5 · Q2

```sql
PRAGMA query_only=ON
```

## S6 · Q2

```sql
SELECT COUNT(*) AS n_orders,
AVG("Profit Margin") AS avg_margin,
AVG("Profit Margin")*0.5 AS low_margin_threshold,
MIN("Profit Margin") AS min_margin, MAX("Profit Margin") AS max_margin,
MIN("Date") AS min_date, MAX("Date") AS max_date
FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/05de7e1131794d5bb7e853aabb23e5b1.json)

## S7 · Q3

```sql
PRAGMA query_only=ON
```

## S8 · Q3

```sql
SELECT "Total Logistics Revenue" AS rev, "Total Logistics Cost" AS cost, "Profit" AS profit,
"Profit Margin" AS margin,
ROUND("Profit"/"Total Logistics Revenue",4) AS pm_rev,
ROUND("Profit"/"Total Logistics Cost",4) AS pm_cost
FROM sheet1 LIMIT 10

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/468a805fa65b40819da5b12143420e53.json)

## S9 · Q4

```sql
PRAGMA query_only=ON
```

## S10 · Q4

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS grp,
COUNT(*) AS n,
AVG("Sales Quantity") AS avg_qty,
AVG("Total Logistics Revenue") AS avg_rev,
SUM("Total Logistics Revenue") AS sum_rev,
SUM("Profit") AS sum_profit,
AVG("Profit") AS avg_profit,
AVG("List Price Revenue") AS avg_list,
AVG("Logistics Value-Added Service Revenue") AS avg_vas,
AVG("Discount Amount") AS avg_disc,
AVG("Discount Amount"/"List Price Revenue") AS avg_disc_rate,
AVG("Freight Cost") AS avg_freight,
AVG("Warehousing Cost") AS avg_wh,
AVG("Other Operating Costs") AS avg_other,
AVG("Total Logistics Cost") AS avg_cost,
AVG("Total Logistics Cost"/"Sales Quantity") AS cost_per_unit,
AVG("Customer Age") AS avg_age,
SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS n_loss
FROM sheet1 GROUP BY grp

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/a3f12d18c9174fdab455f28afd5d50e8.json)

## S11 · Q5

```sql
PRAGMA query_only=ON
```

## S12 · Q5

```sql
SELECT "Sales Quantity" AS qty, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low
FROM sheet1 GROUP BY qty ORDER BY qty

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/f69754f57e9a418fae065861e3b57f52.json)

## S13 · Q6

```sql
PRAGMA query_only=ON
```

## S14 · Q6

```sql
SELECT "Destination" AS dest, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Freight Cost"),1) AS avg_freight,
ROUND(AVG("Total Logistics Cost"),1) AS avg_cost
FROM sheet1 GROUP BY dest ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/ff1d52c467044dada27adbc895c214f7.json)

## S15 · Q7

```sql
PRAGMA query_only=ON
```

## S16 · Q7

```sql
SELECT "Consigned Product" AS prod, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Discount Amount"/"List Price Revenue")*100,2) AS avg_disc_pct,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY prod ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/793509e81c254204b2164410103c016f.json)

## S17 · Q8

```sql
PRAGMA query_only=ON
```

## S18 · Q8

```sql
SELECT SUBSTR("Destination",1,INSTR("Destination",'-')-1) AS region, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Freight Cost"),1) AS avg_freight,
ROUND(AVG("Total Logistics Cost"),1) AS avg_cost,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY region ORDER BY low_pct DESC

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/1704b01a214d47888089d2a12790dcd6.json)

## S19 · Q9

```sql
PRAGMA query_only=ON
```

## S20 · Q9

```sql
SELECT "Age Range" AS ar, "Customer Gender" AS g, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty,
ROUND(AVG("Profit Margin"),3) AS avg_margin
FROM sheet1 GROUP BY ar, g ORDER BY ar, g

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/fee046c8edd84ffaba47ab6efd4b643c.json)

## S21 · Q10

```sql
PRAGMA query_only=ON
```

## S22 · Q10

```sql
SELECT STRFTIME('%Y-%m',"Date") AS ym, COUNT(*) AS n,
SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
ROUND(AVG(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1.0 ELSE 0 END)*100,2) AS low_pct,
ROUND(AVG("Profit Margin"),3) AS avg_margin,
ROUND(AVG("Discount Amount"/"List Price Revenue")*100,2) AS avg_disc_pct,
ROUND(AVG("Sales Quantity"),1) AS avg_qty
FROM sheet1 GROUP BY ym ORDER BY ym

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/165d9e972a674fa189f5a4908c26ec47.json)

## S23 · Q11

```sql
PRAGMA query_only=ON
```

## S24 · Q11

```sql
SELECT "Date", "Destination", "Customer Gender", "Customer Age", "Age Range",
"Consigned Product", "Sales Quantity", "Logistics Unit Price", "List Price Revenue",
"Logistics Value-Added Service Revenue", "Discount Amount", "Total Logistics Revenue",
"Freight Cost", "Warehousing Cost", "Other Operating Costs", "Total Logistics Cost",
"Profit", "Profit Margin" FROM sheet1

```

[完整结果](../runs/natural/dacomp-005/pilot-01/results/6535ec41c6fb4e4ab3a53106bbf9a323.json)
