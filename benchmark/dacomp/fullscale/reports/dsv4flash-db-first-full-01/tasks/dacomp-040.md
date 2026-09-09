# dacomp-040

Based on the data for 2000, 2010, and 2020 in the tables, analyze from perspectives such a…

运行：已提交。官方未评分。全部 SQL 尝试/成功 62/58；数据 SQL 59/55；Python 11 次。

完整原题：

Based on the data for 2000, 2010, and 2020 in the tables, analyze from perspectives such as region, gender, age, etc., and summarize the key achievements of China's education over these 20 years, providing specific data support.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| 2000_cn_pop_6_up_age_sex_edu | 60 | 31 |
| 2000_cn_pop_6_up_age_sex_eduurb | 60 | 31 |
| 2000_cn_twn_pop_6_up_age_sex_ed | 60 | 31 |
| 2000_province_hh_pop_sex_ratio | 31 | 17 |
| 2000_town_prov_hh_pop_sex_rati | 31 | 17 |
| 2000_urban_prov_hh_pop_sex_rati | 31 | 17 |
| 2000_villa_prov_hh_pop_sex_rati | 31 | 17 |
| 2000cnpop6upagesexeduvillage | 60 | 31 |
| 2010_cn_city_pop_6_up_age_sex_e | 80 | 25 |
| 2010_cn_pop_6_up_age_sex_edu | 80 | 25 |
| 2010_cn_rural_6_up_age_sex_edu | 80 | 25 |
| 2010_cn_town_pop6up_agesexedu | 80 | 25 |
| 2010_region_hh_pop_sex_ratio | 31 | 17 |
| 2010_rural_region_hh_pop_sexrat | 31 | 17 |
| 2010_town_reg_hh_pop_sexratio | 31 | 17 |
| 2010_urban_region_hh_pop_sexrat | 31 | 17 |
| 2020_cn_city_pop_3_up_age_sex_e | 83 | 31 |
| 2020_cn_pop_3_up_age_sex_edu | 83 | 31 |
| 2020_cn_rural_pop_3up_agesexed | 83 | 31 |
| 2020_cn_town_pop_3up_agesexedu | 83 | 31 |
| 2020_region_hh_pop_sex_ratio | 31 | 17 |
| 2020_rural_reg_hh_pop_sexratio | 31 | 17 |
| 2020_town_reg_hh_pop_sexratio | 31 | 17 |
| 2020_urban_region_hh_pop_sexrat | 31 | 17 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：分别读取 2000/2010/2020 教育人口数据 → Python 对齐年龄和教育层级口径 → 汇总年龄、性别和地区比例 → 绘制长期变化。

