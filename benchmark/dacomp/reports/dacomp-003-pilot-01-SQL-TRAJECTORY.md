# dacomp-003：展开 Python 工具后的 SQL 轨迹

S 编号包含数据 SQL、元数据 SQL 和可据工具源码恢复的连接设置；Q 编号保持原查询清单不变。

**源码恢复的 PRAGMA 并非历史引擎日志，不能与有执行记录的 SQL 混称为实测调用。** SQL 经 Python 工具执行只记一次；Pandas 计算不虚构成 SQL。

有日志的 SQL 尝试：3；成功：3；其中查表元数据：1；额外恢复连接设置：3。

独立 Python 源码检查：3 次；需要进一步核查：0 次。静态检查不能替代运行时数据库追踪。

| 顺序 | 原编号 | 类型 | 来源 | 状态 |
|---|---|---|---|---|
| S1 | list-db | connection_setup | 源码恢复 | 未独立记录 |
| S2 | list-db | metadata | 工具日志 | 成功 |
| S3 | Q1 | connection_setup | 源码恢复 | 未独立记录 |
| S4 | Q1 | query | 工具日志 | 成功 |
| S5 | Q2 | connection_setup | 源码恢复 | 未独立记录 |
| S6 | Q2 | query | 工具日志 | 成功 |

## S1 · list-db

```sql
PRAGMA query_only=ON
```

## S2 · list-db

```sql
SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[完整结果](../runs/natural/dacomp-003/pilot-01/results/9de509ecc07845c49ccbd870ae13da53.json)

## S3 · Q1

```sql
PRAGMA query_only=ON
```

## S4 · Q1

```sql
SELECT MIN("Year") AS min_year, MAX("Year") AS max_year, COUNT(*) AS n_rows, COUNT(DISTINCT "Region Code") AS n_regions
FROM sheet1;

```

[完整结果](../runs/natural/dacomp-003/pilot-01/results/6c47b63d36c840d5a08c4b308bedccc2.json)

## S5 · Q2

```sql
PRAGMA query_only=ON
```

## S6 · Q2

```sql
SELECT e."Year" AS yr, e."Region Code" AS rcode, e."Region Name" AS rname,
e."Per capita GDP (yuan/person)" AS gdp_pc,
s."Industrial Water Consumption (100 million m³)" AS ind_wc,
s."Total Water Consumption (100 million m³) " AS tot_wc,
e."Urbanization rate (%)" AS urb,
e."Industrial value added (100 million yuan)" AS iva
FROM economic_indicator_data e
JOIN sheet1 s ON e."Year" = s."Year" AND e."Region Code" = s."Region Code"
ORDER BY rcode, yr;

```

[完整结果](../runs/natural/dacomp-003/pilot-01/results/970b2031ecca4a52a6a4fa7e64c4385d.json)
