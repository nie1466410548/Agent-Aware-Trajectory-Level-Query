# dacomp-003-01：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10、Q11、Q18 |
| Q1 / 候选2 | 读取：sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q2、Q12、Q13、Q14、Q15 |
| Q2 / 候选1 | 读取：sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q12、Q13、Q14、Q15 |
| Q2 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10、Q11、Q18 |
| Q3 / 候选1 | 读取：economic_indicator_data.Region Name, economic_indicator_data.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：economic_indicator_data.Region Name<br>聚合：COUNT(*) | 列：Q10、Q11、Q18<br>分组：Q8<br>聚合：Q4、Q8、Q9、Q12、Q13、Q14、Q15、Q18 |
| Q3 / 候选2 | 读取：sheet1.Region Name, sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：Q4、Q12、Q13、Q14、Q15、Q17<br>分组：Q4、Q9、Q12、Q13、Q14、Q15<br>聚合：Q4、Q8、Q9、Q12、Q13、Q14、Q15、Q18 |
| Q4 / 候选1 | 读取：sheet1.Region Name, sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：Q12、Q13、Q14、Q15、Q17<br>分组：Q9、Q12、Q13、Q14、Q15<br>聚合：Q8、Q9、Q12、Q13、Q14、Q15、Q18 |
| Q4 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Name, economic_indicator_data.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10、Q11、Q18 |
| Q5 / 候选1 | 读取：<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） |  |
| Q5 / 候选2 | 读取：<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） |  |
| Q6 / 候选1 | 读取：<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） |  |
| Q6 / 候选2 | 读取：<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） |  |
| Q7 / 候选1 | 读取：economic_indicator_data.Region Name, economic_indicator_data.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：MIN(economic_indicator_data.Year)、MAX(economic_indicator_data.Year) | 列：Q10、Q11、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q8 / 候选1 | 读取：economic_indicator_data.Region Name<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q10、Q11、Q18 |
| Q9 / 候选1 | 读取：sheet1.Region Name<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q12、Q13、Q14、Q15、Q17 |
| Q10 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：economic_indicator_data.Region Name eq "China"<br>连接：inner：economic_indicator_data.Year=sheet1.Year 且 economic_indicator_data.Region Code=sheet1.Region Code<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q11、Q18<br>过滤：Q11、Q18<br>连接：Q11、Q12、Q13、Q14、Q15、Q18 |
| Q10 / 候选2 | 读取：sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Region Name<br>聚合：COUNT(*)、SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：Q12、Q13、Q14、Q15<br>分组：Q12、Q13、Q14、Q15<br>聚合：后续未找到全部所述项同时出现 |
| Q11 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：economic_indicator_data.Region Name eq "China"<br>连接：inner：economic_indicator_data.Year=sheet1.Year 且 economic_indicator_data.Region Code=sheet1.Region Code<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q18<br>过滤：Q18<br>连接：Q12、Q13、Q14、Q15、Q18 |
| Q11 / 候选2 | 读取：sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Region Name<br>聚合：COUNT(*)、SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：Q12、Q13、Q14、Q15<br>分组：Q12、Q13、Q14、Q15<br>聚合：后续未找到全部所述项同时出现 |
| Q12 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q13、Q14、Q15、Q17<br>连接：Q13、Q14、Q15、Q18<br>分组：Q13、Q14、Q15<br>聚合：Q13、Q14、Q15、Q18 |
| Q12 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：AVG(economic_indicator_data.Per capita GDP (yuan/person))、SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q13、Q14、Q15、Q18<br>分组：Q13、Q14、Q15<br>聚合：后续未找到全部所述项同时出现 |
| Q13 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q14、Q15、Q17<br>连接：Q14、Q15、Q18<br>分组：Q14、Q15<br>聚合：Q14、Q15、Q18 |
| Q13 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：AVG(economic_indicator_data.Per capita GDP (yuan/person))、SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q14、Q15、Q18<br>分组：Q14、Q15<br>聚合：后续未找到全部所述项同时出现 |
| Q14 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q15、Q17<br>连接：Q15、Q18<br>分组：Q15<br>聚合：Q15、Q18 |
| Q14 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：AVG(economic_indicator_data.Per capita GDP (yuan/person))、SUM(sheet1.Industrial Water Consumption (100 million m³))、SUM(sheet1.Total Water Consumption (100 million m³) ) | 列：后续未找到全部所述项同时出现<br>连接：Q15、Q18<br>分组：Q15<br>聚合：后续未找到全部所述项同时出现 |
| Q15 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Region Name ne "China"<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q17<br>连接：Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q18 |
| Q15 / 候选2 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：未提供（none）<br>连接：inner：sheet1.Year=economic_indicator_data.Year 且 sheet1.Region Code=economic_indicator_data.Region Code<br>分组：sheet1.Region Name<br>聚合：AVG(economic_indicator_data.Per capita GDP (yuan/person)) | 列：后续未找到全部所述项同时出现<br>连接：Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q16 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：economic_indicator_data.Region Name eq "China"<br>连接：inner：economic_indicator_data.Year=sheet1.Year 且 economic_indicator_data.Region Code=sheet1.Region Code<br>分组：未提供（none）<br>聚合：COUNT(*) | 列：Q18<br>过滤：Q18<br>连接：Q18<br>聚合：Q18 |
| Q17 / 候选1 | 读取：sheet1.Region Name, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：sheet1.Year eq 2018<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>聚合：Q18 |
| Q18 / 候选1 | 读取：economic_indicator_data.Per capita GDP (yuan/person), economic_indicator_data.Region Code, economic_indicator_data.Region Name, economic_indicator_data.Year, sheet1.Industrial Water Consumption (100 million m³), sheet1.Region Code, sheet1.Total Water Consumption (100 million m³) , sheet1.Year<br>过滤：economic_indicator_data.Region Name eq "China"<br>连接：inner：economic_indicator_data.Year=sheet1.Year 且 economic_indicator_data.Region Code=sheet1.Region Code<br>分组：未提供（none）<br>聚合：COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>连接：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT * FROM economic_indicator_data LIMIT 10
```

### Q2（成功）

```sql
SELECT * FROM sheet1 LIMIT 10
```

### Q3（成功）

```sql
SELECT "Region Name", COUNT(*) AS n, MIN(Year) AS min_year, MAX(Year) AS max_year FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q4（成功）

