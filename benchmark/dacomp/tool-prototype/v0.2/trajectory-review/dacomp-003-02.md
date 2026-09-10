# dacomp-003-02：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Year<br>聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q1 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Region Name<br>聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q7 |
| Q2 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Year<br>聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q2 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Region Name<br>聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q7 |
| Q3 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Year<br>聚合：SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q3 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Region Name<br>聚合：AVG(sheet1.Industrial Water Consumption (100 million m³)) | 列：后续未找到全部所述项同时出现<br>连接：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：Q7、Q8、Q9、Q10<br>聚合：Q7 |
| Q4 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Year ＋ sheet1.Region Name<br>聚合：未提供（none） | 列：Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>过滤：Q6、Q7、Q8、Q9、Q10、Q11<br>连接：Q5、Q6、Q7、Q8、Q9、Q10、Q11<br>分组：Q8、Q9、Q10、Q11 |
| Q5 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Region Name<br>聚合：未提供（none） | 列：Q6、Q7、Q8、Q9、Q10、Q11<br>过滤：Q6、Q7、Q8、Q9、Q10、Q11<br>连接：Q6、Q7、Q8、Q9、Q10、Q11<br>分组：Q7、Q8、Q9、Q10 |
| Q5 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：sheet1.Year<br>聚合：未提供（none） | 列：Q6、Q7、Q8、Q9、Q10、Q11<br>连接：Q6、Q7、Q8、Q9、Q10、Q11<br>分组：后续未找到全部所述项同时出现 |
| Q6 | 没有候选：no_further_access | — |
| Q7 | 没有候选：no_further_access | — |
| Q8 | 没有候选：no_further_access | — |
| Q9 | 没有候选：no_further_access | — |
| Q10 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) <br>过滤：未提供（none）<br>连接：inner：sheet1.Region Code=economic_indicator_data.Region Code（只描述了部分）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Industrial Water Consumption (100 million m³))、AVG(sheet1.Total Water Consumption (100 million m³) ) | 列：Q11<br>连接：Q11<br>聚合：后续未找到全部所述项同时出现 |
| Q11 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT "Region Name", COUNT(*) AS n_rows, MIN("Year") AS min_year, MAX("Year") AS max_year FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q2（成功）

```sql
SELECT "Region Name", COUNT(*) AS n_rows, MIN("Year") AS min_year, MAX("Year") AS max_year FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q3（成功）

```sql
SELECT DISTINCT "Region Name" FROM sheet1 ORDER BY "Region Name"
```

### Q4（成功）

```sql
SELECT s."Year", s."Industrial Water Consumption (100 million m³)", s."Total Water Consumption (100 million m³) ", e."Per capita GDP (yuan/person)" FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" = 'China' ORDER BY s."Year"
```

### Q5（成功）

```sql
SELECT s."Year", ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct, ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" = 'China' ORDER BY s."Year"
```

### Q6（成功）

```sql
SELECT s."Region Name", s."Year", ROUND(100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct, ROUND(e."Per capita GDP (yuan/person)", 0) AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' ORDER BY s."Region Name", s."Year"
```

### Q7（成功）

```sql
SELECT s."Region Name", COUNT(*) AS n, ROUND(AVG(s."Industrial Water Consumption (100 million m³)") * 100.0 / AVG(s."Total Water Consumption (100 million m³) "), 2) AS avg_share, ROUND(AVG(e."Per capita GDP (yuan/person)"), 0) AS avg_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name" ORDER BY avg_share DESC
```

### Q8（成功）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year"), stats AS (SELECT "Region Name", COUNT(*) AS n, SUM(ind_share) AS sx, SUM(pc_gdp) AS sy, SUM(ind_share * pc_gdp) AS sxy, SUM(ind_share * ind_share) AS sx2, SUM(pc_gdp * pc_gdp) AS sy2 FROM main GROUP BY "Region Name") SELECT "Region Name", ROUND((n * sxy - sx * sy) / SQRT((n * sx2 - sx * sx) * (n * sy2 - sy * sy)), 4) AS corr_share_gdp, ROUND(sx/n, 2) AS avg_share FROM stats ORDER BY corr_share_gdp DESC
```

### Q9（成功）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT "Region Name", ROUND(MAX(CASE WHEN "Year" = (SELECT MIN("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_first, ROUND(MAX(CASE WHEN "Year" = (SELECT MAX("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN ind_share END), 2) AS share_last, ROUND(MAX(CASE WHEN "Year" = (SELECT MIN("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_first, ROUND(MAX(CASE WHEN "Year" = (SELECT MAX("Year") FROM main m2 WHERE m2."Region Name" = main."Region Name") THEN pc_gdp END), 0) AS gdp_last FROM main GROUP BY "Region Name" ORDER BY share_last DESC
```

### Q10（成功）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT "Region Name", "Year" AS peak_year, ROUND(ind_share, 2) AS peak_share FROM main WHERE ("Region Name", ind_share) IN (SELECT "Region Name", MAX(ind_share) FROM main GROUP BY "Region Name") ORDER BY "Region Name"
```

### Q11（成功）

```sql
WITH main AS (SELECT s."Region Name", s."Year", 100.0 * s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " AS ind_share, e."Per capita GDP (yuan/person)" AS pc_gdp FROM sheet1 s JOIN economic_indicator_data e ON s."Year" = e."Year" AND s."Region Code" = e."Region Code" WHERE s."Region Name" != 'China' GROUP BY s."Region Name", s."Year") SELECT m1."Region Name", ROUND(m1.ind_share, 2) AS share_2003, ROUND(m1.pc_gdp, 0) AS gdp_2003, ROUND(m2.ind_share, 2) AS share_2018, ROUND(m2.pc_gdp, 0) AS gdp_2018 FROM main m1 JOIN main m2 ON m1."Region Name" = m2."Region Name" WHERE m1."Year" = 2003 AND m2."Year" = 2018 ORDER BY gdp_2018 DESC
```
