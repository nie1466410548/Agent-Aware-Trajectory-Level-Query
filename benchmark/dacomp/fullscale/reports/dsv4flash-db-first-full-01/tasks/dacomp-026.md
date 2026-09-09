# dacomp-026

For the Level 5 disasters in the `disaster_events` table, identify the relevant records an…

运行：已提交。官方未评分。全部 SQL 尝试/成功 61/61；数据 SQL 59/59；Python 6 次。

完整原题：

For the Level 5 disasters in the `disaster_events` table, identify the relevant records and then systematically assess emergency response resource allocation effectiveness across the human resources (`human_resources` + `operations1`), financial resources (`financials1`), material supplies (`supplies1` + `distribution_hubs`), and transportation (`transportation1`) dimensions. Describe how the resource mix supports operational outcomes, highlight documented anchors (e.g., staffing ratios, ROI, delivery efficiency), and explain how your conclusions draw on the English schema terminology so that the assessment fully captures the quantified performance expectations for Level 5 events.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| beneficiaries_and_assessments | 999 | 10 |
| coordination_and_evaluation | 999 | 29 |
| disaster_events | 999 | 9 |
| distribution_hubs | 999 | 11 |
| environment_and_health | 999 | 13 |
| financials1 | 999 | 13 |
| human_resources | 999 | 4 |
| operations1 | 999 | 12 |
| supplies1 | 999 | 4 |
| transportation1 | 999 | 18 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：筛选 Level 5 灾害 → 多表关联人力、资金、物资、运输和运营指标 → 比较资源强度及交付结果 → Python 相关检验和图表，追加受益者反馈分析。

