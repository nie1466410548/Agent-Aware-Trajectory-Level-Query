# dacomp-006：展开 Python 工具后的 SQL 轨迹

S 编号包含数据 SQL、元数据 SQL 和可据工具源码恢复的连接设置；Q 编号保持原查询清单不变。

**源码恢复的 PRAGMA 并非历史引擎日志，不能与有执行记录的 SQL 混称为实测调用。** SQL 经 Python 工具执行只记一次；Pandas 计算不虚构成 SQL。

有日志的 SQL 尝试：9；成功：9；其中查表元数据：1；额外恢复连接设置：9。

独立 Python 源码检查：3 次；需要进一步核查：0 次。静态检查不能替代运行时数据库追踪。

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
| S15 | Q7 | connection_setup | 源码恢复 | 未独立记录 |
| S16 | Q7 | query | 工具日志 | 成功 |
| S17 | Q8 | connection_setup | 源码恢复 | 未独立记录 |
| S18 | Q8 | query | 工具日志 | 成功 |

## S1 · list-db

```sql
PRAGMA query_only=ON
```

## S2 · list-db

```sql
SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/0a77744c0f354624b35f37ead2634d0e.json)

## S3 · Q1

```sql
PRAGMA query_only=ON
```

## S4 · Q1

```sql
SELECT MIN("Date") AS min_date, MAX("Date") AS max_date, COUNT(*) AS n_rows,
       COUNT(DISTINCT "Destination") AS n_dest
FROM sheet1
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/4c1c0a96fa9749ee860995a30d7c4bfb.json)

## S5 · Q2

```sql
PRAGMA query_only=ON
```

## S6 · Q2

```sql
SELECT "Destination" AS dest, COUNT(*) AS n, ROUND(SUM("Profit"),2) AS total_profit
FROM sheet1
GROUP BY "Destination"
ORDER BY n DESC
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/46b9b15b9e5246ee9a9bf953a3939593.json)

## S7 · Q3

```sql
PRAGMA query_only=ON
```

## S8 · Q3

```sql
SELECT
  CASE
    WHEN "Destination" LIKE 'South China%' THEN 'South China'
    WHEN "Destination" LIKE 'North China%' THEN 'North China'
    WHEN "Destination" LIKE 'East China%' THEN 'East China'
    WHEN "Destination" LIKE 'Northeast%' THEN 'Northeast'
    WHEN "Destination" LIKE 'Northwest%' THEN 'Northwest'
    WHEN "Destination" LIKE 'Southwest%' THEN 'Southwest'
    ELSE 'Other' END AS region,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Total Logistics Cost"),2) AS cost
FROM sheet1
GROUP BY region, month
ORDER BY region, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/bbba0500d8ae439d9f4206db9bcd65b0.json)

## S9 · Q4

```sql
PRAGMA query_only=ON
```

## S10 · Q4

```sql
SELECT
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("List Price Revenue"),2) AS list_rev,
  ROUND(SUM("Logistics Value-Added Service Revenue"),2) AS vas_rev,
  ROUND(SUM("Discount Amount"),2) AS discount,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Freight Cost"),2) AS freight,
  ROUND(SUM("Warehousing Cost"),2) AS warehousing,
  ROUND(SUM("Other Operating Costs"),2) AS other_cost,
  ROUND(SUM("Total Logistics Cost"),2) AS cost,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(AVG("Profit Margin"),4) AS avg_margin
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/dba21aaa488a4a50844a2225fa3f465e.json)

## S11 · Q5

```sql
PRAGMA query_only=ON
```

## S12 · Q5

```sql
SELECT
  COUNT(*) AS n,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit,
  SUM(CASE WHEN "Profit Margin" > 1 OR "Profit Margin" < 0 THEN 1 ELSE 0 END) AS bad_margin,
  ROUND(MIN("Profit"),2) AS min_profit,
  ROUND(MAX("Profit"),2) AS max_profit,
  ROUND(MIN("Profit Margin"),4) AS min_margin,
  ROUND(MAX("Profit Margin"),4) AS max_margin,
  ROUND(AVG("Profit"),2) AS avg_profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/2afde08295a04d8485ef68b1ad97974d.json)

## S13 · Q6

```sql
PRAGMA query_only=ON
```

## S14 · Q6

```sql
SELECT "Consigned Product" AS product,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_orders,
  ROUND(SUM(CASE WHEN "Profit" < 0 THEN "Profit" ELSE 0 END),2) AS neg_profit_sum
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY product, month
ORDER BY product, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/91c3b0c7572b44eb898eca77acc81baf.json)

## S15 · Q7

```sql
PRAGMA query_only=ON
```

## S16 · Q7

```sql
SELECT
  SUBSTR(SUBSTR("Destination", INSTR("Destination",'-')+1), 1,
         INSTR(SUBSTR("Destination", INSTR("Destination",'-')+1),'-')-1) AS province,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Profit"),2) AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province, month
ORDER BY province, month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/b684b63cb0ba4646ac4380b436718fc4.json)

## S17 · Q8

```sql
PRAGMA query_only=ON
```

## S18 · Q8

```sql
SELECT
  strftime('%Y-%m', "Date") AS month,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(AVG("Sales Quantity"),1) AS avg_qty_per_order,
  ROUND(AVG("List Price Revenue"),2) AS avg_list_rev_per_order,
  ROUND(AVG("Discount Amount"),2) AS avg_discount,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(SUM("Discount Amount")/SUM("List Price Revenue")*100,3) AS discount_rate_pct,
  ROUND(SUM("Freight Cost")/SUM("Total Logistics Revenue")*100,3) AS freight_ratio_pct
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month
```

[完整结果](../runs/natural/dacomp-006/pilot-01/results/c8ae543682c84e9d9e8b0d6d10fb1eb8.json)