```sql
SELECT "Region Name", COUNT(*) AS n, MIN(Year) AS min_year, MAX(Year) AS max_year FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q5（成功）

```sql
SELECT DISTINCT "Region Name" FROM economic_indicator_data ORDER BY "Region Name"
```

### Q6（成功）

```sql
SELECT DISTINCT "Region Name" FROM sheet1 ORDER BY "Region Name"
```

### Q7（失败）

```sql
SELECT group_concat(DISTINCT "Region Name", ' | ') AS regions FROM economic_indicator_data
```

### Q8（成功）

```sql
SELECT "Region Name", COUNT(*) AS cnt FROM economic_indicator_data GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q9（成功）

```sql
SELECT "Region Name", COUNT(*) AS cnt FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

### Q10（成功）

```sql
SELECT e.Year, e."Per capita GDP (yuan/person)" AS gdp_pc, w."Industrial Water Consumption (100 million m³)" AS ind_w, w."Total Water Consumption (100 million m³) " AS tot_w, ROUND(100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China' AND e.Year BETWEEN 2000 AND 2009 ORDER BY e.Year
```

### Q11（成功）

```sql
SELECT e.Year, e."Per capita GDP (yuan/person)" AS gdp_pc, w."Industrial Water Consumption (100 million m³)" AS ind_w, w."Total Water Consumption (100 million m³) " AS tot_w, ROUND(100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) ", 2) AS ind_share_pct FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China' AND e.Year BETWEEN 2010 AND 2018 ORDER BY e.Year
```

### Q12（成功）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 0
```

### Q13（成功）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 12
```

### Q14（成功）

```sql
SELECT t.rn AS region, COUNT(*) AS n, ROUND(AVG(t.y),0) AS avg_gdp_pc, ROUND(MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS share_2003, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END),2) AS share_2018, ROUND(MAX(CASE WHEN t.yr=2018 THEN t.x END)-MAX(CASE WHEN t.yr=2003 THEN t.x END),2) AS chg_pp, ROUND((COUNT(*)*SUM(t.x*t.y)-SUM(t.x)*SUM(t.y))/(SQRT(COUNT(*)*SUM(t.x*t.x)-SUM(t.x)*SUM(t.x))*SQRT(COUNT(*)*SUM(t.y*t.y)-SUM(t.y)*SUM(t.y))),3) AS corr FROM (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China') t GROUP BY t.rn ORDER BY corr DESC LIMIT 12 OFFSET 24
```

### Q15（成功）

```sql
WITH base AS (SELECT w."Region Name" AS rn, w.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM sheet1 w JOIN economic_indicator_data e ON w.Year=e.Year AND w."Region Code"=e."Region Code" WHERE w."Region Name"!='China'), prov AS (SELECT rn, AVG(y) AS avg_g, MAX(CASE WHEN yr=2003 THEN x END) AS s03, MAX(CASE WHEN yr=2010 THEN x END) AS s10, MAX(CASE WHEN yr=2018 THEN x END) AS s18 FROM base GROUP BY rn) SELECT CASE WHEN avg_g<15000 THEN 'low(<15k)' WHEN avg_g<25000 THEN 'mid(15-25k)' ELSE 'high(>25k)' END AS tier, COUNT(*) AS n, ROUND(AVG(s03),2) AS avg_s03, ROUND(AVG(s10),2) AS avg_s10, ROUND(AVG(s18),2) AS avg_s18, ROUND(AVG(s18-s03),2) AS avg_chg_pp FROM prov GROUP BY tier ORDER BY tier
```

### Q16（失败）

```sql
SELECT CASE WHEN e.Year<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END AS phase, COUNT(*) AS n, ROUND((COUNT(*)*SUM(x*y)-SUM(x)*SUM(y))/(SQRT(COUNT(*)*SUM(x*x)-SUM(x)*SUM(x))*SQRT(COUNT(*)*SUM(y*y)-SUM(y)*SUM(y))),3) AS corr FROM (SELECT e.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China') t GROUP BY phase
```

### Q17（成功）

```sql
SELECT SUM("Total Water Consumption (100 million m³) ") AS prov_sum_tot, (SELECT "Total Water Consumption (100 million m³) " FROM sheet1 WHERE Year=2018 AND "Region Name"='China') AS china_tot FROM sheet1 WHERE Year=2018 AND "Region Name"!='China'
```

### Q18（成功）

```sql
SELECT CASE WHEN yr<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END AS phase, COUNT(*) AS n, ROUND((COUNT(*)*SUM(x*y)-SUM(x)*SUM(y))/(SQRT(COUNT(*)*SUM(x*x)-SUM(x)*SUM(x))*SQRT(COUNT(*)*SUM(y*y)-SUM(y)*SUM(y))),3) AS corr FROM (SELECT e.Year AS yr, 100.0*w."Industrial Water Consumption (100 million m³)"/w."Total Water Consumption (100 million m³) " AS x, e."Per capita GDP (yuan/person)" AS y FROM economic_indicator_data e JOIN sheet1 w ON e.Year=w.Year AND e."Region Code"=w."Region Code" WHERE e."Region Name"='China') t GROUP BY CASE WHEN yr<=2010 THEN 'phase1_2000-2010' ELSE 'phase2_2011-2018' END
```