数据库大小：3,694,592 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["disaster_events"] | 0 / {} | [] | [] | 202 | 1.476 |
| [S4/Q2](#s4) | success | ["disaster_events"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.334 |
| [S5/Q3](#s5) | success | ["human_resources"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.527 |
| [S6/Q4](#s6) | success | ["operations1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.346 |
| [S7/Q5](#s7) | success | ["financials1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.301 |
| [S8/Q6](#s8) | success | ["supplies1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.466 |
| [S9/Q7](#s9) | success | ["distribution_hubs"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.288 |
| [S10/Q8](#s10) | success | ["transportation1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.327 |
| [S11/Q9](#s11) | success | ["human_resources"] | 0 / {} | [] | [] | 5 | 0.305 |
| [S12/Q10](#s12) | success | ["operations1"] | 0 / {} | [] | [] | 5 | 0.463 |
| [S13/Q11](#s13) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Severity Level\""] | ["COUNT(*)"] | 5 | 0.712 |
| [S14/Q12](#s14) | success | ["financials1"] | 0 / {} | [] | [] | 5 | 0.344 |
| [S15/Q13](#s15) | success | ["supplies1"] | 0 / {} | [] | [] | 5 | 0.317 |
| [S16/Q14](#s16) | success | ["distribution_hubs"] | 0 / {} | [] | [] | 5 | 0.299 |
| [S17/Q15](#s17) | success | ["transportation1"] | 0 / {} | [] | [] | 5 | 0.359 |
| [S18/Q16](#s18) | success | ["disaster_events", "distribution_hubs", "financials1", "human_resources", "operations1", "supplies1", "transportation1"] | 7 / {'LEFT': 6} | [] | ["COUNT(DISTINCT hr.\"Disaster Reference ID\")", "COUNT(DISTINCT op.\"Disaster Reference ID\")", "COUNT(DISTINCT fin.\"Disaster Reference ID\")", "COUNT(DISTINCT sup.\"Disaster Reference ID\")", "COUNT(DISTINCT hub.\"Disaster Event Reference ID\")", "COUNT(DISTINCT tr.\"Disaster Reference ID\")"] | 1 | 6.116 |
| [S19/Q17](#s19) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["op.\"Emergency Level\""] | ["COUNT(*)"] | 4 | 1.442 |
| [S20/Q18](#s20) | success | ["human_resources"] | 0 / {} | [] | [] | 3 | 0.347 |
| [S21/Q19](#s21) | success | ["supplies1"] | 0 / {} | [] | [] | 3 | 0.416 |
| [S22/Q20](#s22) | success | ["disaster_events", "human_resources"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN JSON_EXTRACT(\"Staffing\", '$.readiness.ppe_status') = 'Critical' THEN 1 ELSE 0 END)", "SUM(CASE WHEN JSON_EXTRACT(\"Staffing\", '$.readiness.ppe_status') = 'Adequate' THEN 1 ELSE 0 END)", "SUM(CASE WHEN JSON_EXTRACT(\"Staffing\", '$.readiness.ppe_status') = 'Limited' THEN 1 ELSE 0 END)", "SUM(CASE WHEN JSON_EXTRACT(\"Staffing\", '$.readiness.training_status') = 'Complete' THEN 1 ELSE 0 END)", "AVG(JSON_EXTRACT(\"Staffing\", '$.personnel.total'))", "AVG(JSON_EXTRACT(\"Staffing\", '$.personnel.medical'))", "AVG(JSON_EXTRACT(\"Staffing\", '$.personnel.security'))", "AVG(JSON_EXTRACT(\"Staffing\", '$.personnel.logistics'))", "AVG(JSON_EXTRACT(\"Staffing\", '$.personnel.volunteers'))", "AVG(JSON_EXTRACT(\"Staffing\", '$.readiness.availability_percent'))"] | 1 | 3.03 |
| [S23/Q21](#s23) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["\"Resource Allocation Status\""] | ["COUNT(*)"] | 3 | 1.506 |
| [S24/Q22](#s24) | success | ["disaster_events", "financials1"] | 2 / {'INNER': 1} | [] | ["SUM(CASE WHEN \"fundingstate\" = 'Adequate' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"fundingstate\" = 'Critical' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"fundingstate\" = 'Sufficient' THEN 1 ELSE 0 END)", "AVG(\"budgetallot(USD)\")", "AVG(\"fundsutilpct(%)\")", "AVG(\"costbene(USD)\")", "AVG(\"opscosts(USD)\")", "AVG(\"transportcosts(USD)\")", "AVG(\"storagecosts(USD)\")", "AVG(\"personnelcosts(USD)\")", "AVG(\"donorcommitments(USD)\")", "AVG(\"resourcegaps(USD)\")"] | 1 | 2.076 |
| [S25/Q23](#s25) | success | ["disaster_events", "supplies1"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.power.generators'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.power.fuel_liters'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.medical'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.shelter.units'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.shelter.blankets'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.essentials.food_tons'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.essentials.water_liters'))", "AVG(JSON_EXTRACT(\"Inventory resources\", '$.hygiene_kits'))"] | 1 | 2.62 |
| [S26/Q24](#s26) | success | ["disaster_events", "distribution_hubs"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Warehouse Status\" = 'Excellent' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Warehouse Status\" = 'Good' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Warehouse Status\" = 'Fair' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Warehouse Status\" = 'Poor' THEN 1 ELSE 0 END)", "AVG(\"Center Capacity (tons)\")", "AVG(\"Utilization (%)\")", "AVG(\"Storage Capacity (m³)\")", "AVG(\"Available Capacity (m³)\")", "AVG(\"Inventory Accuracy (%)\")", "AVG(\"Inventory Turnover Rate\")"] | 1 | 1.968 |
| [S27/Q25](#s27) | success | ["disaster_events", "transportation1"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Last-Mile Delivery Status\" = 'On Track' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Last-Mile Delivery Status\" = 'Delayed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Route Optimization Status\" = 'Optimized' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Maintenance Status\" = 'Up to Date' THEN 1 ELSE 0 END)", "AVG(\"Number of Vehicles\")", "AVG(\"Available Trucks\")", "AVG(\"Available Helicopters\")", "AVG(\"Available Ships\")", "AVG(\"Total Transport Volume (tons)\")", "AVG(\"Daily Transport Volume (tons)\")", "AVG(\"Number of Distribution Points\")", "AVG(\"Average Delivery Time\")", "AVG(\"Delivery Success Rate\")", "AVG(\"Fuel Consumption (L/km)\")", "AVG(\"Vehicle Failure Rate\")"] | 1 | 3.383 |
| [S28/Q26](#s28) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["\"Response Phase\""] | ["COUNT(*)"] | 4 | 1.563 |
| [S29/Q27](#s29) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["\"Operation Status\""] | ["COUNT(*)"] | 4 | 1.474 |
| [S30/Q28](#s30) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["\"Supply Flow Status\""] | ["COUNT(*)"] | 3 | 1.404 |
| [S31/Q29](#s31) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["\"Priority\""] | ["COUNT(*)"] | 4 | 1.459 |
| [S32/Q30](#s32) | success | ["disaster_events", "distribution_hubs", "financials1", "human_resources", "transportation1"] | 5 / {'LEFT': 4} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["COUNT(*)", "AVG(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'))", "AVG(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.volunteers'))", "AVG(JSON_EXTRACT(hr.\"Staffing\", '$.readiness.availability_percent'))", "AVG(fin.\"budgetallot(USD)\")", "AVG(fin.\"fundsutilpct(%)\")", "AVG(fin.\"costbene(USD)\")", "AVG(fin.\"resourcegaps(USD)\")", "AVG(hub.\"Center Capacity (tons)\")", "AVG(hub.\"Utilization (%)\")", "AVG(tr.\"Delivery Success Rate\")", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN JSON_EXTRACT(hr.\"Staffing\", '$.readiness.ppe_status') = 'Critical' THEN 1 ELSE 0 END)", "SUM(CASE WHEN JSON_EXTRACT(hr.\"Staffing\", '$.readiness.training_status') = 'Complete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN fin.\"fundingstate\" = 'Critical' THEN 1 ELSE 0 END)", "SUM(CASE WHEN tr.\"Last-Mile Delivery Status\" = 'Delayed' THEN 1 ELSE 0 END)"] | 2 | 10.082 |
| [S33/Q31](#s33) | success | ["disaster_events"] | 0 / {} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["COUNT(*)", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected'))", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.displaced'))", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.injured'))", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.casualties'))", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.infrastructure.damage_percent'))", "AVG(JSON_EXTRACT(de.\"Impact Indicator\", '$.infrastructure.power_outage_percent'))"] | 2 | 3.176 |
| [S34/Q32](#s34) | success | ["disaster_events", "financials1", "human_resources", "supplies1", "transportation1"] | 5 / {'LEFT': 4} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(fin.\"budgetallot(USD)\", 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.displaced') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.shelter.units'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.essentials.food_tons'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.injured') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.medical'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(tr.\"Total Transport Volume (tons)\", 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(tr.\"Number of Distribution Points\", 0))"] | 2 | 13.386 |
| [S35/Q33](#s35) | success | ["disaster_events", "financials1", "human_resources", "transportation1"] | 4 / {'LEFT': 3} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["AVG(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.medical') * 1.0 / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0) * 100)", "AVG(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.volunteers') * 1.0 / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.injured') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.medical'), 0))", "AVG(fin.\"costbene(USD)\" * 1.0 / NULLIF(fin.\"budgetallot(USD)\", 0))", "AVG((fin.\"transportcosts(USD)\" + fin.\"storagecosts(USD)\" + fin.\"personnelcosts(USD)\" + fin.\"opscosts(USD)\") * 1.0 / NULLIF(fin.\"budgetallot(USD)\", 0) * 100)", "AVG(tr.\"Average Delivery Time\")", "AVG(tr.\"Delivery Success Rate\")", "AVG(tr.\"Daily Transport Volume (tons)\" * 1.0 / NULLIF(tr.\"Number of Vehicles\", 0))"] | 2 | 10.181 |
| [S36/Q34](#s36) | success | ["disaster_events", "supplies1", "transportation1"] | 3 / {'LEFT': 2} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(tr.\"Number of Distribution Points\", 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(tr.\"Daily Transport Volume (tons)\", 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.displaced') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.shelter.blankets'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.hygiene_kits'), 0))", "AVG(CAST(JSON_EXTRACT(de.\"Impact Indicator\", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup.\"Inventory resources\", '$.essentials.water_liters'), 0))"] | 2 | 7.885 |
| [S37/Q35](#s37) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Type\""] | ["COUNT(*)"] | 5 | 0.691 |
| [S38/Q36](#s38) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["op.\"Resource Allocation Status\"", "op.\"Supply Flow Status\""] | ["COUNT(*)"] | 9 | 1.725 |
| [S39/Q37](#s39) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["op.\"Emergency Level\""] | ["COUNT(*)", "AVG(op.\"Estimated Duration (days)\")"] | 4 | 1.507 |
| [S40/Q38](#s40) | success | ["disaster_events", "operations1"] | 2 / {'INNER': 1} | ["de.\"Disaster Severity Level\"", "op.\"Emergency Level\""] | ["COUNT(*)"] | 20 | 2.168 |
| [S41/Q39](#s41) | success | ["disaster_events", "distribution_hubs", "financials1", "operations1", "transportation1"] | 5 / {'INNER': 1, 'LEFT': 3} | ["op.\"Resource Allocation Status\""] | ["AVG(tr.\"Delivery Success Rate\")", "AVG(tr.\"Average Delivery Time\")", "AVG(hub.\"Utilization (%)\")", "AVG(fin.\"fundsutilpct(%)\")"] | 3 | 4.263 |
| [S42/Q40](#s42) | success | ["disaster_events", "distribution_hubs", "financials1", "human_resources", "supplies1", "transportation1"] | 6 / {'LEFT': 5} | [] | [] | 202 | 8.664 |
| [S43/Q41](#s43) | success | ["disaster_events", "distribution_hubs", "financials1", "transportation1"] | 5 / {'INNER': 1, 'CROSS': 1, 'LEFT': 2} | [] | ["MIN(\"costbene(USD)\")", "MAX(\"costbene(USD)\")", "MIN(\"fundsutilpct(%)\")", "MAX(\"fundsutilpct(%)\")", "MIN(\"Delivery Success Rate\")", "MAX(\"Delivery Success Rate\")", "MIN(\"Average Delivery Time\")", "MAX(\"Average Delivery Time\")", "MIN(\"Center Capacity (tons)\")", "MAX(\"Center Capacity (tons)\")", "MIN(\"Utilization (%)\")", "MAX(\"Utilization (%)\")", "AVG(\"costbene(USD)\")"] | 1 | 3.706 |
| [S44/Q42](#s44) | success | ["disaster_events", "distribution_hubs"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Inventory Accuracy (%)\" >= 95 THEN 1 ELSE 0 END)", "AVG(\"Inventory Accuracy (%)\")", "AVG(\"Available Capacity (m³)\")", "AVG(\"Cold Storage Capacity (m³)\")", "AVG(\"Cold Storage Temperature (℃)\")"] | 1 | 1.656 |
| [S45/Q43](#s45) | success | ["disaster_events", "transportation1"] | 2 / {'INNER': 1} | ["\"Route Optimization Status\""] | ["COUNT(*)", "AVG(\"Delivery Success Rate\")", "AVG(\"Average Delivery Time\")"] | 3 | 1.695 |
| [S46/Q44](#s46) | success | ["disaster_events", "transportation1"] | 2 / {'INNER': 1} | ["\"Last-Mile Delivery Status\""] | ["COUNT(*)"] | 3 | 1.548 |
| [S47/Q45](#s47) | success | ["disaster_events", "financials1"] | 2 / {'INNER': 1} | ["\"fundingstate\""] | ["COUNT(*)"] | 3 | 1.374 |
| [S48/Q46](#s48) | success | ["disaster_events", "distribution_hubs"] | 2 / {'INNER': 1} | ["\"Warehouse Status\""] | ["COUNT(*)", "AVG(\"Utilization (%)\")", "AVG(\"Inventory Accuracy (%)\")"] | 4 | 1.688 |
| [S49/Q47](#s49) | success | ["disaster_events", "financials1"] | 2 / {'INNER': 1} | [] | ["MIN(\"costbene(USD)\")", "MAX(\"costbene(USD)\")", "AVG(\"costbene(USD)\")", "AVG(\"costbene(USD)\" * 1.0 / NULLIF(\"budgetallot(USD)\", 0))"] | 1 | 1.508 |
| [S50/Q48](#s50) | success | ["disaster_events", "human_resources"] | 2 / {'INNER': 1} | [] | ["AVG(CAST(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.medical') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0) * 100)", "AVG(CAST(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.logistics') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0) * 100)", "AVG(CAST(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.security') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0) * 100)", "AVG(CAST(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.volunteers') AS REAL) / NULLIF(JSON_EXTRACT(hr.\"Staffing\", '$.personnel.total'), 0))"] | 1 | 2.763 |
| [S51/Q49](#s51) | success | ["disaster_events", "financials1", "transportation1"] | 3 / {'LEFT': 2} | ["\"Disaster Type\""] | ["COUNT(*)", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.population.affected'))", "AVG(fin.\"budgetallot(USD)\")", "AVG(fin.\"fundsutilpct(%)\")", "AVG(tr.\"Delivery Success Rate\")", "AVG(tr.\"Average Delivery Time\")", "AVG(tr.\"Daily Transport Volume (tons)\")"] | 5 | 2.882 |
| [S52/Q50](#s52) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 3 | 0.441 |
| [S53/Q51](#s53) | success | ["coordination_and_evaluation", "disaster_events"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN \"compliancestate\" = 'Compliant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"auditstate\" = 'Passed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"lessonsrecorded\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"bestpracticeslisted\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"improvementrecs\" > 0 THEN 1 ELSE 0 END)", "AVG(\"partnerorgs\")", "AVG(\"reportcompliance\")", "AVG(\"dataqualityvalue\")", "AVG(\"stakeholdersatisf\")", "AVG(\"publicperception\")", "AVG(\"Secincident Count\")"] | 1 | 2.087 |
| [S54/Q52](#s54) | success | ["coordination_and_evaluation", "disaster_events", "operations1"] | 3 / {'INNER': 2} | [] | ["COUNT(*)", "SUM(CASE WHEN ce.\"compliancestate\" = 'Compliant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ce.\"auditstate\" = 'Passed' THEN 1 ELSE 0 END)", "AVG(ce.\"partnerorgs\")", "AVG(ce.\"reportcompliance\")", "AVG(ce.\"dataqualityvalue\")", "AVG(ce.\"stakeholdersatisf\")", "AVG(ce.\"publicperception\")", "AVG(ce.\"Secincident Count\")", "AVG(ce.\"lessonsrecorded\")", "AVG(ce.\"bestpracticeslisted\")", "AVG(ce.\"improvementrecs\")"] | 1 | 3.031 |
| [S55/Q53](#s55) | success | ["coordination_and_evaluation", "disaster_events", "operations1"] | 3 / {'INNER': 2} | ["\"auditstate\""] | ["COUNT(*)"] | 3 | 2.362 |
| [S56/Q54](#s56) | success | ["beneficiaries_and_assessments", "disaster_events"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Needs Assessment Status\" = 'Complete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Vulnerability Assessment\" = 'Complete' THEN 1 ELSE 0 END)", "AVG(\"Distribution Equity Index\")", "AVG(\"Affected Population Feedback Score\")"] | 1 | 1.006 |
| [S57/Q55](#s57) | success | ["beneficiaries_and_assessments", "disaster_events"] | 2 / {'INNER': 1} | [] | [] | 5 | 1.086 |
| [S58/Q56](#s58) | success | ["beneficiaries_and_assessments", "disaster_events"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN ba.\"Needs Assessment Status\" = 'Complete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ba.\"Vulnerability Assessment\" = 'Complete' THEN 1 ELSE 0 END)", "AVG(ba.\"Distribution Equity Index\")", "AVG(ba.\"Affected Population Feedback Score\")"] | 1 | 1.831 |
| [S59/Q57](#s59) | success | ["disaster_events", "supplies1", "transportation1"] | 3 / {'LEFT': 2} | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] | ["AVG(JSON_EXTRACT(sup.\"Inventory resources\", '$.power.generators'))", "AVG(JSON_EXTRACT(sup.\"Inventory resources\", '$.medical'))", "AVG(JSON_EXTRACT(sup.\"Inventory resources\", '$.shelter.units'))", "AVG(JSON_EXTRACT(sup.\"Inventory resources\", '$.essentials.food_tons'))", "AVG(JSON_EXTRACT(sup.\"Inventory resources\", '$.essentials.water_liters'))", "AVG(tr.\"Total Transport Volume (tons)\")", "AVG(tr.\"Daily Transport Volume (tons)\")", "AVG(tr.\"Number of Vehicles\")", "AVG(tr.\"Number of Distribution Points\")", "AVG(tr.\"Average Delivery Time\")", "AVG(tr.\"Delivery Success Rate\")", "AVG(tr.\"Vehicle Failure Rate\")"] | 2 | 6.72 |
| [S60/Q58](#s60) | success | ["beneficiaries_and_assessments", "disaster_events"] | 2 / {'LEFT': 1} | [] | [] | 202 | 1.649 |
| [S61/Q59](#s61) | success | ["beneficiaries_and_assessments", "disaster_events"] | 2 / {'LEFT': 1} | ["de.\"Disaster Severity Level\""] | ["AVG(ba.\"Distribution Equity Index\")", "AVG(ba.\"Affected Population Feedback Score\")"] | 5 | 2.136 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL performs multi-table disaster/resource joins, JSON extraction and many resource summaries. Python computes correlations and figures, which are reasonable supplements. P1 additionally extracts inventory JSON keys and computes allocation ratios, P4 selects top/bottom delivery events, and P5 merges outcome rows in pandas. SQLite JSON functions/joins/arithmetic/Top-K can reasonably perform these preparation steps. [证据](../reviews/dacomp-026.json)。

P1：Compute correlations between resource inputs and operational outcomes for Level 5 events, and produce visualization data. Correlation/significance testing is a statistical procedure not reasonably supported by SQLite, so the joined Level 5 rows are pulled via the logged db.query interface and analyzed with scipy/matplotlib.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P2：Create visualizations comparing Level 5 vs non-Level 5 resource intensity metrics and Level 5 operational status distributions, which are best done as matplotlib bar charts and pie charts in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Correct Figure 2 because Last-Mile Delivery Status has three distinct values (On Track=64, Delayed=73, Suspended=65) and funding state has Adequate/Critical/Limited, not the values assumed earlier. Regenerating the pie charts with the verified SQL distributions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Examine the costbene(USD) field to understand its meaning (ratio vs absolute value) by computing correlations with budget and affected population, and check distribution shape. This statistical exploration is easier in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Assess whether better-resourced Level 5 events achieve better beneficiary-level outcomes (delivery success, distribution equity, feedback) using correlations in Python, since multi-column correlation testing is a statistical step beyond SQL aggregation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P6：Verify the created figures exist in the workspace so they can be referenced in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common filtered view | False | ["S3", "S37"] | 1 | 202 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S13", "S33"] | 2 | 5 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：5/59 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-026.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S13](#s13), [S33](#s33) → 新增共享状态 C2 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Disaster Severity Level" AS __g0, CASE WHEN "Disaster Severity Level" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS __g1, COUNT(*) AS __a0, SUM(JSON_EXTRACT("Impact Indicator", '$.population.affected')) AS __a1_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.affected')) AS __a1_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.displaced')) AS __a2_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.displaced')) AS __a2_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.injured')) AS __a3_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.injured')) AS __a3_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.casualties')) AS __a4_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.casualties')) AS __a4_n, SUM(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) AS __a5_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) AS __a5_n, SUM(JSON_EXTRACT("Impact Indicator", '$.infrastructure.power_outage_percent')) AS __a6_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.infrastructure.power_outage_percent')) AS __a6_n FROM "disaster_events"  GROUP BY "Disaster Severity Level", CASE WHEN "Disaster Severity Level" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S33 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S3](#s3), [S37](#s37) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "disaster_events" WHERE "Disaster Severity Level" = 'Level 5'
```

受益查询 S3 的改写示例：

```sql
SELECT * FROM temp.reuse_candidate AS disaster_events WHERE "Disaster Severity Level" = 'Level 5'
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-026.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `0f6712817d59484088d5f8682a3cb644`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `0f6712817d59484088d5f8682a3cb644`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`53bf96c8af352fb7ce5000649b38b7b8c6a296e71b5224af9f2c74b9287e55ad`。

## S3

类别 `data`；来源 `query_db`；调用 `cec51a54f62246579d1828e9add0b717`；状态 `success`。

```sql
SELECT * FROM disaster_events WHERE "Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`0d3ec3854de37d58431b983b016894095a70543d05ffab67396ce0f51b433c99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `a68c06c66b93458dbe5b33ee10e0bbf1`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM disaster_events
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM human_resources;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "human_resources", "kind": "base", "block": null, "base_tables": ["human_resources"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
 SELECT COUNT(*) AS n FROM operations1;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "operations1", "kind": "base", "block": null, "base_tables": ["operations1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
 SELECT COUNT(*) AS n FROM financials1;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "financials1", "kind": "base", "block": null, "base_tables": ["financials1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
 SELECT COUNT(*) AS n FROM supplies1;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "supplies1", "kind": "base", "block": null, "base_tables": ["supplies1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
 SELECT COUNT(*) AS n FROM distribution_hubs;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "distribution_hubs", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `56febc7c36af4d9f8c102474155f68df`；状态 `success`。

```sql
 SELECT COUNT(*) AS n FROM transportation1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transportation1", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `d045c0d752144789b8ddba5d6530184e`；状态 `success`。

```sql
SELECT * FROM human_resources LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`543ed45421bcfac213ae32740cac2070de0826505ad237bfa8bee3709d009670`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "human_resources", "kind": "base", "block": null, "base_tables": ["human_resources"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `ef1b368986c04f4eb5c34f08defe980a`；状态 `success`。

```sql
SELECT * FROM operations1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`5a5dd05980693d6328d1dd2a51a6a8936208b42951837a2f55456bf33e54235c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "operations1", "kind": "base", "block": null, "base_tables": ["operations1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `5c373c3a67f64c98a0ac69a01f21a13c`；状态 `success`。

```sql
SELECT "Disaster Severity Level", COUNT(*) AS cnt FROM disaster_events GROUP BY "Disaster Severity Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`b5dfbe95cbc74c85c743aab3e5100f83c6c1a921714eecc18653f6bc1f80c3fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Severity Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `f48af4163b674d509863db884cd820f0`；状态 `success`。

```sql
SELECT * FROM financials1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`ed301dd94b19b35e49eddaaea061620f8c5422723db5aa8badf6206310917138`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "financials1", "kind": "base", "block": null, "base_tables": ["financials1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `8fc3515617a3496096ac5c16075ee1b8`；状态 `success`。

```sql
SELECT * FROM supplies1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`99b05aea139b5fe0334eb5906ab35d1c41746a7ae63fa578a010f2e0121cd04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "supplies1", "kind": "base", "block": null, "base_tables": ["supplies1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `9226bffb149f486d89498bc2d2cfd07f`；状态 `success`。

```sql
SELECT * FROM distribution_hubs LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4664db6d910630095f13405430b1b12c0f85d6f3fb19f432a99c8dc0cae67db4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "distribution_hubs", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `0db49edefc744f77bec5c9b440e9d5ce`；状态 `success`。

```sql
SELECT * FROM transportation1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`620e459f5f069aa7f0a20fba6597ed8d1477d84f2ee69b3a993d3c4c044e1051`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transportation1", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `6ee2a684da964ec3b73737b708e3d11b`；状态 `success`。

```sql
SELECT COUNT(DISTINCT hr."Disaster Reference ID") AS hr_events,
       COUNT(DISTINCT op."Disaster Reference ID") AS op_events,
       COUNT(DISTINCT fin."Disaster Reference ID") AS fin_events,
       COUNT(DISTINCT sup."Disaster Reference ID") AS sup_events,
       COUNT(DISTINCT hub."Disaster Event Reference ID") AS hub_events,
       COUNT(DISTINCT tr."Disaster Reference ID") AS tr_events
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN operations1 op ON op."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`4b7570ce0c3f4b78e2d07cc095798f2d3b536f6c2630c8b399e6b9444ca11263`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}, {"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "human_resources AS hr", "on": "hr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "operations1 AS op", "on": "op.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "supplies1 AS sup", "on": "sup.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "distribution_hubs AS hub", "on": "hub.\"Disaster Event Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT hr."Disaster Reference ID") | [{"table": "human_resources", "column": "Disaster Reference ID"}] | [] | False |
| B1 | COUNT(DISTINCT op."Disaster Reference ID") | [{"table": "operations1", "column": "Disaster Reference ID"}] | [] | False |
| B1 | COUNT(DISTINCT fin."Disaster Reference ID") | [{"table": "financials1", "column": "Disaster Reference ID"}] | [] | False |
| B1 | COUNT(DISTINCT sup."Disaster Reference ID") | [{"table": "supplies1", "column": "Disaster Reference ID"}] | [] | False |
| B1 | COUNT(DISTINCT hub."Disaster Event Reference ID") | [{"table": "distribution_hubs", "column": "Disaster Event Reference ID"}] | [] | False |
| B1 | COUNT(DISTINCT tr."Disaster Reference ID") | [{"table": "transportation1", "column": "Disaster Reference ID"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `e38e9b76a37e4f3eb13713895e93a0d9`；状态 `success`。

```sql
SELECT op."Emergency Level", COUNT(*) AS cnt FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level" = 'Level 5' GROUP BY op."Emergency Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`d4bea6109845508e694110a6ac72031dd40977fc098a9f39c123b6c38eceb95c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["op.\"Emergency Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `b286b8c2d456493a8d264c251f7929d1`；状态 `success`。

```sql
SELECT "Human Resources ID", json_extract("Staffing", '$.personnel.total') AS total, json_extract("Staffing", '$.personnel.volunteers') AS vol FROM human_resources LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`74128f7c55498d33e5f2a2737e9edf4e0e88bd9ef0370e8a04cb906122cda803`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "human_resources", "kind": "base", "block": null, "base_tables": ["human_resources"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `d604529515154ebd9d85e30658406c9a`；状态 `success`。

```sql
SELECT "Material ID", json_extract("Inventory resources", '$.power.generators') AS gen, json_extract("Inventory resources", '$.essentials.food_tons') AS food FROM supplies1 LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`109f34c2fc0550cc39f3618d23ccf7dc83aed261bedf30b52ca647d0150938da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "supplies1", "kind": "base", "block": null, "base_tables": ["supplies1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `c6913cd4b821486c94aced533d137aa8`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG(json_extract("Staffing", '$.personnel.total')),1) AS avg_total_staff,
  ROUND(AVG(json_extract("Staffing", '$.personnel.medical')),1) AS avg_medical,
  ROUND(AVG(json_extract("Staffing", '$.personnel.security')),1) AS avg_security,
  ROUND(AVG(json_extract("Staffing", '$.personnel.logistics')),1) AS avg_logistics,
  ROUND(AVG(json_extract("Staffing", '$.personnel.volunteers')),1) AS avg_volunteers,
  ROUND(AVG(json_extract("Staffing", '$.readiness.availability_percent')),1) AS avg_availability,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Critical' THEN 1 ELSE 0 END) AS ppe_critical,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Adequate' THEN 1 ELSE 0 END) AS ppe_adequate,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.ppe_status')='Limited' THEN 1 ELSE 0 END) AS ppe_limited,
  SUM(CASE WHEN json_extract("Staffing", '$.readiness.training_status')='Complete' THEN 1 ELSE 0 END) AS training_complete
FROM human_resources hr JOIN disaster_events de ON de."Disaster Event ID" = hr."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`3a709025abe98a34612cfb7b84564c6d50a8b55e5d50d200be73386445ffba3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = hr.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN JSON_EXTRACT("Staffing", '$.readiness.ppe_status') = 'Critical' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | SUM(CASE WHEN JSON_EXTRACT("Staffing", '$.readiness.ppe_status') = 'Adequate' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | SUM(CASE WHEN JSON_EXTRACT("Staffing", '$.readiness.ppe_status') = 'Limited' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | SUM(CASE WHEN JSON_EXTRACT("Staffing", '$.readiness.training_status') = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.personnel.total')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.personnel.medical')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.personnel.security')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.personnel.logistics')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.personnel.volunteers')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Staffing", '$.readiness.availability_percent')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `d978b2d46fbe409895d5cafc77f3a250`；状态 `success`。

```sql
SELECT 
  "Resource Allocation Status" AS alloc_status, COUNT(*) AS cnt
FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY "Resource Allocation Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`163cce9300f1f30d79859d1124ab80a29d744fa4036aac7a096c6ca5578a846b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"Resource Allocation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `f6c278343c0e4bf183630334b697efa5`；状态 `success`。

```sql
SELECT 
  ROUND(AVG("budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG("fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG("costbene(USD)"),2) AS avg_costbene,
  ROUND(AVG("opscosts(USD)"),0) AS avg_opscosts,
  ROUND(AVG("transportcosts(USD)"),0) AS avg_transport,
  ROUND(AVG("storagecosts(USD)"),0) AS avg_storage,
  ROUND(AVG("personnelcosts(USD)"),0) AS avg_personnel,
  ROUND(AVG("donorcommitments(USD)"),0) AS avg_donor,
  ROUND(AVG("resourcegaps(USD)"),0) AS avg_gaps,
  SUM(CASE WHEN "fundingstate"='Adequate' THEN 1 ELSE 0 END) AS funding_adequate,
  SUM(CASE WHEN "fundingstate"='Critical' THEN 1 ELSE 0 END) AS funding_critical,
  SUM(CASE WHEN "fundingstate"='Sufficient' THEN 1 ELSE 0 END) AS funding_sufficient
FROM financials1 fin JOIN disaster_events de ON de."Disaster Event ID" = fin."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`2835e0419198a37dd6ea43446d0ec2f32384fe24ff5b09093f6bc41341c1ae93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = fin.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "fundingstate" = 'Adequate' THEN 1 ELSE 0 END) | [] | [{"table": "financials1", "column": "fundingstate"}] | False |
| B1 | SUM(CASE WHEN "fundingstate" = 'Critical' THEN 1 ELSE 0 END) | [] | [{"table": "financials1", "column": "fundingstate"}] | False |
| B1 | SUM(CASE WHEN "fundingstate" = 'Sufficient' THEN 1 ELSE 0 END) | [] | [{"table": "financials1", "column": "fundingstate"}] | False |
| B1 | AVG("budgetallot(USD)") | [{"table": "financials1", "column": "budgetallot(USD)"}] | [] | False |
| B1 | AVG("fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B1 | AVG("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | AVG("opscosts(USD)") | [{"table": "financials1", "column": "opscosts(USD)"}] | [] | False |
| B1 | AVG("transportcosts(USD)") | [{"table": "financials1", "column": "transportcosts(USD)"}] | [] | False |
| B1 | AVG("storagecosts(USD)") | [{"table": "financials1", "column": "storagecosts(USD)"}] | [] | False |
| B1 | AVG("personnelcosts(USD)") | [{"table": "financials1", "column": "personnelcosts(USD)"}] | [] | False |
| B1 | AVG("donorcommitments(USD)") | [{"table": "financials1", "column": "donorcommitments(USD)"}] | [] | False |
| B1 | AVG("resourcegaps(USD)") | [{"table": "financials1", "column": "resourcegaps(USD)"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `f7c6b23c06ea43019eee701dec12e1a0`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG(json_extract("Inventory resources", '$.power.generators')),1) AS avg_generators,
  ROUND(AVG(json_extract("Inventory resources", '$.power.fuel_liters')),0) AS avg_fuel,
  ROUND(AVG(json_extract("Inventory resources", '$.medical')),0) AS avg_medical,
  ROUND(AVG(json_extract("Inventory resources", '$.shelter.units')),0) AS avg_shelter,
  ROUND(AVG(json_extract("Inventory resources", '$.shelter.blankets')),0) AS avg_blankets,
  ROUND(AVG(json_extract("Inventory resources", '$.essentials.food_tons')),1) AS avg_food,
  ROUND(AVG(json_extract("Inventory resources", '$.essentials.water_liters')),0) AS avg_water,
  ROUND(AVG(json_extract("Inventory resources", '$.hygiene_kits')),0) AS avg_hygiene
FROM supplies1 sup JOIN disaster_events de ON de."Disaster Event ID" = sup."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`affe19977096952a3ca0c9967e6b30d39b5c6f4ad1c200af26eb49132ee83a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = sup.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.power.generators')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.power.fuel_liters')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.medical')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.shelter.units')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.shelter.blankets')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.essentials.food_tons')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.essentials.water_liters')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Inventory resources", '$.hygiene_kits')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `0f3ded6df96746478a0035af4661213e`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Center Capacity (tons)"),0) AS avg_capacity,
  ROUND(AVG("Utilization (%)"),1) AS avg_util,
  ROUND(AVG("Storage Capacity (m³)"),0) AS avg_storage_m3,
  ROUND(AVG("Available Capacity (m³)"),0) AS avg_avail_m3,
  ROUND(AVG("Inventory Accuracy (%)"),1) AS avg_inv_accuracy,
  ROUND(AVG("Inventory Turnover Rate"),2) AS avg_turnover,
  SUM(CASE WHEN "Warehouse Status"='Excellent' THEN 1 ELSE 0 END) AS wh_excellent,
  SUM(CASE WHEN "Warehouse Status"='Good' THEN 1 ELSE 0 END) AS wh_good,
  SUM(CASE WHEN "Warehouse Status"='Fair' THEN 1 ELSE 0 END) AS wh_fair,
  SUM(CASE WHEN "Warehouse Status"='Poor' THEN 1 ELSE 0 END) AS wh_poor
FROM distribution_hubs hub JOIN disaster_events de ON de."Disaster Event ID" = hub."Disaster Event Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`b1784f013a3aefdcd5de3cd07f068a4336802008c1922f76c475b58e5a552ebe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = hub.\"Disaster Event Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Warehouse Status" = 'Excellent' THEN 1 ELSE 0 END) | [] | [{"table": "distribution_hubs", "column": "Warehouse Status"}] | False |
| B1 | SUM(CASE WHEN "Warehouse Status" = 'Good' THEN 1 ELSE 0 END) | [] | [{"table": "distribution_hubs", "column": "Warehouse Status"}] | False |
| B1 | SUM(CASE WHEN "Warehouse Status" = 'Fair' THEN 1 ELSE 0 END) | [] | [{"table": "distribution_hubs", "column": "Warehouse Status"}] | False |
| B1 | SUM(CASE WHEN "Warehouse Status" = 'Poor' THEN 1 ELSE 0 END) | [] | [{"table": "distribution_hubs", "column": "Warehouse Status"}] | False |
| B1 | AVG("Center Capacity (tons)") | [{"table": "distribution_hubs", "column": "Center Capacity (tons)"}] | [] | False |
| B1 | AVG("Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B1 | AVG("Storage Capacity (m³)") | [{"table": "distribution_hubs", "column": "Storage Capacity (m³)"}] | [] | False |
| B1 | AVG("Available Capacity (m³)") | [{"table": "distribution_hubs", "column": "Available Capacity (m³)"}] | [] | False |
| B1 | AVG("Inventory Accuracy (%)") | [{"table": "distribution_hubs", "column": "Inventory Accuracy (%)"}] | [] | False |
| B1 | AVG("Inventory Turnover Rate") | [{"table": "distribution_hubs", "column": "Inventory Turnover Rate"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `323a4391623e4e85bf4f90305d101a3a`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Number of Vehicles"),1) AS avg_vehicles,
  ROUND(AVG("Available Trucks"),1) AS avg_trucks,
  ROUND(AVG("Available Helicopters"),1) AS avg_helis,
  ROUND(AVG("Available Ships"),1) AS avg_ships,
  ROUND(AVG("Total Transport Volume (tons)"),0) AS avg_total_vol,
  ROUND(AVG("Daily Transport Volume (tons)"),0) AS avg_daily_vol,
  ROUND(AVG("Number of Distribution Points"),0) AS avg_dist_points,
  ROUND(AVG("Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG("Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG("Fuel Consumption (L/km)"),1) AS avg_fuel,
  ROUND(AVG("Vehicle Failure Rate"),1) AS avg_fail_rate,
  SUM(CASE WHEN "Last-Mile Delivery Status"='On Track' THEN 1 ELSE 0 END) AS lm_ontrack,
  SUM(CASE WHEN "Last-Mile Delivery Status"='Delayed' THEN 1 ELSE 0 END) AS lm_delayed,
  SUM(CASE WHEN "Route Optimization Status"='Optimized' THEN 1 ELSE 0 END) AS route_opt,
  SUM(CASE WHEN "Maintenance Status"='Up to Date' THEN 1 ELSE 0 END) AS maint_ok
FROM transportation1 tr JOIN disaster_events de ON de."Disaster Event ID" = tr."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`f1befeba42d4ff9c3a27e06306b10b0987eac91508279413fd2e592fb401d288`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = tr.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Last-Mile Delivery Status" = 'On Track' THEN 1 ELSE 0 END) | [] | [{"table": "transportation1", "column": "Last-Mile Delivery Status"}] | False |
| B1 | SUM(CASE WHEN "Last-Mile Delivery Status" = 'Delayed' THEN 1 ELSE 0 END) | [] | [{"table": "transportation1", "column": "Last-Mile Delivery Status"}] | False |
| B1 | SUM(CASE WHEN "Route Optimization Status" = 'Optimized' THEN 1 ELSE 0 END) | [] | [{"table": "transportation1", "column": "Route Optimization Status"}] | False |
| B1 | SUM(CASE WHEN "Maintenance Status" = 'Up to Date' THEN 1 ELSE 0 END) | [] | [{"table": "transportation1", "column": "Maintenance Status"}] | False |
| B1 | AVG("Number of Vehicles") | [{"table": "transportation1", "column": "Number of Vehicles"}] | [] | False |
| B1 | AVG("Available Trucks") | [{"table": "transportation1", "column": "Available Trucks"}] | [] | False |
| B1 | AVG("Available Helicopters") | [{"table": "transportation1", "column": "Available Helicopters"}] | [] | False |
| B1 | AVG("Available Ships") | [{"table": "transportation1", "column": "Available Ships"}] | [] | False |
| B1 | AVG("Total Transport Volume (tons)") | [{"table": "transportation1", "column": "Total Transport Volume (tons)"}] | [] | False |
| B1 | AVG("Daily Transport Volume (tons)") | [{"table": "transportation1", "column": "Daily Transport Volume (tons)"}] | [] | False |
| B1 | AVG("Number of Distribution Points") | [{"table": "transportation1", "column": "Number of Distribution Points"}] | [] | False |
| B1 | AVG("Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG("Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG("Fuel Consumption (L/km)") | [{"table": "transportation1", "column": "Fuel Consumption (L/km)"}] | [] | False |
| B1 | AVG("Vehicle Failure Rate") | [{"table": "transportation1", "column": "Vehicle Failure Rate"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `3b7c3a4bc4004a4aa500fe50b3cdb10c`；状态 `success`。

```sql
SELECT "Response Phase", COUNT(*) AS cnt FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Response Phase" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`e0e069bcf09e867f7718d6611dd2a6d949a60e0fd7e7135fac9354896df28726`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"Response Phase\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `aed045af34834e24adf59e74659a7a09`；状态 `success`。

```sql
SELECT "Operation Status", COUNT(*) AS cnt FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Operation Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`7f770c42125abd331216300af254708c7b9869b0984020ac096f038c6731bafb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"Operation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `22d1768a3d2a4ab39dce07f98b8103a6`；状态 `success`。

```sql
SELECT "Supply Flow Status", COUNT(*) AS cnt FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Supply Flow Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`0203182a7d3f2bd58b725c1d4d4618ad35b4363cd9b65f90554812ab0e6a3bf8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"Supply Flow Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `cf19a17dade24f549e986291a322e393`；状态 `success`。

```sql
SELECT "Priority", COUNT(*) AS cnt FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Priority" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`6c6c6dfb8ac56686ad40b66b3b14079e9a65de6f91454aface5a94ae52f199ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `fc5748da67944b86aa1f67ceaae367ed`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  COUNT(*) AS n,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.total')),1) AS avg_total_staff,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.volunteers')),1) AS avg_volunteers,
  ROUND(AVG(json_extract(hr."Staffing", '$.readiness.availability_percent')),1) AS avg_avail,
  ROUND(SUM(CASE WHEN json_extract(hr."Staffing", '$.readiness.ppe_status')='Critical' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_ppe_critical,
  ROUND(SUM(CASE WHEN json_extract(hr."Staffing", '$.readiness.training_status')='Complete' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_training_complete,
  ROUND(AVG(fin."budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG(fin."costbene(USD)"),2) AS avg_costbene,
  ROUND(AVG(fin."resourcegaps(USD)"),0) AS avg_gaps,
  ROUND(SUM(CASE WHEN fin."fundingstate"='Critical' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_funding_critical,
  ROUND(AVG(hub."Center Capacity (tons)"),0) AS avg_hub_capacity,
  ROUND(AVG(hub."Utilization (%)"),1) AS avg_hub_util,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(SUM(CASE WHEN tr."Last-Mile Delivery Status"='Delayed' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_delayed
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`095c37d44a3d6e225854962e0099545c96d9d9f044c517aba3d258e57350b5a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "human_resources AS hr", "on": "hr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "distribution_hubs AS hub", "on": "hub.\"Disaster Event Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JSON_EXTRACT(hr."Staffing", '$.personnel.total')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(hr."Staffing", '$.personnel.volunteers')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(hr."Staffing", '$.readiness.availability_percent')) | [{"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(fin."budgetallot(USD)") | [{"table": "financials1", "column": "budgetallot(USD)"}] | [] | False |
| B1 | AVG(fin."fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B1 | AVG(fin."costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | AVG(fin."resourcegaps(USD)") | [{"table": "financials1", "column": "resourcegaps(USD)"}] | [] | False |
| B1 | AVG(hub."Center Capacity (tons)") | [{"table": "distribution_hubs", "column": "Center Capacity (tons)"}] | [] | False |
| B1 | AVG(hub."Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B1 | AVG(tr."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN JSON_EXTRACT(hr."Staffing", '$.readiness.ppe_status') = 'Critical' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | SUM(CASE WHEN JSON_EXTRACT(hr."Staffing", '$.readiness.training_status') = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "human_resources", "column": "Staffing"}] | False |
| B1 | SUM(CASE WHEN fin."fundingstate" = 'Critical' THEN 1 ELSE 0 END) | [] | [{"table": "financials1", "column": "fundingstate"}] | False |
| B1 | SUM(CASE WHEN tr."Last-Mile Delivery Status" = 'Delayed' THEN 1 ELSE 0 END) | [] | [{"table": "transportation1", "column": "Last-Mile Delivery Status"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `f3080ca435dc45b7a4812d2615622361`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  COUNT(*) AS n,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.affected')),0) AS avg_affected,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.displaced')),0) AS avg_displaced,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.injured')),0) AS avg_injured,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.population.casualties')),0) AS avg_casualties,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.infrastructure.damage_percent')),1) AS avg_damage_pct,
  ROUND(AVG(json_extract(de."Impact Indicator", '$.infrastructure.power_outage_percent')),1) AS avg_power_outage
FROM disaster_events de
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`98d514c1d2c8bc1061adde84222789aad070b19e60703fdb63b4a27b38c4aca5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.population.affected')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.population.displaced')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.population.injured')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.population.casualties')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.infrastructure.damage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(de."Impact Indicator", '$.infrastructure.power_outage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `9fafa58703424c028ed5b3e16c020cc8`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),0) AS affected_per_staff,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(fin."budgetallot(USD)",0)),3) AS affected_per_1000usd,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.shelter.units'),0)),1) AS displaced_per_shelter_unit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.essentials.food_tons'),0)),0) AS affected_per_food_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.medical'),0)),3) AS injured_per_medical_unit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Total Transport Volume (tons)",0)),1) AS affected_per_transport_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points",0)),0) AS affected_per_dist_point
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`726ddecb3fc753401d2442c7f8c07d8ea45af9fa163dadd211471ea0505ba969`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "human_resources AS hr", "on": "hr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "supplies1 AS sup", "on": "sup.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(fin."budgetallot(USD)", 0)) | [{"table": "financials1", "column": "budgetallot(USD)"}, {"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.shelter.units'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.essentials.food_tons'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.medical'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Total Transport Volume (tons)", 0)) | [{"table": "transportation1", "column": "Total Transport Volume (tons)"}, {"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points", 0)) | [{"table": "transportation1", "column": "Number of Distribution Points"}, {"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `96faf3fc7cf14882b6e25dd970f6aa10`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.medical')*1.0 / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS medical_pct_of_staff,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.volunteers')*1.0 / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),1) AS volunteer_ratio,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.medical'),0)),1) AS injured_per_medic,
  ROUND(AVG(fin."costbene(USD)"*1.0 / NULLIF(fin."budgetallot(USD)",0)),4) AS roi_ratio,
  ROUND(AVG((fin."transportcosts(USD)"+fin."storagecosts(USD)"+fin."personnelcosts(USD)"+fin."opscosts(USD)")*1.0 / NULLIF(fin."budgetallot(USD)",0)*100),1) AS ops_cost_pct_of_budget,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_delivery_time,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS delivery_success_rate,
  ROUND(AVG(tr."Daily Transport Volume (tons)"*1.0 / NULLIF(tr."Number of Vehicles",0)),1) AS tons_per_vehicle_per_day
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`7faf312c28d58d4caf08a04ffc3976390cfbf3a24456b3cb9b18a9f307a418f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "human_resources AS hr", "on": "hr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(JSON_EXTRACT(hr."Staffing", '$.personnel.medical') * 1.0 / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0) * 100) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(hr."Staffing", '$.personnel.volunteers') * 1.0 / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0)) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.medical'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(fin."costbene(USD)" * 1.0 / NULLIF(fin."budgetallot(USD)", 0)) | [{"table": "financials1", "column": "costbene(USD)"}, {"table": "financials1", "column": "budgetallot(USD)"}] | [] | False |
| B1 | AVG((fin."transportcosts(USD)" + fin."storagecosts(USD)" + fin."personnelcosts(USD)" + fin."opscosts(USD)") * 1.0 / NULLIF(fin."budgetallot(USD)", 0) * 100) | [{"table": "financials1", "column": "budgetallot(USD)"}, {"table": "financials1", "column": "opscosts(USD)"}, {"table": "financials1", "column": "personnelcosts(USD)"}, {"table": "financials1", "column": "transportcosts(USD)"}, {"table": "financials1", "column": "storagecosts(USD)"}] | [] | False |
| B1 | AVG(tr."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(tr."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(tr."Daily Transport Volume (tons)" * 1.0 / NULLIF(tr."Number of Vehicles", 0)) | [{"table": "transportation1", "column": "Daily Transport Volume (tons)"}, {"table": "transportation1", "column": "Number of Vehicles"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `e00554544d5a435187b8235d8a3539cb`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points",0)),0) AS affected_per_dist_point,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Daily Transport Volume (tons)",0)),0) AS affected_per_daily_ton,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.shelter.blankets'),0)),3) AS displaced_per_blanket,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.hygiene_kits'),0)),0) AS affected_per_hygiene_kit,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(json_extract(sup."Inventory resources", '$.essentials.water_liters'),0)),2) AS affected_per_liter_water
FROM disaster_events de
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`61d1c981a28aa069698247d219f976a4b58d0b6b488f2db8a174538cd122e839`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "supplies1 AS sup", "on": "sup.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Number of Distribution Points", 0)) | [{"table": "transportation1", "column": "Number of Distribution Points"}, {"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(tr."Daily Transport Volume (tons)", 0)) | [{"table": "transportation1", "column": "Daily Transport Volume (tons)"}, {"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.displaced') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.shelter.blankets'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.hygiene_kits'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(de."Impact Indicator", '$.population.affected') AS REAL) / NULLIF(JSON_EXTRACT(sup."Inventory resources", '$.essentials.water_liters'), 0)) | [{"table": "disaster_events", "column": "Impact Indicator"}, {"table": "supplies1", "column": "Inventory resources"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `35f9808224e346d985684d1be6595d6f`；状态 `success`。

```sql
SELECT "Disaster Type", COUNT(*) AS cnt FROM disaster_events WHERE "Disaster Severity Level" = 'Level 5' GROUP BY "Disaster Type" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`49d222f2995745ad6efab5dd5143e35b27dcec86ce1901f1598a9a042b4fe561`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `e21f9c1cd0194396af2ab4237110d465`；状态 `success`。

```sql
SELECT 
  op."Resource Allocation Status",
  op."Supply Flow Status",
  COUNT(*) AS cnt
FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY op."Resource Allocation Status", op."Supply Flow Status"
ORDER BY op."Resource Allocation Status", op."Supply Flow Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`739d2b94ed6f9ce2a61d1ecf2e8b445080ef96ed81768a54a602e646d900f194`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["op.\"Resource Allocation Status\"", "op.\"Supply Flow Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `e4e581c0b2174427a1326bbd2757638b`；状态 `success`。

```sql
SELECT 
  op."Emergency Level",
  COUNT(*) AS cnt,
  ROUND(AVG(op."Estimated Duration (days)"),0) AS avg_duration
FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY op."Emergency Level"
ORDER BY op."Emergency Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`32916442b3b46f9c096511709f6438def575d443ca4bf7ce66c945b44ede24ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["op.\"Emergency Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(op."Estimated Duration (days)") | [{"table": "operations1", "column": "Estimated Duration (days)"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `a88c9fea144f4ee3bcea8129a0e36328`；状态 `success`。

```sql
SELECT de."Disaster Severity Level", op."Emergency Level", COUNT(*) AS cnt
FROM disaster_events de JOIN operations1 op ON de."Disaster Event ID" = op."Disaster Reference ID"
GROUP BY de."Disaster Severity Level", op."Emergency Level"
ORDER BY de."Disaster Severity Level", op."Emergency Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`c5ef777b36b89a0510c498c1af2a830d7ddcb388addfc54ba2f9d5a9709af452`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}] | [{"type": "INNER", "right": "operations1 AS op", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["de.\"Disaster Severity Level\"", "op.\"Emergency Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `d0aab86f5e694393badbbdbd0bd8fb17`；状态 `success`。

```sql
SELECT 
  op."Resource Allocation Status",
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(hub."Utilization (%)"),1) AS avg_hub_util,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil
FROM operations1 op 
JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY op."Resource Allocation Status"
ORDER BY op."Resource Allocation Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`c1cff06124144e239d1b8a1677aaf91d62ccb235def1d2016db7172ffff743ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "distribution_hubs AS hub", "on": "hub.\"Disaster Event Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["op.\"Resource Allocation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(tr."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(tr."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(hub."Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B1 | AVG(fin."fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |


## S42

类别 `data`；来源 `python`；调用 `c8a1abc24447466a8df74a040d77b9b3`；状态 `success`。

```sql

SELECT de."Disaster Event ID",
  json_extract(de."Impact Indicator", '$.population.affected') AS affected,
  json_extract(de."Impact Indicator", '$.population.displaced') AS displaced,
  json_extract(de."Impact Indicator", '$.population.injured') AS injured,
  json_extract(hr."Staffing", '$.personnel.total') AS staff_total,
  json_extract(hr."Staffing", '$.personnel.medical') AS staff_medical,
  json_extract(hr."Staffing", '$.personnel.logistics') AS staff_logistics,
  json_extract(hr."Staffing", '$.personnel.volunteers') AS volunteers,
  json_extract(hr."Staffing", '$.readiness.availability_percent') AS avail_pct,
  fin."budgetallot(USD)" AS budget,
  fin."fundsutilpct(%)" AS fundsutil,
  fin."costbene(USD)" AS costbene,
  fin."resourcegaps(USD)" AS gaps,
  hub."Utilization (%)" AS hub_util,
  hub."Inventory Accuracy (%)" AS inv_acc,
  tr."Total Transport Volume (tons)" AS transport_vol,
  tr."Daily Transport Volume (tons)" AS daily_vol,
  tr."Average Delivery Time" AS deliv_time,
  tr."Delivery Success Rate" AS deliv_success,
  tr."Number of Distribution Points" AS dist_points,
  tr."Number of Vehicles" AS vehicles,
  sup."Inventory resources" AS inv
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`4c038026246a89c8d15e63e838038d2bd2ae17d3630909fa45c6fe8e67fbc63a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}] | [{"type": "LEFT", "right": "human_resources AS hr", "on": "hr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "distribution_hubs AS hub", "on": "hub.\"Disaster Event Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "supplies1 AS sup", "on": "sup.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `c33109f6723a4c799edeb6cf8aee82ec`；状态 `success`。

```sql
SELECT 
  MIN("costbene(USD)") AS min_cb, MAX("costbene(USD)") AS max_cb, ROUND(AVG("costbene(USD)"),1) AS avg_cb,
  MIN("fundsutilpct(%)") AS min_fu, MAX("fundsutilpct(%)") AS max_fu,
  MIN("Delivery Success Rate") AS min_ds, MAX("Delivery Success Rate") AS max_ds,
  MIN("Average Delivery Time") AS min_dt, MAX("Average Delivery Time") AS max_dt,
  MIN("Center Capacity (tons)") AS min_cap, MAX("Center Capacity (tons)") AS max_cap,
  MIN("Utilization (%)") AS min_util, MAX("Utilization (%)") AS max_util
FROM financials1 fin 
JOIN disaster_events de ON de."Disaster Event ID"=fin."Disaster Reference ID"
CROSS JOIN (SELECT 1) 
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID"=de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID"=de."Disaster Event ID"
WHERE de."Disaster Severity Level"='Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`112a942b33918755bbdf40a3f56033bb3b6da56eb8b96c850a8e95a9e137cca1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [{"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "", "kind": "derived", "block": "B1", "base_tables": []}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = fin.\"Disaster Reference ID\"", "using": []}, {"type": "CROSS", "right": "(SELECT 1)", "on": null, "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "distribution_hubs AS hub", "on": "hub.\"Disaster Event Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B2 | MAX("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B2 | MIN("fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B2 | MAX("fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B2 | MIN("Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B2 | MAX("Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B2 | MIN("Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B2 | MAX("Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B2 | MIN("Center Capacity (tons)") | [{"table": "distribution_hubs", "column": "Center Capacity (tons)"}] | [] | False |
| B2 | MAX("Center Capacity (tons)") | [{"table": "distribution_hubs", "column": "Center Capacity (tons)"}] | [] | False |
| B2 | MIN("Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B2 | MAX("Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B2 | AVG("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `ffeb2567e69a4476bc8de5376bd9bb4c`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Inventory Accuracy (%)"),1) AS avg_inv_acc,
  SUM(CASE WHEN "Inventory Accuracy (%)" >= 95 THEN 1 ELSE 0 END) AS inv_acc_ge95,
  ROUND(AVG("Available Capacity (m³)"),0) AS avg_avail_m3,
  ROUND(AVG("Cold Storage Capacity (m³)"),0) AS avg_cold_m3,
  ROUND(AVG("Cold Storage Temperature (℃)"),1) AS avg_cold_temp
FROM distribution_hubs hub JOIN disaster_events de ON de."Disaster Event ID" = hub."Disaster Event Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`f74c4374c8c3877657a977cf269d745ce92d503424cd29fd36179be3f575db8b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = hub.\"Disaster Event Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Inventory Accuracy (%)" >= 95 THEN 1 ELSE 0 END) | [] | [{"table": "distribution_hubs", "column": "Inventory Accuracy (%)"}] | False |
| B1 | AVG("Inventory Accuracy (%)") | [{"table": "distribution_hubs", "column": "Inventory Accuracy (%)"}] | [] | False |
| B1 | AVG("Available Capacity (m³)") | [{"table": "distribution_hubs", "column": "Available Capacity (m³)"}] | [] | False |
| B1 | AVG("Cold Storage Capacity (m³)") | [{"table": "distribution_hubs", "column": "Cold Storage Capacity (m³)"}] | [] | False |
| B1 | AVG("Cold Storage Temperature (℃)") | [{"table": "distribution_hubs", "column": "Cold Storage Temperature (℃)"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `d902dadbd8754e78ab15618e86743a54`；状态 `success`。

```sql
SELECT 
  "Route Optimization Status", COUNT(*) AS cnt,
  ROUND(AVG("Delivery Success Rate"),1) AS avg_success,
  ROUND(AVG("Average Delivery Time"),1) AS avg_time
FROM transportation1 tr JOIN disaster_events de ON de."Disaster Event ID" = tr."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
GROUP BY "Route Optimization Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`207d1da6cd5bd6f265bfeaafc1abed4f9a2d18b91b5271744167ed35fd93b2b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = tr.\"Disaster Reference ID\"", "using": []}] | ["\"Route Optimization Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG("Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `7ef79cf38b3f471d8319120e3506fd80`；状态 `success`。

```sql
SELECT "Last-Mile Delivery Status", COUNT(*) AS cnt FROM transportation1 tr JOIN disaster_events de ON de."Disaster Event ID"=tr."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Last-Mile Delivery Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`5a27f44328ba7441f21b096e8d4037d5bd8a54cbfd41a57a51e18364413fa054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = tr.\"Disaster Reference ID\"", "using": []}] | ["\"Last-Mile Delivery Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `b84938708cd04649867f9b230f50ddfa`；状态 `success`。

```sql
SELECT "fundingstate", COUNT(*) AS cnt FROM financials1 fin JOIN disaster_events de ON de."Disaster Event ID"=fin."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "fundingstate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`05b442a884769ba75e4be7fea60543806d63793a6d2936ba9049b5523ad0ae12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = fin.\"Disaster Reference ID\"", "using": []}] | ["\"fundingstate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `b6d7505296934927a246546e3decb197`；状态 `success`。

```sql
SELECT "Warehouse Status", COUNT(*) AS cnt, ROUND(AVG("Utilization (%)"),1) AS avg_util, ROUND(AVG("Inventory Accuracy (%)"),1) AS avg_acc FROM distribution_hubs hub JOIN disaster_events de ON de."Disaster Event ID"=hub."Disaster Event Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "Warehouse Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`be06b21c582de54d68256dd5fb0a505af58d04d645aa8482845489a2ccd58076`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "hub", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = hub.\"Disaster Event Reference ID\"", "using": []}] | ["\"Warehouse Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B1 | AVG("Inventory Accuracy (%)") | [{"table": "distribution_hubs", "column": "Inventory Accuracy (%)"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `d0aadd9415f74b5998509a899cc0be07`；状态 `success`。

```sql
SELECT 
  MIN("costbene(USD)") AS min_cb, 
  ROUND(AVG("costbene(USD)"),1) AS avg_cb, 
  MAX("costbene(USD)") AS max_cb,
  ROUND(AVG("costbene(USD)"*1.0/NULLIF("budgetallot(USD)",0)),6) AS avg_benefit_cost_ratio
FROM financials1 fin JOIN disaster_events de ON de."Disaster Event ID"=fin."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`0a6256bc88515af388eddf720c90d02ff69908ad0486868ba9d4b6acbdba8b8e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = fin.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | MAX("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | AVG("costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | AVG("costbene(USD)" * 1.0 / NULLIF("budgetallot(USD)", 0)) | [{"table": "financials1", "column": "costbene(USD)"}, {"table": "financials1", "column": "budgetallot(USD)"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `fa39dd6a94dc4f8ea897589f893b3b00`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.medical') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS med_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.logistics') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS log_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.security') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS sec_pct,
  ROUND(AVG(CAST(json_extract(hr."Staffing", '$.personnel.volunteers') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),1) AS vol_ratio
FROM human_resources hr JOIN disaster_events de ON de."Disaster Event ID"=hr."Disaster Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`2928abeb4dc838e42bf0f2b83092157133a9a931c2ee2c7b029359291e1cfb74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "hr", "kind": "base", "block": null, "base_tables": ["human_resources"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = hr.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST(JSON_EXTRACT(hr."Staffing", '$.personnel.medical') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0) * 100) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(hr."Staffing", '$.personnel.logistics') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0) * 100) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(hr."Staffing", '$.personnel.security') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0) * 100) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |
| B1 | AVG(CAST(JSON_EXTRACT(hr."Staffing", '$.personnel.volunteers') AS REAL) / NULLIF(JSON_EXTRACT(hr."Staffing", '$.personnel.total'), 0)) | [{"table": "human_resources", "column": "Staffing"}, {"table": "human_resources", "column": "Staffing"}] | [] | False |


## S51

类别 `data`；来源 `query_db`；调用 `93bf51658cba4e13a54b216b718e6331`；状态 `success`。

```sql
SELECT 
  "Disaster Type",
  COUNT(*) AS cnt,
  ROUND(AVG(json_extract("Impact Indicator", '$.population.affected')),0) AS avg_affected,
  ROUND(AVG(fin."budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(tr."Daily Transport Volume (tons)"),0) AS avg_daily_vol
FROM disaster_events de
LEFT JOIN financials1 fin ON fin."Disaster Reference ID"=de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID"=de."Disaster Event ID"
WHERE de."Disaster Severity Level"='Level 5'
GROUP BY "Disaster Type"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`de569bc6d97ce2ae680da521f154bfd2fb5b3865336ad666990df5286c6f7971`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "fin", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "financials1 AS fin", "on": "fin.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["\"Disaster Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.population.affected')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(fin."budgetallot(USD)") | [{"table": "financials1", "column": "budgetallot(USD)"}] | [] | False |
| B1 | AVG(fin."fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B1 | AVG(tr."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(tr."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(tr."Daily Transport Volume (tons)") | [{"table": "transportation1", "column": "Daily Transport Volume (tons)"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `808888e357cc42858d820ed6e78d6993`；状态 `success`。

```sql
SELECT * FROM coordination_and_evaluation LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`a8956674045938811852d1b15b66be4a37f3f384b71e86da5213cd9324cb517b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "coordination_and_evaluation", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `query_db`；调用 `03e2907910f94e44834eed4f947a89e5`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG("partnerorgs"),1) AS avg_partner_orgs,
  ROUND(AVG("reportcompliance"),1) AS avg_report_compliance,
  ROUND(AVG("dataqualityvalue"),0) AS avg_data_quality,
  ROUND(AVG("stakeholdersatisf"),1) AS avg_stakeholder_satisf,
  ROUND(AVG("publicperception"),1) AS avg_public_perception,
  ROUND(AVG("Secincident Count"),0) AS avg_sec_incidents,
  SUM(CASE WHEN "compliancestate"='Compliant' THEN 1 ELSE 0 END) AS compliant,
  SUM(CASE WHEN "auditstate"='Passed' THEN 1 ELSE 0 END) AS audit_passed,
  SUM(CASE WHEN "lessonsrecorded">0 THEN 1 ELSE 0 END) AS has_lessons,
  SUM(CASE WHEN "bestpracticeslisted">0 THEN 1 ELSE 0 END) AS has_best_practices,
  SUM(CASE WHEN "improvementrecs">0 THEN 1 ELSE 0 END) AS has_improvements
FROM coordination_and_evaluation ce JOIN disaster_events de ON de."Disaster Event ID"=ce."Action Reference ID"
WHERE de."Disaster Severity Level"='Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`585504d3ea02bb5efd92361a7ae7aeeb1c6fb5f5b84cc6e864b04b1752b7c0bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = ce.\"Action Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "compliancestate" = 'Compliant' THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "compliancestate"}] | False |
| B1 | SUM(CASE WHEN "auditstate" = 'Passed' THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "auditstate"}] | False |
| B1 | SUM(CASE WHEN "lessonsrecorded" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "lessonsrecorded"}] | False |
| B1 | SUM(CASE WHEN "bestpracticeslisted" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "bestpracticeslisted"}] | False |
| B1 | SUM(CASE WHEN "improvementrecs" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "improvementrecs"}] | False |
| B1 | AVG("partnerorgs") | [{"table": "coordination_and_evaluation", "column": "partnerorgs"}] | [] | False |
| B1 | AVG("reportcompliance") | [{"table": "coordination_and_evaluation", "column": "reportcompliance"}] | [] | False |
| B1 | AVG("dataqualityvalue") | [{"table": "coordination_and_evaluation", "column": "dataqualityvalue"}] | [] | False |
| B1 | AVG("stakeholdersatisf") | [{"table": "coordination_and_evaluation", "column": "stakeholdersatisf"}] | [] | False |
| B1 | AVG("publicperception") | [{"table": "coordination_and_evaluation", "column": "publicperception"}] | [] | False |
| B1 | AVG("Secincident Count") | [{"table": "coordination_and_evaluation", "column": "Secincident Count"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `0276c35ac9884397a6dee284b0febf75`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG(ce."partnerorgs"),1) AS avg_partner_orgs,
  ROUND(AVG(ce."reportcompliance"),1) AS avg_report_compliance,
  ROUND(AVG(ce."dataqualityvalue"),0) AS avg_data_quality,
  ROUND(AVG(ce."stakeholdersatisf"),1) AS avg_stakeholder_satisf,
  ROUND(AVG(ce."publicperception"),1) AS avg_public_perception,
  ROUND(AVG(ce."Secincident Count"),0) AS avg_sec_incidents,
  SUM(CASE WHEN ce."compliancestate"='Compliant' THEN 1 ELSE 0 END) AS compliant,
  SUM(CASE WHEN ce."auditstate"='Passed' THEN 1 ELSE 0 END) AS audit_passed,
  ROUND(AVG(ce."lessonsrecorded"),0) AS avg_lessons,
  ROUND(AVG(ce."bestpracticeslisted"),0) AS avg_best_practices,
  ROUND(AVG(ce."improvementrecs"),0) AS avg_improvements
FROM coordination_and_evaluation ce
JOIN operations1 op ON op."Operation ID" = ce."Action Reference ID"
JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`b8f30871c574e227290b084646e2a92f77c79c7d4a01ce2ca1c68f74ad2eed80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "operations1 AS op", "on": "op.\"Operation ID\" = ce.\"Action Reference ID\"", "using": []}, {"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN ce."compliancestate" = 'Compliant' THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "compliancestate"}] | False |
| B1 | SUM(CASE WHEN ce."auditstate" = 'Passed' THEN 1 ELSE 0 END) | [] | [{"table": "coordination_and_evaluation", "column": "auditstate"}] | False |
| B1 | AVG(ce."partnerorgs") | [{"table": "coordination_and_evaluation", "column": "partnerorgs"}] | [] | False |
| B1 | AVG(ce."reportcompliance") | [{"table": "coordination_and_evaluation", "column": "reportcompliance"}] | [] | False |
| B1 | AVG(ce."dataqualityvalue") | [{"table": "coordination_and_evaluation", "column": "dataqualityvalue"}] | [] | False |
| B1 | AVG(ce."stakeholdersatisf") | [{"table": "coordination_and_evaluation", "column": "stakeholdersatisf"}] | [] | False |
| B1 | AVG(ce."publicperception") | [{"table": "coordination_and_evaluation", "column": "publicperception"}] | [] | False |
| B1 | AVG(ce."Secincident Count") | [{"table": "coordination_and_evaluation", "column": "Secincident Count"}] | [] | False |
| B1 | AVG(ce."lessonsrecorded") | [{"table": "coordination_and_evaluation", "column": "lessonsrecorded"}] | [] | False |
| B1 | AVG(ce."bestpracticeslisted") | [{"table": "coordination_and_evaluation", "column": "bestpracticeslisted"}] | [] | False |
| B1 | AVG(ce."improvementrecs") | [{"table": "coordination_and_evaluation", "column": "improvementrecs"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `3fbf5703ef1e4470a4c13880e43ea72b`；状态 `success`。

```sql
SELECT "auditstate", COUNT(*) AS cnt FROM coordination_and_evaluation ce JOIN operations1 op ON op."Operation ID" = ce."Action Reference ID" JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID" WHERE de."Disaster Severity Level"='Level 5' GROUP BY "auditstate" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`a9807dad6b3a6f3dde9b6cf84193b02ca78578eae8f7774f3a404572153a676d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "op", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "operations1 AS op", "on": "op.\"Operation ID\" = ce.\"Action Reference ID\"", "using": []}, {"type": "INNER", "right": "disaster_events AS de", "on": "de.\"Disaster Event ID\" = op.\"Disaster Reference ID\"", "using": []}] | ["\"auditstate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `query_db`；调用 `53253bc5d739417f9b17a400798227fe`；状态 `success`。

```sql
SELECT 
  ROUND(AVG("Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG("Affected Population Feedback Score"),2) AS avg_feedback,
  COUNT(*) AS n,
  SUM(CASE WHEN "Needs Assessment Status"='Complete' THEN 1 ELSE 0 END) AS needs_complete,
  SUM(CASE WHEN "Vulnerability Assessment"='Complete' THEN 1 ELSE 0 END) AS vuln_complete
FROM beneficiaries_and_assessments ba
WHERE "Distribution Reference ID" IN (SELECT "Disaster Event ID" FROM disaster_events WHERE "Disaster Severity Level"='Level 5')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`a7f9ac14c260fb933963682bc55efd94adcb37d80e568fff1012715fb55c651d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |
| B2 | [{"alias": "ba", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN "Needs Assessment Status" = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "beneficiaries_and_assessments", "column": "Needs Assessment Status"}] | False |
| B2 | SUM(CASE WHEN "Vulnerability Assessment" = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "beneficiaries_and_assessments", "column": "Vulnerability Assessment"}] | False |
| B2 | AVG("Distribution Equity Index") | [{"table": "beneficiaries_and_assessments", "column": "Distribution Equity Index"}] | [] | False |
| B2 | AVG("Affected Population Feedback Score") | [{"table": "beneficiaries_and_assessments", "column": "Affected Population Feedback Score"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "\"Disaster Event ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Disaster Severity Level\"", "reason": "ambiguous_or_missing_source"}]

## S57

类别 `data`；来源 `query_db`；调用 `a15031dc32d345a3b1bd6c398cf1d1f3`；状态 `success`。

```sql
SELECT ba."Distribution Reference ID" AS ba_ref, de."Disaster Event ID" AS de_ref
FROM beneficiaries_and_assessments ba
JOIN disaster_events de ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`f5a2c501fd0c889f81068c74d55fb9ad50ea7a0fc35cc24a5f7c0564ae806d2d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ba", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "ba.\"Distribution Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `query_db`；调用 `5318f6f3c6214f5483c30764764f2096`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(ba."Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG(ba."Affected Population Feedback Score"),2) AS avg_feedback,
  COUNT(*) AS n_ba,
  SUM(CASE WHEN ba."Needs Assessment Status"='Complete' THEN 1 ELSE 0 END) AS needs_complete,
  SUM(CASE WHEN ba."Vulnerability Assessment"='Complete' THEN 1 ELSE 0 END) AS vuln_complete
FROM beneficiaries_and_assessments ba
JOIN disaster_events de ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`a7f9ac14c260fb933963682bc55efd94adcb37d80e568fff1012715fb55c651d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ba", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}, {"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "disaster_events AS de", "on": "ba.\"Distribution Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN ba."Needs Assessment Status" = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "beneficiaries_and_assessments", "column": "Needs Assessment Status"}] | False |
| B1 | SUM(CASE WHEN ba."Vulnerability Assessment" = 'Complete' THEN 1 ELSE 0 END) | [] | [{"table": "beneficiaries_and_assessments", "column": "Vulnerability Assessment"}] | False |
| B1 | AVG(ba."Distribution Equity Index") | [{"table": "beneficiaries_and_assessments", "column": "Distribution Equity Index"}] | [] | False |
| B1 | AVG(ba."Affected Population Feedback Score") | [{"table": "beneficiaries_and_assessments", "column": "Affected Population Feedback Score"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `4103f835e62b4217a7b04fa831f75ad3`；状态 `success`。

```sql
SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.power.generators')),1) AS avg_gen,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.medical')),0) AS avg_med,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.shelter.units')),0) AS avg_shelter,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.essentials.food_tons')),1) AS avg_food,
  ROUND(AVG(json_extract(sup."Inventory resources", '$.essentials.water_liters')),0) AS avg_water,
  ROUND(AVG(tr."Total Transport Volume (tons)"),0) AS avg_transport_vol,
  ROUND(AVG(tr."Daily Transport Volume (tons)"),0) AS avg_daily_vol,
  ROUND(AVG(tr."Number of Vehicles"),1) AS avg_vehicles,
  ROUND(AVG(tr."Number of Distribution Points"),0) AS avg_dist_points,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Vehicle Failure Rate"),1) AS avg_failure_rate
FROM disaster_events de
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`af83495f40ffab4b047b8625f6b641cb45a73fb39c6392b4ab8eb60759697d15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "sup", "kind": "base", "block": null, "base_tables": ["supplies1"]}, {"alias": "tr", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "LEFT", "right": "supplies1 AS sup", "on": "sup.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}, {"type": "LEFT", "right": "transportation1 AS tr", "on": "tr.\"Disaster Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN de.\"Disaster Severity Level\" = 'Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(JSON_EXTRACT(sup."Inventory resources", '$.power.generators')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(sup."Inventory resources", '$.medical')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(sup."Inventory resources", '$.shelter.units')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(sup."Inventory resources", '$.essentials.food_tons')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(sup."Inventory resources", '$.essentials.water_liters')) | [{"table": "supplies1", "column": "Inventory resources"}] | [] | False |
| B1 | AVG(tr."Total Transport Volume (tons)") | [{"table": "transportation1", "column": "Total Transport Volume (tons)"}] | [] | False |
| B1 | AVG(tr."Daily Transport Volume (tons)") | [{"table": "transportation1", "column": "Daily Transport Volume (tons)"}] | [] | False |
| B1 | AVG(tr."Number of Vehicles") | [{"table": "transportation1", "column": "Number of Vehicles"}] | [] | False |
| B1 | AVG(tr."Number of Distribution Points") | [{"table": "transportation1", "column": "Number of Distribution Points"}] | [] | False |
| B1 | AVG(tr."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(tr."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(tr."Vehicle Failure Rate") | [{"table": "transportation1", "column": "Vehicle Failure Rate"}] | [] | False |


## S60

类别 `data`；来源 `python`；调用 `bdf9eb0796bf4391b9193eb93ee52d9c`；状态 `success`。

```sql

SELECT de."Disaster Event ID",
  ba."Distribution Equity Index" AS equity,
  ba."Affected Population Feedback Score" AS feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`06149e04fa66e1f2afb355d0cb69708bf618aa9ad8f17cc8f3518b7c311a232a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "ba", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}] | [{"type": "LEFT", "right": "beneficiaries_and_assessments AS ba", "on": "ba.\"Distribution Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `bdf9eb0796bf4391b9193eb93ee52d9c`；状态 `success`。

```sql

SELECT de."Disaster Severity Level",
  ROUND(AVG(ba."Distribution Equity Index"),3) AS avg_equity,
  ROUND(AVG(ba."Affected Population Feedback Score"),2) AS avg_feedback
FROM disaster_events de
LEFT JOIN beneficiaries_and_assessments ba ON ba."Distribution Reference ID" = de."Disaster Event ID"
GROUP BY de."Disaster Severity Level"
ORDER BY de."Disaster Severity Level"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-026/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`acaa45daa8a5bc4eb587e41f9462e2e9e700daea4be2a997776783ec980d84a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "de", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "ba", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}] | [{"type": "LEFT", "right": "beneficiaries_and_assessments AS ba", "on": "ba.\"Distribution Reference ID\" = de.\"Disaster Event ID\"", "using": []}] | ["de.\"Disaster Severity Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ba."Distribution Equity Index") | [{"table": "beneficiaries_and_assessments", "column": "Distribution Equity Index"}] | [] | False |
| B1 | AVG(ba."Affected Population Feedback Score") | [{"table": "beneficiaries_and_assessments", "column": "Affected Population Feedback Score"}] | [] | False |

