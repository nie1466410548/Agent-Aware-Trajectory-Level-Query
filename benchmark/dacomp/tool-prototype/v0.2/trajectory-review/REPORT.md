# FAD与实际SQL轨迹分析

按任务分别整理。每个任务的结论、预测与实际查询对照、遗漏、统计及逐轮证据放在同一节，表格不混入其他任务。本文只分析迭代后本次运行的结果。

将FAD与后续实际SQL对照。分析模型明确写出的内容，不以接口是否接收判断预测对错；没有重跑模型或修改历史日志。

任务目录：

- [DAComp-003：水资源与经济指标](#task-003)
- [DAComp-004：产品销售与复购](#task-004)
- [DAComp-005：低利润率订单](#task-005)
- [DAComp-006：华南利润波动](#task-006)

<a id="task-003"></a>

## DAComp-003：水资源与经济指标

**本题结论：表列和部分连接、分组方向对了，完整操作及后续阶段预测不足。**

本节只分析该任务本次运行的FAD与实际SQL。Q1、Q2等编号表示该任务内的SQL执行顺序。
解开字符串、补齐唯一可确定的表名前缀，并计入FAD操作字段明确引用的列；不按接口是否接收筛选预测，不从列名推测未写出的分组或聚合。

<!-- task-rates-start -->
### 本题数量与预测成功比例

**计数单位：一轮SQL附带一份FAD，一份FAD可以包含多个候选。预测成功比例按候选算。**
这里“成功”采用统一的保守标准：候选明确写出的列、过滤条件、连接、分组和聚合，能在某条严格后续成功SQL中一起找到；如果同时写了分组和聚合，它们还需要出现在同一个查询层。只说对其中一部分，单独计为部分对应。没有候选的FAD不进入候选成功率分母。

| 统计内容 | 本题结果 |
|---|---|
| 共提交多少份FAD | 11份 |
| 其中有候选 / 没有候选 | 6份 / 5份 |
| 共提出多少个候选 | 10个 |
| **候选预测成功：已写信息全部对应** | **2个，2/10 = 20.0%** |
| 只对应一部分 | 8个，8/10 = 80.0% |
| 已写内容都没找到后续对应 | 0个，0/10 = 0.0% |
| 写了具体操作的候选，其已写信息全部对应 | 2/10 = 20.0% |
| 只列字段、没写具体操作的候选，其列清单全部对应 | 没有这种候选 |

**分开看各字段的预测比例：**

| 预测内容 | 写了多少个候选 | 其中多少个后来对应 | 比例 |
|---|---:|---:|---:|
| 列清单（包括操作里引用的列） | 10 | 4 | 4/10 = 40.0% |
| 已知过滤条件 | 2 | 2 | 2/2 = 100.0% |
| 连接 | 10 | 10 | 10/10 = 100.0% |
| 分组 | 9 | 5 | 5/9 = 55.6% |
| 聚合 | 7 | 3 | 3/7 = 42.9% |

分项比例只判断该字段；候选成功率要求这些信息在同一条后续SQL里共同出现，所以通常更低。只列字段的成功不表示预测了查询操作，已在上表单列。none/unknown不作为已写出的操作项计分；因此成功只表示已写信息对应，不表示完整预测了后续SQL全部内容。
同一候选在多轮重复提交会重复计数，多个候选也可能对应同一条后续SQL。复杂表达式与近似方向的人工解释保留在下文；自动过滤匹配仅检查已知条件单项，以上是统一规则下的对应比例，不是完整SQL语义等价率。
逐候选分类及对应SQL编号保存在[比例复核数据](task-rates.json)的003项。
<!-- task-rates-end -->

### 逐轮FAD与后续query核对

从Q1开始逐轮列出全部候选；不是选例子。每个候选列出所有完整对应的后续query，部分对应按字段单独列出。本轮涉及的后续SQL原文紧接在候选后面，同一条SQL在本轮内只展示一次。SQL可展开查看。

#### Q1：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Year。
- 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) )。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q2](#t003-from1-sql2) | economic_indicator_data.Region Name, economic_indicator_data.Year |
| [Q3](#t003-from1-sql3) | sheet1.Region Name |
| [Q4](#t003-from1-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from1-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from1-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from1-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from1-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from1-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from1-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from1-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Region Name。
- 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³))。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from1-sql4)、[Q5](#t003-from1-sql5)、[Q6](#t003-from1-sql6)、[Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10)、[Q11](#t003-from1-sql11) |
| 分组 | [Q7](#t003-from1-sql7)、[Q8](#t003-from1-sql8)、[Q9](#t003-from1-sql9)、[Q10](#t003-from1-sql10) |
| 聚合 | [Q7](#t003-from1-sql7) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q2](#t003-from1-sql2) | economic_indicator_data.Region Name, economic_indicator_data.Year |
| [Q3](#t003-from1-sql3) | sheet1.Region Name |
| [Q4](#t003-from1-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from1-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from1-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from1-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from1-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from1-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from1-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from1-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from1-sql2"></a>
<details><summary>后续Q2：实际SQL</summary>

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
<details><summary>后续Q3：实际SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

<a id="t003-from1-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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

#### Q2：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Year。
- 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) )。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q3](#t003-from2-sql3) | sheet1.Region Name |
| [Q4](#t003-from2-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from2-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from2-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from2-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from2-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from2-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from2-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from2-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Region Name。
- 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³))。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from2-sql4)、[Q5](#t003-from2-sql5)、[Q6](#t003-from2-sql6)、[Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10)、[Q11](#t003-from2-sql11) |
| 分组 | [Q7](#t003-from2-sql7)、[Q8](#t003-from2-sql8)、[Q9](#t003-from2-sql9)、[Q10](#t003-from2-sql10) |
| 聚合 | [Q7](#t003-from2-sql7) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q3](#t003-from2-sql3) | sheet1.Region Name |
| [Q4](#t003-from2-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from2-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from2-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from2-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from2-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from2-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from2-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from2-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from2-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

<a id="t003-from2-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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

#### Q3：本轮FAD（2个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT "Region Name"
FROM sheet1
ORDER BY "Region Name"
```

</details>

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Year。
- 聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) )。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q4](#t003-from3-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from3-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from3-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from3-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from3-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from3-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from3-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from3-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Region Name。
- 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³))。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q4](#t003-from3-sql4)、[Q5](#t003-from3-sql5)、[Q6](#t003-from3-sql6)、[Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10)、[Q11](#t003-from3-sql11) |
| 分组 | [Q7](#t003-from3-sql7)、[Q8](#t003-from3-sql8)、[Q9](#t003-from3-sql9)、[Q10](#t003-from3-sql10) |
| 聚合 | [Q7](#t003-from3-sql7) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q4](#t003-from3-sql4) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q5](#t003-from3-sql5) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q6](#t003-from3-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from3-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from3-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from3-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from3-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from3-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from3-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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

#### Q4：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：sheet1.Region Name ne "China"。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Year ＋ sheet1.Region Name。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q8、Q9、Q10、Q11。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 过滤 | [Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 连接 | [Q5](#t003-from4-sql5)、[Q6](#t003-from4-sql6)、[Q7](#t003-from4-sql7)、[Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 分组 | [Q8](#t003-from4-sql8)、[Q9](#t003-from4-sql9)、[Q10](#t003-from4-sql10)、[Q11](#t003-from4-sql11) |
| 聚合 | 未提供具体项，不算预测成功 |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from4-sql5"></a>
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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

#### Q5：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：sheet1.Region Name ne "China"。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Region Name。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q7、Q8、Q9、Q10。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 过滤 | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 连接 | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 分组 | [Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10) |
| 聚合 | 未提供具体项，不算预测成功 |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：sheet1.Year。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q6](#t003-from5-sql6)、[Q7](#t003-from5-sql7)、[Q8](#t003-from5-sql8)、[Q9](#t003-from5-sql9)、[Q10](#t003-from5-sql10)、[Q11](#t003-from5-sql11) |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q6](#t003-from5-sql6) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q7](#t003-from5-sql7) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q8](#t003-from5-sql8) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q9](#t003-from5-sql9) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q10](#t003-from5-sql10) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |
| [Q11](#t003-from5-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from5-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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

#### Q6：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：没有提供后续访问候选，但之后仍执行了Q7、Q8、Q9、Q10、Q11。**

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from6-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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

<a id="t003-from6-sql8"></a>
<details><summary>后续Q8：实际SQL</summary>

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

<a id="t003-from6-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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

<a id="t003-from6-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t003-from6-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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

#### Q7：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：没有提供后续访问候选，但之后仍执行了Q8、Q9、Q10、Q11。**

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from7-sql8"></a>
<details><summary>后续Q8：实际SQL</summary>

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

<a id="t003-from7-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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

<a id="t003-from7-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t003-from7-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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

#### Q8：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：没有提供后续访问候选，但之后仍执行了Q9、Q10、Q11。**

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from8-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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

<a id="t003-from8-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t003-from8-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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

#### Q9：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：没有提供后续访问候选，但之后仍执行了Q10、Q11。**

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from9-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t003-from9-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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

#### Q10：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1, economic_indicator_data。
- 列：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) 。
- 过滤：未声明此操作。
- 连接：inner：sheet1.Region Code = economic_indicator_data.Region Code（部分信息）。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Industrial Water Consumption (100 million m³))、AVG(sheet1.Total Water Consumption (100 million m³) )。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q11](#t003-from10-sql11) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | [Q11](#t003-from10-sql11) |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q11](#t003-from10-sql11) | economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³)  |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t003-from10-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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

#### Q11：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：之后没有再执行SQL，与结束判断一致。**

<!-- task-notes-start -->
### 哪些预测没有发生，哪些只说对一部分

| 提出预测的轮次 | FAD说了什么 | 后面实际情况 | 判断 |
|---|---|---|---|
| Q1—Q3各自的候选1 | 按Year分组，SUM(工业用水量)、SUM(总用水量) | Q4、Q5直接读取China各年记录并算占比；之后主要按地区计算均值和相关性，没有执行所预测的按年份求和 | 这条访问预测没有发生。Year被用到，不等于GROUP BY Year被预测正确 |
| Q6—Q9 | no_further_access，即没有后续访问 | Q7—Q11仍在执行均值、相关性、首末年、峰值等查询 | 明确的后续访问判断错误，不能只看早期预测对过哪些列 |
| Q10 | 预计再计算两项用水均值 | 剩下的Q11比较2003与2018的记录，没有再次求这两项均值 | 预测没有发生 |

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

### 本题分组和聚合的数量

- 分组：9个候选写了具体分组，其中5个后来出现相同分组。
- 聚合：7个候选写了具体聚合，其中3个后来在同一条SQL里出现全部所述聚合。

每个候选计一次；同一预测在不同轮次重复提交会重复计数，不是独立样本。分组与聚合分别比较，不能将分别出现在不同SQL的操作说成整个候选在同一SQL中发生。没有填写的操作不进入上述数量。
known联合分组比较完整维度，partial允许增加维度；partial连接允许增加条件。过滤自动核对的是已知条件单项；相近但不相同的日期写法、粒度变化及复杂表达式，按上面的具体例子解释。

<!-- task-notes-end -->

原始记录：[events.jsonl](../runs/dacomp-003-02/events.jsonl)；本题复核数据：[JSON](dacomp-003-02.json)。

<a id="task-004"></a>

## DAComp-004：产品销售与复购

**本题结论：四题中主要分析步骤对应最清楚，但仍有细节遗漏。**

本节只分析该任务本次运行的FAD与实际SQL。Q1、Q2等编号表示该任务内的SQL执行顺序。
解开字符串、补齐唯一可确定的表名前缀，并计入FAD操作字段明确引用的列；不按接口是否接收筛选预测，不从列名推测未写出的分组或聚合。

<!-- task-rates-start -->
### 本题数量与预测成功比例

**计数单位：一轮SQL附带一份FAD，一份FAD可以包含多个候选。预测成功比例按候选算。**
这里“成功”采用统一的保守标准：候选明确写出的列、过滤条件、连接、分组和聚合，能在某条严格后续成功SQL中一起找到；如果同时写了分组和聚合，它们还需要出现在同一个查询层。只说对其中一部分，单独计为部分对应。没有候选的FAD不进入候选成功率分母。

| 统计内容 | 本题结果 |
|---|---|
| 共提交多少份FAD | 10份 |
| 其中有候选 / 没有候选 | 9份 / 1份 |
| 共提出多少个候选 | 9个 |
| **候选预测成功：已写信息全部对应** | **8个，8/9 = 88.9%** |
| 只对应一部分 | 1个，1/9 = 11.1% |
| 已写内容都没找到后续对应 | 0个，0/9 = 0.0% |
| 写了具体操作的候选，其已写信息全部对应 | 8/8 = 100.0% |
| 只列字段、没写具体操作的候选，其列清单全部对应 | 0/1 = 0.0% |

**分开看各字段的预测比例：**

| 预测内容 | 写了多少个候选 | 其中多少个后来对应 | 比例 |
|---|---:|---:|---:|
| 列清单（包括操作里引用的列） | 9 | 8 | 8/9 = 88.9% |
| 已知过滤条件 | 5 | 5 | 5/5 = 100.0% |
| 连接 | 0 | 0 | 没有这种候选 |
| 分组 | 5 | 5 | 5/5 = 100.0% |
| 聚合 | 6 | 6 | 6/6 = 100.0% |

分项比例只判断该字段；候选成功率要求这些信息在同一条后续SQL里共同出现，所以通常更低。只列字段的成功不表示预测了查询操作，已在上表单列。none/unknown不作为已写出的操作项计分；因此成功只表示已写信息对应，不表示完整预测了后续SQL全部内容。
同一候选在多轮重复提交会重复计数，多个候选也可能对应同一条后续SQL。复杂表达式与近似方向的人工解释保留在下文；自动过滤匹配仅检查已知条件单项，以上是统一规则下的对应比例，不是完整SQL语义等价率。
逐候选分类及对应SQL编号保存在[比例复核数据](task-rates.json)的004项。
<!-- task-rates-end -->

### 逐轮FAD与后续query核对

从Q1开始逐轮列出全部候选；不是选例子。每个候选列出所有完整对应的后续query，部分对应按字段单独列出。本轮涉及的后续SQL原文紧接在候选后面，同一条SQL在本轮内只展示一次。SQL可展开查看。

#### Q1：本轮FAD（1个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM sheet1
LIMIT 20
```

</details>

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Sales Month ＋ sheet1.Product Code。
- 聚合：SUM(sheet1.Sales Amount)。

**整个候选对应的后续query：** Q3、Q4、Q5、Q9。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9) |
| 聚合 | [Q3](#t004-from1-sql3)、[Q4](#t004-from1-sql4)、[Q5](#t004-from1-sql5)、[Q9](#t004-from1-sql9)、[Q10](#t004-from1-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from1-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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

<a id="t004-from1-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q2：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Sales Month ＋ sheet1.Product Code。
- 聚合：SUM(sheet1.Sales Amount)。

**整个候选对应的后续query：** Q3、Q4、Q5、Q9。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9) |
| 聚合 | [Q3](#t004-from2-sql3)、[Q4](#t004-from2-sql4)、[Q5](#t004-from2-sql5)、[Q9](#t004-from2-sql9)、[Q10](#t004-from2-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from2-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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

<a id="t004-from2-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q3：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Sales Month ＋ sheet1.Product Code。
- 聚合：SUM(sheet1.Sales Amount)。

**整个候选对应的后续query：** Q4、Q5、Q9。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9) |
| 聚合 | [Q4](#t004-from3-sql4)、[Q5](#t004-from3-sql5)、[Q9](#t004-from3-sql9)、[Q10](#t004-from3-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from3-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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

<a id="t004-from3-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q4：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Customer ID, sheet1.Is Promotional, sheet1.Major Category Name, sheet1.Middle Category Name, sheet1.Minor Category Name, sheet1.Product Code, sheet1.Product Type, sheet1.Sales Amount, sheet1.Sales Month, sheet1.Specification/Model。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q5](#t004-from4-sql5) | sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month |
| [Q6](#t004-from4-sql6) | sheet1.Major Category Name, sheet1.Middle Category Name, sheet1.Minor Category Name, sheet1.Product Code, sheet1.Product Type, sheet1.Specification/Model |
| [Q7](#t004-from4-sql7) | sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month |
| [Q8](#t004-from4-sql8) | sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month |
| [Q9](#t004-from4-sql9) | sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month |
| [Q10](#t004-from4-sql10) | sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Amount, sheet1.Sales Month |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from4-sql5"></a>
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q5：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month。
- 过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]。
- 连接：未声明此操作。
- 分组：sheet1.Customer ID ＋ sheet1.Product Code。
- 聚合：COUNT_DISTINCT(sheet1.Sales Month)。

**整个候选对应的后续query：** Q7。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q10](#t004-from5-sql10) |
| 过滤 | [Q6](#t004-from5-sql6)、[Q7](#t004-from5-sql7)、[Q8](#t004-from5-sql8)、[Q9](#t004-from5-sql9)、[Q10](#t004-from5-sql10) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q7](#t004-from5-sql7) |
| 聚合 | [Q7](#t004-from5-sql7)、[Q10](#t004-from5-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from5-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q6：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month。
- 过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]。
- 连接：未声明此操作。
- 分组：sheet1.Customer ID ＋ sheet1.Product Code。
- 聚合：COUNT_DISTINCT(sheet1.Sales Month)。

**整个候选对应的后续query：** Q7。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q10](#t004-from6-sql10) |
| 过滤 | [Q7](#t004-from6-sql7)、[Q8](#t004-from6-sql8)、[Q9](#t004-from6-sql9)、[Q10](#t004-from6-sql10) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q7](#t004-from6-sql7) |
| 聚合 | [Q7](#t004-from6-sql7)、[Q10](#t004-from6-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from6-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q7：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month。
- 过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q8、Q10。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q8](#t004-from7-sql8)、[Q10](#t004-from7-sql10) |
| 过滤 | [Q8](#t004-from7-sql8)、[Q9](#t004-from7-sql9)、[Q10](#t004-from7-sql10) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from7-sql8"></a>
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q8：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Customer ID, sheet1.Product Code, sheet1.Sales Month。
- 过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q10。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q10](#t004-from8-sql10) |
| 过滤 | [Q9](#t004-from8-sql9)、[Q10](#t004-from8-sql10) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from8-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

#### Q9：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Product Code, sheet1.Sales Amount。
- 过滤：sheet1.Product Code in ["DW-1001040125", "DW-2316020016", "DW-1203130446", "DW-1518040045"]。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：SUM(sheet1.Sales Amount)。

**整个候选对应的后续query：** Q10。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q10](#t004-from9-sql10) |
| 过滤 | [Q10](#t004-from9-sql10) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q10](#t004-from9-sql10) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t004-from9-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

#### Q10：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：之后没有再执行SQL，与结束判断一致。**

<!-- task-notes-start -->
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

### 本题分组和聚合的数量

- 分组：5个候选写了具体分组，5个后来都出现。
- 聚合：6个候选写了具体聚合，6个后来都出现。

每个候选计一次；同一预测在不同轮次重复提交会重复计数，不是独立样本。分组与聚合分别比较，不能将分别出现在不同SQL的操作说成整个候选在同一SQL中发生。没有填写的操作不进入上述数量。
known联合分组比较完整维度，partial允许增加维度；partial连接允许增加条件。过滤自动核对的是已知条件单项；相近但不相同的日期写法、粒度变化及复杂表达式，按上面的具体例子解释。

<!-- task-notes-end -->

原始记录：[events.jsonl](../runs/dacomp-004-02/events.jsonl)；本题复核数据：[JSON](dacomp-004-02.json)。

<a id="task-005"></a>

## DAComp-005：低利润率订单

**本题结论：能预见会看哪些数据，较少说清楚具体怎样查。**

本节只分析该任务本次运行的FAD与实际SQL。Q1、Q2等编号表示该任务内的SQL执行顺序。
解开字符串、补齐唯一可确定的表名前缀，并计入FAD操作字段明确引用的列；不按接口是否接收筛选预测，不从列名推测未写出的分组或聚合。

<!-- task-rates-start -->
### 本题数量与预测成功比例

**计数单位：一轮SQL附带一份FAD，一份FAD可以包含多个候选。预测成功比例按候选算。**
这里“成功”采用统一的保守标准：候选明确写出的列、过滤条件、连接、分组和聚合，能在某条严格后续成功SQL中一起找到；如果同时写了分组和聚合，它们还需要出现在同一个查询层。只说对其中一部分，单独计为部分对应。没有候选的FAD不进入候选成功率分母。

| 统计内容 | 本题结果 |
|---|---|
| 共提交多少份FAD | 21份 |
| 其中有候选 / 没有候选 | 20份 / 1份 |
| 共提出多少个候选 | 28个 |
| **候选预测成功：已写信息全部对应** | **7个，7/28 = 25.0%** |
| 只对应一部分 | 20个，20/28 = 71.4% |
| 已写内容都没找到后续对应 | 1个，1/28 = 3.6% |
| 写了具体操作的候选，其已写信息全部对应 | 3/9 = 33.3% |
| 只列字段、没写具体操作的候选，其列清单全部对应 | 4/19 = 21.1% |

**分开看各字段的预测比例：**

| 预测内容 | 写了多少个候选 | 其中多少个后来对应 | 比例 |
|---|---:|---:|---:|
| 列清单（包括操作里引用的列） | 28 | 10 | 10/28 = 35.7% |
| 已知过滤条件 | 2 | 1 | 1/2 = 50.0% |
| 连接 | 0 | 0 | 没有这种候选 |
| 分组 | 1 | 0 | 0/1 = 0.0% |
| 聚合 | 7 | 4 | 4/7 = 57.1% |

分项比例只判断该字段；候选成功率要求这些信息在同一条后续SQL里共同出现，所以通常更低。只列字段的成功不表示预测了查询操作，已在上表单列。none/unknown不作为已写出的操作项计分；因此成功只表示已写信息对应，不表示完整预测了后续SQL全部内容。
同一候选在多轮重复提交会重复计数，多个候选也可能对应同一条后续SQL。复杂表达式与近似方向的人工解释保留在下文；自动过滤匹配仅检查已知条件单项，以上是统一规则下的对应比例，不是完整SQL语义等价率。
逐候选分类及对应SQL编号保存在[比例复核数据](task-rates.json)的005项。
<!-- task-rates-end -->

### 逐轮FAD与后续query核对

从Q1开始逐轮列出全部候选；不是选例子。每个候选列出所有完整对应的后续query，部分对应按字段单独列出。本轮涉及的后续SQL原文紧接在候选后面，同一条SQL在本轮内只展示一次。SQL可展开查看。

#### Q1：本轮FAD（2个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT *
FROM sheet1
LIMIT 5
```

</details>

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Profit Margin。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** Q2、Q3、Q4、Q5、Q6、Q7、Q9、Q10、Q12、Q14、Q16、Q19。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q8](#t005-from1-sql8)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q14](#t005-from1-sql14)、[Q16](#t005-from1-sql16)、[Q19](#t005-from1-sql19) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Profit Margin。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：COUNT(*)。

**整个候选对应的后续query：** Q2、Q3、Q4、Q5、Q6、Q7、Q9、Q10、Q12、Q13、Q14、Q15、Q16、Q18、Q19。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q8](#t005-from1-sql8)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q2](#t005-from1-sql2)、[Q3](#t005-from1-sql3)、[Q4](#t005-from1-sql4)、[Q5](#t005-from1-sql5)、[Q6](#t005-from1-sql6)、[Q7](#t005-from1-sql7)、[Q9](#t005-from1-sql9)、[Q10](#t005-from1-sql10)、[Q11](#t005-from1-sql11)、[Q12](#t005-from1-sql12)、[Q13](#t005-from1-sql13)、[Q14](#t005-from1-sql14)、[Q15](#t005-from1-sql15)、[Q16](#t005-from1-sql16)、[Q18](#t005-from1-sql18)、[Q19](#t005-from1-sql19) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from1-sql2"></a>
<details><summary>后续Q2：实际SQL</summary>

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
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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

#### Q2：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Profit Margin)、COUNT(*)。

**整个候选对应的后续query：** Q3、Q10、Q12。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t005-from2-sql3)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q18](#t005-from2-sql18) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q14](#t005-from2-sql14)、[Q16](#t005-from2-sql16)、[Q19](#t005-from2-sql19) |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Profit Margin。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t005-from2-sql3)、[Q4](#t005-from2-sql4)、[Q5](#t005-from2-sql5)、[Q6](#t005-from2-sql6)、[Q7](#t005-from2-sql7)、[Q8](#t005-from2-sql8)、[Q9](#t005-from2-sql9)、[Q10](#t005-from2-sql10)、[Q12](#t005-from2-sql12)、[Q13](#t005-from2-sql13)、[Q14](#t005-from2-sql14)、[Q15](#t005-from2-sql15)、[Q16](#t005-from2-sql16)、[Q18](#t005-from2-sql18)、[Q19](#t005-from2-sql19) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q3](#t005-from2-sql3) | sheet1.Profit Margin |
| [Q4](#t005-from2-sql4) | sheet1.Profit Margin |
| [Q5](#t005-from2-sql5) | sheet1.Profit Margin |
| [Q6](#t005-from2-sql6) | sheet1.Profit Margin |
| [Q7](#t005-from2-sql7) | sheet1.Profit Margin |
| [Q8](#t005-from2-sql8) | sheet1.Profit Margin |
| [Q9](#t005-from2-sql9) | sheet1.Profit Margin |
| [Q10](#t005-from2-sql10) | sheet1.Profit Margin |
| [Q12](#t005-from2-sql12) | sheet1.Profit Margin |
| [Q13](#t005-from2-sql13) | sheet1.Profit Margin |
| [Q14](#t005-from2-sql14) | sheet1.Profit Margin |
| [Q15](#t005-from2-sql15) | sheet1.Profit Margin |
| [Q16](#t005-from2-sql16) | sheet1.Profit Margin |
| [Q18](#t005-from2-sql18) | sheet1.Profit Margin |
| [Q19](#t005-from2-sql19) | sheet1.Profit Margin |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from2-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t005-from2-sql12"></a>
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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

<a id="t005-from2-sql18"></a>
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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

#### Q3：本轮FAD（3个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Profit Margin)、AVG(sheet1.Profit)、AVG(sheet1.Total Logistics Revenue)、AVG(sheet1.Total Logistics Cost)、AVG(sheet1.Freight Cost)、AVG(sheet1.Warehousing Cost)、AVG(sheet1.Other Operating Costs)、AVG(sheet1.Sales Quantity)、AVG(sheet1.Discount Amount)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q4](#t005-from3-sql4) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q5](#t005-from3-sql5) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q6](#t005-from3-sql6) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q7](#t005-from3-sql7) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q8](#t005-from3-sql8) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q9](#t005-from3-sql9) | sheet1.Profit Margin |
| [Q10](#t005-from3-sql10) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t005-from3-sql11) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q12](#t005-from3-sql12) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from3-sql13) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from3-sql14) | sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from3-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from3-sql16) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from3-sql17) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q18](#t005-from3-sql18) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q19](#t005-from3-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from3-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Destination。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Destination。
- 聚合：COUNT(*)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q4](#t005-from3-sql4)、[Q13](#t005-from3-sql13)、[Q15](#t005-from3-sql15) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q4](#t005-from3-sql4)、[Q5](#t005-from3-sql5)、[Q6](#t005-from3-sql6)、[Q7](#t005-from3-sql7)、[Q9](#t005-from3-sql9)、[Q10](#t005-from3-sql10)、[Q11](#t005-from3-sql11)、[Q12](#t005-from3-sql12)、[Q13](#t005-from3-sql13)、[Q14](#t005-from3-sql14)、[Q15](#t005-from3-sql15)、[Q16](#t005-from3-sql16)、[Q18](#t005-from3-sql18)、[Q19](#t005-from3-sql19) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q4](#t005-from3-sql4) | sheet1.Destination |
| [Q13](#t005-from3-sql13) | sheet1.Destination |
| [Q15](#t005-from3-sql15) | sheet1.Destination |

##### 候选3：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q5](#t005-from3-sql5) | sheet1.Age Range |
| [Q6](#t005-from3-sql6) | sheet1.Customer Gender |
| [Q7](#t005-from3-sql7) | sheet1.Consigned Product |
| [Q14](#t005-from3-sql14) | sheet1.Consigned Product |
| [Q16](#t005-from3-sql16) | sheet1.Age Range |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from3-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q4：本轮FAD（4个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q9。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q9](#t005-from4-sql9) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q5](#t005-from4-sql5) | sheet1.Age Range |
| [Q6](#t005-from4-sql6) | sheet1.Customer Gender |
| [Q16](#t005-from4-sql16) | sheet1.Age Range |

##### 候选3：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q7、Q14。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t005-from4-sql7)、[Q14](#t005-from4-sql14) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 候选4：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Sales Quantity)、AVG(sheet1.Discount Amount)、AVG(sheet1.List Price Revenue)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q8](#t005-from4-sql8) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q5](#t005-from4-sql5) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q6](#t005-from4-sql6) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q7](#t005-from4-sql7) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q8](#t005-from4-sql8) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q9](#t005-from4-sql9) | sheet1.Profit Margin |
| [Q10](#t005-from4-sql10) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t005-from4-sql11) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q12](#t005-from4-sql12) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from4-sql13) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from4-sql14) | sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from4-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from4-sql16) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from4-sql17) | sheet1.Discount Amount, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from4-sql18) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from4-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from4-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from4-sql5"></a>
<details><summary>后续Q5：实际SQL</summary>

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
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q5：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q6](#t005-from5-sql6) | sheet1.Customer Gender, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q7](#t005-from5-sql7) | sheet1.Consigned Product, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q8](#t005-from5-sql8) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q9](#t005-from5-sql9) | sheet1.Profit Margin |
| [Q10](#t005-from5-sql10) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q11](#t005-from5-sql11) | sheet1.Sales Quantity |
| [Q12](#t005-from5-sql12) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q13](#t005-from5-sql13) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from5-sql14) | sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from5-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from5-sql16) | sheet1.Age Range, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from5-sql17) | sheet1.Profit, sheet1.Sales Quantity |
| [Q18](#t005-from5-sql18) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q19](#t005-from5-sql19) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from5-sql20) | sheet1.Sales Quantity |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from5-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

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
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q6：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q7](#t005-from6-sql7) | sheet1.Consigned Product, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q8](#t005-from6-sql8) | sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q9](#t005-from6-sql9) | sheet1.Profit Margin |
| [Q10](#t005-from6-sql10) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t005-from6-sql11) | sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q12](#t005-from6-sql12) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from6-sql13) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from6-sql14) | sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from6-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from6-sql16) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from6-sql17) | sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from6-sql18) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from6-sql19) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from6-sql20) | sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from6-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q7：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q8](#t005-from7-sql8) | sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q9](#t005-from7-sql9) | sheet1.Date, sheet1.Profit Margin |
| [Q10](#t005-from7-sql10) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t005-from7-sql11) | sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q12](#t005-from7-sql12) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from7-sql13) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from7-sql14) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from7-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from7-sql16) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from7-sql17) | sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from7-sql18) | sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from7-sql19) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from7-sql20) | sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from7-sql8"></a>
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q8：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q9](#t005-from8-sql9) | sheet1.Date, sheet1.Profit Margin |
| [Q10](#t005-from8-sql10) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t005-from8-sql11) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q12](#t005-from8-sql12) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from8-sql13) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from8-sql14) | sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from8-sql15) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from8-sql16) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from8-sql17) | sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from8-sql18) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from8-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from8-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from8-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q10：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q9：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q10、Q12、Q18。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q10](#t005-from9-sql10)、[Q12](#t005-from9-sql12)、[Q18](#t005-from9-sql18) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Profit Margin。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q10](#t005-from9-sql10) | sheet1.Profit Margin |
| [Q12](#t005-from9-sql12) | sheet1.Profit Margin |
| [Q13](#t005-from9-sql13) | sheet1.Profit Margin |
| [Q14](#t005-from9-sql14) | sheet1.Profit Margin |
| [Q15](#t005-from9-sql15) | sheet1.Profit Margin |
| [Q16](#t005-from9-sql16) | sheet1.Profit Margin |
| [Q18](#t005-from9-sql18) | sheet1.Profit Margin |
| [Q19](#t005-from9-sql19) | sheet1.Profit Margin |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from9-sql10"></a>
<details><summary>后续Q10：实际SQL</summary>

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

<a id="t005-from9-sql12"></a>
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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

<a id="t005-from9-sql18"></a>
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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

#### Q10：本轮FAD（1个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** Q18。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q18](#t005-from10-sql18) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from10-sql18"></a>
<details><summary>后续Q18：实际SQL</summary>

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

#### Q11：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q12](#t005-from11-sql12) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t005-from11-sql13) | sheet1.Destination, sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from11-sql14) | sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from11-sql15) | sheet1.Destination, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from11-sql16) | sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from11-sql17) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q18](#t005-from11-sql18) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q19](#t005-from11-sql19) | sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from11-sql20) | sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from11-sql12"></a>
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q12：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：sheet1.Sales Quantity le 10（部分信息）。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q16](#t005-from12-sql16) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q13](#t005-from12-sql13) | sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q14](#t005-from12-sql14) | sheet1.Consigned Product, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from12-sql15) | sheet1.Destination, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from12-sql16) | sheet1.Age Range, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from12-sql17) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q18](#t005-from12-sql18) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q19](#t005-from12-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from12-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from12-sql13"></a>
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q13：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Consigned Product, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q14](#t005-from13-sql14) | sheet1.Consigned Product, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q15](#t005-from13-sql15) | sheet1.Destination, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from13-sql16) | sheet1.Age Range, sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from13-sql17) | sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from13-sql18) | sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from13-sql19) | sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from13-sql20) | sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from13-sql14"></a>
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q14：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q15](#t005-from14-sql15) | sheet1.Destination, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q16](#t005-from14-sql16) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from14-sql17) | sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from14-sql18) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from14-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from14-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from14-sql15"></a>
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q15：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q16](#t005-from15-sql16) | sheet1.Age Range, sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q17](#t005-from15-sql17) | sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t005-from15-sql18) | sheet1.Discount Amount, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q19](#t005-from15-sql19) | sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from15-sql20) | sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from15-sql16"></a>
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q16：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：sheet1.Sales Quantity le 10（部分信息）。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 没有；后续SQL未完整包含这一项所述内容 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q17](#t005-from16-sql17) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q18](#t005-from16-sql18) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q19](#t005-from16-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from16-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from16-sql17"></a>
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q17：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q18](#t005-from17-sql18) | sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost |
| [Q19](#t005-from17-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from17-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from17-sql18"></a>
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q18：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q19](#t005-from18-sql19) | sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Value-Added Service Revenue, sheet1.Profit Margin, sheet1.Sales Quantity |
| [Q20](#t005-from18-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from18-sql19"></a>
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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

#### Q19：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q20](#t005-from19-sql20) | sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t005-from19-sql20"></a>
<details><summary>后续Q20：实际SQL</summary>

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

#### Q20：本轮FAD（1个候选）

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

##### 候选1：没有找到对应内容

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Unit Price, sheet1.Logistics Value-Added Service Revenue, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：未声明此操作。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 未提供具体项，不算预测成功 |

**未找到匹配。剩余实际query为：** Q21。

<details><summary>未匹配的后续Q21：实际SQL</summary>

```sql
SELECT 1
```

</details>

#### Q21：本轮FAD（0个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT 1
```

</details>

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：之后没有再执行SQL，与结束判断一致。**

<!-- task-notes-start -->
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

### 本题分组和聚合的数量

- 分组：1个候选写了具体分组，后续没有出现完全相同分组；地理方向部分对应。
- 聚合：7个候选写了具体聚合，4个后来出现全部所述聚合；其余有拆散执行或只在当前SQL执行的情况。

每个候选计一次；同一预测在不同轮次重复提交会重复计数，不是独立样本。分组与聚合分别比较，不能将分别出现在不同SQL的操作说成整个候选在同一SQL中发生。没有填写的操作不进入上述数量。
known联合分组比较完整维度，partial允许增加维度；partial连接允许增加条件。过滤自动核对的是已知条件单项；相近但不相同的日期写法、粒度变化及复杂表达式，按上面的具体例子解释。

旧报告把AVG(Profit Margin)等缺少表前缀的列判成不匹配。本次依据唯一真实列核对后，聚合为7个中4个对应，而不是旧报告的7个中2个。九项AVG分散执行的情况已在本题补充分析单列，不把它们全判错。

<!-- task-notes-end -->

原始记录：[events.jsonl](../runs/dacomp-005-02/events.jsonl)；本题复核数据：[JSON](dacomp-005-02.json)。

<a id="task-006"></a>

## DAComp-006：华南利润波动

**本题结论：前中段契合较好，后段候选更新不及时。**

本节只分析该任务本次运行的FAD与实际SQL。Q1、Q2等编号表示该任务内的SQL执行顺序。
解开字符串、补齐唯一可确定的表名前缀，并计入FAD操作字段明确引用的列；不按接口是否接收筛选预测，不从列名推测未写出的分组或聚合。

<!-- task-rates-start -->
### 本题数量与预测成功比例

**计数单位：一轮SQL附带一份FAD，一份FAD可以包含多个候选。预测成功比例按候选算。**
这里“成功”采用统一的保守标准：候选明确写出的列、过滤条件、连接、分组和聚合，能在某条严格后续成功SQL中一起找到；如果同时写了分组和聚合，它们还需要出现在同一个查询层。只说对其中一部分，单独计为部分对应。没有候选的FAD不进入候选成功率分母。

| 统计内容 | 本题结果 |
|---|---|
| 共提交多少份FAD | 30份 |
| 其中有候选 / 没有候选 | 29份 / 1份 |
| 共提出多少个候选 | 58个 |
| **候选预测成功：已写信息全部对应** | **29个，29/58 = 50.0%** |
| 只对应一部分 | 29个，29/58 = 50.0% |
| 已写内容都没找到后续对应 | 0个，0/58 = 0.0% |
| 写了具体操作的候选，其已写信息全部对应 | 29/58 = 50.0% |
| 只列字段、没写具体操作的候选，其列清单全部对应 | 没有这种候选 |

**分开看各字段的预测比例：**

| 预测内容 | 写了多少个候选 | 其中多少个后来对应 | 比例 |
|---|---:|---:|---:|
| 列清单（包括操作里引用的列） | 58 | 50 | 50/58 = 86.2% |
| 已知过滤条件 | 55 | 51 | 51/55 = 92.7% |
| 连接 | 0 | 0 | 没有这种候选 |
| 分组 | 53 | 40 | 40/53 = 75.5% |
| 聚合 | 58 | 46 | 46/58 = 79.3% |

分项比例只判断该字段；候选成功率要求这些信息在同一条后续SQL里共同出现，所以通常更低。只列字段的成功不表示预测了查询操作，已在上表单列。none/unknown不作为已写出的操作项计分；因此成功只表示已写信息对应，不表示完整预测了后续SQL全部内容。
同一候选在多轮重复提交会重复计数，多个候选也可能对应同一条后续SQL。复杂表达式与近似方向的人工解释保留在下文；自动过滤匹配仅检查已知条件单项，以上是统一规则下的对应比例，不是完整SQL语义等价率。
逐候选分类及对应SQL编号保存在[比例复核数据](task-rates.json)的006项。
<!-- task-rates-end -->

### 逐轮FAD与后续query核对

从Q1开始逐轮列出全部候选；不是选例子。每个候选列出所有完整对应的后续query，部分对应按字段单独列出。本轮涉及的后续SQL原文紧接在候选后面，同一条SQL在本轮内只展示一次。SQL可展开查看。

#### Q1：本轮FAD（2个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT Destination,
 COUNT(*) AS cnt
FROM sheet1
GROUP BY Destination
ORDER BY cnt DESC
```

</details>

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Destination。
- 聚合：COUNT(*)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q24](#t006-from1-sql24)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29)、[Q30](#t006-from1-sql30) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from1-sql14) |
| 聚合 | [Q2](#t006-from1-sql2)、[Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q17](#t006-from1-sql17)、[Q19](#t006-from1-sql19)、[Q25](#t006-from1-sql25)、[Q30](#t006-from1-sql30) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q2](#t006-from1-sql2) | sheet1.Date |
| [Q3](#t006-from1-sql3) | sheet1.Date, sheet1.Destination |
| [Q4](#t006-from1-sql4) | sheet1.Date, sheet1.Destination |
| [Q5](#t006-from1-sql5) | sheet1.Destination |
| [Q6](#t006-from1-sql6) | sheet1.Destination |
| [Q7](#t006-from1-sql7) | sheet1.Date, sheet1.Destination |
| [Q8](#t006-from1-sql8) | sheet1.Destination |
| [Q9](#t006-from1-sql9) | sheet1.Date, sheet1.Destination |
| [Q11](#t006-from1-sql11) | sheet1.Date, sheet1.Destination |
| [Q12](#t006-from1-sql12) | sheet1.Date, sheet1.Destination |
| [Q13](#t006-from1-sql13) | sheet1.Date, sheet1.Destination |
| [Q14](#t006-from1-sql14) | sheet1.Date, sheet1.Destination |
| [Q15](#t006-from1-sql15) | sheet1.Date, sheet1.Destination |
| [Q16](#t006-from1-sql16) | sheet1.Date, sheet1.Destination |
| [Q17](#t006-from1-sql17) | sheet1.Date, sheet1.Destination |
| [Q18](#t006-from1-sql18) | sheet1.Date, sheet1.Destination |
| [Q19](#t006-from1-sql19) | sheet1.Date, sheet1.Destination |
| [Q20](#t006-from1-sql20) | sheet1.Date, sheet1.Destination |
| [Q21](#t006-from1-sql21) | sheet1.Date, sheet1.Destination |
| [Q22](#t006-from1-sql22) | sheet1.Date, sheet1.Destination |
| [Q23](#t006-from1-sql23) | sheet1.Destination |
| [Q24](#t006-from1-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from1-sql25) | sheet1.Destination |
| [Q26](#t006-from1-sql26) | sheet1.Destination |
| [Q27](#t006-from1-sql27) | sheet1.Date, sheet1.Destination |
| [Q28](#t006-from1-sql28) | sheet1.Date, sheet1.Destination |
| [Q29](#t006-from1-sql29) | sheet1.Date, sheet1.Destination |
| [Q30](#t006-from1-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q3、Q9、Q12、Q17、Q19、Q28。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q20](#t006-from1-sql20)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q29](#t006-from1-sql29) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q3](#t006-from1-sql3)、[Q9](#t006-from1-sql9)、[Q11](#t006-from1-sql11)、[Q12](#t006-from1-sql12)、[Q17](#t006-from1-sql17)、[Q19](#t006-from1-sql19)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q24](#t006-from1-sql24)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28)、[Q30](#t006-from1-sql30) |
| 聚合 | [Q3](#t006-from1-sql3)、[Q4](#t006-from1-sql4)、[Q7](#t006-from1-sql7)、[Q9](#t006-from1-sql9)、[Q12](#t006-from1-sql12)、[Q13](#t006-from1-sql13)、[Q14](#t006-from1-sql14)、[Q15](#t006-from1-sql15)、[Q16](#t006-from1-sql16)、[Q17](#t006-from1-sql17)、[Q18](#t006-from1-sql18)、[Q19](#t006-from1-sql19)、[Q21](#t006-from1-sql21)、[Q22](#t006-from1-sql22)、[Q25](#t006-from1-sql25)、[Q27](#t006-from1-sql27)、[Q28](#t006-from1-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from1-sql2"></a>
<details><summary>后续Q2：实际SQL</summary>

```sql
SELECT MIN(Date) AS min_date,
 MAX(Date) AS max_date,
 COUNT(*) AS total_rows
FROM sheet1
```

</details>

<a id="t006-from1-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from1-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from1-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from1-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q2：本轮FAD（1个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT MIN(Date) AS min_date,
 MAX(Date) AS max_date,
 COUNT(*) AS total_rows
FROM sheet1
```

</details>

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：未声明此操作。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q3、Q9、Q12、Q17、Q19、Q28。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q20](#t006-from2-sql20)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q29](#t006-from2-sql29) |
| 过滤 | 未提供具体项，不算预测成功 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q3](#t006-from2-sql3)、[Q9](#t006-from2-sql9)、[Q11](#t006-from2-sql11)、[Q12](#t006-from2-sql12)、[Q17](#t006-from2-sql17)、[Q19](#t006-from2-sql19)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q24](#t006-from2-sql24)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28)、[Q30](#t006-from2-sql30) |
| 聚合 | [Q3](#t006-from2-sql3)、[Q4](#t006-from2-sql4)、[Q7](#t006-from2-sql7)、[Q9](#t006-from2-sql9)、[Q12](#t006-from2-sql12)、[Q13](#t006-from2-sql13)、[Q14](#t006-from2-sql14)、[Q15](#t006-from2-sql15)、[Q16](#t006-from2-sql16)、[Q17](#t006-from2-sql17)、[Q18](#t006-from2-sql18)、[Q19](#t006-from2-sql19)、[Q21](#t006-from2-sql21)、[Q22](#t006-from2-sql22)、[Q25](#t006-from2-sql25)、[Q27](#t006-from2-sql27)、[Q28](#t006-from2-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from2-sql3"></a>
<details><summary>后续Q3：实际SQL</summary>

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
<details><summary>后续Q4：实际SQL</summary>

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

<a id="t006-from2-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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

<a id="t006-from2-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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

<a id="t006-from2-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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

<a id="t006-from2-sql27"></a>
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q3：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q9、Q12、Q17。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q17](#t006-from3-sql17)、[Q20](#t006-from3-sql20) |
| 过滤 | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q17](#t006-from3-sql17)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q24](#t006-from3-sql24)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q30](#t006-from3-sql30) |
| 聚合 | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q4、Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28)、[Q29](#t006-from3-sql29) |
| 过滤 | [Q4](#t006-from3-sql4)、[Q5](#t006-from3-sql5)、[Q6](#t006-from3-sql6)、[Q7](#t006-from3-sql7)、[Q8](#t006-from3-sql8)、[Q9](#t006-from3-sql9)、[Q11](#t006-from3-sql11)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q20](#t006-from3-sql20)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q23](#t006-from3-sql23)、[Q24](#t006-from3-sql24)、[Q25](#t006-from3-sql25)、[Q26](#t006-from3-sql26)、[Q27](#t006-from3-sql27)、[Q29](#t006-from3-sql29)、[Q30](#t006-from3-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q4](#t006-from3-sql4)、[Q14](#t006-from3-sql14)、[Q22](#t006-from3-sql22) |
| 聚合 | [Q4](#t006-from3-sql4)、[Q7](#t006-from3-sql7)、[Q9](#t006-from3-sql9)、[Q12](#t006-from3-sql12)、[Q13](#t006-from3-sql13)、[Q14](#t006-from3-sql14)、[Q15](#t006-from3-sql15)、[Q16](#t006-from3-sql16)、[Q17](#t006-from3-sql17)、[Q18](#t006-from3-sql18)、[Q19](#t006-from3-sql19)、[Q21](#t006-from3-sql21)、[Q22](#t006-from3-sql22)、[Q25](#t006-from3-sql25)、[Q27](#t006-from3-sql27)、[Q28](#t006-from3-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from3-sql4"></a>
<details><summary>后续Q4：实际SQL</summary>

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
<details><summary>后续Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from3-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from3-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from3-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q4：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)。

**整个候选对应的后续query：** Q7。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t006-from4-sql7)、[Q20](#t006-from4-sql20) |
| 过滤 | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q7](#t006-from4-sql7)、[Q13](#t006-from4-sql13)、[Q15](#t006-from4-sql15)、[Q21](#t006-from4-sql21) |
| 聚合 | [Q7](#t006-from4-sql7)、[Q9](#t006-from4-sql9)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17) |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：AVG(sheet1.Profit Margin)、SUM(sheet1.Discount Amount)、SUM(sheet1.Logistics Unit Price)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q5](#t006-from4-sql5)、[Q6](#t006-from4-sql6)、[Q7](#t006-from4-sql7)、[Q8](#t006-from4-sql8)、[Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q13](#t006-from4-sql13)、[Q14](#t006-from4-sql14)、[Q15](#t006-from4-sql15)、[Q16](#t006-from4-sql16)、[Q17](#t006-from4-sql17)、[Q18](#t006-from4-sql18)、[Q19](#t006-from4-sql19)、[Q20](#t006-from4-sql20)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q23](#t006-from4-sql23)、[Q24](#t006-from4-sql24)、[Q25](#t006-from4-sql25)、[Q26](#t006-from4-sql26)、[Q27](#t006-from4-sql27)、[Q29](#t006-from4-sql29)、[Q30](#t006-from4-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q9](#t006-from4-sql9)、[Q11](#t006-from4-sql11)、[Q12](#t006-from4-sql12)、[Q17](#t006-from4-sql17)、[Q19](#t006-from4-sql19)、[Q21](#t006-from4-sql21)、[Q22](#t006-from4-sql22)、[Q24](#t006-from4-sql24)、[Q27](#t006-from4-sql27)、[Q28](#t006-from4-sql28)、[Q30](#t006-from4-sql30) |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q5](#t006-from4-sql5) | sheet1.Destination |
| [Q6](#t006-from4-sql6) | sheet1.Destination |
| [Q7](#t006-from4-sql7) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q8](#t006-from4-sql8) | sheet1.Destination |
| [Q9](#t006-from4-sql9) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t006-from4-sql11) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q12](#t006-from4-sql12) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t006-from4-sql13) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q14](#t006-from4-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from4-sql15) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q16](#t006-from4-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from4-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from4-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from4-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q20](#t006-from4-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from4-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from4-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from4-sql23) | sheet1.Destination |
| [Q24](#t006-from4-sql24) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Logistics Unit Price |
| [Q25](#t006-from4-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from4-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from4-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from4-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from4-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from4-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from4-sql5"></a>
<details><summary>后续Q5：实际SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

<a id="t006-from4-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from4-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from4-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q5：本轮FAD（1个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT "Consigned Product"
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY 1
```

</details>

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)。

**整个候选对应的后续query：** Q7。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t006-from5-sql7)、[Q20](#t006-from5-sql20) |
| 过滤 | [Q6](#t006-from5-sql6)、[Q7](#t006-from5-sql7)、[Q8](#t006-from5-sql8)、[Q9](#t006-from5-sql9)、[Q11](#t006-from5-sql11)、[Q12](#t006-from5-sql12)、[Q13](#t006-from5-sql13)、[Q14](#t006-from5-sql14)、[Q15](#t006-from5-sql15)、[Q16](#t006-from5-sql16)、[Q17](#t006-from5-sql17)、[Q18](#t006-from5-sql18)、[Q19](#t006-from5-sql19)、[Q20](#t006-from5-sql20)、[Q21](#t006-from5-sql21)、[Q22](#t006-from5-sql22)、[Q23](#t006-from5-sql23)、[Q24](#t006-from5-sql24)、[Q25](#t006-from5-sql25)、[Q26](#t006-from5-sql26)、[Q27](#t006-from5-sql27)、[Q29](#t006-from5-sql29)、[Q30](#t006-from5-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q7](#t006-from5-sql7)、[Q13](#t006-from5-sql13)、[Q15](#t006-from5-sql15)、[Q21](#t006-from5-sql21) |
| 聚合 | [Q7](#t006-from5-sql7)、[Q9](#t006-from5-sql9)、[Q12](#t006-from5-sql12)、[Q17](#t006-from5-sql17) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from5-sql6"></a>
<details><summary>后续Q6：实际SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

<a id="t006-from5-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from5-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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

<a id="t006-from5-sql29"></a>
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q6：本轮FAD（2个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT Destination
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY Destination
```

</details>

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Discount Amount)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17)、[Q19](#t006-from6-sql19)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q24](#t006-from6-sql24)、[Q27](#t006-from6-sql27)、[Q28](#t006-from6-sql28)、[Q30](#t006-from6-sql30) |
| 聚合 | [Q9](#t006-from6-sql9) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q7](#t006-from6-sql7) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q8](#t006-from6-sql8) | sheet1.Destination |
| [Q9](#t006-from6-sql9) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t006-from6-sql11) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Total Logistics Revenue |
| [Q12](#t006-from6-sql12) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t006-from6-sql13) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q14](#t006-from6-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from6-sql15) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q16](#t006-from6-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from6-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from6-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from6-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q20](#t006-from6-sql20) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from6-sql21) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from6-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from6-sql23) | sheet1.Destination |
| [Q24](#t006-from6-sql24) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Sales Quantity |
| [Q25](#t006-from6-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from6-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from6-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from6-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from6-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from6-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)。

**整个候选对应的后续query：** Q7。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q7](#t006-from6-sql7)、[Q20](#t006-from6-sql20) |
| 过滤 | [Q7](#t006-from6-sql7)、[Q8](#t006-from6-sql8)、[Q9](#t006-from6-sql9)、[Q11](#t006-from6-sql11)、[Q12](#t006-from6-sql12)、[Q13](#t006-from6-sql13)、[Q14](#t006-from6-sql14)、[Q15](#t006-from6-sql15)、[Q16](#t006-from6-sql16)、[Q17](#t006-from6-sql17)、[Q18](#t006-from6-sql18)、[Q19](#t006-from6-sql19)、[Q20](#t006-from6-sql20)、[Q21](#t006-from6-sql21)、[Q22](#t006-from6-sql22)、[Q23](#t006-from6-sql23)、[Q24](#t006-from6-sql24)、[Q25](#t006-from6-sql25)、[Q26](#t006-from6-sql26)、[Q27](#t006-from6-sql27)、[Q29](#t006-from6-sql29)、[Q30](#t006-from6-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q7](#t006-from6-sql7)、[Q13](#t006-from6-sql13)、[Q15](#t006-from6-sql15)、[Q21](#t006-from6-sql21) |
| 聚合 | [Q7](#t006-from6-sql7)、[Q9](#t006-from6-sql9)、[Q12](#t006-from6-sql12)、[Q17](#t006-from6-sql17) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from6-sql7"></a>
<details><summary>后续Q7：实际SQL</summary>

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
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from6-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q7：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from7-sql20) |
| 过滤 | [Q8](#t006-from7-sql8)、[Q9](#t006-from7-sql9)、[Q11](#t006-from7-sql11)、[Q12](#t006-from7-sql12)、[Q13](#t006-from7-sql13)、[Q14](#t006-from7-sql14)、[Q15](#t006-from7-sql15)、[Q16](#t006-from7-sql16)、[Q17](#t006-from7-sql17)、[Q18](#t006-from7-sql18)、[Q19](#t006-from7-sql19)、[Q20](#t006-from7-sql20)、[Q21](#t006-from7-sql21)、[Q22](#t006-from7-sql22)、[Q23](#t006-from7-sql23)、[Q24](#t006-from7-sql24)、[Q25](#t006-from7-sql25)、[Q26](#t006-from7-sql26)、[Q27](#t006-from7-sql27)、[Q29](#t006-from7-sql29)、[Q30](#t006-from7-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from7-sql13)、[Q15](#t006-from7-sql15)、[Q21](#t006-from7-sql21) |
| 聚合 | [Q9](#t006-from7-sql9)、[Q12](#t006-from7-sql12)、[Q17](#t006-from7-sql17) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q8](#t006-from7-sql8) | sheet1.Destination |
| [Q9](#t006-from7-sql9) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q11](#t006-from7-sql11) | sheet1.Date, sheet1.Destination, sheet1.Total Logistics Revenue |
| [Q12](#t006-from7-sql12) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t006-from7-sql13) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q14](#t006-from7-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from7-sql15) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q16](#t006-from7-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from7-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from7-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from7-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q20](#t006-from7-sql20) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from7-sql21) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from7-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from7-sql23) | sheet1.Destination |
| [Q24](#t006-from7-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from7-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from7-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from7-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from7-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from7-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from7-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from7-sql8"></a>
<details><summary>后续Q8：实际SQL</summary>

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
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from7-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q8：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28)、[Q29](#t006-from8-sql29) |
| 过滤 | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from8-sql14)、[Q22](#t006-from8-sql22) |
| 聚合 | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q13、Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from8-sql13)、[Q15](#t006-from8-sql15)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q29](#t006-from8-sql29) |
| 过滤 | [Q9](#t006-from8-sql9)、[Q11](#t006-from8-sql11)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q20](#t006-from8-sql20)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q23](#t006-from8-sql23)、[Q24](#t006-from8-sql24)、[Q25](#t006-from8-sql25)、[Q26](#t006-from8-sql26)、[Q27](#t006-from8-sql27)、[Q29](#t006-from8-sql29)、[Q30](#t006-from8-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from8-sql13)、[Q15](#t006-from8-sql15)、[Q21](#t006-from8-sql21) |
| 聚合 | [Q9](#t006-from8-sql9)、[Q12](#t006-from8-sql12)、[Q13](#t006-from8-sql13)、[Q14](#t006-from8-sql14)、[Q15](#t006-from8-sql15)、[Q16](#t006-from8-sql16)、[Q17](#t006-from8-sql17)、[Q18](#t006-from8-sql18)、[Q19](#t006-from8-sql19)、[Q21](#t006-from8-sql21)、[Q22](#t006-from8-sql22)、[Q25](#t006-from8-sql25)、[Q27](#t006-from8-sql27)、[Q28](#t006-from8-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from8-sql9"></a>
<details><summary>后续Q9：实际SQL</summary>

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
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from8-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q9：本轮FAD（3个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount)、SUM(sheet1.List Price Revenue)、SUM(sheet1.Logistics Value-Added Service Revenue)、SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q17](#t006-from9-sql17)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q24](#t006-from9-sql24)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q30](#t006-from9-sql30) |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q11](#t006-from9-sql11) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Logistics Value-Added Service Revenue, sheet1.Total Logistics Revenue |
| [Q12](#t006-from9-sql12) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t006-from9-sql13) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q14](#t006-from9-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from9-sql15) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q16](#t006-from9-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from9-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from9-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from9-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q20](#t006-from9-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from9-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from9-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from9-sql23) | sheet1.Destination |
| [Q24](#t006-from9-sql24) | sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Logistics Value-Added Service Revenue, sheet1.Sales Quantity |
| [Q25](#t006-from9-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from9-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from9-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from9-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from9-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from9-sql30) | sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Warehousing Cost |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28)、[Q29](#t006-from9-sql29) |
| 过滤 | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from9-sql14)、[Q22](#t006-from9-sql22) |
| 聚合 | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28) |

##### 候选3：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q13、Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q29](#t006-from9-sql29) |
| 过滤 | [Q11](#t006-from9-sql11)、[Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q20](#t006-from9-sql20)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q23](#t006-from9-sql23)、[Q24](#t006-from9-sql24)、[Q25](#t006-from9-sql25)、[Q26](#t006-from9-sql26)、[Q27](#t006-from9-sql27)、[Q29](#t006-from9-sql29)、[Q30](#t006-from9-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from9-sql13)、[Q15](#t006-from9-sql15)、[Q21](#t006-from9-sql21) |
| 聚合 | [Q12](#t006-from9-sql12)、[Q13](#t006-from9-sql13)、[Q14](#t006-from9-sql14)、[Q15](#t006-from9-sql15)、[Q16](#t006-from9-sql16)、[Q17](#t006-from9-sql17)、[Q18](#t006-from9-sql18)、[Q19](#t006-from9-sql19)、[Q21](#t006-from9-sql21)、[Q22](#t006-from9-sql22)、[Q25](#t006-from9-sql25)、[Q27](#t006-from9-sql27)、[Q28](#t006-from9-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from9-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from9-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q10：本轮FAD（3个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28)、[Q29](#t006-from10-sql29) |
| 过滤 | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from10-sql14)、[Q22](#t006-from10-sql22) |
| 聚合 | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q13、Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from10-sql13)、[Q15](#t006-from10-sql15)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q29](#t006-from10-sql29) |
| 过滤 | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from10-sql13)、[Q15](#t006-from10-sql15)、[Q21](#t006-from10-sql21) |
| 聚合 | [Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q25](#t006-from10-sql25)、[Q27](#t006-from10-sql27)、[Q28](#t006-from10-sql28) |

##### 候选3：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from10-sql20) |
| 过滤 | [Q11](#t006-from10-sql11)、[Q12](#t006-from10-sql12)、[Q13](#t006-from10-sql13)、[Q14](#t006-from10-sql14)、[Q15](#t006-from10-sql15)、[Q16](#t006-from10-sql16)、[Q17](#t006-from10-sql17)、[Q18](#t006-from10-sql18)、[Q19](#t006-from10-sql19)、[Q20](#t006-from10-sql20)、[Q21](#t006-from10-sql21)、[Q22](#t006-from10-sql22)、[Q23](#t006-from10-sql23)、[Q24](#t006-from10-sql24)、[Q25](#t006-from10-sql25)、[Q26](#t006-from10-sql26)、[Q27](#t006-from10-sql27)、[Q29](#t006-from10-sql29)、[Q30](#t006-from10-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q11](#t006-from10-sql11)、[Q19](#t006-from10-sql19) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q11](#t006-from10-sql11) | sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q12](#t006-from10-sql12) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q13](#t006-from10-sql13) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q14](#t006-from10-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from10-sql15) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q16](#t006-from10-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from10-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from10-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from10-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q20](#t006-from10-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from10-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from10-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from10-sql23) | sheet1.Destination |
| [Q24](#t006-from10-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from10-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from10-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from10-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from10-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from10-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from10-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from10-sql11"></a>
<details><summary>后续Q11：实际SQL</summary>

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
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from10-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q11：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28)、[Q29](#t006-from11-sql29) |
| 过滤 | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from11-sql14)、[Q22](#t006-from11-sql22) |
| 聚合 | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q13、Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from11-sql13)、[Q15](#t006-from11-sql15)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q29](#t006-from11-sql29) |
| 过滤 | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q20](#t006-from11-sql20)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q23](#t006-from11-sql23)、[Q24](#t006-from11-sql24)、[Q25](#t006-from11-sql25)、[Q26](#t006-from11-sql26)、[Q27](#t006-from11-sql27)、[Q29](#t006-from11-sql29)、[Q30](#t006-from11-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from11-sql13)、[Q15](#t006-from11-sql15)、[Q21](#t006-from11-sql21) |
| 聚合 | [Q12](#t006-from11-sql12)、[Q13](#t006-from11-sql13)、[Q14](#t006-from11-sql14)、[Q15](#t006-from11-sql15)、[Q16](#t006-from11-sql16)、[Q17](#t006-from11-sql17)、[Q18](#t006-from11-sql18)、[Q19](#t006-from11-sql19)、[Q21](#t006-from11-sql21)、[Q22](#t006-from11-sql22)、[Q25](#t006-from11-sql25)、[Q27](#t006-from11-sql27)、[Q28](#t006-from11-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from11-sql12"></a>
<details><summary>后续Q12：实际SQL</summary>

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
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from11-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q12：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28)、[Q29](#t006-from12-sql29) |
| 过滤 | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from12-sql14)、[Q22](#t006-from12-sql22) |
| 聚合 | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q13、Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q13](#t006-from12-sql13)、[Q15](#t006-from12-sql15)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q29](#t006-from12-sql29) |
| 过滤 | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q20](#t006-from12-sql20)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q23](#t006-from12-sql23)、[Q24](#t006-from12-sql24)、[Q25](#t006-from12-sql25)、[Q26](#t006-from12-sql26)、[Q27](#t006-from12-sql27)、[Q29](#t006-from12-sql29)、[Q30](#t006-from12-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q13](#t006-from12-sql13)、[Q15](#t006-from12-sql15)、[Q21](#t006-from12-sql21) |
| 聚合 | [Q13](#t006-from12-sql13)、[Q14](#t006-from12-sql14)、[Q15](#t006-from12-sql15)、[Q16](#t006-from12-sql16)、[Q17](#t006-from12-sql17)、[Q18](#t006-from12-sql18)、[Q19](#t006-from12-sql19)、[Q21](#t006-from12-sql21)、[Q22](#t006-from12-sql22)、[Q25](#t006-from12-sql25)、[Q27](#t006-from12-sql27)、[Q28](#t006-from12-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from12-sql13"></a>
<details><summary>后续Q13：实际SQL</summary>

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
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from12-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q13：本轮FAD（3个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q15](#t006-from13-sql15)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q29](#t006-from13-sql29) |
| 过滤 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q15](#t006-from13-sql15)、[Q21](#t006-from13-sql21) |
| 聚合 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q14、Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28)、[Q29](#t006-from13-sql29) |
| 过滤 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q14](#t006-from13-sql14)、[Q22](#t006-from13-sql22) |
| 聚合 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q25](#t006-from13-sql25)、[Q27](#t006-from13-sql27)、[Q28](#t006-from13-sql28) |

##### 候选3：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from13-sql20) |
| 过滤 | [Q14](#t006-from13-sql14)、[Q15](#t006-from13-sql15)、[Q16](#t006-from13-sql16)、[Q17](#t006-from13-sql17)、[Q18](#t006-from13-sql18)、[Q19](#t006-from13-sql19)、[Q20](#t006-from13-sql20)、[Q21](#t006-from13-sql21)、[Q22](#t006-from13-sql22)、[Q23](#t006-from13-sql23)、[Q24](#t006-from13-sql24)、[Q25](#t006-from13-sql25)、[Q26](#t006-from13-sql26)、[Q27](#t006-from13-sql27)、[Q29](#t006-from13-sql29)、[Q30](#t006-from13-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q15](#t006-from13-sql15)、[Q21](#t006-from13-sql21) |
| 聚合 | [Q17](#t006-from13-sql17) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q14](#t006-from13-sql14) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q15](#t006-from13-sql15) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q16](#t006-from13-sql16) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q17](#t006-from13-sql17) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q18](#t006-from13-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from13-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q20](#t006-from13-sql20) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q21](#t006-from13-sql21) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from13-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from13-sql23) | sheet1.Destination |
| [Q24](#t006-from13-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from13-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from13-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q27](#t006-from13-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from13-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from13-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from13-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from13-sql14"></a>
<details><summary>后续Q14：实际SQL</summary>

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
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from13-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q14：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28)、[Q29](#t006-from14-sql29) |
| 过滤 | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q22](#t006-from14-sql22) |
| 聚合 | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q15、Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q15](#t006-from14-sql15)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q29](#t006-from14-sql29) |
| 过滤 | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q20](#t006-from14-sql20)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q23](#t006-from14-sql23)、[Q24](#t006-from14-sql24)、[Q25](#t006-from14-sql25)、[Q26](#t006-from14-sql26)、[Q27](#t006-from14-sql27)、[Q29](#t006-from14-sql29)、[Q30](#t006-from14-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q15](#t006-from14-sql15)、[Q21](#t006-from14-sql21) |
| 聚合 | [Q15](#t006-from14-sql15)、[Q16](#t006-from14-sql16)、[Q17](#t006-from14-sql17)、[Q18](#t006-from14-sql18)、[Q19](#t006-from14-sql19)、[Q21](#t006-from14-sql21)、[Q22](#t006-from14-sql22)、[Q25](#t006-from14-sql25)、[Q27](#t006-from14-sql27)、[Q28](#t006-from14-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from14-sql15"></a>
<details><summary>后续Q15：实际SQL</summary>

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
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from14-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q15：本轮FAD（2个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q29](#t006-from15-sql29) |
| 过滤 | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q21](#t006-from15-sql21) |
| 聚合 | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q25](#t006-from15-sql25)、[Q27](#t006-from15-sql27)、[Q28](#t006-from15-sql28) |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from15-sql20)、[Q29](#t006-from15-sql29) |
| 过滤 | [Q16](#t006-from15-sql16)、[Q17](#t006-from15-sql17)、[Q18](#t006-from15-sql18)、[Q19](#t006-from15-sql19)、[Q20](#t006-from15-sql20)、[Q21](#t006-from15-sql21)、[Q22](#t006-from15-sql22)、[Q23](#t006-from15-sql23)、[Q24](#t006-from15-sql24)、[Q25](#t006-from15-sql25)、[Q26](#t006-from15-sql26)、[Q27](#t006-from15-sql27)、[Q29](#t006-from15-sql29)、[Q30](#t006-from15-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q21](#t006-from15-sql21) |
| 聚合 | [Q19](#t006-from15-sql19) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q16](#t006-from15-sql16) | sheet1.Date, sheet1.Destination |
| [Q17](#t006-from15-sql17) | sheet1.Date, sheet1.Destination, sheet1.Total Logistics Revenue |
| [Q18](#t006-from15-sql18) | sheet1.Date, sheet1.Destination |
| [Q19](#t006-from15-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q20](#t006-from15-sql20) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q21](#t006-from15-sql21) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination |
| [Q22](#t006-from15-sql22) | sheet1.Date, sheet1.Destination |
| [Q23](#t006-from15-sql23) | sheet1.Destination |
| [Q24](#t006-from15-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from15-sql25) | sheet1.Destination |
| [Q26](#t006-from15-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Total Logistics Revenue |
| [Q27](#t006-from15-sql27) | sheet1.Date, sheet1.Destination |
| [Q28](#t006-from15-sql28) | sheet1.Date, sheet1.Destination |
| [Q29](#t006-from15-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q30](#t006-from15-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from15-sql16"></a>
<details><summary>后续Q16：实际SQL</summary>

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
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from15-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q16：本轮FAD（3个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q29](#t006-from16-sql29) |
| 过滤 | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q22](#t006-from16-sql22) |
| 聚合 | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q25](#t006-from16-sql25)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Sales Quantity)、COUNT(*)。

**整个候选对应的后续query：** Q17。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q17](#t006-from16-sql17)、[Q20](#t006-from16-sql20) |
| 过滤 | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q17](#t006-from16-sql17)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q30](#t006-from16-sql30) |
| 聚合 | [Q17](#t006-from16-sql17) |

##### 候选3：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit Margin。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：AVG(sheet1.Profit Margin)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)。

**整个候选对应的后续query：** Q19。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q29](#t006-from16-sql29) |
| 过滤 | [Q17](#t006-from16-sql17)、[Q18](#t006-from16-sql18)、[Q19](#t006-from16-sql19)、[Q20](#t006-from16-sql20)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q23](#t006-from16-sql23)、[Q24](#t006-from16-sql24)、[Q25](#t006-from16-sql25)、[Q26](#t006-from16-sql26)、[Q27](#t006-from16-sql27)、[Q29](#t006-from16-sql29)、[Q30](#t006-from16-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q17](#t006-from16-sql17)、[Q19](#t006-from16-sql19)、[Q21](#t006-from16-sql21)、[Q22](#t006-from16-sql22)、[Q24](#t006-from16-sql24)、[Q27](#t006-from16-sql27)、[Q28](#t006-from16-sql28)、[Q30](#t006-from16-sql30) |
| 聚合 | [Q19](#t006-from16-sql19) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from16-sql17"></a>
<details><summary>后续Q17：实际SQL</summary>

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
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from16-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q17：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Sales Quantity)、COUNT(*)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from17-sql20) |
| 过滤 | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q19](#t006-from17-sql19)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q30](#t006-from17-sql30) |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q18](#t006-from17-sql18) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q19](#t006-from17-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q20](#t006-from17-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |
| [Q21](#t006-from17-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from17-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from17-sql23) | sheet1.Destination |
| [Q24](#t006-from17-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from17-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from17-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue |
| [Q27](#t006-from17-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from17-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from17-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q30](#t006-from17-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit Margin。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：AVG(sheet1.Profit Margin)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)。

**整个候选对应的后续query：** Q19。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q29](#t006-from17-sql29) |
| 过滤 | [Q18](#t006-from17-sql18)、[Q19](#t006-from17-sql19)、[Q20](#t006-from17-sql20)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q23](#t006-from17-sql23)、[Q24](#t006-from17-sql24)、[Q25](#t006-from17-sql25)、[Q26](#t006-from17-sql26)、[Q27](#t006-from17-sql27)、[Q29](#t006-from17-sql29)、[Q30](#t006-from17-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q19](#t006-from17-sql19)、[Q21](#t006-from17-sql21)、[Q22](#t006-from17-sql22)、[Q24](#t006-from17-sql24)、[Q27](#t006-from17-sql27)、[Q28](#t006-from17-sql28)、[Q30](#t006-from17-sql30) |
| 聚合 | [Q19](#t006-from17-sql19) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from17-sql18"></a>
<details><summary>后续Q18：实际SQL</summary>

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
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from17-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q18：本轮FAD（3个候选）

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

##### 候选1：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28)、[Q29](#t006-from18-sql29) |
| 过滤 | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q22](#t006-from18-sql22) |
| 聚合 | [Q19](#t006-from18-sql19)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28) |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q21。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q29](#t006-from18-sql29) |
| 过滤 | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q23](#t006-from18-sql23)、[Q24](#t006-from18-sql24)、[Q25](#t006-from18-sql25)、[Q26](#t006-from18-sql26)、[Q27](#t006-from18-sql27)、[Q29](#t006-from18-sql29)、[Q30](#t006-from18-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q21](#t006-from18-sql21) |
| 聚合 | [Q19](#t006-from18-sql19)、[Q21](#t006-from18-sql21)、[Q22](#t006-from18-sql22)、[Q25](#t006-from18-sql25)、[Q27](#t006-from18-sql27)、[Q28](#t006-from18-sql28) |

##### 候选3：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue。
- 过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q19](#t006-from18-sql19)、[Q20](#t006-from18-sql20)、[Q29](#t006-from18-sql29) |
| 过滤 | 没有；后续SQL未完整包含这一项所述内容 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | [Q19](#t006-from18-sql19) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q19](#t006-from18-sql19) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q20](#t006-from18-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q21](#t006-from18-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from18-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from18-sql23) | sheet1.Destination |
| [Q24](#t006-from18-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from18-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from18-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q27](#t006-from18-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from18-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from18-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q30](#t006-from18-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from18-sql19"></a>
<details><summary>后续Q19：实际SQL</summary>

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
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from18-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q19：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue。
- 过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q20](#t006-from19-sql20)、[Q29](#t006-from19-sql29) |
| 过滤 | 没有；后续SQL未完整包含这一项所述内容 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q20](#t006-from19-sql20) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q21](#t006-from19-sql21) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from19-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from19-sql23) | sheet1.Destination |
| [Q24](#t006-from19-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from19-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from19-sql26) | sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q27](#t006-from19-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from19-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from19-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue |
| [Q30](#t006-from19-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from19-sql20"></a>
<details><summary>后续Q20：实际SQL</summary>

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
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from19-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q20：本轮FAD（1个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue, sheet1.Waybill Number。
- 过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from20-sql29) |
| 过滤 | 没有；后续SQL未完整包含这一项所述内容 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q21](#t006-from20-sql21) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q22](#t006-from20-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from20-sql23) | sheet1.Destination |
| [Q24](#t006-from20-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from20-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from20-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Revenue |
| [Q27](#t006-from20-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from20-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from20-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue, sheet1.Waybill Number |
| [Q30](#t006-from20-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from20-sql21"></a>
<details><summary>后续Q21：实际SQL</summary>

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
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from20-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q21：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q22](#t006-from21-sql22) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q23](#t006-from21-sql23) | sheet1.Destination |
| [Q24](#t006-from21-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from21-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from21-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q27](#t006-from21-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from21-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from21-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin |
| [Q30](#t006-from21-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：已写信息全部对应

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** Q22。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q22](#t006-from21-sql22)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28)、[Q29](#t006-from21-sql29) |
| 过滤 | [Q22](#t006-from21-sql22)、[Q23](#t006-from21-sql23)、[Q24](#t006-from21-sql24)、[Q25](#t006-from21-sql25)、[Q26](#t006-from21-sql26)、[Q27](#t006-from21-sql27)、[Q29](#t006-from21-sql29)、[Q30](#t006-from21-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q22](#t006-from21-sql22) |
| 聚合 | [Q22](#t006-from21-sql22)、[Q25](#t006-from21-sql25)、[Q27](#t006-from21-sql27)、[Q28](#t006-from21-sql28) |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from21-sql22"></a>
<details><summary>后续Q22：实际SQL</summary>

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
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from21-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q22：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q23](#t006-from22-sql23) | sheet1.Destination |
| [Q24](#t006-from22-sql24) | sheet1.Date, sheet1.Destination, sheet1.Sales Quantity |
| [Q25](#t006-from22-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from22-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity |
| [Q27](#t006-from22-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from22-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from22-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin |
| [Q30](#t006-from22-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28)、[Q29](#t006-from22-sql29) |
| 过滤 | [Q23](#t006-from22-sql23)、[Q24](#t006-from22-sql24)、[Q25](#t006-from22-sql25)、[Q26](#t006-from22-sql26)、[Q27](#t006-from22-sql27)、[Q29](#t006-from22-sql29)、[Q30](#t006-from22-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q25](#t006-from22-sql25)、[Q27](#t006-from22-sql27)、[Q28](#t006-from22-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q23](#t006-from22-sql23) | sheet1.Destination |
| [Q24](#t006-from22-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from22-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from22-sql26) | sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from22-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from22-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from22-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from22-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from22-sql23"></a>
<details><summary>后续Q23：实际SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

<a id="t006-from22-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q23：本轮FAD（2个候选）

<details><summary>当前执行的SQL</summary>

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province
FROM sheet1
WHERE Destination LIKE 'South China%'
ORDER BY province
```

</details>

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from23-sql29) |
| 过滤 | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q25](#t006-from23-sql25)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q24](#t006-from23-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from23-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from23-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from23-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from23-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from23-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from23-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28)、[Q29](#t006-from23-sql29) |
| 过滤 | [Q24](#t006-from23-sql24)、[Q25](#t006-from23-sql25)、[Q26](#t006-from23-sql26)、[Q27](#t006-from23-sql27)、[Q29](#t006-from23-sql29)、[Q30](#t006-from23-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q25](#t006-from23-sql25)、[Q27](#t006-from23-sql27)、[Q28](#t006-from23-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q24](#t006-from23-sql24) | sheet1.Date, sheet1.Destination |
| [Q25](#t006-from23-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from23-sql26) | sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from23-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from23-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from23-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from23-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from23-sql24"></a>
<details><summary>后续Q24：实际SQL</summary>

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
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q24：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from24-sql29) |
| 过滤 | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q25](#t006-from24-sql25)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q25](#t006-from24-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from24-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from24-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from24-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from24-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from24-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28)、[Q29](#t006-from24-sql29) |
| 过滤 | [Q25](#t006-from24-sql25)、[Q26](#t006-from24-sql26)、[Q27](#t006-from24-sql27)、[Q29](#t006-from24-sql29)、[Q30](#t006-from24-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q25](#t006-from24-sql25)、[Q27](#t006-from24-sql27)、[Q28](#t006-from24-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q25](#t006-from24-sql25) | sheet1.Destination, sheet1.Profit |
| [Q26](#t006-from24-sql26) | sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from24-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from24-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from24-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from24-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from24-sql25"></a>
<details><summary>后续Q25：实际SQL</summary>

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
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q25：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28)、[Q29](#t006-from25-sql29) |
| 过滤 | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q26](#t006-from25-sql26) | sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from25-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from25-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from25-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from25-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from25-sql29) |
| 过滤 | [Q26](#t006-from25-sql26)、[Q27](#t006-from25-sql27)、[Q29](#t006-from25-sql29)、[Q30](#t006-from25-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q27](#t006-from25-sql27)、[Q28](#t006-from25-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q26](#t006-from25-sql26) | sheet1.Consigned Product, sheet1.Destination, sheet1.Profit |
| [Q27](#t006-from25-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from25-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from25-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from25-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from25-sql26"></a>
<details><summary>后续Q26：实际SQL</summary>

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
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q26：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q27](#t006-from26-sql27)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q27](#t006-from26-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from26-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from26-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue |
| [Q30](#t006-from26-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)、COUNT(*)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from26-sql29) |
| 过滤 | [Q27](#t006-from26-sql27)、[Q29](#t006-from26-sql29)、[Q30](#t006-from26-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q27](#t006-from26-sql27)、[Q28](#t006-from26-sql28)、[Q30](#t006-from26-sql30) |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q27](#t006-from26-sql27) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q28](#t006-from26-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from26-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin |
| [Q30](#t006-from26-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from26-sql27"></a>
<details><summary>后续Q27：实际SQL</summary>

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
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q27：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from27-sql29) |
| 过滤 | [Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q28](#t006-from27-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q28](#t006-from27-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from27-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from27-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Destination。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q28](#t006-from27-sql28)、[Q29](#t006-from27-sql29) |
| 过滤 | [Q29](#t006-from27-sql29)、[Q30](#t006-from27-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | [Q28](#t006-from27-sql28) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q28](#t006-from27-sql28) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q29](#t006-from27-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from27-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from27-sql28"></a>
<details><summary>后续Q28：实际SQL</summary>

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
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q28：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Profit)、COUNT(*)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from28-sql29) |
| 过滤 | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q30](#t006-from28-sql30) |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q29](#t006-from28-sql29) | sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin |
| [Q30](#t006-from28-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月） ＋ sheet1.Consigned Product。
- 聚合：SUM(sheet1.Profit)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | [Q29](#t006-from28-sql29) |
| 过滤 | [Q29](#t006-from28-sql29)、[Q30](#t006-from28-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 没有；后续SQL未完整包含这一项所述内容 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q29](#t006-from28-sql29) | sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit |
| [Q30](#t006-from28-sql30) | sheet1.Date, sheet1.Destination |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from28-sql29"></a>
<details><summary>后续Q29：实际SQL</summary>

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
<details><summary>后续Q30：实际SQL</summary>

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

#### Q29：本轮FAD（2个候选）

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

##### 候选1：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue。
- 过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-08-01", "2023-08-31"])。
- 连接：未声明此操作。
- 分组：未声明此操作。
- 聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | 没有；后续SQL未完整包含这一项所述内容 |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | 未提供具体项，不算预测成功 |
| 聚合 | 没有；后续SQL未完整包含这一项所述内容 |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q30](#t006-from29-sql30) | sheet1.Date, sheet1.Destination |

##### 候选2：部分对应，整个候选未命中

**对后续查询的预测：**

- 表：sheet1。
- 列：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Total Logistics Cost, sheet1.Warehousing Cost。
- 过滤：sheet1.Destination like "South China%"。
- 连接：未声明此操作。
- 分组：sheet1.Date（按月）。
- 聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)。

**整个候选对应的后续query：** 无。

| FAD中的信息 | 后续哪些query对应了这一整项 |
|---|---|
| 列清单 | 没有；后续SQL未完整包含这一项所述内容 |
| 过滤 | [Q30](#t006-from29-sql30) |
| 连接 | 未提供具体项，不算预测成功 |
| 分组 | [Q30](#t006-from29-sql30) |
| 聚合 | [Q30](#t006-from29-sql30) |

**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。

| 后续query | 与本候选相同的已写列 |
|---|---|
| [Q30](#t006-from29-sql30) | sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Warehousing Cost |

##### 本轮FAD对应的后续SQL原文

对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。

<a id="t006-from29-sql30"></a>
<details><summary>后续Q30：实际SQL</summary>

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

#### Q30：本轮FAD（0个候选）

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

**本轮FAD：** `{"status": "no_further_access", "candidates": []}`

**判断：之后没有再执行SQL，与结束判断一致。**

<!-- task-notes-start -->
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

### 本题分组和聚合的数量

- 分组：53个候选写了具体分组，其中40个后来出现相同分组。
- 聚合：58个候选写了具体聚合，其中46个后来出现全部所述聚合。

每个候选计一次；同一预测在不同轮次重复提交会重复计数，不是独立样本。分组与聚合分别比较，不能将分别出现在不同SQL的操作说成整个候选在同一SQL中发生。没有填写的操作不进入上述数量。
known联合分组比较完整维度，partial允许增加维度；partial连接允许增加条件。过滤自动核对的是已知条件单项；相近但不相同的日期写法、粒度变化及复杂表达式，按上面的具体例子解释。

<!-- task-notes-end -->

原始记录：[events.jsonl](../runs/dacomp-006-02/events.jsonl)；本题复核数据：[JSON](dacomp-006-02.json)。
