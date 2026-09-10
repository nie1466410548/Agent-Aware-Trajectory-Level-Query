# dacomp-003：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Year","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q1 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"avg"}],"status":"known"}<br>priority: medium | Q7, Q8, Q9, Q10 | Q7 | 没有提供具体项（none） |
| Q2 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Year","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q2 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"avg"}],"status":"known"}<br>priority: medium | Q7, Q8, Q9, Q10 | Q7 | 没有提供具体项（none） |
| Q3 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Year","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q3 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"avg"}],"status":"known"}<br>priority: medium | Q7, Q8, Q9, Q10 | Q7 | 没有提供具体项（none） |
| Q4 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Year","type":"column"},{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | Q8, Q9, Q10, Q11 | 没有提供具体项（none） | Q6, Q7, Q8, Q9, Q10, Q11 |
| Q5 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | Q7, Q8, Q9, Q10 | 没有提供具体项（none） | Q6, Q7, Q8, Q9, Q10, Q11 |
| Q5 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[{"column":"sheet1.Year","type":"column"}],"status":"known"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 未发现对应查询 | 没有提供具体项（none） | 没有提供具体项（none） |
| Q10 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) ","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"partial"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"avg"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"avg"}],"status":"known"}<br>priority: low | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q6 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q7 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q8 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q9 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q11 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT "Region Name", COUNT(*) AS n_rows, MIN("Year") AS min_year, MAX("Year") AS max_year FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q2（ok）

```sql
SELECT "Region Name", COUNT(*) AS n_rows, MIN("Year") AS min_year, MAX("Year") AS max_year FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q3（ok）

```sql
SELECT DISTINCT "Region Name" FROM sheet1 ORDER BY "Region Name"
```

### Q4（ok）

```sql
SELECT s."Year", s."Industrial Water Consumption (100 million m³)", s."Total Water Consumption (100 million m³) ", e."Per capita GDP (yuan/person)" FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" = 'China' ORDER BY s."Year"
```

### Q5（ok）

```sql
SELECT s."Year", ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct, ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" = 'China' ORDER BY s."Year"
```

### Q6（ok）

```sql
SELECT s."Region Name", s."Year", ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct, ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' ORDER BY s."Region Name", s."Year"
```

### Q7（ok）

```sql
SELECT s."Region Name", COUNT(*) AS n, ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share, ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name" ORDER BY avg_share DESC
```

### Q8（ok）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year"), stats AS (SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2 FROM main GROUP BY "Region Name") SELECT "Region Name", ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp, ROUND(sx/n, 2) AS avg_share FROM stats ORDER BY corr_share_gdp DESC
```

### Q9（ok）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT "Region Name", ROUND(MAX(CASE WHEN "Year" = (SELECT MIN("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first, ROUND(MAX(CASE WHEN "Year" = (SELECT MAX("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last, ROUND(MAX(CASE WHEN "Year" = (SELECT MIN("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first, ROUND(MAX(CASE WHEN "Year" = (SELECT MAX("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last FROM main GROUP BY "Region Name" ORDER BY share_last DESC
```

### Q10（ok）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT "Region Name", "Year" AS peak_year, ROUND(ind_share, 2) AS peak_share FROM main WHERE ("Region Name", ind_share) IN (SELECT "Region Name", MAX(ind_share) FROM main GROUP BY "Region Name") ORDER BY "Region Name"
```

### Q11（ok）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT m1."Region Name", ROUND(m1.ind_share, 2) AS share_2003, ROUND(m1.pc_gdp, 0) AS gdp_2003, ROUND(m2.ind_share, 2) AS share_2018, ROUND(m2.pc_gdp, 0) AS gdp_2018 FROM main m1 JOIN main m2 ON m1."Region Name" = m2."Region Name" WHERE m1."Year" = 2003 AND m2."Year" = 2018 ORDER BY gdp_2018 DESC
```