数据库大小：352,256 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 60 | 0.966 |
| [S4/Q2](#s4) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 80 | 0.684 |
| [S5/Q3](#s5) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 83 | 0.732 |
| [S6/Q4](#s6) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 5 | 0.276 |
| [S7/Q5](#s7) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 5 | 0.237 |
| [S8/Q6](#s8) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 5 | 0.23 |
| [S9/Q7](#s9) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 8 | 0.291 |
| [S10/Q8](#s10) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 8 | 0.265 |
| [S11/Q9](#s11) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 8 | 0.293 |
| [S12/Q10](#s12) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 0 | 0.364 |
| [S13/Q11](#s13) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 0 | 0.354 |
| [S14/Q12](#s14) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 0 | 0.322 |
| [S15/Q13](#s15) | failed | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\"Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Postgraduate - Total\", ' ', '') AS INTEGER))"] | unknown | 未取得；调用总时长 0.177 ms |
| [S16/Q14](#s16) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")"] | 1 | 0.369 |
| [S17/Q15](#s17) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 3 and Over - Total\")", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Preschool - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)"] | 1 | 0.462 |
| [S19/Q16](#s19) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))"] | 1 | 0.457 |
| [S20/Q17](#s20) | success | ["\"2010_region_hh_pop_sex_ratio\""] | 0 / {} | [] | [] | 31 | 0.31 |
| [S21/Q18](#s21) | success | ["\"2020_region_hh_pop_sex_ratio\""] | 0 / {} | [] | [] | 31 | 0.306 |
| [S22/Q19](#s22) | success | ["\"2000_province_hh_pop_sex_ratio\""] | 0 / {} | [] | [] | 31 | 0.257 |
| [S23/Q20](#s23) | success | ["\"2000_cn_pop_6_up_age_sex_eduurb\"", "\"2000cnpop6upagesexeduvillage\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Population Aged 6 and Over - Total\")"] | 2 | 0.436 |
| [S24/Q21](#s24) | success | ["\"2010_cn_city_pop_6_up_age_sex_e\"", "\"2010_cn_rural_6_up_age_sex_edu\"", "\"2010_cn_town_pop6up_agesexedu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Population Aged 6 and Over - Total\")"] | 3 | 0.364 |
| [S25/Q22](#s25) | success | ["\"2020_cn_city_pop_3_up_age_sex_e\"", "\"2020_cn_rural_pop_3up_agesexed\"", "\"2020_cn_town_pop_3up_agesexedu\""] | 0 / {} | [] | ["SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)"] | 3 | 0.435 |
| [S26/Q23](#s26) | success | ["\"2000_cn_twn_pop_6_up_age_sex_ed\""] | 0 / {} | [] | [] | 3 | 0.288 |
| [S27/Q24](#s27) | success | ["\"2000_cn_twn_pop_6_up_age_sex_ed\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")"] | 1 | 0.448 |
| [S28/Q25](#s28) | failed | ["\"2000_cn_pop_6_up_age_sex_eduurb\"", "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "\"2000cnpop6upagesexeduvillage\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))"] | unknown | 未取得；调用总时长 0.124 ms |
| [S29/Q26](#s29) | failed | ["\"2010_cn_city_pop_6_up_age_sex_e\"", "\"2010_cn_rural_6_up_age_sex_edu\"", "\"2010_cn_town_pop6up_agesexedu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")"] | unknown | 未取得；调用总时长 0.114 ms |
| [S30/Q27](#s30) | failed | ["\"2020_cn_city_pop_3_up_age_sex_e\"", "\"2020_cn_rural_pop_3up_agesexed\"", "\"2020_cn_town_pop_3up_agesexedu\""] | 0 / {} | [] | ["SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)"] | unknown | 未取得；调用总时长 0.12 ms |
| [S31/Q28](#s31) | success | ["\"2000_cn_pop_6_up_age_sex_eduurb\"", "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "\"2000cnpop6upagesexeduvillage\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(CAST(REPLACE(\" Literacy Class - Total\", ' ', '') AS INTEGER))", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Vocational School - Total\")", "SUM(CAST(REPLACE(\"Junior College - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Total\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Postgraduate - Total\", ' ', '') AS INTEGER))"] | 3 | 0.744 |
| [S32/Q29](#s32) | success | ["\"2010_cn_city_pop_6_up_age_sex_e\"", "\"2010_cn_rural_6_up_age_sex_edu\"", "\"2010_cn_town_pop6up_agesexedu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")", "SUM(\"Population Aged 6 and Over - Total\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Primary School - Total\")", "SUM(\"Junior High School - Total\")", "SUM(\"Senior High School - Total\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Postgraduate - Total\")"] | 3 | 0.538 |
| [S33/Q30](#s33) | success | ["\"2020_cn_city_pop_3_up_age_sex_e\"", "\"2020_cn_rural_pop_3up_agesexed\"", "\"2020_cn_town_pop_3up_agesexedu\""] | 0 / {} | [] | ["SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"ever Attended School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Total\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Total\" ELSE 0 END)"] | 3 | 0.775 |
| [S34/Q31](#s34) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Male\")", "SUM(\"Population Aged 6 and Over - Female\")", "SUM(\"Never Attended School - Male\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Primary School - Male\")", "SUM(\"Primary School - Female\")", "SUM(\"Junior High School - Male\")", "SUM(\"Junior High School - Female\")", "SUM(\"Senior High School - Male\")", "SUM(\"Senior High School - Female\")", "SUM(\"Vocational School - Male\")", "SUM(\"Vocational School - Female\")", "SUM(CAST(REPLACE(\"Junior College - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Junior College - Female\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Female\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Postgraduate - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Postgraduate - Female\", ' ', '') AS INTEGER))"] | 1 | 0.529 |
| [S35/Q32](#s35) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Male\")", "SUM(\"Population Aged 6 and Over - Female\")", "SUM(\"Never Attended School - Male\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Primary School - Male\")", "SUM(\"Primary School - Female\")", "SUM(\"Junior High School - Male\")", "SUM(\"Junior High School - Female\")", "SUM(\"Senior High School - Male\")", "SUM(\"Senior High School - Female\")", "SUM(\"Junior College - Male\")", "SUM(\" Junior College - Female\")", "SUM(\"Undergraduate - Male\")", "SUM(\"Undergraduate - Female\")", "SUM(\"Postgraduate - Male\")", "SUM(\"Postgraduate - Female\")"] | 1 | 0.544 |
| [S36/Q33](#s36) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Never Attended School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Never Attended School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Female\" ELSE 0 END)"] | 1 | 0.61 |
| [S37/Q34](#s37) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Male\")", "SUM(\"Population Aged 6 and Over - Female\")", "SUM(\" Never Attended School - Male\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Primary School - Male\")", "SUM(\"Primary School - Female\")", "SUM(\"Junior High School - Male\")", "SUM(\"Junior High School - Female\")", "SUM(\"Senior High School - Male\")", "SUM(\"Senior High School - Female\")", "SUM(\"Vocational School - Male\")", "SUM(\"Vocational School - Female\")", "SUM(CAST(REPLACE(\"Junior College - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\" Junior College - Female\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Undergraduate - Female\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Postgraduate - Male\", ' ', '') AS INTEGER))", "SUM(CAST(REPLACE(\"Postgraduate - Female\", ' ', '') AS INTEGER))"] | 1 | 0.635 |
| [S38/Q35](#s38) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Male\")", "SUM(\"Population Aged 6 and Over - Female\")", "SUM(\"Never Attended School - Male\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Primary School - Male\")", "SUM(\"Primary School - Female\")", "SUM(\" Junior High School - Male\")", "SUM(\"Junior High School - Female\")", "SUM(\"Senior High School - Male\")", "SUM(\"Senior High School - Female\")", "SUM(\"Junior College - Male\")", "SUM(\" Junior College - Female\")", "SUM(\"Undergraduate - Male\")", "SUM(\"Undergraduate - Female\")", "SUM(\"Postgraduate - Male\")", "SUM(\"Postgraduate - Female\")"] | 1 | 0.439 |
| [S39/Q36](#s39) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Population Aged 3 and Over - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Never Attended School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Never Attended School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \" Primary School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Primary School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior High School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Senior High School - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Junior College - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Undergraduate - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \" Undergraduate - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Master's Degree - Female\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Male\" ELSE 0 END)", "SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN \"Doctoral Degree - Female\" ELSE 0 END)"] | 1 | 0.599 |
| [S40/Q37](#s40) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 1 | 0.367 |
| [S41/Q38](#s41) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 1 | 0.323 |
| [S42/Q39](#s42) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 1 | 0.318 |
| [S43/Q40](#s43) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | ["SUM(\"Population Aged 6 and Over - Male\")", "SUM(\"Population Aged 6 and Over - Female\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Primary School - Male\")", "SUM(\"Primary School - Female\")", "SUM(\"Junior High School - Male\")", "SUM(\"Junior High School - Female\")", "SUM(\"Senior High School - Male\")", "SUM(\"Senior High School - Female\")", "SUM(\"Vocational School - Male\")", "SUM(\"Vocational School - Female\")", "SUM(\"Junior College - Male\")", "SUM(\"Undergraduate - Male\")", "SUM(\"Undergraduate - Female\")", "SUM(\"Postgraduate - Male\")", "SUM(\"Postgraduate - Female\")", "SUM(\"Never Attended School - Total\")", "SUM(\"Never Attended School - Female\")", "SUM(\"Junior College - Total\")", "SUM(\"Undergraduate - Total\")", "SUM(\"Junior College - Male\")"] | 1 | 0.55 |
| [S44/Q41](#s44) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 60 | 0.727 |
| [S45/Q42](#s45) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 60 | 0.629 |
| [S46/Q43](#s46) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 80 | 0.633 |
| [S47/Q44](#s47) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 83 | 0.683 |
| [S48/Q45](#s48) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 60 | 0.611 |
| [S49/Q46](#s49) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 80 | 0.561 |
| [S50/Q47](#s50) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 83 | 0.582 |
| [S51/Q48](#s51) | success | ["\"2000_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 60 | 0.591 |
| [S52/Q49](#s52) | success | ["\"2010_cn_pop_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 80 | 0.513 |
| [S53/Q50](#s53) | success | ["\"2020_cn_pop_3_up_age_sex_edu\""] | 0 / {} | [] | [] | 83 | 0.569 |
| [S54/Q51](#s54) | success | ["\"2000_cn_pop_6_up_age_sex_eduurb\""] | 0 / {} | [] | [] | 60 | 0.651 |
| [S55/Q52](#s55) | success | ["\"2000_cn_twn_pop_6_up_age_sex_ed\""] | 0 / {} | [] | [] | 60 | 0.64 |
| [S56/Q53](#s56) | success | ["\"2000cnpop6upagesexeduvillage\""] | 0 / {} | [] | [] | 60 | 0.645 |
| [S57/Q54](#s57) | success | ["\"2010_cn_city_pop_6_up_age_sex_e\""] | 0 / {} | [] | [] | 80 | 0.577 |
| [S58/Q55](#s58) | success | ["\"2010_cn_town_pop6up_agesexedu\""] | 0 / {} | [] | [] | 80 | 0.584 |
| [S59/Q56](#s59) | success | ["\"2010_cn_rural_6_up_age_sex_edu\""] | 0 / {} | [] | [] | 80 | 0.597 |
| [S60/Q57](#s60) | success | ["\"2020_cn_city_pop_3_up_age_sex_e\""] | 0 / {} | [] | [] | 83 | 0.674 |
| [S61/Q58](#s61) | success | ["\"2020_cn_town_pop_3up_agesexedu\""] | 0 / {} | [] | [] | 83 | 0.663 |
| [S62/Q59](#s62) | success | ["\"2020_cn_rural_pop_3up_agesexed\""] | 0 / {} | [] | [] | 83 | 0.793 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S18 | metadata | success | PRAGMA table_info("2000_cn_pop_6_up_age_sex_edu") |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 主要读取不同年份人口教育表及少量总量。P4–P8 在 Python 中按年龄范围筛选、求各教育层级人口和性别总量、计算占比、再按年龄区间和地区循环汇总；这些可用 SQL WHERE、SUM、CASE 和 GROUP BY 完成。原轨迹没有 GROUP BY SQL，不把 Python 汇总虚构成 SQL。绘图另行允许。 [证据](../reviews/dacomp-040.json)。

P1：Inspect exact column names (including possible non-breaking spaces) using repr, since leading-space column aliases are returning 0. This metadata check informs correct SQL column references.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Load the small age-level tables (60-83 rows each) into pandas to handle non-breaking-space column names and text-to-integer conversions more reliably than SQL. The tables are small enough that this is not a large export — each row is one age group.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Load compact age-level census tables into pandas for careful handling of non-breaking-space column names and text-to-integer conversions, which is more reliable than SQL for these small tables.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Build a cleaned dataset from the small age-level census tables: handle \xa0 columns, convert text columns to numeric, and compute education distributions by year, gender, age group, and urbanicity. This cleaning/computation is done in Python because SQL column identifiers contain non-breaking spaces making them unreliable.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Compute comparable national education-attainment distributions across 2000/2010/2020 from the cleaned small tables, aggregating levels for comparability.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Compute national education attainment distributions across 2000/2010/2020 from cleaned small tables, aggregating levels for comparability. All in one cell to persist variables.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Compute gender-based education attainment distributions for each year from the cleaned small tables, handling the \xa0 column names.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Combined analysis: compute national distributions, gender breakdowns, age-group breakdowns, and urban/rural breakdowns for all three years in one cell to avoid variable persistence issues.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Create visualization figures for the Markdown report: national education distribution trends, gender gaps, age cohort progression, and urban/rural disparities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Check the actual location of saved figures to reference them correctly in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Compute final summary statistics for the report: higher-education counts/rates by gender, regional population shares, and key growth multiples.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S44", "S45", "S48", "S51"] | 3 | 60 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S46", "S49", "S52"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S47", "S50", "S53"] | 2 | 83 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S19", "S34", "S37", "S43"] | 3 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S16", "S35", "S38"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S17", "S36", "S39"] | 2 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：11/55 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-040.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S44](#s44), [S45](#s45), [S48](#s48), [S51](#s51) → 保留前序结果 S44 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S45 | True | True | exact_multiset |
| S48 | True | True | exact_multiset |
| S51 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S19](#s19), [S34](#s34), [S37](#s37), [S43](#s43) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT SUM("Population Aged 6 and Over - Total") AS __a0, SUM("Never Attended School - Total") AS __a1, SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) AS __a2, SUM("Primary School - Total") AS __a3, SUM("Junior High School - Total") AS __a4, SUM("Senior High School - Total") AS __a5, SUM("Vocational School - Total") AS __a6, SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) AS __a7, SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) AS __a8, SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) AS __a9, SUM("Population Aged 6 and Over - Male") AS __a10, SUM("Population Aged 6 and Over - Female") AS __a11, SUM("Never Attended School - Male") AS __a12, SUM("Never Attended School - Female") AS __a13, SUM("Primary School - Male") AS __a14, SUM("Primary School - Female") AS __a15, SUM("Junior High School - Male") AS __a16, SUM("Junior High School - Female") AS __a17, SUM("Senior High School - Male") AS __a18, SUM("Senior High School - Female") AS __a19, SUM("Vocational School - Male") AS __a20, SUM("Vocational School - Female") AS __a21, SUM(CAST(REPLACE("Junior College - Male", ' ', '') AS INTEGER)) AS __a22, SUM(CAST(REPLACE(" Junior College - Female", ' ', '') AS INTEGER)) AS __a23, SUM(CAST(REPLACE("Undergraduate - Male", ' ', '') AS INTEGER)) AS __a24, SUM(CAST(REPLACE("Undergraduate - Female", ' ', '') AS INTEGER)) AS __a25, SUM(CAST(REPLACE("Postgraduate - Male", ' ', '') AS INTEGER)) AS __a26, SUM(CAST(REPLACE("Postgraduate - Female", ' ', '') AS INTEGER)) AS __a27, SUM(" Never Attended School - Male") AS __a28, SUM(CAST(REPLACE(" Junior College - Female", ' ', '') AS INTEGER)) AS __a29, SUM("Junior College - Male") AS __a30, SUM("Undergraduate - Male") AS __a31, SUM("Undergraduate - Female") AS __a32, SUM("Postgraduate - Male") AS __a33, SUM("Postgraduate - Female") AS __a34, SUM("Junior College - Total") AS __a35, SUM("Undergraduate - Total") AS __a36 FROM "2000_cn_pop_6_up_age_sex_edu" 
```

受益查询 S19 的改写示例：

```sql
SELECT SUM(__a0) AS total_pop6, SUM(__a1) AS never_attended, SUM(__a2) AS literacy_class, SUM(__a3) AS primary_school, SUM(__a4) AS junior_high, SUM(__a5) AS senior_high, SUM(__a6) AS vocational, SUM(__a7) AS junior_college, SUM(__a8) AS undergraduate, SUM(__a9) AS postgraduate FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S47](#s47), [S50](#s50), [S53](#s53) → 保留前序结果 S47 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S50 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-040.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `e4d4a11705994ac9b5040f2b42ab504c`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `e4d4a11705994ac9b5040f2b42ab504c`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`3c4290cd6cbb3e86556c3102f2f964dcf1b552fda26567ca5c9f8013733c4d6d`。

## S3

类别 `data`；来源 `query_db`；调用 `2a3940dacae64ea8b7ff0db6e4f65250`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu" ORDER BY Age
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`979507a48d98a45ab7608a1b4e4b215dd6e4381231baa7abed2c688f461b96bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `4ec58d19342d4d1ba0882be47b3b2d30`；状态 `success`。

```sql
SELECT * FROM "2010_cn_pop_6_up_age_sex_edu" ORDER BY Age
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b5993fb070792c02d3b1528d38d4c15f4410aa2ad5287f430add7f8202abf8f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `8d2acf5f43654a63abf528fbc6290bfd`；状态 `success`。

```sql
SELECT * FROM "2020_cn_pop_3_up_age_sex_edu" ORDER BY Age
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`04a114fba01386d26959859c9a4d0f9967d6ca7badb4ca3671f2c6076e7dadf8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `90a1c00f7bc64b4fa1331c671359d680`；状态 `success`。

```sql
SELECT Age FROM "2000_cn_pop_6_up_age_sex_edu" LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`aa3694cc8f5b626e193186a8219abdbbf24d89442d449d2d627e1c9e9fccbee5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `a3526b2460794a73a110cd9ab46f2db1`；状态 `success`。

```sql
SELECT Age FROM "2010_cn_pop_6_up_age_sex_edu" LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`2e0d376dcfc7856ed46354d6ddecaa0fb507edbf65e4151aa3e33ff3bb327b52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `33812de31d98457daec064bdc7c56e90`；状态 `success`。

```sql
SELECT Age FROM "2020_cn_pop_3_up_age_sex_edu" LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`721a8c23024423b671aa6d78affb61b6f78c6e8f35e75117769d5fe16927671a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `d4cca324fa564280b3feb9b94112912c`；状态 `success`。

```sql
SELECT Age FROM "2000_cn_pop_6_up_age_sex_edu" ORDER BY rowid DESC LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7d3fe02feb3a59fb42c54229ea4cf07fe6854023466d19658743805f1a42ff32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "rowid", "reason": "ambiguous_or_missing_source"}]

## S10

类别 `data`；来源 `query_db`；调用 `2877d204d38c4bf3a62fd3849a99fe11`；状态 `success`。

```sql
SELECT Age FROM "2010_cn_pop_6_up_age_sex_edu" ORDER BY rowid DESC LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`4419aa8fa2f733b11153233a7c288655ad0270a2fc3ca3932d38eecc4f315484`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "rowid", "reason": "ambiguous_or_missing_source"}]

## S11

类别 `data`；来源 `query_db`；调用 `912cef740d6247f390d4e7a286616a11`；状态 `success`。

```sql
SELECT Age FROM "2020_cn_pop_3_up_age_sex_edu" ORDER BY rowid DESC LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`4419aa8fa2f733b11153233a7c288655ad0270a2fc3ca3932d38eecc4f315484`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "rowid", "reason": "ambiguous_or_missing_source"}]

## S12

类别 `data`；来源 `query_db`；调用 `8a1647ef80a04647bd203ee378be129d`；状态 `success`。

```sql
SELECT DISTINCT Age FROM "2000_cn_pop_6_up_age_sex_edu" WHERE Age LIKE '%otal%' OR Age LIKE '%otal%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `5a72d61df77441a995e0b2d0293df4ac`；状态 `success`。

```sql
SELECT DISTINCT Age FROM "2010_cn_pop_6_up_age_sex_edu" WHERE Age LIKE '%otal%' OR Age = 'Total'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `c504eed83a5d4e34891fa4321eb44b9a`；状态 `success`。

```sql
SELECT DISTINCT Age FROM "2020_cn_pop_3_up_age_sex_edu" WHERE Age LIKE '%otal%' OR Age = 'Total'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `ae9b80dcbddd4fc59b19eae145b86828`；状态 `failed`。

```sql
SELECT 
  SUM([Population Aged 6 and Over - Total]) AS total_pop6,
  SUM([Never Attended School - Total]) AS never_attended,
  SUM(CAST(REPLACE([Literacy Class - Total],' ','') AS INTEGER)) AS literacy_class,
  SUM([Primary School - Total]) AS primary_school,
  SUM([Junior High School - Total]) AS junior_high,
  SUM([Senior High School - Total]) AS senior_high,
  SUM([Vocational School - Total]) AS vocational,
  SUM(CAST(REPLACE([Junior College - Total],' ','') AS INTEGER)) AS junior_college,
  SUM(CAST(REPLACE([Undergraduate - Total],' ','') AS INTEGER)) AS undergraduate,
  SUM(CAST(REPLACE([Postgraduate - Total],' ','') AS INTEGER)) AS postgraduate
FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S15.parameters.json)。

错误：`OperationalError('no such column: Literacy Class - Total')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Literacy Class - Total", ' ', '') AS INTEGER)) | [{"unknown": "\"Literacy Class - Total\""}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Postgraduate - Total", ' ', '') AS INTEGER)) | [{"unknown": "\"Postgraduate - Total\""}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\"Literacy Class - Total\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Postgraduate - Total\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Literacy Class - Total\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Postgraduate - Total\"", "reason": "ambiguous_or_missing_source"}]

## S16

类别 `data`；来源 `query_db`；调用 `ceb40939d94c4e57baa7414274f28a61`；状态 `success`。

```sql
SELECT 
  SUM([Population Aged 6 and Over - Total]) AS total_pop6,
  SUM([Never Attended School - Total]) AS never_attended,
  SUM([Primary School - Total]) AS primary_school,
  SUM([Junior High School - Total]) AS junior_high,
  SUM([Senior High School - Total]) AS senior_high,
  SUM([Junior College - Total]) AS junior_college,
  SUM([Undergraduate - Total]) AS undergraduate,
  SUM([Postgraduate - Total]) AS postgraduate
FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`86c36a304e74321c89b8b7de6a5e01cc1bbf1de65bd812e86851bc64edaf173e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Junior College - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Total"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `71abd77f69324093b69cbcc6be6c19c8`；状态 `success`。

```sql
SELECT 
  SUM([Population Aged 3 and Over - Total]) AS total_pop3,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Population Aged 3 and Over - Total] ELSE 0 END) AS total_pop6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [ever Attended School - Total] ELSE 0 END) AS never_attended,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Preschool - Total] ELSE 0 END) AS preschool6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Primary School - Total] ELSE 0 END) AS primary_school,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Junior High School - Total] ELSE 0 END) AS junior_high,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Senior High School - Total] ELSE 0 END) AS senior_high,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Junior College - Total] ELSE 0 END) AS junior_college,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Undergraduate - Total] ELSE 0 END) AS undergraduate,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Master's Degree - Total] ELSE 0 END) AS masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN [Doctoral Degree - Total] ELSE 0 END) AS doctoral
FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`1fc8e1fb5ec8101053c3e09dff7373d7f6b77ad4ea721c14b644e05a7a3c984c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 3 and Over - Total") | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Total"}] | [] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Preschool - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Preschool - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |


## S18

类别 `metadata`；来源 `query_db`；调用 `32b96ba8525141c48d1510976a3fee2f`；状态 `success`。

```sql
PRAGMA table_info("2000_cn_pop_6_up_age_sex_edu")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f4011a046d1ffde1b700d9148ed332243edd1b636e6e349dfd89004940ae830b`。

## S19

类别 `data`；来源 `query_db`；调用 `986dbe82451c43a0a16277995001923a`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Total") AS total_pop6,
  SUM("Never Attended School - Total") AS never_attended,
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)) AS literacy_class,
  SUM("Primary School - Total") AS primary_school,
  SUM("Junior High School - Total") AS junior_high,
  SUM("Senior High School - Total") AS senior_high,
  SUM("Vocational School - Total") AS vocational,
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)) AS junior_college,
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)) AS undergraduate,
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER)) AS postgraduate
FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`b6d45b5366f285d76688ea143531cefc15ee668ebc868d34eac325a376690024`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": " Literacy Class - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": " Postgraduate - Total"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `bc27b47a469c4c2d8ba2de3dde39b378`；状态 `success`。

```sql
SELECT Region, "Total Population" FROM "2010_region_hh_pop_sex_ratio"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e344d3af401e2c1bf1996a9da51cb3d2aeabfab82cfc395d7c1687bc361fa405`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_region_hh_pop_sex_ratio", "kind": "base", "block": null, "base_tables": ["\"2010_region_hh_pop_sex_ratio\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `32df0015c600446fb155a71574f49c3d`；状态 `success`。

```sql
SELECT Region, "Total Population" FROM "2020_region_hh_pop_sex_ratio"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`d56603830ffe36b23793b49a2209fe670ab59cf2f3dc383136ed9f8226300339`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_region_hh_pop_sex_ratio", "kind": "base", "block": null, "base_tables": ["\"2020_region_hh_pop_sex_ratio\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `c602f87dab5544ccaaae3477c2da3549`；状态 `success`。

```sql
SELECT Province, "Total Population" FROM "2000_province_hh_pop_sex_ratio" LIMIT 35
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`040026f2c319a8c69d575410f9fd85a1b8738c67aaa98f33eb30ef524094c5bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_province_hh_pop_sex_ratio", "kind": "base", "block": null, "base_tables": ["\"2000_province_hh_pop_sex_ratio\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `8bcc4cbec58f40d3a850a6c14d162dfb`；状态 `success`。

```sql
SELECT 
  'urban' AS src, SUM("Population Aged 6 and Over - Total") AS pop6
FROM "2000_cn_pop_6_up_age_sex_eduurb"
UNION ALL
SELECT 'village', SUM("Population Aged 6 and Over - Total")
FROM "2000cnpop6upagesexeduvillage"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`b58df1c23b1e565e81e99b173f4d6fe6fbcd82cee15a7cb320f67dfd4fe5a49a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_eduurb", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_eduurb\""]}] | [] | [] |
| B2 | [{"alias": "2000cnpop6upagesexeduvillage", "kind": "base", "block": null, "base_tables": ["\"2000cnpop6upagesexeduvillage\""]}] | [] | [] |
| B3 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `3c2e47af322b483dbcc37b7de5e79106`；状态 `success`。

```sql
SELECT 
  'city' AS src, SUM("Population Aged 6 and Over - Total") AS pop6
FROM "2010_cn_city_pop_6_up_age_sex_e"
UNION ALL
SELECT 'town', SUM("Population Aged 6 and Over - Total")
FROM "2010_cn_town_pop6up_agesexedu"
UNION ALL
SELECT 'rural', SUM("Population Aged 6 and Over - Total")
FROM "2010_cn_rural_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`137914efb59677195c5971de4474926dac86d07caffe861d1ef647956ba3ae1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_city_pop_6_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2010_cn_city_pop_6_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2010_cn_town_pop6up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_town_pop6up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2010_cn_rural_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_rural_6_up_age_sex_edu\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B4 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `6ea13ba1079e43a19b934c602eabe972`；状态 `success`。

```sql
SELECT 
  'city' AS src, SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) AS pop6
FROM "2020_cn_city_pop_3_up_age_sex_e"
UNION ALL
SELECT 'town', SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END)
FROM "2020_cn_town_pop_3up_agesexedu"
UNION ALL
SELECT 'rural', SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END)
FROM "2020_cn_rural_pop_3up_agesexed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`71795c4d5b8da58e4f072e5cd4e479e5d51b8bcd4a0f2daa3fd169820f2b5740`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_city_pop_3_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2020_cn_city_pop_3_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2020_cn_town_pop_3up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_town_pop_3up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2020_cn_rural_pop_3up_agesexed", "kind": "base", "block": null, "base_tables": ["\"2020_cn_rural_pop_3up_agesexed\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `3749031ba5a546df92b6e1393fac6485`；状态 `success`。

```sql
SELECT Age, "Population Aged 6 and Over - Total" FROM "2000_cn_twn_pop_6_up_age_sex_ed" LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`44ccf3f513a9ed091ba882aae914a265eaa73257435e25686f55ff14a4cebc7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_twn_pop_6_up_age_sex_ed", "kind": "base", "block": null, "base_tables": ["\"2000_cn_twn_pop_6_up_age_sex_ed\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `346d3d3ed5704f27ac5c5b77ba404b72`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM("Primary School - Total") AS primary_school,
  SUM("Junior High School - Total") AS junior_high
FROM "2000_cn_twn_pop_6_up_age_sex_ed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`1a5f65556620c2e7bd7cdf03022f9226a80c3ddcee4f3062f64eba96b8d4bb70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_twn_pop_6_up_age_sex_ed", "kind": "base", "block": null, "base_tables": ["\"2000_cn_twn_pop_6_up_age_sex_ed\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Junior High School - Total"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `5861bfce3f634ff095b14694eba32700`；状态 `failed`。

```sql
SELECT 
  'urban' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)) AS literacy,
  SUM("Primary School - Total") AS primary,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Vocational School - Total") AS vocational,
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)) AS jcollege,
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)) AS undergrad,
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER)) AS postgrad
FROM "2000_cn_pop_6_up_age_sex_eduurb"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000_cn_twn_pop_6_up_age_sex_ed"
UNION ALL
SELECT 'village',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000cnpop6upagesexeduvillage"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('near "primary": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_eduurb", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_eduurb\""]}] | [] | [] |
| B2 | [{"alias": "2000_cn_twn_pop_6_up_age_sex_ed", "kind": "base", "block": null, "base_tables": ["\"2000_cn_twn_pop_6_up_age_sex_ed\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2000cnpop6upagesexeduvillage", "kind": "base", "block": null, "base_tables": ["\"2000cnpop6upagesexeduvillage\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": " Literacy Class - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Vocational School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": " Postgraduate - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Never Attended School - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": " Literacy Class - Total"}] | [] | False |
| B2 | SUM("Primary School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Primary School - Total"}] | [] | False |
| B2 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Junior High School - Total"}] | [] | False |
| B2 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Senior High School - Total"}] | [] | False |
| B2 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Vocational School - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Junior College - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Undergraduate - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": " Postgraduate - Total"}] | [] | False |
| B4 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B4 | SUM("Never Attended School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Never Attended School - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": " Literacy Class - Total"}] | [] | False |
| B4 | SUM("Primary School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Primary School - Total"}] | [] | False |
| B4 | SUM("Junior High School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Junior High School - Total"}] | [] | False |
| B4 | SUM("Senior High School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Senior High School - Total"}] | [] | False |
| B4 | SUM("Vocational School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Vocational School - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Junior College - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Undergraduate - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": " Postgraduate - Total"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `ff684ae399bf410b8f8504f62bdc2ba6`；状态 `failed`。

```sql
SELECT 
  'city' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM("Primary School - Total") AS primary,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Junior College - Total") AS jcollege,
  SUM("Undergraduate - Total") AS undergrad,
  SUM("Postgraduate - Total") AS postgrad
FROM "2010_cn_city_pop_6_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_town_pop6up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_rural_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S29.parameters.json)。

错误：`OperationalError('near "primary": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_city_pop_6_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2010_cn_city_pop_6_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2010_cn_town_pop6up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_town_pop6up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2010_cn_rural_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_rural_6_up_age_sex_edu\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Junior College - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Postgraduate - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Never Attended School - Total"}] | [] | False |
| B2 | SUM("Primary School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Primary School - Total"}] | [] | False |
| B2 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Junior High School - Total"}] | [] | False |
| B2 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Senior High School - Total"}] | [] | False |
| B2 | SUM("Junior College - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Junior College - Total"}] | [] | False |
| B2 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Undergraduate - Total"}] | [] | False |
| B2 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Postgraduate - Total"}] | [] | False |
| B4 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B4 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B4 | SUM("Primary School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Primary School - Total"}] | [] | False |
| B4 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [] | False |
| B4 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [] | False |
| B4 | SUM("Junior College - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B4 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B4 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Postgraduate - Total"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `6e31e2ad927548d5b8f5e49ababda1be`；状态 `failed`。

```sql
SELECT 
  'city' AS src,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) AS pop6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) AS never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) AS primary,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) AS junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) AS senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) AS jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) AS undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) AS masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) AS doctoral
FROM "2020_cn_city_pop_3_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_town_pop_3up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_rural_pop_3up_agesexed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S30.parameters.json)。

错误：`OperationalError('near "primary": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_city_pop_3_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2020_cn_city_pop_3_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2020_cn_town_pop_3up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_town_pop_3up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2020_cn_rural_pop_3up_agesexed", "kind": "base", "block": null, "base_tables": ["\"2020_cn_rural_pop_3up_agesexed\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |


## S31

类别 `data`；来源 `query_db`；调用 `5f3e024858b04e348af38101d01fd26c`；状态 `success`。

```sql
SELECT 
  'urban' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)) AS literacy,
  SUM("Primary School - Total") AS prim,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Vocational School - Total") AS vocational,
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)) AS jcollege,
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)) AS undergrad,
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER)) AS postgrad
FROM "2000_cn_pop_6_up_age_sex_eduurb"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000_cn_twn_pop_6_up_age_sex_ed"
UNION ALL
SELECT 'village',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM(CAST(REPLACE(" Literacy Class - Total",' ','') AS INTEGER)),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Vocational School - Total"),
  SUM(CAST(REPLACE("Junior College - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE("Undergraduate - Total",' ','') AS INTEGER)),
  SUM(CAST(REPLACE(" Postgraduate - Total",' ','') AS INTEGER))
FROM "2000cnpop6upagesexeduvillage"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`49d9657b42d0abff8c91dbf64f47d1deb547d230c5d92d24f84511856efc6604`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_eduurb", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_eduurb\""]}] | [] | [] |
| B2 | [{"alias": "2000_cn_twn_pop_6_up_age_sex_ed", "kind": "base", "block": null, "base_tables": ["\"2000_cn_twn_pop_6_up_age_sex_ed\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2000cnpop6upagesexeduvillage", "kind": "base", "block": null, "base_tables": ["\"2000cnpop6upagesexeduvillage\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": " Literacy Class - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Vocational School - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_eduurb\"", "column": " Postgraduate - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Never Attended School - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": " Literacy Class - Total"}] | [] | False |
| B2 | SUM("Primary School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Primary School - Total"}] | [] | False |
| B2 | SUM("Junior High School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Junior High School - Total"}] | [] | False |
| B2 | SUM("Senior High School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Senior High School - Total"}] | [] | False |
| B2 | SUM("Vocational School - Total") | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Vocational School - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Junior College - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": "Undergraduate - Total"}] | [] | False |
| B2 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_twn_pop_6_up_age_sex_ed\"", "column": " Postgraduate - Total"}] | [] | False |
| B4 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B4 | SUM("Never Attended School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Never Attended School - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE(" Literacy Class - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": " Literacy Class - Total"}] | [] | False |
| B4 | SUM("Primary School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Primary School - Total"}] | [] | False |
| B4 | SUM("Junior High School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Junior High School - Total"}] | [] | False |
| B4 | SUM("Senior High School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Senior High School - Total"}] | [] | False |
| B4 | SUM("Vocational School - Total") | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Vocational School - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE("Junior College - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Junior College - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE("Undergraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": "Undergraduate - Total"}] | [] | False |
| B4 | SUM(CAST(REPLACE(" Postgraduate - Total", ' ', '') AS INTEGER)) | [{"table": "\"2000cnpop6upagesexeduvillage\"", "column": " Postgraduate - Total"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `09813bbe229c422ebd7d7ae9ec70792c`；状态 `success`。

```sql
SELECT 
  'city' AS src,
  SUM("Population Aged 6 and Over - Total") AS pop6,
  SUM("Never Attended School - Total") AS never,
  SUM("Primary School - Total") AS prim,
  SUM("Junior High School - Total") AS junior,
  SUM("Senior High School - Total") AS senior,
  SUM("Junior College - Total") AS jcollege,
  SUM("Undergraduate - Total") AS undergrad,
  SUM("Postgraduate - Total") AS postgrad
FROM "2010_cn_city_pop_6_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_town_pop6up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM("Population Aged 6 and Over - Total"),
  SUM("Never Attended School - Total"),
  SUM("Primary School - Total"),
  SUM("Junior High School - Total"),
  SUM("Senior High School - Total"),
  SUM("Junior College - Total"),
  SUM("Undergraduate - Total"),
  SUM("Postgraduate - Total")
FROM "2010_cn_rural_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`98084569206b016d75dd9f1ccdefb487f6652308a4131481b98eb9a33a935bb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_city_pop_6_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2010_cn_city_pop_6_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2010_cn_town_pop6up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_town_pop6up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2010_cn_rural_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_rural_6_up_age_sex_edu\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM("Primary School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Primary School - Total"}] | [] | False |
| B1 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Junior High School - Total"}] | [] | False |
| B1 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Senior High School - Total"}] | [] | False |
| B1 | SUM("Junior College - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_city_pop_6_up_age_sex_e\"", "column": "Postgraduate - Total"}] | [] | False |
| B2 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B2 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Never Attended School - Total"}] | [] | False |
| B2 | SUM("Primary School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Primary School - Total"}] | [] | False |
| B2 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Junior High School - Total"}] | [] | False |
| B2 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Senior High School - Total"}] | [] | False |
| B2 | SUM("Junior College - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Junior College - Total"}] | [] | False |
| B2 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Undergraduate - Total"}] | [] | False |
| B2 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_town_pop6up_agesexedu\"", "column": "Postgraduate - Total"}] | [] | False |
| B4 | SUM("Population Aged 6 and Over - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Total"}] | [] | False |
| B4 | SUM("Never Attended School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B4 | SUM("Primary School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Primary School - Total"}] | [] | False |
| B4 | SUM("Junior High School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Junior High School - Total"}] | [] | False |
| B4 | SUM("Senior High School - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Senior High School - Total"}] | [] | False |
| B4 | SUM("Junior College - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B4 | SUM("Undergraduate - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B4 | SUM("Postgraduate - Total") | [{"table": "\"2010_cn_rural_6_up_age_sex_edu\"", "column": "Postgraduate - Total"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `3d50155de5a34c33a4e371b40023c55d`；状态 `success`。

```sql
SELECT 
  'city' AS src,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) AS pop6,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) AS never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) AS prim,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) AS junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) AS senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) AS jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) AS undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) AS masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) AS doctoral
FROM "2020_cn_city_pop_3_up_age_sex_e"
UNION ALL
SELECT 'town',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_town_pop_3up_agesexedu"
UNION ALL
SELECT 'rural',
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END),
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END)
FROM "2020_cn_rural_pop_3up_agesexed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`4c9dbac5ec738e2e774c7cc94b6a88d0e80d3533f04b291ea9d9e50480dcb972`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_city_pop_3_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2020_cn_city_pop_3_up_age_sex_e\""]}] | [] | [] |
| B2 | [{"alias": "2020_cn_town_pop_3up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_town_pop_3up_agesexedu\""]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "2020_cn_rural_pop_3up_agesexed", "kind": "base", "block": null, "base_tables": ["\"2020_cn_rural_pop_3up_agesexed\""]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_city_pop_3_up_age_sex_e\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B2 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_town_pop_3up_agesexedu\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Population Aged 3 and Over - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "ever Attended School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "ever Attended School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Primary School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Junior High School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Senior High School - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Junior College - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Undergraduate - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Master's Degree - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |
| B4 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Total" ELSE 0 END) | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Doctoral Degree - Total"}] | [{"table": "\"2020_cn_rural_pop_3up_agesexed\"", "column": "Age"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `7af3da88fc00450c9d59f9d5fef275fb`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM("Never Attended School - Male") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM("Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Vocational School - Male") AS male_voc,
  SUM("Vocational School - Female") AS female_voc,
  SUM(CAST(REPLACE("Junior College - Male",' ','') AS INTEGER)) AS male_jcollege,
  SUM(CAST(REPLACE(" Junior College - Female",' ','') AS INTEGER)) AS female_jcollege,
  SUM(CAST(REPLACE("Undergraduate - Male",' ','') AS INTEGER)) AS male_undergrad,
  SUM(CAST(REPLACE("Undergraduate - Female",' ','') AS INTEGER)) AS female_undergrad,
  SUM(CAST(REPLACE("Postgraduate - Male",' ','') AS INTEGER)) AS male_postgrad,
  SUM(CAST(REPLACE("Postgraduate - Female",' ','') AS INTEGER)) AS female_postgrad
FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`1b6fd0951c021d0173d92eaca32471492289f34e213f1d1cff6565dcba53d826`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Male"}] | [] | False |
| B1 | SUM("Population Aged 6 and Over - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Female"}] | [] | False |
| B1 | SUM("Never Attended School - Male") | [{"unknown": "\"Never Attended School - Male\""}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Primary School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Male"}] | [] | False |
| B1 | SUM("Primary School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Female"}] | [] | False |
| B1 | SUM("Junior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Male"}] | [] | False |
| B1 | SUM("Junior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [] | False |
| B1 | SUM("Senior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [] | False |
| B1 | SUM("Senior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [] | False |
| B1 | SUM("Vocational School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Male"}] | [] | False |
| B1 | SUM("Vocational School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Female"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Junior College - Female", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": " Junior College - Female"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Female", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Female"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Postgraduate - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Postgraduate - Female", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Female"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\"Never Attended School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Never Attended School - Male\"", "reason": "ambiguous_or_missing_source"}]

## S35

类别 `data`；来源 `query_db`；调用 `d1462c29970d451f8fcd8382693d410e`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM("Never Attended School - Male") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM("Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Junior College - Male") AS male_jcollege,
  SUM(" Junior College - Female") AS female_jcollege,
  SUM("Undergraduate - Male") AS male_undergrad,
  SUM("Undergraduate - Female") AS female_undergrad,
  SUM("Postgraduate - Male") AS male_postgrad,
  SUM("Postgraduate - Female") AS female_postgrad
FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`748c3d20208d46222dfbd8979c2ca6004e2df38e9d48a12ce4c3f1ed25302476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Male"}] | [] | False |
| B1 | SUM("Population Aged 6 and Over - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Female"}] | [] | False |
| B1 | SUM("Never Attended School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Male"}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Primary School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Male"}] | [] | False |
| B1 | SUM("Primary School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Female"}] | [] | False |
| B1 | SUM("Junior High School - Male") | [{"unknown": "\"Junior High School - Male\""}] | [] | False |
| B1 | SUM("Junior High School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [] | False |
| B1 | SUM("Senior High School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [] | False |
| B1 | SUM("Senior High School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [] | False |
| B1 | SUM("Junior College - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |
| B1 | SUM(" Junior College - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": " Junior College - Female"}] | [] | False |
| B1 | SUM("Undergraduate - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [] | False |
| B1 | SUM("Undergraduate - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Female"}] | [] | False |
| B1 | SUM("Postgraduate - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Male"}] | [] | False |
| B1 | SUM("Postgraduate - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Female"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\"Junior High School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Junior High School - Male\"", "reason": "ambiguous_or_missing_source"}]

## S36

类别 `data`；来源 `query_db`；调用 `a64631a77e784736b6b3ef07e2746e70`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Male" ELSE 0 END) AS male_pop,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Female" ELSE 0 END) AS female_pop,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Male" ELSE 0 END) AS male_never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Female" ELSE 0 END) AS female_never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Male" ELSE 0 END) AS male_prim,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Female" ELSE 0 END) AS female_prim,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Male" ELSE 0 END) AS male_junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Female" ELSE 0 END) AS female_junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Male" ELSE 0 END) AS male_senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Female" ELSE 0 END) AS female_senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Male" ELSE 0 END) AS male_jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Female" ELSE 0 END) AS female_jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Male" ELSE 0 END) AS male_undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Female" ELSE 0 END) AS female_undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Male" ELSE 0 END) AS male_masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Female" ELSE 0 END) AS female_masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Male" ELSE 0 END) AS male_doctoral,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Female" ELSE 0 END) AS female_doctoral
FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`070e23b99da57ec32b7737c6d8a6e40d6ef3dec360209bdfedcb3d2418369b11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Never Attended School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Male" ELSE 0 END) | [{"unknown": "\"Primary School - Male\""}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Primary School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior High School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior College - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior College - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Female" ELSE 0 END) | [{"unknown": "\"Undergraduate - Female\""}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Master's Degree - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Master's Degree - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Doctoral Degree - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Doctoral Degree - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |


未解析列血缘：[{"block": "B1", "column": "\"Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}]

## S37

类别 `data`；来源 `query_db`；调用 `5f80b04d0ace46f9a5643914e3ace2d4`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM(" Never Attended School - Male") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM("Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Vocational School - Male") AS male_voc,
  SUM("Vocational School - Female") AS female_voc,
  SUM(CAST(REPLACE("Junior College - Male",' ','') AS INTEGER)) AS male_jcollege,
  SUM(CAST(REPLACE(" Junior College - Female",' ','') AS INTEGER)) AS female_jcollege,
  SUM(CAST(REPLACE("Undergraduate - Male",' ','') AS INTEGER)) AS male_undergrad,
  SUM(CAST(REPLACE("Undergraduate - Female",' ','') AS INTEGER)) AS female_undergrad,
  SUM(CAST(REPLACE("Postgraduate - Male",' ','') AS INTEGER)) AS male_postgrad,
  SUM(CAST(REPLACE("Postgraduate - Female",' ','') AS INTEGER)) AS female_postgrad
FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`0e105935431090517db1adedba20476b7fe047ea54316f3dda6f1dac5a0633a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Male"}] | [] | False |
| B1 | SUM("Population Aged 6 and Over - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Female"}] | [] | False |
| B1 | SUM(" Never Attended School - Male") | [{"unknown": "\" Never Attended School - Male\""}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Primary School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Male"}] | [] | False |
| B1 | SUM("Primary School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Female"}] | [] | False |
| B1 | SUM("Junior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Male"}] | [] | False |
| B1 | SUM("Junior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [] | False |
| B1 | SUM("Senior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [] | False |
| B1 | SUM("Senior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [] | False |
| B1 | SUM("Vocational School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Male"}] | [] | False |
| B1 | SUM("Vocational School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Female"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Junior College - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE(" Junior College - Female", ' ', '') AS INTEGER)) | [{"unknown": "\" Junior College - Female\""}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Undergraduate - Female", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Female"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Postgraduate - Male", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Male"}] | [] | False |
| B1 | SUM(CAST(REPLACE("Postgraduate - Female", ' ', '') AS INTEGER)) | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Female"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\" Never Attended School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Junior College - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Never Attended School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Junior College - Female\"", "reason": "ambiguous_or_missing_source"}]

## S38

类别 `data`；来源 `query_db`；调用 `1908798b4ad445f1af5a2ac46d6eb666`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM("Never Attended School - Male") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM(" Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Junior College - Male") AS male_jcollege,
  SUM(" Junior College - Female") AS female_jcollege,
  SUM("Undergraduate - Male") AS male_undergrad,
  SUM("Undergraduate - Female") AS female_undergrad,
  SUM("Postgraduate - Male") AS male_postgrad,
  SUM("Postgraduate - Female") AS female_postgrad
FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`04141da71a53a5e814130efe4317298b812767ea67dff414f235098ca744127f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Male"}] | [] | False |
| B1 | SUM("Population Aged 6 and Over - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Female"}] | [] | False |
| B1 | SUM("Never Attended School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Male"}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Primary School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Male"}] | [] | False |
| B1 | SUM("Primary School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Female"}] | [] | False |
| B1 | SUM(" Junior High School - Male") | [{"unknown": "\" Junior High School - Male\""}] | [] | False |
| B1 | SUM("Junior High School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [] | False |
| B1 | SUM("Senior High School - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [] | False |
| B1 | SUM("Senior High School - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [] | False |
| B1 | SUM("Junior College - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |
| B1 | SUM(" Junior College - Female") | [{"unknown": "\" Junior College - Female\""}] | [] | False |
| B1 | SUM("Undergraduate - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [] | False |
| B1 | SUM("Undergraduate - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Female"}] | [] | False |
| B1 | SUM("Postgraduate - Male") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Male"}] | [] | False |
| B1 | SUM("Postgraduate - Female") | [{"table": "\"2010_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Female"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\" Junior High School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Junior College - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Junior High School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Junior College - Female\"", "reason": "ambiguous_or_missing_source"}]

## S39

类别 `data`；来源 `query_db`；调用 `c3ad313b07624aa38864a4a4a5da42c6`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Male" ELSE 0 END) AS male_pop,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Female" ELSE 0 END) AS female_pop,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Male" ELSE 0 END) AS male_never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Female" ELSE 0 END) AS female_never,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN " Primary School - Male" ELSE 0 END) AS male_prim,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Female" ELSE 0 END) AS female_prim,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Male" ELSE 0 END) AS male_junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Female" ELSE 0 END) AS female_junior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Male" ELSE 0 END) AS male_senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Female" ELSE 0 END) AS female_senior,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Male" ELSE 0 END) AS male_jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Female" ELSE 0 END) AS female_jcollege,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Male" ELSE 0 END) AS male_undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN " Undergraduate - Female" ELSE 0 END) AS female_undergrad,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Male" ELSE 0 END) AS male_masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Female" ELSE 0 END) AS female_masters,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Male" ELSE 0 END) AS male_doctoral,
  SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Female" ELSE 0 END) AS female_doctoral
FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`070e23b99da57ec32b7737c6d8a6e40d6ef3dec360209bdfedcb3d2418369b11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Population Aged 3 and Over - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Population Aged 3 and Over - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Never Attended School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Never Attended School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN " Primary School - Male" ELSE 0 END) | [{"unknown": "\" Primary School - Male\""}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Primary School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Primary School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior High School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior High School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Senior High School - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior College - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Junior College - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Junior College - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Undergraduate - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN " Undergraduate - Female" ELSE 0 END) | [{"unknown": "\" Undergraduate - Female\""}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Master's Degree - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Master's Degree - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Master's Degree - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Male" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Doctoral Degree - Male"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN CAST(Age AS INTEGER) >= 6 THEN "Doctoral Degree - Female" ELSE 0 END) | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Doctoral Degree - Female"}] | [{"table": "\"2020_cn_pop_3_up_age_sex_edu\"", "column": "Age"}] | False |


未解析列血缘：[{"block": "B1", "column": "\" Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Primary School - Male\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\" Undergraduate - Female\"", "reason": "ambiguous_or_missing_source"}]

## S40

类别 `data`；来源 `python`；调用 `fcdaeb71b2084f5aa50506df77069023`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu" LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`7767b3526ba8930cccc70b3409b6cec2d7dab8a7df137eb62649b2a08f7e3521`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `fcdaeb71b2084f5aa50506df77069023`；状态 `success`。

```sql
SELECT * FROM "2010_cn_pop_6_up_age_sex_edu" LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`4285c100775251cde8af0e7f287e39169b10e3ca17b127bd130f118cd983653d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `fcdaeb71b2084f5aa50506df77069023`；状态 `success`。

```sql
SELECT * FROM "2020_cn_pop_3_up_age_sex_edu" LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`fcda55067a6b53251007b1542ad47cf5674e8760d5d9c7d995e44e92206f066b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `5cbd0ae66e274073b18b391ca3e373b8`；状态 `success`。

```sql
SELECT 
  SUM("Population Aged 6 and Over - Male") AS male_pop,
  SUM("Population Aged 6 and Over - Female") AS female_pop,
  SUM("Never Attended School - Total") - SUM("Never Attended School - Female") AS male_never,
  SUM("Never Attended School - Female") AS female_never,
  SUM("Primary School - Male") AS male_prim,
  SUM("Primary School - Female") AS female_prim,
  SUM("Junior High School - Male") AS male_junior,
  SUM("Junior High School - Female") AS female_junior,
  SUM("Senior High School - Male") AS male_senior,
  SUM("Senior High School - Female") AS female_senior,
  SUM("Vocational School - Male") AS male_voc,
  SUM("Vocational School - Female") AS female_voc,
  SUM("Junior College - Male") AS male_jcollege,
  SUM("Undergraduate - Total") - SUM("Junior College - Male") - SUM("Junior College - Total") AS junk,
  SUM("Undergraduate - Male") AS male_undergrad,
  SUM("Undergraduate - Female") AS female_undergrad,
  SUM("Postgraduate - Male") AS male_postgrad,
  SUM("Postgraduate - Female") AS female_postgrad
FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`d2ea8741455ebbafcc9fe2acf878b5fa0e578ae76c1018256bb0b528edcb0bb0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Population Aged 6 and Over - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Male"}] | [] | False |
| B1 | SUM("Population Aged 6 and Over - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Population Aged 6 and Over - Female"}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Primary School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Male"}] | [] | False |
| B1 | SUM("Primary School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Primary School - Female"}] | [] | False |
| B1 | SUM("Junior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Male"}] | [] | False |
| B1 | SUM("Junior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior High School - Female"}] | [] | False |
| B1 | SUM("Senior High School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Male"}] | [] | False |
| B1 | SUM("Senior High School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Senior High School - Female"}] | [] | False |
| B1 | SUM("Vocational School - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Male"}] | [] | False |
| B1 | SUM("Vocational School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Vocational School - Female"}] | [] | False |
| B1 | SUM("Junior College - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |
| B1 | SUM("Undergraduate - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Male"}] | [] | False |
| B1 | SUM("Undergraduate - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Female"}] | [] | False |
| B1 | SUM("Postgraduate - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Male"}] | [] | False |
| B1 | SUM("Postgraduate - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Postgraduate - Female"}] | [] | False |
| B1 | SUM("Never Attended School - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Total"}] | [] | False |
| B1 | SUM("Never Attended School - Female") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Never Attended School - Female"}] | [] | False |
| B1 | SUM("Junior College - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Total"}] | [] | False |
| B1 | SUM("Undergraduate - Total") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Undergraduate - Total"}] | [] | False |
| B1 | SUM("Junior College - Male") | [{"table": "\"2000_cn_pop_6_up_age_sex_edu\"", "column": "Junior College - Male"}] | [] | False |


