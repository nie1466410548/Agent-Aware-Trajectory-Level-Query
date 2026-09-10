# FAD与实际SQL轨迹分析

按任务分别整理。每个任务的结论、预测与实际查询对照、遗漏、统计及逐轮证据放在同一节，表格不混入其他任务。本文只分析迭代后本次运行的结果。

将FAD与后续实际SQL对照。分析模型明确写出的内容，不以接口是否接收判断预测对错；没有重跑模型或修改历史日志。

任务目录：

- [DAComp-003：水资源与经济指标](#task-003)
- [DAComp-004：产品销售与复购](#task-004)
- [DAComp-005：低利润率订单](#task-005)
- [DAComp-006：华南利润波动](#task-006)



**本次命中口径：一份FAD中任意一项明确预测被后续成功SQL使用，就算这份FAD命中。不同信息可以在不同SQL中使用。下面已替换旧的“全部信息必须共同出现”口径。**


<a id="task-003"></a>

## DAComp-003：水资源与经济指标

### 本题命中率

**一份FAD有任意一项被后续SQL用到，就记为命中。** 没提供预测的FAD单列，不混入“有预测的FAD命中率”；同时给出占全部提交的比例。

| 统计内容 | 结果 |
|---|---|
| 共提交FAD | 11份 |
| 有预测 / 没提供预测 | 6份 / 5份 |
| **有预测的FAD命中率** | **6/6 = 100.0%** |
| 命中份数占全部提交 | 6/11 = 54.5% |

**候选访问预测的命中情况：** 每个候选中任意一项明确预测被后续SQL使用，该候选就算命中。一份FAD可以有多个候选，所以与上面的FAD份数分别统计。

| 统计内容 | 结果 |
|---|---|
| 候选总数 | 10个 |
| 命中的候选 | 10个 |
| 未命中的候选 | 0个 |
| **候选命中率** | **10/10 = 100.0%** |

**具体预测信息用了多少：** 同一份FAD中重复出现的同类信息只计一次，不同轮次重复预测分别计数。列、聚合、过滤条件、连接等值条件分别逐项数；联合分组作为一项，所列维度需在后续某个分组中一起使用，允许实际增加维度。

| 信息类别 | 提前写了多少项 | 后来使用了多少项 | 比例 |
|---|---:|---:|---|
| 列 | 47 | 45 | 45/47 = 95.7% |
| 分组 | 9 | 9 | 9/9 = 100.0% |
| 聚合 | 11 | 3 | 3/11 = 27.3% |
| 过滤 | 2 | 2 | 2/2 = 100.0% |
| 连接 | 6 | 6 | 6/6 = 100.0% |

命中一列就足以让该份FAD命中，并不意味着其中所有分组、聚合都对。上表用来区分“有用到一点”与“具体信息用了多少”。过滤按已知条件项匹配，连接按类型＋等值条件匹配；复杂表达式无法自动确认的部分保留在具体分析中。

### 逐轮FAD与后续query

#### Q1：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Region Name",
 COUNT(*) AS n_rows,
 MIN("Year") AS min_year,
 MAX("Year") AS max_year
FROM sheet1
GROUP BY "Region Name"
ORDER BY "Region Name"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：economic_indicator_data.Region Name | [Q2](#t003-from1-sql2) |
| 列：economic_indicator_data.Year | [Q2](#t003-from1-sql2)、[Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Region Name | [Q3](#t003-from1-sql3)、[Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Year | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 分组：sheet1.Year | [Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³)) | 未找到 |
| 聚合：SUM(sheet1.Total Water Consumption (100 million m³) ) | 未找到 |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：economic_indicator_data.Region Name | [Q2](#t003-from1-sql2) |
| 列：economic_indicator_data.Year | [Q2](#t003-from1-sql2)、[Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Region Name | [Q3](#t003-from1-sql3)、[Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 列：sheet1.Year | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 分组：sheet1.Region Name | [Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | [Q7](#t003-from1-sql7) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |

##### 后续SQL原文

<a id="t003-from1-sql2"></a>
<details><summary>Q2：实际SQL</summary>

```sql
SELECT "Region Name",
 COUNT(*) AS n_rows,
 MIN("Year") AS min_year,
 MAX("Year") AS max_year
FROM economic_indicator_data
GROUP BY "Region Name"
ORDER BY "Region Name"
```

</details>

<a id="t003-from1-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

<a id="t003-from1-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT s."Year",
 s."Industrial Water Consumption (100 million m³)",
 s."Total Water Consumption (100 million m³) ",
 e."Per capita GDP (yuan/person)"
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from1-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from1-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

<a id="t003-from1-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<a id="t003-from1-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<a id="t003-from1-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<a id="t003-from1-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<a id="t003-from1-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q2：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Region Name",
 COUNT(*) AS n_rows,
 MIN("Year") AS min_year,
 MAX("Year") AS max_year
FROM economic_indicator_data
GROUP BY "Region Name"
ORDER BY "Region Name"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：economic_indicator_data.Region Name | 未找到 |
| 列：economic_indicator_data.Year | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Region Name | [Q3](#t003-from2-sql3)、[Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Year | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 分组：sheet1.Year | [Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³)) | 未找到 |
| 聚合：SUM(sheet1.Total Water Consumption (100 million m³) ) | 未找到 |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：economic_indicator_data.Region Name | 未找到 |
| 列：economic_indicator_data.Year | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Region Name | [Q3](#t003-from2-sql3)、[Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 列：sheet1.Year | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 分组：sheet1.Region Name | [Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | [Q7](#t003-from2-sql7) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |

##### 后续SQL原文

<a id="t003-from2-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

<a id="t003-from2-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT s."Year",
 s."Industrial Water Consumption (100 million m³)",
 s."Total Water Consumption (100 million m³) ",
 e."Per capita GDP (yuan/person)"
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from2-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from2-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

<a id="t003-from2-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<a id="t003-from2-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<a id="t003-from2-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<a id="t003-from2-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<a id="t003-from2-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q3：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：economic_indicator_data.Region Name | 未找到 |
| 列：economic_indicator_data.Year | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Region Name | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Year | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 分组：sheet1.Year | [Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³)) | 未找到 |
| 聚合：SUM(sheet1.Total Water Consumption (100 million m³) ) | 未找到 |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：economic_indicator_data.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：economic_indicator_data.Region Name | 未找到 |
| 列：economic_indicator_data.Year | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Region Name | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 列：sheet1.Year | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 分组：sheet1.Region Name | [Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | [Q7](#t003-from3-sql7) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |

##### 后续SQL原文

<a id="t003-from3-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT s."Year",
 s."Industrial Water Consumption (100 million m³)",
 s."Total Water Consumption (100 million m³) ",
 e."Per capita GDP (yuan/person)"
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from3-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from3-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

<a id="t003-from3-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<a id="t003-from3-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<a id="t003-from3-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<a id="t003-from3-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<a id="t003-from3-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q4：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT s."Year",
 s."Industrial Water Consumption (100 million m³)",
 s."Total Water Consumption (100 million m³) ",
 e."Per capita GDP (yuan/person)"
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：economic_indicator_data.Region Code | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：sheet1.Region Code | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：sheet1.Region Name | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 列：sheet1.Year | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 分组：sheet1.Region Name ＋ sheet1.Year | [Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 过滤：sheet1.Region Name ne "China" | [Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |

##### 后续SQL原文

<a id="t003-from4-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

<a id="t003-from4-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

<a id="t003-from4-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<a id="t003-from4-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<a id="t003-from4-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<a id="t003-from4-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<a id="t003-from4-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q5：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" = 'China'
ORDER BY s."Year"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：economic_indicator_data.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Region Name | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Year | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 分组：sheet1.Region Name | [Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 过滤：sheet1.Region Name ne "China" | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：economic_indicator_data.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Region Name | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 列：sheet1.Year | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 分组：sheet1.Year | [Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |

##### 后续SQL原文

<a id="t003-from5-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

<a id="t003-from5-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<a id="t003-from5-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<a id="t003-from5-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<a id="t003-from5-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<a id="t003-from5-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q6：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT s."Region Name",
 s."Year",
 ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct,
 ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
ORDER BY s."Region Name",
s."Year"
```

</details>

没有提供未来访问预测。之后仍执行了Q7、Q8、Q9、Q10、Q11。

##### 后续SQL原文

<details><summary>Q7：实际SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q7：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT s."Region Name",
 COUNT(*) AS n,
 ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share,
 ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name"
ORDER BY avg_share DESC
```

</details>

没有提供未来访问预测。之后仍执行了Q8、Q9、Q10、Q11。

##### 后续SQL原文

<details><summary>Q8：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q8：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year"),
 stats AS (
SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2
FROM main
GROUP BY "Region Name")
SELECT "Region Name",
 ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp,
 ROUND(sx/n, 2) AS avg_share
FROM stats
ORDER BY corr_share_gdp DESC
```

</details>

没有提供未来访问预测。之后仍执行了Q9、Q10、Q11。

##### 后续SQL原文

<details><summary>Q9：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q9：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MIN("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first,
 ROUND(MAX(CASE WHEN "Year" = (
SELECT MAX("Year")
FROM main m2
WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last
FROM main
GROUP BY "Region Name"
ORDER BY share_last DESC
```

</details>

没有提供未来访问预测。之后仍执行了Q10、Q11。

##### 后续SQL原文

<details><summary>Q10：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q10：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT "Region Name",
 "Year" AS peak_year,
 ROUND(ind_share, 2) AS peak_share
FROM main
WHERE ("Region Name", ind_share) IN (
SELECT "Region Name", MAX(ind_share)
FROM main
GROUP BY "Region Name")
ORDER BY "Region Name"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：economic_indicator_data.Per capita GDP (yuan/person) | [Q11](#t003-from10-sql11) |
| 列：economic_indicator_data.Region Code | [Q11](#t003-from10-sql11) |
| 列：sheet1.Industrial Water Consumption (100 million m³) | [Q11](#t003-from10-sql11) |
| 列：sheet1.Region Code | [Q11](#t003-from10-sql11) |
| 列：sheet1.Region Name | [Q11](#t003-from10-sql11) |
| 列：sheet1.Total Water Consumption (100 million m³)  | [Q11](#t003-from10-sql11) |
| 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | 未找到 |
| 聚合：AVG(sheet1.Total Water Consumption (100 million m³) ) | 未找到 |
| 连接：inner：economic_indicator_data.Region Code = sheet1.Region Code | [Q11](#t003-from10-sql11) |

##### 后续SQL原文

<a id="t003-from10-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

#### Q11：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
WITH main AS (
SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp
FROM sheet1 s
JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code"
WHERE s."Region Name" != 'China'
GROUP BY s."Region Name", s."Year")
SELECT m1."Region Name",
 ROUND(m1.ind_share, 2) AS share_2003,
 ROUND(m1.pc_gdp, 0) AS gdp_2003,
 ROUND(m2.ind_share, 2) AS share_2018,
 ROUND(m2.pc_gdp, 0) AS gdp_2018
FROM main m1
JOIN main m2 ON m1."Region Name" = m2."Region Name"
WHERE m1."Year" = 2003 AND m2."Year" = 2018
ORDER BY gdp_2018 DESC
```

</details>

没有提供未来访问预测。之后没有再查询。

<!-- task-notes-start -->
### 具体操作的差异与遗漏

下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。

### 哪些预测没有发生，哪些只说对一部分

| 提出预测的轮次 | FAD说了什么 | 后面实际情况 | 判断 |
|---|---|---|---|
| Q1—Q3各自的候选1 | 按Year分组，SUM(工业用水量)、SUM(总用水量) | Q4、Q5直接读取China各年记录并算占比；之后主要按地区计算均值和相关性，没有执行所预测的按年份求和 | Year后来作为地区＋年份联合分组的维度被使用，按本次口径分组项命中；但两项用水SUM没有发生 |
| Q6—Q9 | no_further_access，即没有后续访问 | Q7—Q11仍在执行均值、相关性、首末年、峰值等查询 | 明确的后续访问判断错误，不能只看早期预测对过哪些列 |
| Q10 | 预计再计算两项用水均值 | 剩下的Q11比较2003与2018的记录，没有再次求这两项均值 | 这两项均值未命中，但这份FAD仍可能因列或连接被使用而命中 |

### 实际做了，但FAD没有提前说清楚什么

| 实际SQL中的内容 | 之前FAD说到了什么 | 缺了什么 |
|---|---|---|
| Q4开始按Region Code＋Year连接两表 | 两个Region Code明确出现在joins里，Year也出现在列清单里 | Year=Year没有写成连接条件；连接键只预测了一部分 |
| Q7用水均值、GDP均值；Q8相关性及后续首末年/峰值分析 | 提前说了工业用水均值、地区等字段 | 其他均值和更复杂的计算未完整描述；Q6—Q9更直接停止提供候选 |

CASE、窗口和复杂嵌套计算可能超出当前FAD表达能力；已有Schema能表达却未填写的操作，与这些表达能力限制分别看待。

### 本题高频列有没有提前说

每条成功SQL中同一列只数一次，排除第一条SQL。FAD里任何字段明确引用都算提到；这里问的是访问之前是否曾经说过，不要求紧邻上一轮。

| 列 | 后续多少条SQL访问了它 | 其中多少次已被更早FAD提到 |
|---|---|---|
| 两表各自的Region Code | 各8条 | 各8次 |
| 经济表Year | 9条 | 9次 |
| 人均GDP | 8条 | 8次 |
<!-- task-notes-end -->

原始数据：[events.jsonl](../runs/dacomp-003-02/events.jsonl)。本次逐项命中记录：[item-hit-rates.json](item-hit-rates.json)。

<a id="task-004"></a>

## DAComp-004：产品销售与复购

### 本题命中率

**一份FAD有任意一项被后续SQL用到，就记为命中。** 没提供预测的FAD单列，不混入“有预测的FAD命中率”；同时给出占全部提交的比例。

| 统计内容 | 结果 |
|---|---|
| 共提交FAD | 10份 |
| 有预测 / 没提供预测 | 9份 / 1份 |
| **有预测的FAD命中率** | **9/9 = 100.0%** |
| 命中份数占全部提交 | 9/10 = 90.0% |

**候选访问预测的命中情况：** 每个候选中任意一项明确预测被后续SQL使用，该候选就算命中。一份FAD可以有多个候选，所以与上面的FAD份数分别统计。

| 统计内容 | 结果 |
|---|---|
| 候选总数 | 9个 |
| 命中的候选 | 9个 |
| 未命中的候选 | 0个 |
| **候选命中率** | **9/9 = 100.0%** |

**具体预测信息用了多少：** 同一份FAD中重复出现的同类信息只计一次，不同轮次重复预测分别计数。列、聚合、过滤条件、连接等值条件分别逐项数；联合分组作为一项，所列维度需在后续某个分组中一起使用，允许实际增加维度。

| 信息类别 | 提前写了多少项 | 后来使用了多少项 | 比例 |
|---|---:|---:|---|
| 列 | 33 | 32 | 32/33 = 97.0% |
| 分组 | 5 | 5 | 5/5 = 100.0% |
| 聚合 | 6 | 6 | 6/6 = 100.0% |
| 过滤 | 5 | 5 | 5/5 = 100.0% |
| 连接 | 0 | 0 | 未提供 |

命中一列就足以让该份FAD命中，并不意味着其中所有分组、聚合都对。上表用来区分“有用到一点”与“具体信息用了多少”。过滤按已知条件项匹配，连接按类型＋等值条件匹配；复杂表达式无法自动确认的部分保留在具体分析中。

### 逐轮FAD与后续query

#### Q1：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM sheet1
LIMIT 20
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Product Code | [Q2](#t004-from1-sql2)、[Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q6](#t004-from1-sql6)、[Q7](#t004-from1-sql7)、[Q8](#t004-from1-sql8)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |
| 列：sheet1.Sales Amount | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |
| 列：sheet1.Sales Month | [Q2](#t004-from1-sql2)、[Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q7](#t004-from1-sql7)、[Q8](#t004-from1-sql8)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |
| 分组：sheet1.Product Code ＋ sheet1.Sales Month | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9) |
| 聚合：SUM(sheet1.Sales Amount) | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |

##### 后续SQL原文

<a id="t004-from1-sql2"></a>
<details><summary>Q2：实际SQL</summary>

```sql
SELECT COUNT(*) AS row_count,
 COUNT(DISTINCT "Product Code") AS n_products,
 COUNT(DISTINCT "Sales Month") AS n_months,
 MIN("Sales Month") AS min_month,
 MAX("Sales Month") AS max_month
FROM sheet1
```

</details>

<a id="t004-from1-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales
FROM sheet1
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Sales Month",
total_sales DESC
```

</details>

<a id="t004-from1-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS rnk
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE rnk = 1
ORDER BY "Sales Month"
```

</details>

<a id="t004-from1-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales,
 COUNT(*) AS n_transactions,
 COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from1-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

<a id="t004-from1-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from1-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from1-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from1-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q2：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT COUNT(*) AS row_count,
 COUNT(DISTINCT "Product Code") AS n_products,
 COUNT(DISTINCT "Sales Month") AS n_months,
 MIN("Sales Month") AS min_month,
 MAX("Sales Month") AS max_month
FROM sheet1
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Product Code | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q6](#t004-from2-sql6)、[Q7](#t004-from2-sql7)、[Q8](#t004-from2-sql8)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |
| 列：sheet1.Sales Amount | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |
| 列：sheet1.Sales Month | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q7](#t004-from2-sql7)、[Q8](#t004-from2-sql8)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |
| 分组：sheet1.Product Code ＋ sheet1.Sales Month | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9) |
| 聚合：SUM(sheet1.Sales Amount) | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |

##### 后续SQL原文

<a id="t004-from2-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales
FROM sheet1
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Sales Month",
total_sales DESC
```

</details>

<a id="t004-from2-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS rnk
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE rnk = 1
ORDER BY "Sales Month"
```

</details>

<a id="t004-from2-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales,
 COUNT(*) AS n_transactions,
 COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from2-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

<a id="t004-from2-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from2-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from2-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from2-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q3：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales
FROM sheet1
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Sales Month",
total_sales DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Product Code | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q6](#t004-from3-sql6)、[Q7](#t004-from3-sql7)、[Q8](#t004-from3-sql8)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |
| 列：sheet1.Sales Amount | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |
| 列：sheet1.Sales Month | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q7](#t004-from3-sql7)、[Q8](#t004-from3-sql8)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |
| 分组：sheet1.Product Code ＋ sheet1.Sales Month | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9) |
| 聚合：SUM(sheet1.Sales Amount) | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |

##### 后续SQL原文

<a id="t004-from3-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS rnk
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE rnk = 1
ORDER BY "Sales Month"
```

</details>

<a id="t004-from3-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales,
 COUNT(*) AS n_transactions,
 COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from3-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

<a id="t004-from3-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from3-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from3-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from3-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q4：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS rnk
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE rnk = 1
ORDER BY "Sales Month"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Customer ID | [Q5](#t004-from4-sql5)、[Q7](#t004-from4-sql7)、[Q8](#t004-from4-sql8)、[Q10](#t004-from4-sql10) |
| 列：sheet1.Is Promotional | 未找到 |
| 列：sheet1.Major Category Name | [Q6](#t004-from4-sql6) |
| 列：sheet1.Middle Category Name | [Q6](#t004-from4-sql6) |
| 列：sheet1.Minor Category Name | [Q6](#t004-from4-sql6) |
| 列：sheet1.Product Code | [Q5](#t004-from4-sql5)、[Q6](#t004-from4-sql6)、[Q7](#t004-from4-sql7)、[Q8](#t004-from4-sql8)、[Q9](#t004-from4-sql9)、[Q10](#t004-from4-sql10) |
| 列：sheet1.Product Type | [Q6](#t004-from4-sql6) |
| 列：sheet1.Sales Amount | [Q5](#t004-from4-sql5)、[Q9](#t004-from4-sql9)、[Q10](#t004-from4-sql10) |
| 列：sheet1.Sales Month | [Q5](#t004-from4-sql5)、[Q7](#t004-from4-sql7)、[Q8](#t004-from4-sql8)、[Q9](#t004-from4-sql9)、[Q10](#t004-from4-sql10) |
| 列：sheet1.Specification/Model | [Q6](#t004-from4-sql6) |

##### 后续SQL原文

<a id="t004-from4-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales,
 COUNT(*) AS n_transactions,
 COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from4-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

<a id="t004-from4-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from4-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from4-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from4-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q5：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Sales Month",
 "Product Code",
 SUM("Sales Amount") AS total_sales,
 COUNT(*) AS n_transactions,
 COUNT(DISTINCT "Customer ID") AS n_customers
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Sales Month",
 "Product Code"
ORDER BY "Product Code",
"Sales Month"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Customer ID | [Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q10](#t004-from5-sql10) |
| 列：sheet1.Product Code | [Q6](#t004-from5-sql6)、[Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q9](#t004-from5-sql9)、[Q10](#t004-from5-sql10) |
| 列：sheet1.Sales Month | [Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q9](#t004-from5-sql9)、[Q10](#t004-from5-sql10) |
| 分组：sheet1.Customer ID ＋ sheet1.Product Code | [Q7](#t004-from5-sql7) |
| 聚合：COUNT_DISTINCT(sheet1.Sales Month) | [Q7](#t004-from5-sql7)、[Q10](#t004-from5-sql10) |
| 过滤：sheet1.Product Code in ["DW-1001040125", "DW-1203130446", "DW-1518040045", "DW-2316020016"] | [Q6](#t004-from5-sql6)、[Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q9](#t004-from5-sql9)、[Q10](#t004-from5-sql10) |

##### 后续SQL原文

<a id="t004-from5-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

<a id="t004-from5-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from5-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from5-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from5-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q6：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
 "Unit",
 COUNT(*) AS n_rows
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code",
 "Major Category Name",
 "Middle Category Name",
 "Minor Category Name",
 "Specification/Model",
 "Product Type",
"Unit"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Customer ID | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q10](#t004-from6-sql10) |
| 列：sheet1.Product Code | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q9](#t004-from6-sql9)、[Q10](#t004-from6-sql10) |
| 列：sheet1.Sales Month | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q9](#t004-from6-sql9)、[Q10](#t004-from6-sql10) |
| 分组：sheet1.Customer ID ＋ sheet1.Product Code | [Q7](#t004-from6-sql7) |
| 聚合：COUNT_DISTINCT(sheet1.Sales Month) | [Q7](#t004-from6-sql7)、[Q10](#t004-from6-sql10) |
| 过滤：sheet1.Product Code in ["DW-1001040125", "DW-1203130446", "DW-1518040045", "DW-2316020016"] | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q9](#t004-from6-sql9)、[Q10](#t004-from6-sql10) |

##### 后续SQL原文

<a id="t004-from6-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from6-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from6-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from6-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q7：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Product Code",

       COUNT(DISTINCT "Customer ID") AS total_customers,

       SUM(CASE WHEN n_months >= 2 THEN 1 ELSE 0 END) AS repeat_customers
FROM (
SELECT "Product Code", "Customer ID", COUNT(DISTINCT "Sales Month") AS n_months
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code", "Customer ID"
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Customer ID | [Q8](#t004-from7-sql8)、[Q10](#t004-from7-sql10) |
| 列：sheet1.Product Code | [Q8](#t004-from7-sql8)、[Q9](#t004-from7-sql9)、[Q10](#t004-from7-sql10) |
| 列：sheet1.Sales Month | [Q8](#t004-from7-sql8)、[Q9](#t004-from7-sql9)、[Q10](#t004-from7-sql10) |
| 过滤：sheet1.Product Code in ["DW-1001040125", "DW-1203130446", "DW-1518040045", "DW-2316020016"] | [Q8](#t004-from7-sql8)、[Q9](#t004-from7-sql9)、[Q10](#t004-from7-sql10) |

##### 后续SQL原文

<a id="t004-from7-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

<a id="t004-from7-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from7-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q8：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Product Code",

       COUNT(*) AS total_rows,

       SUM(CASE WHEN is_repeat = 1 THEN 1 ELSE 0 END) AS repeat_rows
FROM (
SELECT "Product Code", "Customer ID", "Sales Month",
         CASE WHEN COUNT(*) OVER (PARTITION BY "Product Code", "Customer ID"
ORDER BY "Sales Month" ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING) > 0 THEN 1 ELSE 0 END AS is_repeat
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
)
GROUP BY "Product Code"
ORDER BY "Product Code"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Customer ID | [Q10](#t004-from8-sql10) |
| 列：sheet1.Product Code | [Q9](#t004-from8-sql9)、[Q10](#t004-from8-sql10) |
| 列：sheet1.Sales Month | [Q9](#t004-from8-sql9)、[Q10](#t004-from8-sql10) |
| 过滤：sheet1.Product Code in ["DW-1001040125", "DW-1203130446", "DW-1518040045", "DW-2316020016"] | [Q9](#t004-from8-sql9)、[Q10](#t004-from8-sql10) |

##### 后续SQL原文

<a id="t004-from8-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

<a id="t004-from8-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q9：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM (
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_sales,
         RANK() OVER (PARTITION BY "Sales Month"
ORDER BY SUM("Sales Amount") DESC) AS monthly_rank,
         COUNT(*) OVER (PARTITION BY "Sales Month") AS n_products_in_month
FROM sheet1
GROUP BY "Sales Month", "Product Code"
)
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
ORDER BY "Product Code",
"Sales Month"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Product Code | [Q10](#t004-from9-sql10) |
| 列：sheet1.Sales Amount | [Q10](#t004-from9-sql10) |
| 聚合：SUM(sheet1.Sales Amount) | [Q10](#t004-from9-sql10) |
| 过滤：sheet1.Product Code in ["DW-1001040125", "DW-1203130446", "DW-1518040045", "DW-2316020016"] | [Q10](#t004-from9-sql10) |

##### 后续SQL原文

<a id="t004-from9-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

#### Q10：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Product Code",
 SUM("Sales Amount") AS total_sales,

       COUNT(DISTINCT "Customer ID") AS total_customers,

       COUNT(DISTINCT "Sales Month") AS months_active
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125','DW-2316020016','DW-1203130446','DW-1518040045')
GROUP BY "Product Code"
ORDER BY total_sales DESC
```

</details>

没有提供未来访问预测。之后没有再查询。

<!-- task-notes-start -->
### 具体操作的差异与遗漏

下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。

### 哪些预测没有发生，哪些只说对一部分

本轮写出的5个具体分组和6个具体聚合，后来分别都有对应。这不表示整个FAD完整预测了所有查询：有些候选只写了列，实际后续增加了操作，具体遗漏见下一节。

### 实际做了，但FAD没有提前说清楚什么

| 实际SQL中的内容 | 之前FAD说到了什么 | 缺了什么 |
|---|---|---|
| Q5统计客户数和交易数；Q6按产品＋分类名称＋规格＋类型＋单位等联合分组 | 之前说过销售额汇总和若干产品属性列 | 客户计数、这组属性的联合分组没有提前描述，Unit列也未提前提到 |
| Q8用窗口判断重复购买；Q10按Product Code分组汇总 | 前面的FAD提供了相关列和产品筛选；Q9还写了销售额SUM | 窗口逻辑超出当前FAD表达范围；Q9却把group_by写为none，遗漏了Q10能表达的产品分组 |

CASE、窗口和复杂嵌套计算可能超出当前FAD表达能力；已有Schema能表达却未填写的操作，与这些表达能力限制分别看待。

### 本题高频列有没有提前说

每条成功SQL中同一列只数一次，排除第一条SQL。FAD里任何字段明确引用都算提到；这里问的是访问之前是否曾经说过，不要求紧邻上一轮。

| 列 | 后续多少条SQL访问了它 | 其中多少次已被更早FAD提到 |
|---|---|---|
| Product Code | 9条 | 9次 |
| Sales Month | 8条 | 8次 |
| Customer ID | 4条 | 4次 |
<!-- task-notes-end -->

原始数据：[events.jsonl](../runs/dacomp-004-02/events.jsonl)。本次逐项命中记录：[item-hit-rates.json](item-hit-rates.json)。

<a id="task-005"></a>

## DAComp-005：低利润率订单

### 本题命中率

**一份FAD有任意一项被后续SQL用到，就记为命中。** 没提供预测的FAD单列，不混入“有预测的FAD命中率”；同时给出占全部提交的比例。

| 统计内容 | 结果 |
|---|---|
| 共提交FAD | 21份 |
| 有预测 / 没提供预测 | 20份 / 1份 |
| **有预测的FAD命中率** | **19/20 = 95.0%** |
| 命中份数占全部提交 | 19/21 = 90.5% |

**候选访问预测的命中情况：** 每个候选中任意一项明确预测被后续SQL使用，该候选就算命中。一份FAD可以有多个候选，所以与上面的FAD份数分别统计。

| 统计内容 | 结果 |
|---|---|
| 候选总数 | 28个 |
| 命中的候选 | 27个 |
| 未命中的候选 | 1个 |
| **候选命中率** | **27/28 = 96.4%** |

**具体预测信息用了多少：** 同一份FAD中重复出现的同类信息只计一次，不同轮次重复预测分别计数。列、聚合、过滤条件、连接等值条件分别逐项数；联合分组作为一项，所列维度需在后续某个分组中一起使用，允许实际增加维度。

| 信息类别 | 提前写了多少项 | 后来使用了多少项 | 比例 |
|---|---:|---:|---|
| 列 | 186 | 155 | 155/186 = 83.3% |
| 分组 | 1 | 0 | 0/1 = 0.0% |
| 聚合 | 19 | 17 | 17/19 = 89.5% |
| 过滤 | 2 | 1 | 1/2 = 50.0% |
| 连接 | 0 | 0 | 未提供 |

命中一列就足以让该份FAD命中，并不意味着其中所有分组、聚合都对。上表用来区分“有用到一点”与“具体信息用了多少”。过滤按已知条件项匹配，连接按类型＋等值条件匹配；复杂表达式无法自动确认的部分保留在具体分析中。

### 逐轮FAD与后续query

#### Q1：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM sheet1
LIMIT 5
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Profit Margin | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q8](#t005-from1-sql8)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |
| 聚合：AVG(sheet1.Profit Margin) | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q14](#t005-from1-sql14)、[Q16](#t005-from1-sql16)、[Q19](#t005-from1-sql19) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Profit Margin | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q8](#t005-from1-sql8)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |
| 聚合：COUNT(*) | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q11](#t005-from1-sql11)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |

##### 后续SQL原文

<a id="t005-from1-sql2"></a>
<details><summary>Q2：实际SQL</summary>

```sql
SELECT COUNT(*) AS n_orders,
 AVG("Profit Margin") AS avg_profit_margin,
 MIN("Profit Margin") AS min_pm,
 MAX("Profit Margin") AS max_pm,
 AVG("Profit") AS avg_profit,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
```

</details>

<a id="t005-from1-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low_margin' ELSE 'normal' END AS seg,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_warehouse,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount") AS avg_discount,
 AVG("List Price Revenue") AS avg_list_rev
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from1-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 region
ORDER BY region,
seg
```

</details>

<a id="t005-from1-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from1-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

<a id="t005-from1-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from1-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from1-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from1-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from1-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from1-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from1-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from1-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from1-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from1-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from1-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from1-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

#### Q2：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT COUNT(*) AS n_orders,
 AVG("Profit Margin") AS avg_profit_margin,
 MIN("Profit Margin") AS min_pm,
 MAX("Profit Margin") AS max_pm,
 AVG("Profit") AS avg_profit,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Profit | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q17](#t005-from2-sql17)、[Q18](#t005-from2-sql18) |
| 列：sheet1.Profit Margin | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q8](#t005-from2-sql8)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q13](#t005-from2-sql13)、[Q14](#t005-from2-sql14)、[Q15](#t005-from2-sql15)、[Q16](#t005-from2-sql16)、[Q18](#t005-from2-sql18)、[Q19](#t005-from2-sql19) |
| 列：sheet1.Total Logistics Revenue | [Q3](#t005-from2-sql3)、[Q8](#t005-from2-sql8)、[Q10](#t005-from2-sql10)、[Q11](#t005-from2-sql11)、[Q12](#t005-from2-sql12)、[Q17](#t005-from2-sql17)、[Q18](#t005-from2-sql18)、[Q20](#t005-from2-sql20) |
| 聚合：AVG(sheet1.Profit Margin) | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q14](#t005-from2-sql14)、[Q16](#t005-from2-sql16)、[Q19](#t005-from2-sql19) |
| 聚合：COUNT(*) | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q11](#t005-from2-sql11)、[Q12](#t005-from2-sql12)、[Q13](#t005-from2-sql13)、[Q14](#t005-from2-sql14)、[Q15](#t005-from2-sql15)、[Q16](#t005-from2-sql16)、[Q18](#t005-from2-sql18)、[Q19](#t005-from2-sql19) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Profit Margin | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q8](#t005-from2-sql8)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q13](#t005-from2-sql13)、[Q14](#t005-from2-sql14)、[Q15](#t005-from2-sql15)、[Q16](#t005-from2-sql16)、[Q18](#t005-from2-sql18)、[Q19](#t005-from2-sql19) |
| 聚合：MAX(sheet1.Profit Margin) | 未找到 |
| 聚合：MIN(sheet1.Profit Margin) | 未找到 |

##### 后续SQL原文

<a id="t005-from2-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low_margin' ELSE 'normal' END AS seg,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_warehouse,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount") AS avg_discount,
 AVG("List Price Revenue") AS avg_list_rev
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from2-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 region
ORDER BY region,
seg
```

</details>

<a id="t005-from2-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from2-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

<a id="t005-from2-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from2-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from2-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from2-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from2-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from2-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from2-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from2-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from2-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from2-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from2-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from2-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from2-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from2-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q3：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low_margin' ELSE 'normal' END AS seg,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_warehouse,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount") AS avg_discount,
 AVG("List Price Revenue") AS avg_list_rev
FROM sheet1
GROUP BY seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q8](#t005-from3-sql8)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q16](#t005-from3-sql16)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19) |
| 列：sheet1.Freight Cost | [Q8](#t005-from3-sql8)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18) |
| 列：sheet1.List Price Revenue | [Q8](#t005-from3-sql8)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q16](#t005-from3-sql16)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19)、[Q20](#t005-from3-sql20) |
| 列：sheet1.Logistics Unit Price | [Q8](#t005-from3-sql8)、[Q14](#t005-from3-sql14)、[Q16](#t005-from3-sql16)、[Q20](#t005-from3-sql20) |
| 列：sheet1.Other Operating Costs | [Q11](#t005-from3-sql11)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18) |
| 列：sheet1.Profit | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q10](#t005-from3-sql10)、[Q12](#t005-from3-sql12)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18) |
| 列：sheet1.Profit Margin | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q8](#t005-from3-sql8)、[Q9](#t005-from3-sql9)、[Q10](#t005-from3-sql10)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q14](#t005-from3-sql14)、[Q15](#t005-from3-sql15)、[Q16](#t005-from3-sql16)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19) |
| 列：sheet1.Sales Quantity | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q8](#t005-from3-sql8)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q14](#t005-from3-sql14)、[Q15](#t005-from3-sql15)、[Q16](#t005-from3-sql16)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19)、[Q20](#t005-from3-sql20) |
| 列：sheet1.Total Logistics Cost | [Q8](#t005-from3-sql8)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q8](#t005-from3-sql8)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18)、[Q20](#t005-from3-sql20) |
| 列：sheet1.Warehousing Cost | [Q8](#t005-from3-sql8)、[Q11](#t005-from3-sql11)、[Q17](#t005-from3-sql17)、[Q18](#t005-from3-sql18) |
| 聚合：AVG(sheet1.Discount Amount) | [Q11](#t005-from3-sql11) |
| 聚合：AVG(sheet1.Freight Cost) | [Q11](#t005-from3-sql11) |
| 聚合：AVG(sheet1.Other Operating Costs) | [Q11](#t005-from3-sql11) |
| 聚合：AVG(sheet1.Profit Margin) | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q9](#t005-from3-sql9)、[Q10](#t005-from3-sql10)、[Q12](#t005-from3-sql12)、[Q14](#t005-from3-sql14)、[Q16](#t005-from3-sql16)、[Q19](#t005-from3-sql19) |
| 聚合：AVG(sheet1.Profit) | [Q10](#t005-from3-sql10)、[Q12](#t005-from3-sql12) |
| 聚合：AVG(sheet1.Sales Quantity) | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q12](#t005-from3-sql12)、[Q14](#t005-from3-sql14)、[Q16](#t005-from3-sql16)、[Q18](#t005-from3-sql18) |
| 聚合：AVG(sheet1.Total Logistics Cost) | [Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12) |
| 聚合：AVG(sheet1.Total Logistics Revenue) | [Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q20](#t005-from3-sql20) |
| 聚合：AVG(sheet1.Warehousing Cost) | [Q11](#t005-from3-sql11) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Destination | [Q4](#t005-from3-sql4)、[Q13](#t005-from3-sql13)、[Q15](#t005-from3-sql15) |
| 分组：sheet1.Destination | 未找到 |
| 聚合：COUNT(*) | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q9](#t005-from3-sql9)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q14](#t005-from3-sql14)、[Q15](#t005-from3-sql15)、[Q16](#t005-from3-sql16)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q5](#t005-from3-sql5)、[Q16](#t005-from3-sql16) |
| 列：sheet1.Consigned Product | [Q7](#t005-from3-sql7)、[Q14](#t005-from3-sql14) |
| 列：sheet1.Customer Gender | [Q6](#t005-from3-sql6) |

##### 后续SQL原文

<a id="t005-from3-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 region
ORDER BY region,
seg
```

</details>

<a id="t005-from3-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from3-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

<a id="t005-from3-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from3-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from3-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from3-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from3-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from3-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from3-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from3-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from3-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from3-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from3-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from3-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from3-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from3-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q4：命中（4项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 region
ORDER BY region,
seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q9](#t005-from4-sql9) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q5](#t005-from4-sql5)、[Q16](#t005-from4-sql16) |
| 列：sheet1.Customer Age | 未找到 |
| 列：sheet1.Customer Gender | [Q6](#t005-from4-sql6) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q7](#t005-from4-sql7)、[Q14](#t005-from4-sql14) |

##### 候选4：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q8](#t005-from4-sql8)、[Q10](#t005-from4-sql10)、[Q11](#t005-from4-sql11)、[Q12](#t005-from4-sql12)、[Q13](#t005-from4-sql13)、[Q16](#t005-from4-sql16)、[Q17](#t005-from4-sql17)、[Q18](#t005-from4-sql18)、[Q19](#t005-from4-sql19) |
| 列：sheet1.List Price Revenue | [Q8](#t005-from4-sql8)、[Q10](#t005-from4-sql10)、[Q11](#t005-from4-sql11)、[Q12](#t005-from4-sql12)、[Q13](#t005-from4-sql13)、[Q16](#t005-from4-sql16)、[Q18](#t005-from4-sql18)、[Q19](#t005-from4-sql19)、[Q20](#t005-from4-sql20) |
| 列：sheet1.Logistics Unit Price | [Q8](#t005-from4-sql8)、[Q14](#t005-from4-sql14)、[Q16](#t005-from4-sql16)、[Q20](#t005-from4-sql20) |
| 列：sheet1.Profit Margin | [Q5](#t005-from4-sql5)、[Q6](#t005-from4-sql6)、[Q7](#t005-from4-sql7)、[Q8](#t005-from4-sql8)、[Q9](#t005-from4-sql9)、[Q10](#t005-from4-sql10)、[Q12](#t005-from4-sql12)、[Q13](#t005-from4-sql13)、[Q14](#t005-from4-sql14)、[Q15](#t005-from4-sql15)、[Q16](#t005-from4-sql16)、[Q18](#t005-from4-sql18)、[Q19](#t005-from4-sql19) |
| 列：sheet1.Sales Quantity | [Q5](#t005-from4-sql5)、[Q6](#t005-from4-sql6)、[Q7](#t005-from4-sql7)、[Q8](#t005-from4-sql8)、[Q10](#t005-from4-sql10)、[Q11](#t005-from4-sql11)、[Q12](#t005-from4-sql12)、[Q13](#t005-from4-sql13)、[Q14](#t005-from4-sql14)、[Q15](#t005-from4-sql15)、[Q16](#t005-from4-sql16)、[Q17](#t005-from4-sql17)、[Q18](#t005-from4-sql18)、[Q19](#t005-from4-sql19)、[Q20](#t005-from4-sql20) |
| 列：sheet1.Total Logistics Cost | [Q8](#t005-from4-sql8)、[Q10](#t005-from4-sql10)、[Q11](#t005-from4-sql11)、[Q12](#t005-from4-sql12)、[Q17](#t005-from4-sql17)、[Q18](#t005-from4-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q8](#t005-from4-sql8)、[Q10](#t005-from4-sql10)、[Q11](#t005-from4-sql11)、[Q12](#t005-from4-sql12)、[Q17](#t005-from4-sql17)、[Q18](#t005-from4-sql18)、[Q20](#t005-from4-sql20) |
| 聚合：AVG(sheet1.Discount Amount) | [Q11](#t005-from4-sql11) |
| 聚合：AVG(sheet1.List Price Revenue) | [Q20](#t005-from4-sql20) |
| 聚合：AVG(sheet1.Sales Quantity) | [Q5](#t005-from4-sql5)、[Q6](#t005-from4-sql6)、[Q7](#t005-from4-sql7)、[Q12](#t005-from4-sql12)、[Q14](#t005-from4-sql14)、[Q16](#t005-from4-sql16)、[Q18](#t005-from4-sql18) |

##### 后续SQL原文

<a id="t005-from4-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from4-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

<a id="t005-from4-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from4-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from4-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from4-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from4-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from4-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from4-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from4-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from4-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from4-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from4-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from4-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from4-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from4-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q5：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q16](#t005-from5-sql16) |
| 列：sheet1.Consigned Product | [Q7](#t005-from5-sql7)、[Q14](#t005-from5-sql14) |
| 列：sheet1.Customer Gender | [Q6](#t005-from5-sql6) |
| 列：sheet1.Profit | [Q6](#t005-from5-sql6)、[Q7](#t005-from5-sql7)、[Q10](#t005-from5-sql10)、[Q12](#t005-from5-sql12)、[Q17](#t005-from5-sql17)、[Q18](#t005-from5-sql18) |
| 列：sheet1.Profit Margin | [Q6](#t005-from5-sql6)、[Q7](#t005-from5-sql7)、[Q8](#t005-from5-sql8)、[Q9](#t005-from5-sql9)、[Q10](#t005-from5-sql10)、[Q12](#t005-from5-sql12)、[Q13](#t005-from5-sql13)、[Q14](#t005-from5-sql14)、[Q15](#t005-from5-sql15)、[Q16](#t005-from5-sql16)、[Q18](#t005-from5-sql18)、[Q19](#t005-from5-sql19) |
| 列：sheet1.Sales Quantity | [Q6](#t005-from5-sql6)、[Q7](#t005-from5-sql7)、[Q8](#t005-from5-sql8)、[Q10](#t005-from5-sql10)、[Q11](#t005-from5-sql11)、[Q12](#t005-from5-sql12)、[Q13](#t005-from5-sql13)、[Q14](#t005-from5-sql14)、[Q15](#t005-from5-sql15)、[Q16](#t005-from5-sql16)、[Q17](#t005-from5-sql17)、[Q18](#t005-from5-sql18)、[Q19](#t005-from5-sql19)、[Q20](#t005-from5-sql20) |

##### 后续SQL原文

<a id="t005-from5-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

<a id="t005-from5-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from5-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from5-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from5-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from5-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from5-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from5-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from5-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from5-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from5-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from5-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from5-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from5-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from5-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q6：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Customer Gender",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Customer Gender"
ORDER BY "Customer Gender",
seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q7](#t005-from6-sql7)、[Q14](#t005-from6-sql14) |
| 列：sheet1.Customer Gender | 未找到 |
| 列：sheet1.Profit | [Q7](#t005-from6-sql7)、[Q10](#t005-from6-sql10)、[Q12](#t005-from6-sql12)、[Q17](#t005-from6-sql17)、[Q18](#t005-from6-sql18) |
| 列：sheet1.Profit Margin | [Q7](#t005-from6-sql7)、[Q8](#t005-from6-sql8)、[Q9](#t005-from6-sql9)、[Q10](#t005-from6-sql10)、[Q12](#t005-from6-sql12)、[Q13](#t005-from6-sql13)、[Q14](#t005-from6-sql14)、[Q15](#t005-from6-sql15)、[Q16](#t005-from6-sql16)、[Q18](#t005-from6-sql18)、[Q19](#t005-from6-sql19) |
| 列：sheet1.Sales Quantity | [Q7](#t005-from6-sql7)、[Q8](#t005-from6-sql8)、[Q10](#t005-from6-sql10)、[Q11](#t005-from6-sql11)、[Q12](#t005-from6-sql12)、[Q13](#t005-from6-sql13)、[Q14](#t005-from6-sql14)、[Q15](#t005-from6-sql15)、[Q16](#t005-from6-sql16)、[Q17](#t005-from6-sql17)、[Q18](#t005-from6-sql18)、[Q19](#t005-from6-sql19)、[Q20](#t005-from6-sql20) |
| 列：sheet1.Total Logistics Cost | [Q8](#t005-from6-sql8)、[Q10](#t005-from6-sql10)、[Q11](#t005-from6-sql11)、[Q12](#t005-from6-sql12)、[Q17](#t005-from6-sql17)、[Q18](#t005-from6-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q8](#t005-from6-sql8)、[Q10](#t005-from6-sql10)、[Q11](#t005-from6-sql11)、[Q12](#t005-from6-sql12)、[Q17](#t005-from6-sql17)、[Q18](#t005-from6-sql18)、[Q20](#t005-from6-sql20) |

##### 后续SQL原文

<a id="t005-from6-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

<a id="t005-from6-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from6-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from6-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from6-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from6-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from6-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from6-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from6-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from6-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from6-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from6-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from6-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from6-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q7：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Consigned Product",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 SUM("Profit") AS total_profit
FROM sheet1
GROUP BY seg,
 "Consigned Product"
ORDER BY "Consigned Product",
seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q9](#t005-from7-sql9) |
| 列：sheet1.Profit | [Q10](#t005-from7-sql10)、[Q12](#t005-from7-sql12)、[Q17](#t005-from7-sql17)、[Q18](#t005-from7-sql18) |
| 列：sheet1.Profit Margin | [Q8](#t005-from7-sql8)、[Q9](#t005-from7-sql9)、[Q10](#t005-from7-sql10)、[Q12](#t005-from7-sql12)、[Q13](#t005-from7-sql13)、[Q14](#t005-from7-sql14)、[Q15](#t005-from7-sql15)、[Q16](#t005-from7-sql16)、[Q18](#t005-from7-sql18)、[Q19](#t005-from7-sql19) |
| 列：sheet1.Sales Quantity | [Q8](#t005-from7-sql8)、[Q10](#t005-from7-sql10)、[Q11](#t005-from7-sql11)、[Q12](#t005-from7-sql12)、[Q13](#t005-from7-sql13)、[Q14](#t005-from7-sql14)、[Q15](#t005-from7-sql15)、[Q16](#t005-from7-sql16)、[Q17](#t005-from7-sql17)、[Q18](#t005-from7-sql18)、[Q19](#t005-from7-sql19)、[Q20](#t005-from7-sql20) |
| 列：sheet1.Total Logistics Cost | [Q8](#t005-from7-sql8)、[Q10](#t005-from7-sql10)、[Q11](#t005-from7-sql11)、[Q12](#t005-from7-sql12)、[Q17](#t005-from7-sql17)、[Q18](#t005-from7-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q8](#t005-from7-sql8)、[Q10](#t005-from7-sql10)、[Q11](#t005-from7-sql11)、[Q12](#t005-from7-sql12)、[Q17](#t005-from7-sql17)、[Q18](#t005-from7-sql18)、[Q20](#t005-from7-sql20) |

##### 后续SQL原文

<a id="t005-from7-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from7-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from7-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from7-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from7-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from7-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from7-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from7-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from7-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from7-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from7-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from7-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from7-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q8：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 MIN("Sales Quantity") AS min_qty,
 MAX("Sales Quantity") AS max_qty,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_discount_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS avg_freight_per_unit,
 AVG("Warehousing Cost"*1.0/"Sales Quantity") AS avg_wh_per_unit
FROM sheet1
GROUP BY seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q9](#t005-from8-sql9) |
| 列：sheet1.Discount Amount | [Q10](#t005-from8-sql10)、[Q11](#t005-from8-sql11)、[Q12](#t005-from8-sql12)、[Q13](#t005-from8-sql13)、[Q16](#t005-from8-sql16)、[Q17](#t005-from8-sql17)、[Q18](#t005-from8-sql18)、[Q19](#t005-from8-sql19) |
| 列：sheet1.List Price Revenue | [Q10](#t005-from8-sql10)、[Q11](#t005-from8-sql11)、[Q12](#t005-from8-sql12)、[Q13](#t005-from8-sql13)、[Q16](#t005-from8-sql16)、[Q18](#t005-from8-sql18)、[Q19](#t005-from8-sql19)、[Q20](#t005-from8-sql20) |
| 列：sheet1.Logistics Unit Price | [Q14](#t005-from8-sql14)、[Q16](#t005-from8-sql16)、[Q20](#t005-from8-sql20) |
| 列：sheet1.Profit | [Q10](#t005-from8-sql10)、[Q12](#t005-from8-sql12)、[Q17](#t005-from8-sql17)、[Q18](#t005-from8-sql18) |
| 列：sheet1.Profit Margin | [Q9](#t005-from8-sql9)、[Q10](#t005-from8-sql10)、[Q12](#t005-from8-sql12)、[Q13](#t005-from8-sql13)、[Q14](#t005-from8-sql14)、[Q15](#t005-from8-sql15)、[Q16](#t005-from8-sql16)、[Q18](#t005-from8-sql18)、[Q19](#t005-from8-sql19) |
| 列：sheet1.Sales Quantity | [Q10](#t005-from8-sql10)、[Q11](#t005-from8-sql11)、[Q12](#t005-from8-sql12)、[Q13](#t005-from8-sql13)、[Q14](#t005-from8-sql14)、[Q15](#t005-from8-sql15)、[Q16](#t005-from8-sql16)、[Q17](#t005-from8-sql17)、[Q18](#t005-from8-sql18)、[Q19](#t005-from8-sql19)、[Q20](#t005-from8-sql20) |
| 列：sheet1.Total Logistics Cost | [Q10](#t005-from8-sql10)、[Q11](#t005-from8-sql11)、[Q12](#t005-from8-sql12)、[Q17](#t005-from8-sql17)、[Q18](#t005-from8-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q10](#t005-from8-sql10)、[Q11](#t005-from8-sql11)、[Q12](#t005-from8-sql12)、[Q17](#t005-from8-sql17)、[Q18](#t005-from8-sql18)、[Q20](#t005-from8-sql20) |

##### 后续SQL原文

<a id="t005-from8-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

<a id="t005-from8-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from8-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from8-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from8-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from8-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from8-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from8-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from8-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from8-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from8-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from8-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q9：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT SUBSTR("Date",1,7) AS ym,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY ym
ORDER BY ym
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q10](#t005-from9-sql10)、[Q11](#t005-from9-sql11)、[Q12](#t005-from9-sql12)、[Q13](#t005-from9-sql13)、[Q16](#t005-from9-sql16)、[Q17](#t005-from9-sql17)、[Q18](#t005-from9-sql18)、[Q19](#t005-from9-sql19) |
| 列：sheet1.Profit | [Q10](#t005-from9-sql10)、[Q12](#t005-from9-sql12)、[Q17](#t005-from9-sql17)、[Q18](#t005-from9-sql18) |
| 列：sheet1.Profit Margin | [Q10](#t005-from9-sql10)、[Q12](#t005-from9-sql12)、[Q13](#t005-from9-sql13)、[Q14](#t005-from9-sql14)、[Q15](#t005-from9-sql15)、[Q16](#t005-from9-sql16)、[Q18](#t005-from9-sql18)、[Q19](#t005-from9-sql19) |
| 列：sheet1.Sales Quantity | [Q10](#t005-from9-sql10)、[Q11](#t005-from9-sql11)、[Q12](#t005-from9-sql12)、[Q13](#t005-from9-sql13)、[Q14](#t005-from9-sql14)、[Q15](#t005-from9-sql15)、[Q16](#t005-from9-sql16)、[Q17](#t005-from9-sql17)、[Q18](#t005-from9-sql18)、[Q19](#t005-from9-sql19)、[Q20](#t005-from9-sql20) |
| 列：sheet1.Total Logistics Cost | [Q10](#t005-from9-sql10)、[Q11](#t005-from9-sql11)、[Q12](#t005-from9-sql12)、[Q17](#t005-from9-sql17)、[Q18](#t005-from9-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q10](#t005-from9-sql10)、[Q11](#t005-from9-sql11)、[Q12](#t005-from9-sql12)、[Q17](#t005-from9-sql17)、[Q18](#t005-from9-sql18)、[Q20](#t005-from9-sql20) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | 未找到 |
| 列：sheet1.Profit Margin | [Q10](#t005-from9-sql10)、[Q12](#t005-from9-sql12)、[Q13](#t005-from9-sql13)、[Q14](#t005-from9-sql14)、[Q15](#t005-from9-sql15)、[Q16](#t005-from9-sql16)、[Q18](#t005-from9-sql18)、[Q19](#t005-from9-sql19) |

##### 后续SQL原文

<a id="t005-from9-sql10"></a>
<details><summary>Q10：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from9-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from9-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from9-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from9-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from9-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from9-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from9-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from9-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from9-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from9-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q10：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS avg_disc_ratio,
 AVG("Total Logistics Cost"*1.0/"Total Logistics Revenue") AS avg_cost_rev_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q11](#t005-from10-sql11)、[Q12](#t005-from10-sql12)、[Q13](#t005-from10-sql13)、[Q16](#t005-from10-sql16)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18)、[Q19](#t005-from10-sql19) |
| 列：sheet1.Freight Cost | [Q11](#t005-from10-sql11)、[Q12](#t005-from10-sql12)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18) |
| 列：sheet1.Other Operating Costs | [Q11](#t005-from10-sql11)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18) |
| 列：sheet1.Profit | [Q12](#t005-from10-sql12)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18) |
| 列：sheet1.Profit Margin | [Q12](#t005-from10-sql12)、[Q13](#t005-from10-sql13)、[Q14](#t005-from10-sql14)、[Q15](#t005-from10-sql15)、[Q16](#t005-from10-sql16)、[Q18](#t005-from10-sql18)、[Q19](#t005-from10-sql19) |
| 列：sheet1.Sales Quantity | [Q11](#t005-from10-sql11)、[Q12](#t005-from10-sql12)、[Q13](#t005-from10-sql13)、[Q14](#t005-from10-sql14)、[Q15](#t005-from10-sql15)、[Q16](#t005-from10-sql16)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18)、[Q19](#t005-from10-sql19)、[Q20](#t005-from10-sql20) |
| 列：sheet1.Total Logistics Cost | [Q11](#t005-from10-sql11)、[Q12](#t005-from10-sql12)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q11](#t005-from10-sql11)、[Q12](#t005-from10-sql12)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18)、[Q20](#t005-from10-sql20) |
| 列：sheet1.Warehousing Cost | [Q11](#t005-from10-sql11)、[Q17](#t005-from10-sql17)、[Q18](#t005-from10-sql18) |

##### 后续SQL原文

<a id="t005-from10-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

<a id="t005-from10-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from10-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from10-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from10-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from10-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from10-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from10-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from10-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from10-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q11：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN '1-10' WHEN "Sales Quantity" <= 20 THEN '11-20' WHEN "Sales Quantity" <= 30 THEN '21-30' WHEN "Sales Quantity" <= 50 THEN '31-50' ELSE '>50' END AS qty_bucket,
 COUNT(*) AS n,
 AVG("Freight Cost") AS avg_freight,
 AVG("Warehousing Cost") AS avg_wh,
 AVG("Other Operating Costs") AS avg_other,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Discount Amount") AS avg_disc_amt,
 AVG("Discount Amount"*1.0/"List Price Revenue") AS disc_ratio
FROM sheet1
GROUP BY qty_bucket
ORDER BY MIN("Sales Quantity")
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Destination | [Q13](#t005-from11-sql13)、[Q15](#t005-from11-sql15) |
| 列：sheet1.Discount Amount | [Q12](#t005-from11-sql12)、[Q13](#t005-from11-sql13)、[Q16](#t005-from11-sql16)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18)、[Q19](#t005-from11-sql19) |
| 列：sheet1.Freight Cost | [Q12](#t005-from11-sql12)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18) |
| 列：sheet1.Other Operating Costs | [Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18) |
| 列：sheet1.Profit | [Q12](#t005-from11-sql12)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18) |
| 列：sheet1.Profit Margin | [Q12](#t005-from11-sql12)、[Q13](#t005-from11-sql13)、[Q14](#t005-from11-sql14)、[Q15](#t005-from11-sql15)、[Q16](#t005-from11-sql16)、[Q18](#t005-from11-sql18)、[Q19](#t005-from11-sql19) |
| 列：sheet1.Sales Quantity | [Q12](#t005-from11-sql12)、[Q13](#t005-from11-sql13)、[Q14](#t005-from11-sql14)、[Q15](#t005-from11-sql15)、[Q16](#t005-from11-sql16)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18)、[Q19](#t005-from11-sql19)、[Q20](#t005-from11-sql20) |
| 列：sheet1.Total Logistics Cost | [Q12](#t005-from11-sql12)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q12](#t005-from11-sql12)、[Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18)、[Q20](#t005-from11-sql20) |
| 列：sheet1.Warehousing Cost | [Q17](#t005-from11-sql17)、[Q18](#t005-from11-sql18) |

##### 后续SQL原文

<a id="t005-from11-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

<a id="t005-from11-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from11-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from11-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from11-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from11-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from11-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from11-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from11-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q12：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.05 THEN '<5%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.15 THEN '5-15%' WHEN "Discount Amount"*1.0/NULLIF("List Price Revenue",0) < 0.30 THEN '15-30%' ELSE '>30%' END AS disc_bucket,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Profit") AS avg_profit,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Freight Cost"*1.0/"Sales Quantity") AS freight_per_unit,
 AVG("Total Logistics Cost") AS avg_cost,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY disc_bucket
ORDER BY MIN("Discount Amount"*1.0/NULLIF("List Price Revenue",0))
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q16](#t005-from12-sql16) |
| 列：sheet1.Consigned Product | [Q14](#t005-from12-sql14) |
| 列：sheet1.Customer Gender | 未找到 |
| 列：sheet1.Destination | [Q13](#t005-from12-sql13)、[Q15](#t005-from12-sql15) |
| 列：sheet1.Discount Amount | [Q13](#t005-from12-sql13)、[Q16](#t005-from12-sql16)、[Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18)、[Q19](#t005-from12-sql19) |
| 列：sheet1.Freight Cost | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18) |
| 列：sheet1.List Price Revenue | [Q13](#t005-from12-sql13)、[Q16](#t005-from12-sql16)、[Q18](#t005-from12-sql18)、[Q19](#t005-from12-sql19)、[Q20](#t005-from12-sql20) |
| 列：sheet1.Logistics Unit Price | [Q14](#t005-from12-sql14)、[Q16](#t005-from12-sql16)、[Q20](#t005-from12-sql20) |
| 列：sheet1.Other Operating Costs | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18) |
| 列：sheet1.Profit | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18) |
| 列：sheet1.Profit Margin | [Q13](#t005-from12-sql13)、[Q14](#t005-from12-sql14)、[Q15](#t005-from12-sql15)、[Q16](#t005-from12-sql16)、[Q18](#t005-from12-sql18)、[Q19](#t005-from12-sql19) |
| 列：sheet1.Sales Quantity | [Q13](#t005-from12-sql13)、[Q14](#t005-from12-sql14)、[Q15](#t005-from12-sql15)、[Q16](#t005-from12-sql16)、[Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18)、[Q19](#t005-from12-sql19)、[Q20](#t005-from12-sql20) |
| 列：sheet1.Total Logistics Cost | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18)、[Q20](#t005-from12-sql20) |
| 列：sheet1.Warehousing Cost | [Q17](#t005-from12-sql17)、[Q18](#t005-from12-sql18) |
| 过滤：sheet1.Sales Quantity le 10.0 | [Q16](#t005-from12-sql16) |

##### 后续SQL原文

<a id="t005-from12-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

<a id="t005-from12-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from12-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from12-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from12-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from12-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from12-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from12-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q13：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT SUBSTR("Destination", 1, INSTR("Destination", '-')-1) AS region,
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 THEN 1 ELSE 0 END) AS n_small_high_disc,
 SUM(CASE WHEN "Sales Quantity" <= 10 AND "Discount Amount"*1.0/NULLIF("List Price Revenue",0) >= 0.15 AND "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_small_high_disc_low
FROM sheet1
GROUP BY region
ORDER BY n_small DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q16](#t005-from13-sql16) |
| 列：sheet1.Consigned Product | [Q14](#t005-from13-sql14) |
| 列：sheet1.Customer Age | 未找到 |
| 列：sheet1.Customer Gender | 未找到 |
| 列：sheet1.Destination | [Q15](#t005-from13-sql15) |
| 列：sheet1.Discount Amount | [Q16](#t005-from13-sql16)、[Q17](#t005-from13-sql17)、[Q18](#t005-from13-sql18)、[Q19](#t005-from13-sql19) |
| 列：sheet1.Profit | [Q17](#t005-from13-sql17)、[Q18](#t005-from13-sql18) |
| 列：sheet1.Profit Margin | [Q14](#t005-from13-sql14)、[Q15](#t005-from13-sql15)、[Q16](#t005-from13-sql16)、[Q18](#t005-from13-sql18)、[Q19](#t005-from13-sql19) |
| 列：sheet1.Sales Quantity | [Q14](#t005-from13-sql14)、[Q15](#t005-from13-sql15)、[Q16](#t005-from13-sql16)、[Q17](#t005-from13-sql17)、[Q18](#t005-from13-sql18)、[Q19](#t005-from13-sql19)、[Q20](#t005-from13-sql20) |
| 列：sheet1.Total Logistics Cost | [Q17](#t005-from13-sql17)、[Q18](#t005-from13-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t005-from13-sql17)、[Q18](#t005-from13-sql18)、[Q20](#t005-from13-sql20) |

##### 后续SQL原文

<a id="t005-from13-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

<a id="t005-from13-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from13-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from13-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from13-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from13-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from13-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q14：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Consigned Product",
 COUNT(*) AS n,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small,
 ROUND(100.0*SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END)/COUNT(*),2) AS small_pct,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Profit Margin") AS avg_pm
FROM sheet1
GROUP BY "Consigned Product"
ORDER BY small_pct DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | 未找到 |
| 列：sheet1.Destination | [Q15](#t005-from14-sql15) |
| 列：sheet1.Discount Amount | [Q16](#t005-from14-sql16)、[Q17](#t005-from14-sql17)、[Q18](#t005-from14-sql18)、[Q19](#t005-from14-sql19) |
| 列：sheet1.List Price Revenue | [Q16](#t005-from14-sql16)、[Q18](#t005-from14-sql18)、[Q19](#t005-from14-sql19)、[Q20](#t005-from14-sql20) |
| 列：sheet1.Logistics Unit Price | [Q16](#t005-from14-sql16)、[Q20](#t005-from14-sql20) |
| 列：sheet1.Profit | [Q17](#t005-from14-sql17)、[Q18](#t005-from14-sql18) |
| 列：sheet1.Profit Margin | [Q15](#t005-from14-sql15)、[Q16](#t005-from14-sql16)、[Q18](#t005-from14-sql18)、[Q19](#t005-from14-sql19) |
| 列：sheet1.Sales Quantity | [Q15](#t005-from14-sql15)、[Q16](#t005-from14-sql16)、[Q17](#t005-from14-sql17)、[Q18](#t005-from14-sql18)、[Q19](#t005-from14-sql19)、[Q20](#t005-from14-sql20) |
| 列：sheet1.Total Logistics Cost | [Q17](#t005-from14-sql17)、[Q18](#t005-from14-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t005-from14-sql17)、[Q18](#t005-from14-sql18)、[Q20](#t005-from14-sql20) |

##### 后续SQL原文

<a id="t005-from14-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

<a id="t005-from14-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from14-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from14-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from14-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from14-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q15：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT SUBSTR("Destination", INSTR("Destination", '-')+1) AS province_city,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),2) AS low_pct,
 SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS n_small
FROM sheet1
GROUP BY province_city
HAVING n >= 100
ORDER BY low_pct DESC
LIMIT 15
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | [Q16](#t005-from15-sql16) |
| 列：sheet1.Customer Age | 未找到 |
| 列：sheet1.Customer Gender | 未找到 |
| 列：sheet1.Destination | 未找到 |
| 列：sheet1.Discount Amount | [Q16](#t005-from15-sql16)、[Q17](#t005-from15-sql17)、[Q18](#t005-from15-sql18)、[Q19](#t005-from15-sql19) |
| 列：sheet1.Profit | [Q17](#t005-from15-sql17)、[Q18](#t005-from15-sql18) |
| 列：sheet1.Profit Margin | [Q16](#t005-from15-sql16)、[Q18](#t005-from15-sql18)、[Q19](#t005-from15-sql19) |
| 列：sheet1.Sales Quantity | [Q16](#t005-from15-sql16)、[Q17](#t005-from15-sql17)、[Q18](#t005-from15-sql18)、[Q19](#t005-from15-sql19)、[Q20](#t005-from15-sql20) |
| 列：sheet1.Total Logistics Cost | [Q17](#t005-from15-sql17)、[Q18](#t005-from15-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t005-from15-sql17)、[Q18](#t005-from15-sql18)、[Q20](#t005-from15-sql20) |

##### 后续SQL原文

<a id="t005-from15-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

<a id="t005-from15-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from15-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from15-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from15-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q16：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 'low' ELSE 'normal' END AS seg,
 "Age Range",
 COUNT(*) AS n,
 AVG("Profit Margin") AS avg_pm,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio,
 AVG("Logistics Unit Price") AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" <= 10
GROUP BY seg,
 "Age Range"
ORDER BY "Age Range",
seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Age Range | 未找到 |
| 列：sheet1.Customer Age | 未找到 |
| 列：sheet1.Customer Gender | 未找到 |
| 列：sheet1.Discount Amount | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18)、[Q19](#t005-from16-sql19) |
| 列：sheet1.Freight Cost | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18) |
| 列：sheet1.List Price Revenue | [Q18](#t005-from16-sql18)、[Q19](#t005-from16-sql19)、[Q20](#t005-from16-sql20) |
| 列：sheet1.Logistics Unit Price | [Q20](#t005-from16-sql20) |
| 列：sheet1.Other Operating Costs | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18) |
| 列：sheet1.Profit | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18) |
| 列：sheet1.Profit Margin | [Q18](#t005-from16-sql18)、[Q19](#t005-from16-sql19) |
| 列：sheet1.Sales Quantity | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18)、[Q19](#t005-from16-sql19)、[Q20](#t005-from16-sql20) |
| 列：sheet1.Total Logistics Cost | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18)、[Q20](#t005-from16-sql20) |
| 列：sheet1.Warehousing Cost | [Q17](#t005-from16-sql17)、[Q18](#t005-from16-sql18) |
| 过滤：sheet1.Sales Quantity le 10.0 | 未找到 |

##### 后续SQL原文

<a id="t005-from16-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

<a id="t005-from16-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from16-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from16-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q17：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small_le10' ELSE 'large_gt10' END AS size_seg,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 SUM("Discount Amount") AS total_discount
FROM sheet1
GROUP BY size_seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q18](#t005-from17-sql18)、[Q19](#t005-from17-sql19) |
| 列：sheet1.Freight Cost | [Q18](#t005-from17-sql18) |
| 列：sheet1.List Price Revenue | [Q18](#t005-from17-sql18)、[Q19](#t005-from17-sql19)、[Q20](#t005-from17-sql20) |
| 列：sheet1.Logistics Unit Price | [Q20](#t005-from17-sql20) |
| 列：sheet1.Other Operating Costs | [Q18](#t005-from17-sql18) |
| 列：sheet1.Profit | [Q18](#t005-from17-sql18) |
| 列：sheet1.Profit Margin | [Q18](#t005-from17-sql18)、[Q19](#t005-from17-sql19) |
| 列：sheet1.Sales Quantity | [Q18](#t005-from17-sql18)、[Q19](#t005-from17-sql19)、[Q20](#t005-from17-sql20) |
| 列：sheet1.Total Logistics Cost | [Q18](#t005-from17-sql18) |
| 列：sheet1.Total Logistics Revenue | [Q18](#t005-from17-sql18)、[Q20](#t005-from17-sql20) |
| 列：sheet1.Warehousing Cost | [Q18](#t005-from17-sql18) |

##### 后续SQL原文

<a id="t005-from17-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

<a id="t005-from17-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from17-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q18：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 AND "Profit Margin" < 0.3976434082191792 THEN 'low_small' WHEN "Sales Quantity" <= 10 THEN 'normal_small' ELSE 'large' END AS seg,
 COUNT(*) AS n,
 SUM("Profit") AS total_profit,
 SUM("Total Logistics Revenue") AS total_rev,
 SUM("Total Logistics Cost") AS total_cost,
 SUM("Discount Amount") AS total_disc,
 SUM("Freight Cost") AS total_freight,
 SUM("Warehousing Cost") AS total_wh,
 SUM("Other Operating Costs") AS total_other,
 AVG("Sales Quantity") AS avg_qty,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS avg_disc_ratio
FROM sheet1
GROUP BY seg
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | [Q19](#t005-from18-sql19) |
| 列：sheet1.Freight Cost | 未找到 |
| 列：sheet1.List Price Revenue | [Q19](#t005-from18-sql19)、[Q20](#t005-from18-sql20) |
| 列：sheet1.Logistics Unit Price | [Q20](#t005-from18-sql20) |
| 列：sheet1.Logistics Value-Added Service Revenue | [Q19](#t005-from18-sql19)、[Q20](#t005-from18-sql20) |
| 列：sheet1.Other Operating Costs | 未找到 |
| 列：sheet1.Profit | 未找到 |
| 列：sheet1.Profit Margin | [Q19](#t005-from18-sql19) |
| 列：sheet1.Sales Quantity | [Q19](#t005-from18-sql19)、[Q20](#t005-from18-sql20) |
| 列：sheet1.Total Logistics Cost | 未找到 |
| 列：sheet1.Total Logistics Revenue | [Q20](#t005-from18-sql20) |
| 列：sheet1.Warehousing Cost | 未找到 |

##### 后续SQL原文

<a id="t005-from18-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

<a id="t005-from18-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q19：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Sales Quantity" AS qty,
 COUNT(*) AS n,
 SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END) AS n_low,
 ROUND(100.0*SUM(CASE WHEN "Profit Margin" < 0.3976434082191792 THEN 1 ELSE 0 END)/COUNT(*),1) AS low_pct,
 AVG("Profit Margin") AS avg_pm,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 AVG("Discount Amount"*1.0/NULLIF("List Price Revenue",0)) AS disc_ratio
FROM sheet1
GROUP BY qty
HAVING qty <= 10
ORDER BY qty
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | 未找到 |
| 列：sheet1.List Price Revenue | [Q20](#t005-from19-sql20) |
| 列：sheet1.Logistics Unit Price | [Q20](#t005-from19-sql20) |
| 列：sheet1.Logistics Value-Added Service Revenue | [Q20](#t005-from19-sql20) |
| 列：sheet1.Profit | 未找到 |
| 列：sheet1.Profit Margin | 未找到 |
| 列：sheet1.Sales Quantity | [Q20](#t005-from19-sql20) |
| 列：sheet1.Total Logistics Cost | 未找到 |
| 列：sheet1.Total Logistics Revenue | [Q20](#t005-from19-sql20) |

##### 后续SQL原文

<a id="t005-from19-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

#### Q20：未命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS size_seg,
 AVG("Logistics Value-Added Service Revenue") AS avg_vas,
 SUM("Logistics Value-Added Service Revenue") AS total_vas,
 AVG("Logistics Unit Price") AS avg_unit_price,
 AVG("List Price Revenue") AS avg_list_rev,
 AVG("Total Logistics Revenue") AS avg_rev
FROM sheet1
GROUP BY size_seg
```

</details>

##### 候选1：未命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Discount Amount | 未找到 |
| 列：sheet1.List Price Revenue | 未找到 |
| 列：sheet1.Logistics Unit Price | 未找到 |
| 列：sheet1.Logistics Value-Added Service Revenue | 未找到 |
| 列：sheet1.Profit | 未找到 |
| 列：sheet1.Profit Margin | 未找到 |
| 列：sheet1.Sales Quantity | 未找到 |
| 列：sheet1.Total Logistics Cost | 未找到 |
| 列：sheet1.Total Logistics Revenue | 未找到 |

##### 后续SQL原文

<details><summary>Q21：实际SQL</summary>

```sql
SELECT 1
```

</details>

#### Q21：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 1
```

</details>

没有提供未来访问预测。之后没有再查询。

<!-- task-notes-start -->
### 具体操作的差异与遗漏

下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。

### 哪些预测没有发生，哪些只说对一部分

| 提出预测的轮次 | FAD说了什么 | 后面实际情况 | 判断 |
|---|---|---|---|
| Q2候选2 | 后续再查利润率MIN和MAX | MIN/MAX(Profit Margin)只在当前Q2执行，后续没有再执行这两项 | 不算提前预测成功，属于把当前访问当成未来访问的表现 |
| Q3候选2 | 按完整Destination分组，统计订单数 | Q4先从Destination提取大区，再与低利润率/正常分段联合分组 | 地理分析方向相近，但分组粒度与维度组合不同，只能说方向部分对应 |
| Q3候选1 | 在一个候选里列出利润率、利润、收入、成本、运费等九项AVG | 九项AVG后来各自都能找到，但没有一条后续SQL同时计算全部九项 | 聚合项目有依据，但候选将后续查询组合得过大。不能说九项全错，也不能说整组访问完整发生 |

### 实际做了，但FAD没有提前说清楚什么

| 实际SQL中的内容 | 之前FAD说到了什么 | 缺了什么 |
|---|---|---|
| Q3开始把订单分成低利润率和正常两组，之后与地区、年龄、性别、产品等联合分组 | 相关字段大多提前列出，group_by却基本为空 | 低/正常分段属于CASE表达式，协议不直接支持；但年龄、性别、产品这些支持的分组部分也没有填出来 |

CASE、窗口和复杂嵌套计算可能超出当前FAD表达能力；已有Schema能表达却未填写的操作，与这些表达能力限制分别看待。

### 本题高频列有没有提前说

每条成功SQL中同一列只数一次，排除第一条SQL。FAD里任何字段明确引用都算提到；这里问的是访问之前是否曾经说过，不要求紧邻上一轮。

| 列 | 后续多少条SQL访问了它 | 其中多少次已被更早FAD提到 |
|---|---|---|
| Profit Margin | 16条 | 16次 |
| Sales Quantity | 17条 | 16次 |
| Profit | 10条 | 9次 |
<!-- task-notes-end -->

原始数据：[events.jsonl](../runs/dacomp-005-02/events.jsonl)。本次逐项命中记录：[item-hit-rates.json](item-hit-rates.json)。

<a id="task-006"></a>

## DAComp-006：华南利润波动

### 本题命中率

**一份FAD有任意一项被后续SQL用到，就记为命中。** 没提供预测的FAD单列，不混入“有预测的FAD命中率”；同时给出占全部提交的比例。

| 统计内容 | 结果 |
|---|---|
| 共提交FAD | 30份 |
| 有预测 / 没提供预测 | 29份 / 1份 |
| **有预测的FAD命中率** | **29/29 = 100.0%** |
| 命中份数占全部提交 | 29/30 = 96.7% |

**候选访问预测的命中情况：** 每个候选中任意一项明确预测被后续SQL使用，该候选就算命中。一份FAD可以有多个候选，所以与上面的FAD份数分别统计。

| 统计内容 | 结果 |
|---|---|
| 候选总数 | 58个 |
| 命中的候选 | 58个 |
| 未命中的候选 | 0个 |
| **候选命中率** | **58/58 = 100.0%** |

**具体预测信息用了多少：** 同一份FAD中重复出现的同类信息只计一次，不同轮次重复预测分别计数。列、聚合、过滤条件、连接等值条件分别逐项数；联合分组作为一项，所列维度需在后续某个分组中一起使用，允许实际增加维度。

| 信息类别 | 提前写了多少项 | 后来使用了多少项 | 比例 |
|---|---:|---:|---|
| 列 | 173 | 168 | 168/173 = 97.1% |
| 分组 | 49 | 36 | 36/49 = 73.5% |
| 聚合 | 94 | 75 | 75/94 = 79.8% |
| 过滤 | 31 | 27 | 27/31 = 87.1% |
| 连接 | 0 | 0 | 未提供 |

命中一列就足以让该份FAD命中，并不意味着其中所有分组、聚合都对。上表用来区分“有用到一点”与“具体信息用了多少”。过滤按已知条件项匹配，连接按类型＋等值条件匹配；复杂表达式无法自动确认的部分保留在具体分析中。

### 逐轮FAD与后续query

#### Q1：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT Destination,
 COUNT(*) AS cnt
FROM sheet1
GROUP BY Destination
ORDER BY cnt DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q2](#t006-from1-sql2)、[Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q24](#t006-from1-sql24)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29)、[Q30](#t006-from1-sql30) |
| 列：sheet1.Destination | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q5](#t006-from1-sql5)、[Q6](#t006-from1-sql6)、[Q7](#t006-from1-sql7)、[Q8](#t006-from1-sql8)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q23](#t006-from1-sql23)、[Q24](#t006-from1-sql24)、[Q25](#t006-from1-sql25)、[Q26](#t006-from1-sql26)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29)、[Q30](#t006-from1-sql30) |
| 分组：sheet1.Destination | [Q4](#t006-from1-sql4)、[Q14](#t006-from1-sql14)、[Q22](#t006-from1-sql22) |
| 聚合：COUNT(*) | [Q2](#t006-from1-sql2)、[Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q17](#t006-from1-sql17)、[Q19](#t006-from1-sql19)、[Q25](#t006-from1-sql25)、[Q30](#t006-from1-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q2](#t006-from1-sql2)、[Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q24](#t006-from1-sql24)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29)、[Q30](#t006-from1-sql30) |
| 列：sheet1.Destination | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q5](#t006-from1-sql5)、[Q6](#t006-from1-sql6)、[Q7](#t006-from1-sql7)、[Q8](#t006-from1-sql8)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q23](#t006-from1-sql23)、[Q24](#t006-from1-sql24)、[Q25](#t006-from1-sql25)、[Q26](#t006-from1-sql26)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29)、[Q30](#t006-from1-sql30) |
| 列：sheet1.Profit | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q25](#t006-from1-sql25)、[Q26](#t006-from1-sql26)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29) |
| 分组：sheet1.Date（按月） | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q24](#t006-from1-sql24)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q30](#t006-from1-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q25](#t006-from1-sql25)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28) |

##### 后续SQL原文

<a id="t006-from1-sql2"></a>
<details><summary>Q2：实际SQL</summary>

```sql
SELECT MIN(Date) AS min_date,
 MAX(Date) AS max_date,
 COUNT(*) AS total_rows
FROM sheet1
```

</details>

<a id="t006-from1-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS total_profit,
 COUNT(*) AS orders,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("Total Logistics Cost") AS cost,
 SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 Destination,
 SUM(Profit) AS profit,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 Destination
ORDER BY month,
Destination
```

</details>

<a id="t006-from1-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from1-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from1-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from1-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from1-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from1-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from1-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from1-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from1-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from1-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from1-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from1-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from1-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from1-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from1-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from1-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from1-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from1-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q2：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT MIN(Date) AS min_date,
 MAX(Date) AS max_date,
 COUNT(*) AS total_rows
FROM sheet1
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q11](#t006-from2-sql11)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q20](#t006-from2-sql20)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q24](#t006-from2-sql24)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q29](#t006-from2-sql29)、[Q30](#t006-from2-sql30) |
| 列：sheet1.Destination | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q5](#t006-from2-sql5)、[Q6](#t006-from2-sql6)、[Q7](#t006-from2-sql7)、[Q8](#t006-from2-sql8)、[Q9](#t006-from2-sql9)、[Q11](#t006-from2-sql11)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q20](#t006-from2-sql20)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q23](#t006-from2-sql23)、[Q24](#t006-from2-sql24)、[Q25](#t006-from2-sql25)、[Q26](#t006-from2-sql26)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q29](#t006-from2-sql29)、[Q30](#t006-from2-sql30) |
| 列：sheet1.Profit | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q20](#t006-from2-sql20)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q25](#t006-from2-sql25)、[Q26](#t006-from2-sql26)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q29](#t006-from2-sql29) |
| 分组：sheet1.Date（按月） | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q11](#t006-from2-sql11)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q24](#t006-from2-sql24)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q30](#t006-from2-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q25](#t006-from2-sql25)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28) |

##### 后续SQL原文

<a id="t006-from2-sql3"></a>
<details><summary>Q3：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS total_profit,
 COUNT(*) AS orders,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("Total Logistics Cost") AS cost,
 SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 Destination,
 SUM(Profit) AS profit,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 Destination
ORDER BY month,
Destination
```

</details>

<a id="t006-from2-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from2-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from2-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from2-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from2-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from2-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from2-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from2-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from2-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from2-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from2-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from2-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from2-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from2-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from2-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from2-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from2-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from2-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q3：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS total_profit,
 COUNT(*) AS orders,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("Total Logistics Cost") AS cost,
 SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q24](#t006-from3-sql24)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 列：sheet1.Destination | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 列：sheet1.Profit | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29) |
| 列：sheet1.Sales Quantity | [Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q15](#t006-from3-sql15)、[Q17](#t006-from3-sql17)、[Q20](#t006-from3-sql20)、[Q24](#t006-from3-sql24)、[Q26](#t006-from3-sql26) |
| 列：sheet1.Total Logistics Cost | [Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q17](#t006-from3-sql17)、[Q20](#t006-from3-sql20)、[Q26](#t006-from3-sql26)、[Q29](#t006-from3-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q17](#t006-from3-sql17)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q26](#t006-from3-sql26)、[Q29](#t006-from3-sql29) |
| 分组：sheet1.Date（按月） | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q24](#t006-from3-sql24)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q30](#t006-from3-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q24](#t006-from3-sql24)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 列：sheet1.Destination | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 列：sheet1.Profit | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q4](#t006-from3-sql4)、[Q14](#t006-from3-sql14)、[Q22](#t006-from3-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |

##### 后续SQL原文

<a id="t006-from3-sql4"></a>
<details><summary>Q4：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 Destination,
 SUM(Profit) AS profit,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 Destination
ORDER BY month,
Destination
```

</details>

<a id="t006-from3-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from3-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from3-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from3-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from3-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from3-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from3-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from3-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from3-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from3-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from3-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from3-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from3-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from3-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from3-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from3-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from3-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from3-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q4：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 Destination,
 SUM(Profit) AS profit,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 Destination
ORDER BY month,
Destination
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q5](#t006-from4-sql5)、[Q7](#t006-from4-sql7)、[Q13](#t006-from4-sql13)、[Q15](#t006-from4-sql15)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q26](#t006-from4-sql26)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Date | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q24](#t006-from4-sql24)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 列：sheet1.Destination | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 列：sheet1.Profit | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Sales Quantity | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q15](#t006-from4-sql15)、[Q17](#t006-from4-sql17)、[Q20](#t006-from4-sql20)、[Q24](#t006-from4-sql24)、[Q26](#t006-from4-sql26) |
| 列：sheet1.Total Logistics Cost | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q20](#t006-from4-sql20)、[Q26](#t006-from4-sql26)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q26](#t006-from4-sql26)、[Q29](#t006-from4-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q7](#t006-from4-sql7)、[Q13](#t006-from4-sql13)、[Q15](#t006-from4-sql15)、[Q21](#t006-from4-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q25](#t006-from4-sql25)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q15](#t006-from4-sql15)、[Q17](#t006-from4-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q19](#t006-from4-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q24](#t006-from4-sql24)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 列：sheet1.Destination | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 列：sheet1.Discount Amount | [Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q24](#t006-from4-sql24) |
| 列：sheet1.Logistics Unit Price | [Q24](#t006-from4-sql24) |
| 列：sheet1.Profit | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Profit Margin | [Q11](#t006-from4-sql11)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Total Logistics Cost | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q20](#t006-from4-sql20)、[Q26](#t006-from4-sql26)、[Q29](#t006-from4-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q26](#t006-from4-sql26)、[Q29](#t006-from4-sql29) |
| 分组：sheet1.Date（按月） | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q24](#t006-from4-sql24)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q30](#t006-from4-sql30) |
| 聚合：AVG(sheet1.Profit Margin) | [Q11](#t006-from4-sql11)、[Q19](#t006-from4-sql19) |
| 聚合：SUM(sheet1.Discount Amount) | [Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q24](#t006-from4-sql24) |
| 聚合：SUM(sheet1.Logistics Unit Price) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |

##### 后续SQL原文

<a id="t006-from4-sql5"></a>
<details><summary>Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from4-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from4-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from4-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from4-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from4-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from4-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from4-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from4-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from4-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from4-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from4-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from4-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from4-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from4-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from4-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from4-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from4-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q5：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q7](#t006-from5-sql7)、[Q13](#t006-from5-sql13)、[Q15](#t006-from5-sql15)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q26](#t006-from5-sql26)、[Q29](#t006-from5-sql29) |
| 列：sheet1.Date | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q24](#t006-from5-sql24)、[Q27](#t006-from5-sql27)、[Q28](#t006-from5-sql28)、[Q29](#t006-from5-sql29)、[Q30](#t006-from5-sql30) |
| 列：sheet1.Destination | [Q6](#t006-from5-sql6)、[Q7](#t006-from5-sql7)、[Q8](#t006-from5-sql8)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q23](#t006-from5-sql23)、[Q24](#t006-from5-sql24)、[Q25](#t006-from5-sql25)、[Q26](#t006-from5-sql26)、[Q27](#t006-from5-sql27)、[Q28](#t006-from5-sql28)、[Q29](#t006-from5-sql29)、[Q30](#t006-from5-sql30) |
| 列：sheet1.Profit | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q25](#t006-from5-sql25)、[Q26](#t006-from5-sql26)、[Q27](#t006-from5-sql27)、[Q28](#t006-from5-sql28)、[Q29](#t006-from5-sql29) |
| 列：sheet1.Sales Quantity | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q15](#t006-from5-sql15)、[Q17](#t006-from5-sql17)、[Q20](#t006-from5-sql20)、[Q24](#t006-from5-sql24)、[Q26](#t006-from5-sql26) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q17](#t006-from5-sql17)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q26](#t006-from5-sql26)、[Q29](#t006-from5-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q7](#t006-from5-sql7)、[Q13](#t006-from5-sql13)、[Q15](#t006-from5-sql15)、[Q21](#t006-from5-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q25](#t006-from5-sql25)、[Q27](#t006-from5-sql27)、[Q28](#t006-from5-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q15](#t006-from5-sql15)、[Q17](#t006-from5-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q17](#t006-from5-sql17)、[Q19](#t006-from5-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q6](#t006-from5-sql6)、[Q7](#t006-from5-sql7)、[Q8](#t006-from5-sql8)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q23](#t006-from5-sql23)、[Q24](#t006-from5-sql24)、[Q25](#t006-from5-sql25)、[Q26](#t006-from5-sql26)、[Q27](#t006-from5-sql27)、[Q29](#t006-from5-sql29)、[Q30](#t006-from5-sql30) |

##### 后续SQL原文

<a id="t006-from5-sql6"></a>
<details><summary>Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from5-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from5-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from5-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from5-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from5-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from5-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from5-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from5-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from5-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from5-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from5-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from5-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from5-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from5-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from5-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from5-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q6：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q7](#t006-from6-sql7)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q26](#t006-from6-sql26)、[Q29](#t006-from6-sql29) |
| 列：sheet1.Date | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q24](#t006-from6-sql24)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 列：sheet1.Destination | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 列：sheet1.Discount Amount | [Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q24](#t006-from6-sql24) |
| 列：sheet1.Profit | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29) |
| 列：sheet1.Sales Quantity | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q17](#t006-from6-sql17)、[Q20](#t006-from6-sql20)、[Q24](#t006-from6-sql24)、[Q26](#t006-from6-sql26) |
| 列：sheet1.Total Logistics Cost | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q20](#t006-from6-sql20)、[Q26](#t006-from6-sql26)、[Q29](#t006-from6-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q26](#t006-from6-sql26)、[Q29](#t006-from6-sql29) |
| 分组：sheet1.Date（按月） | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q24](#t006-from6-sql24)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q30](#t006-from6-sql30) |
| 聚合：SUM(sheet1.Discount Amount) | [Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q24](#t006-from6-sql24) |
| 聚合：SUM(sheet1.Profit) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q25](#t006-from6-sql25)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28) |
| 聚合：SUM(sheet1.Total Logistics Cost) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q19](#t006-from6-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q7](#t006-from6-sql7)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q26](#t006-from6-sql26)、[Q29](#t006-from6-sql29) |
| 列：sheet1.Date | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q24](#t006-from6-sql24)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 列：sheet1.Destination | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 列：sheet1.Profit | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q29](#t006-from6-sql29) |
| 列：sheet1.Sales Quantity | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q17](#t006-from6-sql17)、[Q20](#t006-from6-sql20)、[Q24](#t006-from6-sql24)、[Q26](#t006-from6-sql26) |
| 列：sheet1.Total Logistics Revenue | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q26](#t006-from6-sql26)、[Q29](#t006-from6-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q7](#t006-from6-sql7)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q21](#t006-from6-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q25](#t006-from6-sql25)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q17](#t006-from6-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q19](#t006-from6-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |

##### 后续SQL原文

<a id="t006-from6-sql7"></a>
<details><summary>Q7：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

<a id="t006-from6-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from6-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from6-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from6-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from6-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from6-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from6-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from6-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from6-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from6-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from6-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from6-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from6-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from6-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from6-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q7：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 "Consigned Product",
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 SUM("Total Logistics Revenue") AS rev,
 SUM("Total Logistics Cost") AS cost
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month,
 "Consigned Product"
ORDER BY month,
"Consigned Product"
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from7-sql13)、[Q15](#t006-from7-sql15)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q26](#t006-from7-sql26)、[Q29](#t006-from7-sql29) |
| 列：sheet1.Date | [Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q24](#t006-from7-sql24)、[Q27](#t006-from7-sql27)、[Q28](#t006-from7-sql28)、[Q29](#t006-from7-sql29)、[Q30](#t006-from7-sql30) |
| 列：sheet1.Destination | [Q8](#t006-from7-sql8)、[Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q23](#t006-from7-sql23)、[Q24](#t006-from7-sql24)、[Q25](#t006-from7-sql25)、[Q26](#t006-from7-sql26)、[Q27](#t006-from7-sql27)、[Q28](#t006-from7-sql28)、[Q29](#t006-from7-sql29)、[Q30](#t006-from7-sql30) |
| 列：sheet1.Profit | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q25](#t006-from7-sql25)、[Q26](#t006-from7-sql26)、[Q27](#t006-from7-sql27)、[Q28](#t006-from7-sql28)、[Q29](#t006-from7-sql29) |
| 列：sheet1.Sales Quantity | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q15](#t006-from7-sql15)、[Q17](#t006-from7-sql17)、[Q20](#t006-from7-sql20)、[Q24](#t006-from7-sql24)、[Q26](#t006-from7-sql26) |
| 列：sheet1.Total Logistics Cost | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q17](#t006-from7-sql17)、[Q20](#t006-from7-sql20)、[Q26](#t006-from7-sql26)、[Q29](#t006-from7-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q17](#t006-from7-sql17)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q26](#t006-from7-sql26)、[Q29](#t006-from7-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from7-sql13)、[Q15](#t006-from7-sql15)、[Q21](#t006-from7-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q25](#t006-from7-sql25)、[Q27](#t006-from7-sql27)、[Q28](#t006-from7-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q15](#t006-from7-sql15)、[Q17](#t006-from7-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q17](#t006-from7-sql17)、[Q19](#t006-from7-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q8](#t006-from7-sql8)、[Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q23](#t006-from7-sql23)、[Q24](#t006-from7-sql24)、[Q25](#t006-from7-sql25)、[Q26](#t006-from7-sql26)、[Q27](#t006-from7-sql27)、[Q29](#t006-from7-sql29)、[Q30](#t006-from7-sql30) |

##### 后续SQL原文

<a id="t006-from7-sql8"></a>
<details><summary>Q8：实际SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

<a id="t006-from7-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from7-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from7-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from7-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from7-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from7-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from7-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from7-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from7-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from7-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from7-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from7-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from7-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from7-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q8：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT Destination
FROM (
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%')
ORDER BY Destination
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q24](#t006-from8-sql24)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 列：sheet1.Destination | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 列：sheet1.Profit | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from8-sql14)、[Q22](#t006-from8-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from8-sql13)、[Q15](#t006-from8-sql15)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q26](#t006-from8-sql26)、[Q29](#t006-from8-sql29) |
| 列：sheet1.Date | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q24](#t006-from8-sql24)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 列：sheet1.Destination | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 列：sheet1.Profit | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from8-sql13)、[Q15](#t006-from8-sql15)、[Q21](#t006-from8-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |

##### 后续SQL原文

<a id="t006-from8-sql9"></a>
<details><summary>Q9：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from8-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from8-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from8-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from8-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from8-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from8-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from8-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from8-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from8-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from8-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from8-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from8-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from8-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q9：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 SUM("Total Logistics Revenue") AS revenue,
 SUM("List Price Revenue") AS list_price,
 SUM("Logistics Value-Added Service Revenue") AS vas_revenue,
 SUM("Discount Amount") AS discount,
 SUM("Total Logistics Cost") AS cost,
 SUM("Freight Cost") AS freight,
 SUM("Warehousing Cost") AS warehousing,
 SUM("Other Operating Costs") AS other_cost,
 SUM(Profit) AS profit,
 SUM("Sales Quantity") AS qty,
 COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q24](#t006-from9-sql24)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Discount Amount | [Q11](#t006-from9-sql11)、[Q24](#t006-from9-sql24) |
| 列：sheet1.Freight Cost | [Q30](#t006-from9-sql30) |
| 列：sheet1.List Price Revenue | [Q24](#t006-from9-sql24) |
| 列：sheet1.Logistics Value-Added Service Revenue | [Q11](#t006-from9-sql11)、[Q24](#t006-from9-sql24) |
| 列：sheet1.Other Operating Costs | [Q30](#t006-from9-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29) |
| 列：sheet1.Sales Quantity | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q17](#t006-from9-sql17)、[Q20](#t006-from9-sql20)、[Q24](#t006-from9-sql24)、[Q26](#t006-from9-sql26) |
| 列：sheet1.Total Logistics Cost | [Q12](#t006-from9-sql12)、[Q17](#t006-from9-sql17)、[Q20](#t006-from9-sql20)、[Q26](#t006-from9-sql26)、[Q29](#t006-from9-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q17](#t006-from9-sql17)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q26](#t006-from9-sql26)、[Q29](#t006-from9-sql29) |
| 列：sheet1.Warehousing Cost | [Q30](#t006-from9-sql30) |
| 分组：sheet1.Date（按月） | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q24](#t006-from9-sql24)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q30](#t006-from9-sql30) |
| 聚合：SUM(sheet1.Discount Amount) | [Q11](#t006-from9-sql11)、[Q24](#t006-from9-sql24) |
| 聚合：SUM(sheet1.Freight Cost) | [Q30](#t006-from9-sql30) |
| 聚合：SUM(sheet1.List Price Revenue) | [Q24](#t006-from9-sql24) |
| 聚合：SUM(sheet1.Logistics Value-Added Service Revenue) | [Q11](#t006-from9-sql11)、[Q24](#t006-from9-sql24) |
| 聚合：SUM(sheet1.Other Operating Costs) | [Q30](#t006-from9-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q17](#t006-from9-sql17) |
| 聚合：SUM(sheet1.Total Logistics Cost) | [Q12](#t006-from9-sql12)、[Q17](#t006-from9-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q17](#t006-from9-sql17)、[Q19](#t006-from9-sql19) |
| 聚合：SUM(sheet1.Warehousing Cost) | [Q30](#t006-from9-sql30) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q24](#t006-from9-sql24)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from9-sql14)、[Q22](#t006-from9-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q26](#t006-from9-sql26)、[Q29](#t006-from9-sql29) |
| 列：sheet1.Date | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q24](#t006-from9-sql24)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q21](#t006-from9-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |

##### 后续SQL原文

<a id="t006-from9-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from9-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from9-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from9-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from9-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from9-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from9-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from9-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from9-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from9-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from9-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from9-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from9-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from9-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q10：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(STDEV(profit), 0) AS std_profit,

  ROUND(STDEV(profit)/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(STDEV(revenue), 0) AS std_revenue,

  ROUND(STDEV(revenue)/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(STDEV(cost), 0) AS std_cost,

  ROUND(STDEV(cost)/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(STDEV(qty), 0) AS std_qty,

  ROUND(STDEV(qty)/AVG(qty)*100, 1) AS cv_qty_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q24](#t006-from10-sql24)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from10-sql14)、[Q22](#t006-from10-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from10-sql13)、[Q15](#t006-from10-sql15)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q26](#t006-from10-sql26)、[Q29](#t006-from10-sql29) |
| 列：sheet1.Date | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q24](#t006-from10-sql24)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from10-sql13)、[Q15](#t006-from10-sql15)、[Q21](#t006-from10-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q24](#t006-from10-sql24)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Destination | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29) |
| 列：sheet1.Profit Margin | [Q11](#t006-from10-sql11)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q29](#t006-from10-sql29) |
| 列：sheet1.Sales Quantity | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q15](#t006-from10-sql15)、[Q17](#t006-from10-sql17)、[Q20](#t006-from10-sql20)、[Q24](#t006-from10-sql24)、[Q26](#t006-from10-sql26) |
| 列：sheet1.Total Logistics Cost | [Q12](#t006-from10-sql12)、[Q17](#t006-from10-sql17)、[Q20](#t006-from10-sql20)、[Q26](#t006-from10-sql26)、[Q29](#t006-from10-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q17](#t006-from10-sql17)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q26](#t006-from10-sql26)、[Q29](#t006-from10-sql29) |
| 聚合：AVG(sheet1.Profit Margin) | [Q11](#t006-from10-sql11)、[Q19](#t006-from10-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |

##### 后续SQL原文

<a id="t006-from10-sql11"></a>
<details><summary>Q11：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from10-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from10-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from10-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from10-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from10-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from10-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from10-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from10-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from10-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from10-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from10-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from10-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from10-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q11：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct,
 SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q24](#t006-from11-sql24)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 列：sheet1.Destination | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from11-sql14)、[Q22](#t006-from11-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from11-sql13)、[Q15](#t006-from11-sql15)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q26](#t006-from11-sql26)、[Q29](#t006-from11-sql29) |
| 列：sheet1.Date | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q24](#t006-from11-sql24)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 列：sheet1.Destination | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 列：sheet1.Profit | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from11-sql13)、[Q15](#t006-from11-sql15)、[Q21](#t006-from11-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |

##### 后续SQL原文

<a id="t006-from11-sql12"></a>
<details><summary>Q12：实际SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

<a id="t006-from11-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from11-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from11-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from11-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from11-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from11-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from11-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from11-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from11-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from11-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from11-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from11-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from11-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q12：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 
  ROUND(AVG(profit), 0) AS avg_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit)), 0) AS std_profit,

  ROUND(SQRT(AVG(profit*profit) - AVG(profit)*AVG(profit))/AVG(profit)*100, 1) AS cv_profit_pct,

  ROUND(AVG(revenue), 0) AS avg_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue)), 0) AS std_revenue,

  ROUND(SQRT(AVG(revenue*revenue) - AVG(revenue)*AVG(revenue))/AVG(revenue)*100, 1) AS cv_revenue_pct,

  ROUND(AVG(cost), 0) AS avg_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost)), 0) AS std_cost,

  ROUND(SQRT(AVG(cost*cost) - AVG(cost)*AVG(cost))/AVG(cost)*100, 1) AS cv_cost_pct,

  ROUND(AVG(qty), 0) AS avg_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty)), 0) AS std_qty,

  ROUND(SQRT(AVG(qty*qty) - AVG(qty)*AVG(qty))/AVG(qty)*100, 1) AS cv_qty_pct,

  ROUND(AVG(orders), 0) AS avg_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders)), 0) AS std_orders,

  ROUND(SQRT(AVG(orders*orders) - AVG(orders)*AVG(orders))/AVG(orders)*100, 1) AS cv_orders_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, 
    SUM(Profit) AS profit, 
    SUM("Total Logistics Revenue") AS revenue, 
    SUM("Total Logistics Cost") AS cost,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
)
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q24](#t006-from12-sql24)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 列：sheet1.Destination | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 列：sheet1.Profit | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from12-sql14)、[Q22](#t006-from12-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q13](#t006-from12-sql13)、[Q15](#t006-from12-sql15)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q26](#t006-from12-sql26)、[Q29](#t006-from12-sql29) |
| 列：sheet1.Date | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q24](#t006-from12-sql24)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 列：sheet1.Destination | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 列：sheet1.Profit | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q13](#t006-from12-sql13)、[Q15](#t006-from12-sql15)、[Q21](#t006-from12-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |

##### 后续SQL原文

<a id="t006-from12-sql13"></a>
<details><summary>Q13：实际SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from12-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from12-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from12-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from12-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from12-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from12-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from12-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from12-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from12-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from12-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from12-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from12-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q13：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Consigned Product",
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,

  MIN(profit) AS min_m,
 MAX(profit) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,

  SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q15](#t006-from13-sql15)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q26](#t006-from13-sql26)、[Q29](#t006-from13-sql29) |
| 列：sheet1.Date | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q24](#t006-from13-sql24)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Destination | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Profit | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q15](#t006-from13-sql15)、[Q21](#t006-from13-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q24](#t006-from13-sql24)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Destination | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Profit | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q14](#t006-from13-sql14)、[Q22](#t006-from13-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q15](#t006-from13-sql15)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q26](#t006-from13-sql26)、[Q29](#t006-from13-sql29) |
| 列：sheet1.Date | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q24](#t006-from13-sql24)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Destination | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 列：sheet1.Profit | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29) |
| 列：sheet1.Sales Quantity | [Q15](#t006-from13-sql15)、[Q17](#t006-from13-sql17)、[Q20](#t006-from13-sql20)、[Q24](#t006-from13-sql24)、[Q26](#t006-from13-sql26) |
| 列：sheet1.Total Logistics Cost | [Q17](#t006-from13-sql17)、[Q20](#t006-from13-sql20)、[Q26](#t006-from13-sql26)、[Q29](#t006-from13-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t006-from13-sql17)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q26](#t006-from13-sql26)、[Q29](#t006-from13-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q15](#t006-from13-sql15)、[Q21](#t006-from13-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q15](#t006-from13-sql15)、[Q17](#t006-from13-sql17) |
| 聚合：SUM(sheet1.Total Logistics Cost) | [Q17](#t006-from13-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q17](#t006-from13-sql17)、[Q19](#t006-from13-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |

##### 后续SQL原文

<a id="t006-from13-sql14"></a>
<details><summary>Q14：实际SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

<a id="t006-from13-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from13-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from13-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from13-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from13-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from13-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from13-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from13-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from13-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from13-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from13-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q14：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT Destination,

  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, Destination
)
GROUP BY Destination
ORDER BY std_monthly_profit DESC
LIMIT 20
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q24](#t006-from14-sql24)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 列：sheet1.Destination | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 列：sheet1.Profit | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q22](#t006-from14-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q15](#t006-from14-sql15)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q26](#t006-from14-sql26)、[Q29](#t006-from14-sql29) |
| 列：sheet1.Date | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q24](#t006-from14-sql24)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 列：sheet1.Destination | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 列：sheet1.Profit | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q15](#t006-from14-sql15)、[Q21](#t006-from14-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |

##### 后续SQL原文

<a id="t006-from14-sql15"></a>
<details><summary>Q15：实际SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

<a id="t006-from14-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from14-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from14-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from14-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from14-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from14-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from14-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from14-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from14-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from14-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q15：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT product AS prod,
 
  ROUND(AVG(profit),0) AS avg_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,

  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,

  ROUND(MIN(profit),0) AS min_m,
 ROUND(MAX(profit),0) AS max_m,

  ROUND(MAX(profit)-MIN(profit),0) AS range_m,

  SUM(profit) AS total_profit,
 SUM(qty) AS total_qty
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, product
)
GROUP BY product
ORDER BY std_monthly_profit DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q26](#t006-from15-sql26)、[Q29](#t006-from15-sql29) |
| 列：sheet1.Date | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q24](#t006-from15-sql24)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 列：sheet1.Destination | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 列：sheet1.Profit | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28)、[Q29](#t006-from15-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q21](#t006-from15-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q25](#t006-from15-sql25)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q26](#t006-from15-sql26)、[Q29](#t006-from15-sql29) |
| 列：sheet1.Date | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q24](#t006-from15-sql24)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 列：sheet1.Destination | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 列：sheet1.Profit Margin | [Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q29](#t006-from15-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t006-from15-sql17)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q26](#t006-from15-sql26)、[Q29](#t006-from15-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q21](#t006-from15-sql21) |
| 聚合：AVG(sheet1.Profit Margin) | [Q19](#t006-from15-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |

##### 后续SQL原文

<a id="t006-from15-sql16"></a>
<details><summary>Q16：实际SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from15-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from15-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from15-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from15-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from15-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from15-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from15-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from15-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from15-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q16：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Destination | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Profit | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q22](#t006-from16-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q25](#t006-from16-sql25)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Destination | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Profit | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29) |
| 列：sheet1.Sales Quantity | [Q17](#t006-from16-sql17)、[Q20](#t006-from16-sql20)、[Q24](#t006-from16-sql24)、[Q26](#t006-from16-sql26) |
| 列：sheet1.Total Logistics Revenue | [Q17](#t006-from16-sql17)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q26](#t006-from16-sql26)、[Q29](#t006-from16-sql29) |
| 分组：sheet1.Date（按月） | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q30](#t006-from16-sql30) |
| 聚合：COUNT(*) | [Q17](#t006-from16-sql17)、[Q19](#t006-from16-sql19)、[Q25](#t006-from16-sql25)、[Q30](#t006-from16-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q25](#t006-from16-sql25)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | [Q17](#t006-from16-sql17) |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q17](#t006-from16-sql17)、[Q19](#t006-from16-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Destination | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 列：sheet1.Profit Margin | [Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q29](#t006-from16-sql29) |
| 分组：sheet1.Date（按月） | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q30](#t006-from16-sql30) |
| 聚合：AVG(sheet1.Profit Margin) | [Q19](#t006-from16-sql19) |
| 聚合：MAX(sheet1.Profit Margin) | [Q19](#t006-from16-sql19) |
| 聚合：MIN(sheet1.Profit Margin) | [Q19](#t006-from16-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |

##### 后续SQL原文

<a id="t006-from16-sql17"></a>
<details><summary>Q17：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from16-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from16-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from16-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from16-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from16-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from16-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from16-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from16-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q17：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order,
 ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order,
 ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit,
 ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit,
 ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 列：sheet1.Destination | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 列：sheet1.Profit | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q29](#t006-from17-sql29) |
| 列：sheet1.Sales Quantity | [Q20](#t006-from17-sql20)、[Q24](#t006-from17-sql24)、[Q26](#t006-from17-sql26) |
| 列：sheet1.Total Logistics Revenue | [Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q26](#t006-from17-sql26)、[Q29](#t006-from17-sql29) |
| 分组：sheet1.Date（按月） | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q30](#t006-from17-sql30) |
| 聚合：COUNT(*) | [Q19](#t006-from17-sql19)、[Q25](#t006-from17-sql25)、[Q30](#t006-from17-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q25](#t006-from17-sql25)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | 未找到 |
| 聚合：SUM(sheet1.Total Logistics Revenue) | [Q19](#t006-from17-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 列：sheet1.Destination | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 列：sheet1.Profit Margin | [Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q29](#t006-from17-sql29) |
| 分组：sheet1.Date（按月） | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q30](#t006-from17-sql30) |
| 聚合：AVG(sheet1.Profit Margin) | [Q19](#t006-from17-sql19) |
| 聚合：MAX(sheet1.Profit Margin) | [Q19](#t006-from17-sql19) |
| 聚合：MIN(sheet1.Profit Margin) | [Q19](#t006-from17-sql19) |
| 过滤：sheet1.Destination like "South China%" | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |

##### 后续SQL原文

<a id="t006-from17-sql18"></a>
<details><summary>Q18：实际SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

<a id="t006-from17-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from17-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from17-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from17-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from17-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from17-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from17-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from17-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from17-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from17-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from17-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from17-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q18：命中（3项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region,
 strftime('%Y-%m', Date) AS month,
 SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY region,
 month
ORDER BY region,
month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q24](#t006-from18-sql24)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Destination | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Profit | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q22](#t006-from18-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q19](#t006-from18-sql19)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q26](#t006-from18-sql26)、[Q29](#t006-from18-sql29) |
| 列：sheet1.Date | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q24](#t006-from18-sql24)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Destination | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Profit | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | [Q21](#t006-from18-sql21) |
| 聚合：SUM(sheet1.Profit) | [Q19](#t006-from18-sql19)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |

##### 候选3：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q24](#t006-from18-sql24)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Destination | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 列：sheet1.Profit | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29) |
| 列：sheet1.Profit Margin | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q29](#t006-from18-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q26](#t006-from18-sql26)、[Q29](#t006-from18-sql29) |
| 聚合：AVG(sheet1.Profit Margin) | [Q19](#t006-from18-sql19) |
| 聚合：COUNT(*) | [Q19](#t006-from18-sql19)、[Q25](#t006-from18-sql25)、[Q30](#t006-from18-sql30) |
| 聚合：MAX(sheet1.Profit Margin) | [Q19](#t006-from18-sql19) |
| 聚合：MIN(sheet1.Profit Margin) | [Q19](#t006-from18-sql19) |
| 过滤：sheet1.Date between ["2023-10-01", "2023-10-31"] | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |

##### 后续SQL原文

<a id="t006-from18-sql19"></a>
<details><summary>Q19：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from18-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from18-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from18-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from18-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from18-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from18-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from18-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from18-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from18-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from18-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from18-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q19：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 COUNT(*) AS n,
 ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct,
 ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct,
 ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct,
 ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q20](#t006-from19-sql20)、[Q21](#t006-from19-sql21)、[Q22](#t006-from19-sql22)、[Q24](#t006-from19-sql24)、[Q27](#t006-from19-sql27)、[Q28](#t006-from19-sql28)、[Q29](#t006-from19-sql29)、[Q30](#t006-from19-sql30) |
| 列：sheet1.Destination | [Q20](#t006-from19-sql20)、[Q21](#t006-from19-sql21)、[Q22](#t006-from19-sql22)、[Q23](#t006-from19-sql23)、[Q24](#t006-from19-sql24)、[Q25](#t006-from19-sql25)、[Q26](#t006-from19-sql26)、[Q27](#t006-from19-sql27)、[Q28](#t006-from19-sql28)、[Q29](#t006-from19-sql29)、[Q30](#t006-from19-sql30) |
| 列：sheet1.Profit | [Q20](#t006-from19-sql20)、[Q21](#t006-from19-sql21)、[Q22](#t006-from19-sql22)、[Q25](#t006-from19-sql25)、[Q26](#t006-from19-sql26)、[Q27](#t006-from19-sql27)、[Q28](#t006-from19-sql28)、[Q29](#t006-from19-sql29) |
| 列：sheet1.Profit Margin | [Q20](#t006-from19-sql20)、[Q29](#t006-from19-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q20](#t006-from19-sql20)、[Q26](#t006-from19-sql26)、[Q29](#t006-from19-sql29) |
| 聚合：AVG(sheet1.Profit Margin) | 未找到 |
| 聚合：COUNT(*) | [Q25](#t006-from19-sql25)、[Q30](#t006-from19-sql30) |
| 聚合：MAX(sheet1.Profit Margin) | 未找到 |
| 聚合：MIN(sheet1.Profit Margin) | 未找到 |
| 过滤：sheet1.Date between ["2023-10-01", "2023-10-31"] | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q20](#t006-from19-sql20)、[Q21](#t006-from19-sql21)、[Q22](#t006-from19-sql22)、[Q23](#t006-from19-sql23)、[Q24](#t006-from19-sql24)、[Q25](#t006-from19-sql25)、[Q26](#t006-from19-sql26)、[Q27](#t006-from19-sql27)、[Q29](#t006-from19-sql29)、[Q30](#t006-from19-sql30) |

##### 后续SQL原文

<a id="t006-from19-sql20"></a>
<details><summary>Q20：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

<a id="t006-from19-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from19-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from19-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from19-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from19-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from19-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from19-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from19-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from19-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from19-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q20：命中（1项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Sales Quantity",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10'
ORDER BY "Profit Margin" DESC
LIMIT 10
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q21](#t006-from20-sql21)、[Q26](#t006-from20-sql26)、[Q29](#t006-from20-sql29) |
| 列：sheet1.Date | [Q21](#t006-from20-sql21)、[Q22](#t006-from20-sql22)、[Q24](#t006-from20-sql24)、[Q27](#t006-from20-sql27)、[Q28](#t006-from20-sql28)、[Q29](#t006-from20-sql29)、[Q30](#t006-from20-sql30) |
| 列：sheet1.Destination | [Q21](#t006-from20-sql21)、[Q22](#t006-from20-sql22)、[Q23](#t006-from20-sql23)、[Q24](#t006-from20-sql24)、[Q25](#t006-from20-sql25)、[Q26](#t006-from20-sql26)、[Q27](#t006-from20-sql27)、[Q28](#t006-from20-sql28)、[Q29](#t006-from20-sql29)、[Q30](#t006-from20-sql30) |
| 列：sheet1.Profit | [Q21](#t006-from20-sql21)、[Q22](#t006-from20-sql22)、[Q25](#t006-from20-sql25)、[Q26](#t006-from20-sql26)、[Q27](#t006-from20-sql27)、[Q28](#t006-from20-sql28)、[Q29](#t006-from20-sql29) |
| 列：sheet1.Profit Margin | [Q29](#t006-from20-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q26](#t006-from20-sql26)、[Q29](#t006-from20-sql29) |
| 列：sheet1.Waybill Number | [Q29](#t006-from20-sql29) |
| 聚合：AVG(sheet1.Profit Margin) | 未找到 |
| 聚合：COUNT(*) | [Q25](#t006-from20-sql25)、[Q30](#t006-from20-sql30) |
| 聚合：MAX(sheet1.Profit Margin) | 未找到 |
| 聚合：MIN(sheet1.Profit Margin) | 未找到 |
| 过滤：sheet1.Date between ["2023-10-01", "2023-10-31"] | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q21](#t006-from20-sql21)、[Q22](#t006-from20-sql22)、[Q23](#t006-from20-sql23)、[Q24](#t006-from20-sql24)、[Q25](#t006-from20-sql25)、[Q26](#t006-from20-sql26)、[Q27](#t006-from20-sql27)、[Q29](#t006-from20-sql29)、[Q30](#t006-from20-sql30) |

##### 后续SQL原文

<a id="t006-from20-sql21"></a>
<details><summary>Q21：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from20-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from20-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from20-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from20-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from20-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from20-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from20-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from20-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from20-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q21：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN prod='Auto parts' THEN profit END) AS auto_parts,

  SUM(CASE WHEN prod='Bathroom supplies' THEN profit END) AS bathroom,

  SUM(CASE WHEN prod='Bedding set' THEN profit END) AS bedding,

  SUM(CASE WHEN prod='Bedroom Furniture' THEN profit END) AS bedroom,

  SUM(CASE WHEN prod='Computer hardware' THEN profit END) AS computer,

  SUM(CASE WHEN prod='Home decor items' THEN profit END) AS home_decor,

  SUM(CASE WHEN prod='Kitchen Appliances' THEN profit END) AS kitchen,

  SUM(CASE WHEN prod='Office furniture' THEN profit END) AS office
FROM (
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS prod, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, prod
)
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q26](#t006-from21-sql26)、[Q29](#t006-from21-sql29) |
| 列：sheet1.Date | [Q22](#t006-from21-sql22)、[Q24](#t006-from21-sql24)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 列：sheet1.Destination | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 列：sheet1.Profit | [Q22](#t006-from21-sql22)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29) |
| 列：sheet1.Profit Margin | [Q29](#t006-from21-sql29) |
| 列：sheet1.Sales Quantity | [Q24](#t006-from21-sql24)、[Q26](#t006-from21-sql26) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：AVG(sheet1.Profit Margin) | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q22](#t006-from21-sql22)、[Q25](#t006-from21-sql25)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q22](#t006-from21-sql22)、[Q24](#t006-from21-sql24)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 列：sheet1.Destination | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 列：sheet1.Profit | [Q22](#t006-from21-sql22)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | [Q22](#t006-from21-sql22) |
| 聚合：SUM(sheet1.Profit) | [Q22](#t006-from21-sql22)、[Q25](#t006-from21-sql25)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |

##### 后续SQL原文

<a id="t006-from21-sql22"></a>
<details><summary>Q22：实际SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from21-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from21-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from21-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from21-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from21-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from21-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from21-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from21-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q22：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT month,
 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,

  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,

  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,

  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,

  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month, dest
)
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q26](#t006-from22-sql26)、[Q29](#t006-from22-sql29) |
| 列：sheet1.Date | [Q24](#t006-from22-sql24)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 列：sheet1.Destination | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29) |
| 列：sheet1.Profit Margin | [Q29](#t006-from22-sql29) |
| 列：sheet1.Sales Quantity | [Q24](#t006-from22-sql24)、[Q26](#t006-from22-sql26) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：AVG(sheet1.Profit Margin) | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from22-sql25)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q24](#t006-from22-sql24)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 列：sheet1.Destination | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from22-sql25)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |

##### 后续SQL原文

<a id="t006-from22-sql23"></a>
<details><summary>Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from22-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from22-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from22-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from22-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from22-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from22-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from22-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q23：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q26](#t006-from23-sql26)、[Q29](#t006-from23-sql29) |
| 列：sheet1.Date | [Q24](#t006-from23-sql24)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 列：sheet1.Destination | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from23-sql25)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q24](#t006-from23-sql24)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 列：sheet1.Destination | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from23-sql25)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |

##### 后续SQL原文

<a id="t006-from23-sql24"></a>
<details><summary>Q24：实际SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from23-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from23-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from23-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from23-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from23-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from23-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q24：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT strftime('%Y-%m', Date) AS month,
 ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price,
 ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price,
 SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct,
 SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q26](#t006-from24-sql26)、[Q29](#t006-from24-sql29) |
| 列：sheet1.Date | [Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 列：sheet1.Destination | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from24-sql25)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 列：sheet1.Destination | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 列：sheet1.Profit | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q25](#t006-from24-sql25)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |

##### 后续SQL原文

<a id="t006-from24-sql25"></a>
<details><summary>Q25：实际SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

<a id="t006-from24-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from24-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from24-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from24-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from24-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q25：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
 COUNT(*) AS orders,
 ROUND(SUM(Profit),0) AS total_profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province
ORDER BY total_profit DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 列：sheet1.Destination | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 列：sheet1.Profit | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q26](#t006-from25-sql26)、[Q29](#t006-from25-sql29) |
| 列：sheet1.Date | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 列：sheet1.Destination | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 列：sheet1.Profit | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |

##### 后续SQL原文

<a id="t006-from25-sql26"></a>
<details><summary>Q26：实际SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

<a id="t006-from25-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from25-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from25-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from25-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q26：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Consigned Product",
 ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit,
 ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit,
 ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY "Consigned Product"
ORDER BY avg_profit_per_unit DESC
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q29](#t006-from26-sql29) |
| 列：sheet1.Date | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 列：sheet1.Destination | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 列：sheet1.Profit | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29) |
| 列：sheet1.Sales Quantity | 未找到 |
| 列：sheet1.Total Logistics Cost | [Q29](#t006-from26-sql29) |
| 列：sheet1.Total Logistics Revenue | [Q29](#t006-from26-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28) |
| 聚合：SUM(sheet1.Sales Quantity) | 未找到 |
| 聚合：SUM(sheet1.Total Logistics Cost) | 未找到 |
| 聚合：SUM(sheet1.Total Logistics Revenue) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q27](#t006-from26-sql27)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 列：sheet1.Destination | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 列：sheet1.Profit | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q29](#t006-from26-sql29) |
| 列：sheet1.Profit Margin | [Q29](#t006-from26-sql29) |
| 分组：sheet1.Date（按月） | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q30](#t006-from26-sql30) |
| 聚合：COUNT(*) | [Q30](#t006-from26-sql30) |
| 聚合：SUM(sheet1.Profit) | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q27](#t006-from26-sql27)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |

##### 后续SQL原文

<a id="t006-from26-sql27"></a>
<details><summary>Q27：实际SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

<a id="t006-from26-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from26-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from26-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q27：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT month,

  SUM(CASE WHEN province='Guangdong Province' THEN profit END) AS guangdong,

  SUM(CASE WHEN province='Guangxi' THEN profit END) AS guangxi,

  SUM(CASE WHEN province='Hainan Province' THEN profit END) AS hainan,

  SUM(CASE WHEN province='Henan Province' THEN profit END) AS henan,

  SUM(CASE WHEN province='Hubei Province' THEN profit END) AS hubei,

  SUM(CASE WHEN province='Hunan Province' THEN profit END) AS hunan
FROM (
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province,
    strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY province, month
)
GROUP BY month
ORDER BY month
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q29](#t006-from27-sql29) |
| 列：sheet1.Date | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 列：sheet1.Destination | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 列：sheet1.Profit | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q28](#t006-from27-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 列：sheet1.Destination | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 列：sheet1.Profit | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29) |
| 分组：sheet1.Destination ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | [Q28](#t006-from27-sql28) |
| 过滤：sheet1.Destination like "South China%" | [Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |

##### 后续SQL原文

<a id="t006-from27-sql28"></a>
<details><summary>Q28：实际SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

<a id="t006-from27-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from27-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q28：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 'Guangdong' AS prov,
 ROUND(AVG(profit),0) AS avg_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p,
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangdong%'
GROUP BY month)
UNION ALL
SELECT 'Guangxi',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Guangxi%'
GROUP BY month)
UNION ALL
SELECT 'Hainan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hainan%'
GROUP BY month)
UNION ALL
SELECT 'Henan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Henan%'
GROUP BY month)
UNION ALL
SELECT 'Hubei',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hubei%'
GROUP BY month)
UNION ALL
SELECT 'Hunan',
 ROUND(AVG(profit),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0),
 ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit
FROM sheet1
WHERE Destination LIKE 'South China-Hunan%'
GROUP BY month)
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 列：sheet1.Destination | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 列：sheet1.Profit | [Q29](#t006-from28-sql29) |
| 列：sheet1.Profit Margin | [Q29](#t006-from28-sql29) |
| 分组：sheet1.Date（按月） | [Q30](#t006-from28-sql30) |
| 聚合：COUNT(*) | [Q30](#t006-from28-sql30) |
| 聚合：SUM(sheet1.Profit) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Consigned Product | [Q29](#t006-from28-sql29) |
| 列：sheet1.Date | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 列：sheet1.Destination | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 列：sheet1.Profit | [Q29](#t006-from28-sql29) |
| 分组：sheet1.Consigned Product ＋ sheet1.Date（按月） | 未找到 |
| 聚合：SUM(sheet1.Profit) | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |

##### 后续SQL原文

<a id="t006-from28-sql29"></a>
<details><summary>Q29：实际SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

<a id="t006-from28-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q29：命中（2项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT "Waybill Number",
 Date,
 Destination,
 "Consigned Product",
 "Total Logistics Revenue",
 "Total Logistics Cost",
 Profit,
 "Profit Margin"
FROM sheet1
WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5
ORDER BY "Profit Margin"
LIMIT 5
```

</details>

##### 候选1：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q30](#t006-from29-sql30) |
| 列：sheet1.Destination | [Q30](#t006-from29-sql30) |
| 列：sheet1.Profit | 未找到 |
| 列：sheet1.Profit Margin | 未找到 |
| 列：sheet1.Total Logistics Revenue | 未找到 |
| 聚合：AVG(sheet1.Profit Margin) | 未找到 |
| 聚合：COUNT(*) | [Q30](#t006-from29-sql30) |
| 聚合：MAX(sheet1.Profit Margin) | 未找到 |
| 聚合：MIN(sheet1.Profit Margin) | 未找到 |
| 过滤：sheet1.Date between ["2023-08-01", "2023-08-31"] | 未找到 |
| 过滤：sheet1.Destination like "South China%" | [Q30](#t006-from29-sql30) |

##### 候选2：命中

| 预测的信息 | 后续实际使用它的query |
|---|---|
| 列：sheet1.Date | [Q30](#t006-from29-sql30) |
| 列：sheet1.Destination | [Q30](#t006-from29-sql30) |
| 列：sheet1.Freight Cost | [Q30](#t006-from29-sql30) |
| 列：sheet1.Other Operating Costs | [Q30](#t006-from29-sql30) |
| 列：sheet1.Total Logistics Cost | 未找到 |
| 列：sheet1.Warehousing Cost | [Q30](#t006-from29-sql30) |
| 分组：sheet1.Date（按月） | [Q30](#t006-from29-sql30) |
| 聚合：SUM(sheet1.Freight Cost) | [Q30](#t006-from29-sql30) |
| 聚合：SUM(sheet1.Other Operating Costs) | [Q30](#t006-from29-sql30) |
| 聚合：SUM(sheet1.Warehousing Cost) | [Q30](#t006-from29-sql30) |
| 过滤：sheet1.Destination like "South China%" | [Q30](#t006-from29-sql30) |

##### 后续SQL原文

<a id="t006-from29-sql30"></a>
<details><summary>Q30：实际SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

#### Q30：未提供预测（0项候选访问预测）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 'Freight' AS cost_type,
 ROUND(AVG(val),0) AS avg,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std,
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Warehousing',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Other Costs',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
UNION ALL
SELECT 'Orders',
 ROUND(AVG(val),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0),
 ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1)
FROM (
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val
FROM sheet1
WHERE Destination LIKE 'South China%'
GROUP BY month)
```

</details>

没有提供未来访问预测。之后没有再查询。

<!-- task-notes-start -->
### 具体操作的差异与遗漏

下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。

### 哪些预测没有发生，哪些只说对一部分

| 提出预测的轮次 | FAD说了什么 | 后面实际情况 | 判断 |
|---|---|---|---|
| Q18、Q19 | 筛选华南2023年10月，计算订单数与利润率MIN/MAX/AVG | Q20确实看华南10月，但取的是按利润率排序的订单明细，没有做这些聚合 | 时间和区域方向对应，访问方式没有对应。日期范围和月份字符串是两种写法，不应遮住这个部分对应关系 |
| Q23—Q25 | 继续预测月份＋产品、月份＋原始Destination分组，利润求和 | Q26改按产品计算单位价格/成本/利润；Q27、Q28按省份或省份子集看月度利润。Q22以后没有再出现原来两种完整分组 | 旧分组候选没有及时更新。利润、月份仍会用到，不代表原来那种联合分组还会发生 |
| Q29候选1 | 后续再看华南2023年8月，并计算利润率MIN/MAX/AVG等 | 当前Q29正在查8月异常订单；之后只剩Q30成本波动分析 | 这条未来预测没有发生，又出现了当前访问混入未来预测 |

### 实际做了，但FAD没有提前说清楚什么

| 实际SQL中的内容 | 之前FAD说到了什么 | 缺了什么 |
|---|---|---|
| Q16、Q18、Q27从Destination提取或映射省份后与月份联合分组 | 提前预测的是原始Destination＋月份 | 没表达目的地到省份的粒度变化；该提取表达式也超出当前简单分组Schema |
| Q20、Q29查异常订单明细，输出Waybill Number | 已说到日期、利润率等分析列 | Waybill Number从未在更早FAD中出现；异常订单排序、明细访问也未完整预测 |

CASE、窗口和复杂嵌套计算可能超出当前FAD表达能力；已有Schema能表达却未填写的操作，与这些表达能力限制分别看待。

### 本题高频列有没有提前说

每条成功SQL中同一列只数一次，排除第一条SQL。FAD里任何字段明确引用都算提到；这里问的是访问之前是否曾经说过，不要求紧邻上一轮。

| 列 | 后续多少条SQL访问了它 | 其中多少次已被更早FAD提到 |
|---|---|---|
| Destination | 27条 | 27次 |
| Date | 22条 | 22次 |
| Profit | 20条 | 20次 |
<!-- task-notes-end -->

原始数据：[events.jsonl](../runs/dacomp-006-02/events.jsonl)。本次逐项命中记录：[item-hit-rates.json](item-hit-rates.json)。
