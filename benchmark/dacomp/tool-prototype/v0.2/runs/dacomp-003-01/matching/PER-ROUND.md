# dacomp-003：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Code","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q1 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Year","sheet1.Region Code","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q2 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Year","sheet1.Region Code","sheet1.Region Name","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q2 / 2 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Code","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q3 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"economic_indicator_data.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q8 | Q4, Q8, Q9, Q12, Q13, Q14, Q15, Q18 | 没有提供具体项（none） |
| Q3 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q4, Q9, Q12, Q13, Q14, Q15 | Q4, Q8, Q9, Q12, Q13, Q14, Q15, Q18 | 没有提供具体项（none） |
| Q4 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Year","sheet1.Region Name"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q9, Q12, Q13, Q14, Q15 | Q8, Q9, Q12, Q13, Q14, Q15, Q18 | 没有提供具体项（none） |
| Q4 / 2 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q5 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":[],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q5 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":[],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q6 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":[],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q6 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":[],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q7 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Year"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"economic_indicator_data.Year","function":"min"},{"column":"economic_indicator_data.Year","function":"max"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | 未发现对应查询 | 没有提供具体项（none） |
| Q8 / 1 | 否，见原始错误 | tables: ["economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q9 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Region Name"],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q10 / 1 | 否，见原始错误 | tables: ["economic_indicator_data","sheet1"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"economic_indicator_data.Region Name","op":"eq","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"economic_indicator_data.Year","op":"eq","right_column":"sheet1.Year"},{"left_column":"economic_indicator_data.Region Code","op":"eq","right_column":"sheet1.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q11, Q18 |
| Q10 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: medium | Q12, Q13, Q14, Q15 | 未发现对应查询 | 没有提供具体项（none） |
| Q11 / 1 | 否，见原始错误 | tables: ["economic_indicator_data","sheet1"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"economic_indicator_data.Region Name","op":"eq","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"economic_indicator_data.Year","op":"eq","right_column":"sheet1.Year"},{"left_column":"economic_indicator_data.Region Code","op":"eq","right_column":"sheet1.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q18 |
| Q11 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: medium | Q12, Q13, Q14, Q15 | 未发现对应查询 | 没有提供具体项（none） |
| Q12 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q13, Q14, Q15 | Q13, Q14, Q15, Q18 | Q13, Q14, Q15, Q17 |
| Q12 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"economic_indicator_data.Per capita GDP (yuan/person)","function":"avg"},{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: medium | Q13, Q14, Q15 | 未发现对应查询 | 没有提供具体项（none） |
| Q13 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q14, Q15 | Q14, Q15, Q18 | Q14, Q15, Q17 |
| Q13 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"economic_indicator_data.Per capita GDP (yuan/person)","function":"avg"},{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: medium | Q14, Q15 | 未发现对应查询 | 没有提供具体项（none） |
| Q14 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q15 | Q15, Q18 | Q15, Q17 |
| Q14 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"economic_indicator_data.Per capita GDP (yuan/person)","function":"avg"},{"column":"sheet1.Industrial Water Consumption (100 million m³)","function":"sum"},{"column":"sheet1.Total Water Consumption (100 million m³) ","function":"sum"}],"status":"known"}<br>priority: medium | Q15 | 未发现对应查询 | 没有提供具体项（none） |
| Q15 / 1 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"sheet1.Region Name","op":"ne","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q18 | Q17 |
| Q15 / 2 | 否，见原始错误 | tables: ["sheet1","economic_indicator_data"]<br>columns: {"items":["economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Region Name","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[{"conditions":[{"left_column":"sheet1.Year","op":"eq","right_column":"economic_indicator_data.Year"},{"left_column":"sheet1.Region Code","op":"eq","right_column":"economic_indicator_data.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[{"column":"sheet1.Region Name","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"economic_indicator_data.Per capita GDP (yuan/person)","function":"avg"}],"status":"known"}<br>priority: medium | 未发现对应查询 | 未发现对应查询 | 没有提供具体项（none） |
| Q16 / 1 | 否，见原始错误 | tables: ["economic_indicator_data","sheet1"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"economic_indicator_data.Region Name","op":"eq","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"economic_indicator_data.Year","op":"eq","right_column":"sheet1.Year"},{"left_column":"economic_indicator_data.Region Code","op":"eq","right_column":"sheet1.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | Q18 | Q18 |
| Q17 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Region Name","sheet1.Year","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"sheet1.Year","op":"eq","type":"predicate","value":{"literal":2018,"status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: low | 没有提供具体项（none） | Q18 | 未发现对应查询 |
| Q18 / 1 | 否，见原始错误 | tables: ["economic_indicator_data","sheet1"]<br>columns: {"items":["economic_indicator_data.Year","economic_indicator_data.Region Name","economic_indicator_data.Per capita GDP (yuan/person)","sheet1.Year","sheet1.Industrial Water Consumption (100 million m³)","sheet1.Total Water Consumption (100 million m³) "],"status":"unspecified"}<br>filters: {"items":[{"column":"economic_indicator_data.Region Name","op":"eq","type":"predicate","value":{"literal":"China","status":"known"}}],"status":"known"}<br>joins: {"items":[{"conditions":[{"left_column":"economic_indicator_data.Year","op":"eq","right_column":"sheet1.Year"},{"left_column":"economic_indicator_data.Region Code","op":"eq","right_column":"sheet1.Region Code"}],"type":"inner"}],"status":"known"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | 未发现对应查询 | 未发现对应查询 |

## 实际SQL

### Q1（ok）

```sql
SELECT * FROM economic_indicator_data LIMIT 10
```

### Q2（ok）

```sql
SELECT * FROM sheet1 LIMIT 10
```

### Q3（ok）

```sql
SELECT "Region Name", COUNT(*) AS n, MIN(Year) AS min_year, MAX(Year) AS max_year FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q4（ok）

```sql
SELECT "Region Name", COUNT(*) AS n, MIN(Year) AS min_year, MAX(Year) AS max_year FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q5（ok）

```sql
SELECT DISTINCT "Region Name" FROM economic_indicator_data ORDER BY "Region Name"
```

### Q6（ok）

```sql
SELECT DISTINCT "Region Name" FROM sheet1 ORDER BY "Region Name"
```

### Q7（db_error）

```sql
SELECT group_concat(DISTINCT "Region Name", ' | ') AS regions FROM economic_indicator_data
```

### Q8（ok）

```sql
SELECT "Region Name", COUNT(*) AS cnt FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q9（ok）

```sql
SELECT "Region Name", COUNT(*) AS cnt FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q10（ok）

```sql
SELECT e.Year, e."Per capita GDP (yuan/person)" AS gdp_pc, w."Industrial Water Consumption (100 million m³)" AS ind_w, w."Total Water Consumption (100 million m³) " AS tot_w, ROUND(100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China' AND e.Year BETWEEN 2000 AND 2009 ORDER BY e.Year
```

### Q11（ok）

```sql
SELECT e.Year, e."Per capita GDP (yuan/person)" AS gdp_pc, w."Industrial Water Consumption (100 million m³)" AS ind_w, w."Total Water Consumption (100 million m³) " AS tot_w, ROUND(100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China' AND e.Year BETWEEN 2010 AND 2018 ORDER BY e.Year
```

### Q12（ok）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 0
```

### Q13（ok）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 12
```

### Q14（ok）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 24
```

### Q15（ok）

```sql
WITH base AS (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China'), prov AS (SELECT rn, AVG(y) AS avg_g, MAX(CASE WHEN yr=2003 THEN x END) AS s03, MAX(CASE WHEN yr=2010 THEN x END) AS s10, MAX(CASE WHEN yr=2018 THEN x END) AS s18 FROM base GROUP BY rn) SELECT CASE WHEN avg_g<15000 THEN 'low(<15k)' WHEN avg_g<25000 THEN 'mid(15-25k)' ELSE 'high(>25k)' END AS tier, COUNT(*) AS n, ROUND(AVG(s03),2) AS avg_s03, ROUND(AVG(s10),2) AS avg_s10, ROUND(AVG(s18),2) AS avg_s18, ROUND(AVG(s18-s03),2) AS avg_chg_pp FROM prov GROUP BY tier ORDER BY tier
```

### Q16（db_error）

```sql
SELECT CASE WHEN e.Year<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END AS phase, COUNT(*) AS n, ROUND((COUNT(*)*SUM(x*y)-SUM(x)*SUM(y))/(SQRT(COUNT(*)*SUM(x*x)-SUM(x)*SUM(x))*SQRT(COUNT(*)*SUM(y*y)-SUM(y)*SUM(y))),3) AS corr FROM (SELECT e.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China') t GROUP BY phase
```

### Q17（ok）

```sql
SELECT SUM("Total Water Consumption (100 million m³) ") AS prov_sum_tot, (SELECT "Total Water Consumption (100 million m³) " FROM sheet1 WHERE Year=2018 AND "Region Name"='China') AS china_tot FROM sheet1 WHERE Year=2018 AND "Region Name"!='China'
```

### Q18（ok）

```sql
SELECT CASE WHEN yr<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END AS phase, COUNT(*) AS n, ROUND((COUNT(*)*SUM(x*y)-SUM(x)*SUM(y))/(SQRT(COUNT(*)*SUM(x*x)-SUM(x)*SUM(x))*SQRT(COUNT(*)*SUM(y*y)-SUM(y)*SUM(y))),3) AS corr FROM (SELECT e.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China') t GROUP BY CASE WHEN yr<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END
```