## S44

类别 `data`；来源 `python`；调用 `ba8f12fbdb4a4a3e88b5d69f62e313fd`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`db4623fac67690e3db405c8a106ed39117f9e0cedfaa00180fb395bf6b2cc5bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `391e01ff07294927ac9eba05a4102569`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`db4623fac67690e3db405c8a106ed39117f9e0cedfaa00180fb395bf6b2cc5bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `391e01ff07294927ac9eba05a4102569`；状态 `success`。

```sql
SELECT * FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`f01e6ec28e04ef166b51be19a8a70cc4d672202d368cc05005332a173447d6c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `391e01ff07294927ac9eba05a4102569`；状态 `success`。

```sql
SELECT * FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`8efebc414313adbc05983cde4c20412f88fe3090272fe2be3c2b7f9cefe67018`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `590a0fe35e8e47db8d46dc741f8cfb6d`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`db4623fac67690e3db405c8a106ed39117f9e0cedfaa00180fb395bf6b2cc5bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `590a0fe35e8e47db8d46dc741f8cfb6d`；状态 `success`。

```sql
SELECT * FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`f01e6ec28e04ef166b51be19a8a70cc4d672202d368cc05005332a173447d6c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `590a0fe35e8e47db8d46dc741f8cfb6d`；状态 `success`。

```sql
SELECT * FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`8efebc414313adbc05983cde4c20412f88fe3090272fe2be3c2b7f9cefe67018`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`db4623fac67690e3db405c8a106ed39117f9e0cedfaa00180fb395bf6b2cc5bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2010_cn_pop_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`f01e6ec28e04ef166b51be19a8a70cc4d672202d368cc05005332a173447d6c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_pop_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_pop_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2020_cn_pop_3_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`8efebc414313adbc05983cde4c20412f88fe3090272fe2be3c2b7f9cefe67018`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_pop_3_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_pop_3_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2000_cn_pop_6_up_age_sex_eduurb"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`14824d58299f2edbbdb10c102cd71c265526483ed372128849ec71ca946e5915`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_pop_6_up_age_sex_eduurb", "kind": "base", "block": null, "base_tables": ["\"2000_cn_pop_6_up_age_sex_eduurb\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2000_cn_twn_pop_6_up_age_sex_ed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`fd85d93c92d428dad26b7e47920e7ecb13bf5c1a5724444b61eff2f6b3186b13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000_cn_twn_pop_6_up_age_sex_ed", "kind": "base", "block": null, "base_tables": ["\"2000_cn_twn_pop_6_up_age_sex_ed\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2000cnpop6upagesexeduvillage"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`b1dec41fa0420d282ef22b2c0e9d1fdc2ccd8c262deb55197ae5e2b64a23716a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2000cnpop6upagesexeduvillage", "kind": "base", "block": null, "base_tables": ["\"2000cnpop6upagesexeduvillage\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2010_cn_city_pop_6_up_age_sex_e"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`bdec5623fa44aa458786fe3e8ee898d69101b41ca25a3c30f107221a5f26ba91`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_city_pop_6_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2010_cn_city_pop_6_up_age_sex_e\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2010_cn_town_pop6up_agesexedu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`5cde5a6eb03d4eb606421d7976fbeddc6d09f84061b3252a1f389d3e02791ebc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_town_pop6up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_town_pop6up_agesexedu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2010_cn_rural_6_up_age_sex_edu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`b75f08f9e74b732acc8f44cf1d9a8869f23b306928253a6baa962ac82e2dece6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2010_cn_rural_6_up_age_sex_edu", "kind": "base", "block": null, "base_tables": ["\"2010_cn_rural_6_up_age_sex_edu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2020_cn_city_pop_3_up_age_sex_e"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`d638520af60a21de551916d51a2bcb9b2884222a2091d2c14e3191b7ea9237ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_city_pop_3_up_age_sex_e", "kind": "base", "block": null, "base_tables": ["\"2020_cn_city_pop_3_up_age_sex_e\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2020_cn_town_pop_3up_agesexedu"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`f5f76f2889c5dd4144972cd25f27e4646b89195038bf2283fb462cfcebc1545e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_town_pop_3up_agesexedu", "kind": "base", "block": null, "base_tables": ["\"2020_cn_town_pop_3up_agesexedu\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `76bf6a11c09d42c4a6ccc4b4aca3f562`；状态 `success`。

```sql
SELECT * FROM "2020_cn_rural_pop_3up_agesexed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-040/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`743c11dbbcf3348224ce44d63b7fbcbe7a7bf521cff1a658c740901b72a8d83e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "2020_cn_rural_pop_3up_agesexed", "kind": "base", "block": null, "base_tables": ["\"2020_cn_rural_pop_3up_agesexed\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

