# dacomp-043

To clarify the factors associated with the high case fatality rate of Hand, Foot, and Mout…

运行：已提交。官方未评分。全部 SQL 尝试/成功 91/91；数据 SQL 89/89；Python 6 次。

完整原题：

To clarify the factors associated with the high case fatality rate of Hand, Foot, and Mouth Disease, I want to understand the notable differences between the deceased population and the recovered population across the dimensions of symptoms, prevention/control, and treatment.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| basic_medical_record_informatio | 453 | 26 |
| clinical_manifestations | 282 | 20 |
| complication_management | 261 | 18 |
| diagnosis_and_classification | 298 | 18 |
| epidemic_analysis | 140 | 19 |
| epidemiological_investigation | 245 | 13 |
| health_education | 140 | 20 |
| healthcare_resources | 140 | 21 |
| immunization_management | 140 | 28 |
| isolation_and_disinfection | 216 | 19 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 构造病例结局公共 CTE → 分别比较症状、防控、治疗和记录完整性 → Python 绘图并检验温度/完整性分布。

数据库大小：966,656 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\""] | ["COUNT(*)"] | 3 | 0.449 |
| [S4/Q2](#s4) | success | ["clinical_manifestations"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.31 |
| [S5/Q3](#s5) | success | ["clinical_manifestations"] | 0 / {} | [] | ["COUNT(DISTINCT \"Case ID\")"] | 1 | 0.424 |
| [S6/Q4](#s6) | success | ["complication_management"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.316 |
| [S7/Q5](#s7) | success | ["epidemiological_investigation"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.229 |
| [S8/Q6](#s8) | success | ["isolation_and_disinfection"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.26 |
| [S9/Q7](#s9) | success | ["diagnosis_and_classification"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.318 |
| [S10/Q8](#s10) | success | ["immunization_management"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.311 |
| [S11/Q9](#s11) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Outcome (Cured/Improved/Deceased)\""] | ["COUNT(*)", "AVG(\"Highest Body Temperature (°C)\")", "MIN(\"Highest Body Temperature (°C)\")", "MAX(\"Highest Body Temperature (°C)\")", "AVG(\"Data Completeness Score\")"] | 3 | 1.254 |
| [S12/Q10](#s12) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Hospitalization (Yes/No)\"", "\"Isolation Status (Yes/No)\"", "\"Treatment (Antiviral/Symptomatic)\""] | ["COUNT(*)"] | 24 | 0.655 |
| [S13/Q11](#s13) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\"", "\"Associated Symptoms (Cough/Headache/Vomiting)\"", "\"Rash Distribution (Head & Face/Trunk/Limbs)\"", "\"Rash Morphology (Macule/Papule/Vesicle)\"", "\"TCM Pattern Differentiation (Wind-Heat/Damp-Heat)\""] | ["COUNT(*)"] | 152 | 1.079 |
| [S14/Q12](#s14) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\""] | ["COUNT(*)"] | 9 | 0.525 |
| [S15/Q13](#s15) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Associated Symptoms (Cough/Headache/Vomiting)\""] | ["COUNT(*)"] | 9 | 0.511 |
| [S16/Q14](#s16) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Hospitalization (Yes/No)\""] | ["COUNT(*)"] | 6 | 0.494 |
| [S17/Q15](#s17) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Treatment (Antiviral/Symptomatic)\""] | ["COUNT(*)"] | 6 | 0.517 |
| [S18/Q16](#s18) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Isolation Status (Yes/No)\""] | ["COUNT(*)"] | 6 | 0.509 |
| [S19/Q17](#s19) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Isolation Type (Home/Hospital)\""] | ["COUNT(*)"] | 6 | 0.508 |
| [S20/Q18](#s20) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["cm.\"Outcome (Cured/Improved/Deceased)\"", "cpl.\"Complication type (pneumonia/encephalitis/hepatitis)\"", "cpl.\"Severity grading (mild/moderate/severe)\"", "cpl.\"Management measures (observation/treatment/referral)\"", "cpl.\"Complication outcome (recovered/sequelae)\""] | ["COUNT(*)"] | 63 | 1.284 |
| [S21/Q19](#s21) | success | ["clinical_manifestations"] | 0 / {} | ["\"Case ID\""] | ["COUNT(*)", "COUNT(DISTINCT \"Outcome (Cured/Improved/Deceased)\")", "GROUP_CONCAT(DISTINCT \"Outcome (Cured/Improved/Deceased)\")"] | 20 | 0.87 |
| [S22/Q20](#s22) | success | ["clinical_manifestations"] | 0 / {} | ["\"Case ID\""] | ["COUNT(*)", "COUNT(DISTINCT \"Outcome (Cured/Improved/Deceased)\")", "GROUP_CONCAT(DISTINCT \"Outcome (Cured/Improved/Deceased)\")"] | 56 | 0.999 |
| [S23/Q21](#s23) | success | ["clinical_manifestations"] | 0 / {} | ["\"Outcome (Cured/Improved/Deceased)\""] | ["COUNT(DISTINCT \"Case ID\")", "COUNT(*)"] | 3 | 0.451 |
| [S24/Q22](#s24) | success | ["epidemiological_investigation"] | 0 / {} | ["\"Vaccination History (Doses/Date/Type)\""] | ["COUNT(*)"] | 183 | 0.605 |
| [S25/Q23](#s25) | success | ["epidemiological_investigation"] | 0 / {} | ["\"Contact Status (Positive/Negative/Pending)\""] | ["COUNT(*)"] | 3 | 0.411 |
| [S26/Q24](#s26) | success | ["epidemiological_investigation"] | 0 / {} | ["\"Contact Location Type (Hospital/School/Mall)\""] | ["COUNT(*)"] | 4 | 0.313 |
| [S27/Q25](#s27) | success | ["epidemiological_investigation"] | 0 / {} | ["\"Shared Exposure History (Group Dining/Group Activity)\""] | ["COUNT(*)"] | 2 | 0.308 |
| [S28/Q26](#s28) | success | ["isolation_and_disinfection"] | 0 / {} | ["\"Isolation Type (Home/Hospital/Centralized)\""] | ["COUNT(*)"] | 3 | 0.402 |
| [S29/Q27](#s29) | success | ["isolation_and_disinfection"] | 0 / {} | ["\"PPE Usage\""] | ["COUNT(*)"] | 2 | 0.297 |
| [S30/Q28](#s30) | success | ["isolation_and_disinfection"] | 0 / {} | ["\"Symptom Monitoring During Isolation\""] | ["COUNT(*)"] | 2 | 0.3 |
| [S31/Q29](#s31) | success | ["diagnosis_and_classification"] | 0 / {} | ["\"Initial Diagnosis (Suspected/Clinical/Confirmed)\"", "\"Diagnostic Quality Score\"", "\"Diagnostic Criteria Compliance Rate\""] | ["COUNT(*)"] | 20 | 0.655 |
| [S32/Q30](#s32) | success | ["clinical_manifestations"] | 0 / {} | ["\"Contact Management (Yes/No)\""] | ["COUNT(*)"] | 2 | 0.436 |
| [S33/Q31](#s33) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 1.106 |
| [S34/Q32](#s34) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Associated Symptoms (Cough/Headache/Vomiting)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 1.004 |
| [S35/Q33](#s35) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Hospitalization (Yes/No)\"", "\"Treatment (Antiviral/Symptomatic)\"", "\"Isolation Status (Yes/No)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 16 | 1.116 |
| [S36/Q34](#s36) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT cm.\"Case ID\")", "COUNT(*)", "AVG(\"Highest Body Temperature (°C)\")", "MIN(\"Highest Body Temperature (°C)\")", "MAX(\"Highest Body Temperature (°C)\")"] | 2 | 1.24 |
| [S37/Q35](#s37) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Rash Distribution (Head & Face/Trunk/Limbs)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 1.117 |
| [S38/Q36](#s38) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Rash Morphology (Macule/Papule/Vesicle)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 1.118 |
| [S39/Q37](#s39) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"TCM Pattern Differentiation (Wind-Heat/Damp-Heat)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.956 |
| [S40/Q38](#s40) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccination History (Doses/Date/Type)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 101 | 1.085 |
| [S41/Q39](#s41) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Status (Positive/Negative/Pending)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 0.922 |
| [S42/Q40](#s42) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Location Type (Hospital/School/Mall)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 7 | 0.924 |
| [S43/Q41](#s43) | success | ["epidemiological_investigation"] | 0 / {} | ["CASE WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '0%' THEN '0 dose/None' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '1%' THEN '1 dose' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '2%' THEN '2 doses' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '3%' THEN '3 doses' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE 'No%' OR \"Vaccination History (Doses/Date/Type)\" LIKE 'None%' THEN 'No vaccination' ELSE 'Other' END"] | ["COUNT(*)"] | 2 | 0.538 |
| [S44/Q42](#s44) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "CASE WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '0%' THEN '0 dose/None' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '1%' THEN '1 dose' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '2%' THEN '2 doses' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '3%' THEN '3 doses' ELSE 'No vaccination' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 3 | 0.985 |
| [S45/Q43](#s45) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 2 | 0.85 |
| [S46/Q44](#s46) | success | ["clinical_manifestations", "isolation_and_disinfection"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 2 | 0.807 |
| [S47/Q45](#s47) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 2 | 0.871 |
| [S48/Q46](#s48) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 2 | 0.892 |
| [S49/Q47](#s49) | success | ["clinical_manifestations", "isolation_and_disinfection"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"Isolation Type (Home/Hospital/Centralized)\"", "id.\"Disinfection Frequency (times/day)\"", "id.\"Disinfectant Type (Chlorine-based/Peracetic Acid)\"", "id.\"PPE Usage\"", "id.\"Symptom Monitoring During Isolation\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 45 | 1.092 |
| [S50/Q48](#s50) | success | ["clinical_manifestations", "isolation_and_disinfection"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"Isolation Type (Home/Hospital/Centralized)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 5 | 0.864 |
| [S51/Q49](#s51) | success | ["clinical_manifestations", "isolation_and_disinfection"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"PPE Usage\"", "id.\"Symptom Monitoring During Isolation\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 7 | 0.899 |
| [S52/Q50](#s52) | success | ["clinical_manifestations", "isolation_and_disinfection"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "AVG(id.\"Disinfection Frequency (times/day)\")", "AVG(id.\"Disinfected Area (m²)\")", "AVG(id.\"Isolation Cost\")"] | 2 | 0.9 |
| [S53/Q51](#s53) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Complication type (pneumonia/encephalitis/hepatitis)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 0.927 |
| [S54/Q52](#s54) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Severity grading (mild/moderate/severe)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 0.932 |
| [S55/Q53](#s55) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Management measures (observation/treatment/referral)\"", "cpl.\"Complication outcome (recovered/sequelae)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 12 | 0.978 |
| [S56/Q54](#s56) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Initial Diagnosis (Suspected/Clinical/Confirmed)\"", "dc.\"Case Classification (Sporadic/Outbreak/Sudden Event)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 17 | 1.021 |
| [S57/Q55](#s57) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "AVG(dc.\"Diagnostic Quality Score\")", "AVG(dc.\"Diagnostic Criteria Compliance Rate\")", "MIN(dc.\"Diagnostic Quality Score\")", "MAX(dc.\"Diagnostic Quality Score\")"] | 2 | 0.975 |
| [S58/Q56](#s58) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\"", "cm.\"Imaging Studies (CT/X-ray)\"", "cm.\"Medication & Dosage\"", "cm.\"Allergic Reaction Management\"", "cm.\"Contact Management (Yes/No)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 243 | 1.918 |
| [S59/Q57](#s59) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.95 |
| [S60/Q58](#s60) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Imaging Studies (CT/X-ray)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.01 |
| [S61/Q59](#s61) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Allergic Reaction Management\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.96 |
| [S62/Q60](#s62) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Contact Management (Yes/No)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.941 |
| [S63/Q61](#s63) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "gender"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 4 | 1.141 |
| [S64/Q62](#s64) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Occupation Type (Childcare/Student/Teacher)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 6 | 1.167 |
| [S65/Q63](#s65) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Reporting Method (App/Phone/Paper)\"", "b.\"Data Source (Clinical/Laboratory/Epidemiological Investigation)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 14 | 1.249 |
| [S66/Q64](#s66) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Complication reporting timeliness\"", "cpl.\"Complication management timeliness\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(cpl.\"Complication treatment cost\")", "MIN(cpl.\"Complication treatment cost\")", "MAX(cpl.\"Complication treatment cost\")", "AVG(cpl.\"Medical Insurance Reimbursement Percentage\")"] | 72 | 1.299 |
| [S67/Q65](#s67) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(cpl.\"Complication treatment cost\")", "AVG(cpl.\"Medical Insurance Reimbursement Percentage\")"] | 2 | 1.003 |
| [S68/Q66](#s68) | success | ["clinical_manifestations", "complication_management"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "AVG(cpl.\"Medical Insurance Reimbursement Percentage\")"] | 2 | 1.005 |
| [S69/Q67](#s69) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccine Origin (Domestic/Imported)\"", "ei.\"Shared Exposure History (Group Dining/Group Activity)\"", "ei.\"Environmental Sample Test Result\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 15 | 1.099 |
| [S70/Q68](#s70) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnostic Delay Analysis\"", "dc.\"Differential Diagnosis (Measles/Hand, Foot, and Mouth Disease)\"", "dc.\"Diagnosis Review Flag\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 16 | 1.147 |
| [S71/Q69](#s71) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Initial Diagnosis (Suspected/Clinical/Confirmed)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 0.965 |
| [S72/Q70](#s72) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnostic Delay Analysis\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.965 |
| [S73/Q71](#s73) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccine Origin (Domestic/Imported)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.001 |
| [S74/Q72](#s74) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Case Classification (Sporadic/Outbreak/Sudden Event)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 6 | 1.058 |
| [S75/Q73](#s75) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnosis Review Flag\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.0 |
| [S76/Q74](#s76) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Allergy History (Type)\"", "b.\"Past Medical History (Disease Code)\"", "b.\"Contact History (Hospital/School/Home)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 52 | 1.578 |
| [S77/Q75](#s77) | success | ["clinical_manifestations", "diagnosis_and_classification"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Laboratory Confirmation Basis (PCR/Antibody Test)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.061 |
| [S78/Q76](#s78) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Allergy History (Type)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 6 | 1.278 |
| [S79/Q77](#s79) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Past Medical History (Disease Code)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 6 | 1.276 |
| [S80/Q78](#s80) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Contact History (Hospital/School/Home)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(DISTINCT b.\"Case ID\")"] | 6 | 1.286 |
| [S81/Q79](#s81) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "MIN(b.\"Date of Discovery\")", "MAX(b.\"Date of Discovery\")", "COUNT(DISTINCT b.\"Case ID\")"] | 2 | 1.332 |
| [S82/Q80](#s82) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Emergency Response Activation Time\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 124 | 1.726 |
| [S83/Q81](#s83) | success | ["clinical_manifestations", "epidemiological_investigation"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Location Type (Hospital/School/Mall)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)"] | 7 | 0.929 |
| [S84/Q82](#s84) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 282 | 1.031 |
| [S85/Q83](#s85) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 282 | 0.875 |
| [S86/Q84](#s86) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 282 | 0.916 |
| [S87/Q85](#s87) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 211 | 1.064 |
| [S88/Q86](#s88) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 282 | 0.91 |
| [S89/Q87](#s89) | success | ["basic_medical_record_informatio", "clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)"] | 211 | 0.95 |
| [S90/Q88](#s90) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 1.131 |
| [S91/Q89](#s91) | success | ["clinical_manifestations"] | 2 / {'INNER': 1} | ["\"Case ID\"", "CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Allergic Reaction Management\""] | ["MAX(CASE WHEN \"Outcome (Cured/Improved/Deceased)\" = 'Deceased' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 1.049 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_statistical_and_chart_exceptions**。核心病例结局划分、症状/治疗/防控分组均在 SQL；Python 主要将手工转录摘要转成百分比图，或读取已按 SQL 划分结局的数值用于箱线图和 Mann-Whitney 检验。图表百分比及附带组均值可由 SQL 准备，已单列这一有限偏离。没有发现将完整关联分组工作整体迁到 pandas 的情形；图中转录值的一致性不在本次协议审查中自动认定。 [证据](../reviews/dacomp-043.json)。

P1：Creating summary visualizations comparing deceased vs recovered populations across key dimensions (symptoms, prevention/control, treatment) - these visualizations are best done with matplotlib in Python for customized bar charts, not achievable through SQL alone.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Creating a third visualization for complication management severity and other supplementary findings. Python matplotlib is needed for customized visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Creating a boxplot of highest body temperature by outcome group and a comparison of data completeness scores - these statistical visualizations require matplotlib/scipy in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Retrieving temperature and completeness data via db.frame to construct boxplots; the previous direct iteration failed because db.query returns an execution record, not a row array. Python is used here for the boxplot visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Creating boxplots for temperature and data completeness by outcome group, using the db.frame data retrieval. This visualization requires matplotlib.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Creating boxplots with compatible matplotlib API; labels parameter is not supported in this version.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S84", "S85", "S86", "S88"] | 3 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S87", "S89"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40", "S41", "S42", "S44", "S45", "S46", "S47", "S48", "S49", "S50", "S51", "S52", "S53", "S54", "S55", "S56", "S57", "S58", "S59", "S60", "S61", "S62", "S63", "S64", "S65", "S66", "S67", "S68", "S69", "S70", "S71", "S72", "S73", "S74", "S75", "S76", "S77", "S78", "S79", "S80", "S81", "S82", "S83", "S84", "S85", "S86", "S87", "S88", "S89", "S90", "S91"] | 57 | 211 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S3", "S4", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S32"] | 10 | 171 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S7", "S24", "S25", "S26", "S27", "S43"] | 5 | 219 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S8", "S28", "S29", "S30"] | 3 | unknown | not_verified_cap | Not tested |
| C7 | aggregate MV | False | ["S9", "S31"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：75/89 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-043.analysis.json)。

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S42](#s42), [S44](#s44), [S45](#s45), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S53](#s53), [S54](#s54), [S55](#s55), [S56](#s56), [S57](#s57), [S58](#s58), [S59](#s59), [S60](#s60), [S61](#s61), [S62](#s62), [S63](#s63), [S64](#s64), [S65](#s65), [S66](#s66), [S67](#s67), [S68](#s68), [S69](#s69), [S70](#s70), [S71](#s71), [S72](#s72), [S73](#s73), [S74](#s74), [S75](#s75), [S76](#s76), [S77](#s77), [S78](#s78), [S79](#s79), [S80](#s80), [S81](#s81), [S82](#s82), [S83](#s83), [S84](#s84), [S85](#s85), [S86](#s86), [S87](#s87), [S88](#s88), [S89](#s89), [S90](#s90), [S91](#s91) → 新增共享状态 C3 → 后续 57 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Case ID", MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased FROM clinical_manifestations GROUP BY "Case ID"
```

受益查询 S33 的改写示例：

```sql
WITH case_outcome AS (SELECT * FROM temp.reuse_candidate) SELECT CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END AS grp, "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication, COUNT(*) AS n FROM clinical_manifestations AS cm JOIN case_outcome AS co ON cm."Case ID" = co."Case ID" GROUP BY grp, complication ORDER BY grp, n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S44 | True | True | ordered_numeric_tolerance |
| S45 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |
| S47 | True | True | exact_multiset |
| S48 | True | True | exact_multiset |
| S49 | True | True | ordered_numeric_tolerance |
| S50 | True | True | ordered_numeric_tolerance |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | exact_multiset |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |
| S56 | True | True | ordered_numeric_tolerance |
| S57 | True | True | exact_multiset |
| S58 | True | True | ordered_numeric_tolerance |
| S59 | True | True | ordered_numeric_tolerance |
| S60 | True | True | ordered_numeric_tolerance |
| S61 | True | True | ordered_numeric_tolerance |
| S62 | True | True | ordered_numeric_tolerance |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |
| S65 | True | True | ordered_numeric_tolerance |
| S66 | True | True | ordered_numeric_tolerance |
| S67 | True | True | exact_multiset |
| S68 | True | True | exact_multiset |
| S69 | True | True | ordered_numeric_tolerance |
| S70 | True | True | ordered_numeric_tolerance |
| S71 | True | True | ordered_numeric_tolerance |
| S72 | True | True | ordered_numeric_tolerance |
| S73 | True | True | ordered_numeric_tolerance |
| S74 | True | True | ordered_numeric_tolerance |
| S75 | True | True | ordered_numeric_tolerance |
| S76 | True | True | ordered_numeric_tolerance |
| S77 | True | True | ordered_numeric_tolerance |
| S78 | True | True | ordered_numeric_tolerance |
| S79 | True | True | ordered_numeric_tolerance |
| S80 | True | True | ordered_numeric_tolerance |
| S81 | True | True | exact_multiset |
| S82 | True | True | ordered_numeric_tolerance |
| S83 | True | True | ordered_numeric_tolerance |
| S84 | True | True | exact_multiset |
| S85 | True | True | exact_multiset |
| S86 | True | True | exact_multiset |
| S87 | True | True | exact_multiset |
| S88 | True | True | exact_multiset |
| S89 | True | True | exact_multiset |
| S90 | True | True | ordered_numeric_tolerance |
| S91 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S4](#s4), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S32](#s32) → 新增共享状态 C4 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS __g0, "Hospitalization (Yes/No)" AS __g1, "Isolation Status (Yes/No)" AS __g2, "Treatment (Antiviral/Symptomatic)" AS __g3, "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS __g4, "Associated Symptoms (Cough/Headache/Vomiting)" AS __g5, "Rash Distribution (Head & Face/Trunk/Limbs)" AS __g6, "Rash Morphology (Macule/Papule/Vesicle)" AS __g7, "TCM Pattern Differentiation (Wind-Heat/Damp-Heat)" AS __g8, "Isolation Type (Home/Hospital)" AS __g9, "Contact Management (Yes/No)" AS __g10, COUNT(*) AS __a0 FROM "clinical_manifestations"  GROUP BY "Outcome (Cured/Improved/Deceased)", "Hospitalization (Yes/No)", "Isolation Status (Yes/No)", "Treatment (Antiviral/Symptomatic)", "Complication Type (Pneumonia/Encephalitis/Skin Infection)", "Associated Symptoms (Cough/Headache/Vomiting)", "Rash Distribution (Head & Face/Trunk/Limbs)", "Rash Morphology (Macule/Papule/Vesicle)", "TCM Pattern Differentiation (Wind-Heat/Damp-Heat)", "Isolation Type (Home/Hospital)", "Contact Management (Yes/No)"
```

受益查询 S3 的改写示例：

```sql
SELECT __g0 AS outcome, SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S4 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S24](#s24), [S25](#s25), [S26](#s26), [S27](#s27), [S43](#s43) → 新增共享状态 C5 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Vaccination History (Doses/Date/Type)" AS __g0, "Contact Status (Positive/Negative/Pending)" AS __g1, "Contact Location Type (Hospital/School/Mall)" AS __g2, "Shared Exposure History (Group Dining/Group Activity)" AS __g3, CASE WHEN "Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None' WHEN "Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose' WHEN "Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses' WHEN "Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses' WHEN "Vaccination History (Doses/Date/Type)" LIKE 'No%' OR "Vaccination History (Doses/Date/Type)" LIKE 'None%' THEN 'No vaccination' ELSE 'Other' END AS __g4, COUNT(*) AS __a0 FROM "epidemiological_investigation"  GROUP BY "Vaccination History (Doses/Date/Type)", "Contact Status (Positive/Negative/Pending)", "Contact Location Type (Hospital/School/Mall)", "Shared Exposure History (Group Dining/Group Activity)", CASE WHEN "Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None' WHEN "Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose' WHEN "Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses' WHEN "Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses' WHEN "Vaccination History (Doses/Date/Type)" LIKE 'No%' OR "Vaccination History (Doses/Date/Type)" LIKE 'None%' THEN 'No vaccination' ELSE 'Other' END
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS n_epi FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S43 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-043.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `757b5ee91de54216985231b1bdfbb27a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `757b5ee91de54216985231b1bdfbb27a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1a691d3341035b3555c60d5a29d2565a13ce7b3e4bdc61e4b0af404f94a9cb36`。

## S3

类别 `data`；来源 `query_db`；调用 `c9210bc8abf44a319a5008bdf01a9c73`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`eebafe496d18a0688bfa7af52de1342939307ae33ae6dc87af41203f2c042077`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql
SELECT COUNT(*) AS n_cases FROM clinical_manifestations;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`919cc6e06c528040b11032397350b0de6fafc1b6ddd18ab34623ef5775933576`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(DISTINCT "Case ID") AS n_distinct FROM clinical_manifestations;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`4e693423e19b128d203f9ffdef1cd23f115e18a1e99d5c7d293748f9fd8abbdf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Case ID") | [{"table": "clinical_manifestations", "column": "Case ID"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(*) AS n_compl FROM complication_management;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`4774a001040c6e7821c986e8ecc11d222b794b13a667da2f9c7bbbdb710aea98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complication_management", "kind": "base", "block": null, "base_tables": ["complication_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(*) AS n_epi FROM epidemiological_investigation;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`a4715794a1737d7507f593962e9b09100a82f51bcfae2be78183f95b743e30ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(*) AS n_iso FROM isolation_and_disinfection;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`84af7707226c6704efe52c1e1b41dd560a57afbe0cf18d06175ae9cda07cc9c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "isolation_and_disinfection", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(*) AS n_diag FROM diagnosis_and_classification;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7fc1fa3d35a192ce73d2fc385c19dc2734f9fdb5a95ccc5bb50ea74efe3e2530`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "diagnosis_and_classification", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `6957911f07ba4a4692ce235392aaa5a9`；状态 `success`。

```sql

SELECT COUNT(*) AS n_imm FROM immunization_management;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`c8c2c57917f33563db5c2f1ada29e1541826a5249d340fc4c0d85301f16686e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "immunization_management", "kind": "base", "block": null, "base_tables": ["immunization_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `a9597341e5f74a14b3719598db127857`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  COUNT(*) AS n,
  ROUND(AVG("Highest Body Temperature (°C)"),2) AS avg_temp,
  ROUND(MIN("Highest Body Temperature (°C)"),2) AS min_temp,
  ROUND(MAX("Highest Body Temperature (°C)"),2) AS max_temp,
  ROUND(AVG("Data Completeness Score"),2) AS avg_completeness
FROM clinical_manifestations cm
JOIN basic_medical_record_informatio b ON cm."Case ID" = b."Case ID"
GROUP BY outcome;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`aea924a7cc02c36a48f99ed9c94bb227e7140a6cdc2af0286159ac32a68f4dda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}] | [{"type": "INNER", "right": "basic_medical_record_informatio AS b", "on": "cm.\"Case ID\" = b.\"Case ID\"", "using": []}] | ["\"Outcome (Cured/Improved/Deceased)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |
| B1 | MIN("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |
| B1 | MAX("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |
| B1 | AVG("Data Completeness Score") | [{"table": "basic_medical_record_informatio", "column": "Data Completeness Score"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `b5e02e98d7d04180b01c1304b4ef31a7`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome, "Hospitalization (Yes/No)" AS hosp,
  "Isolation Status (Yes/No)" AS iso, "Treatment (Antiviral/Symptomatic)" AS trt, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, hosp, iso, trt
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`f755e738d60b7f5192eeb3d5ba7d93f04ea6f5585b3710330a444710720788f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Hospitalization (Yes/No)\"", "\"Isolation Status (Yes/No)\"", "\"Treatment (Antiviral/Symptomatic)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `0a393e9ed4e842ca9749590357819de0`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication,
  "Associated Symptoms (Cough/Headache/Vomiting)" AS assoc_symptoms,
  "Rash Distribution (Head & Face/Trunk/Limbs)" AS rash_dist,
  "Rash Morphology (Macule/Papule/Vesicle)" AS rash_morph,
  "TCM Pattern Differentiation (Wind-Heat/Damp-Heat)" AS tcm,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, complication, assoc_symptoms, rash_dist, rash_morph, tcm
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`a24e4c8d3b22e133c0d451f2aa91d862296a09132fa6eeeeb4a56498ac462eb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\"", "\"Associated Symptoms (Cough/Headache/Vomiting)\"", "\"Rash Distribution (Head & Face/Trunk/Limbs)\"", "\"Rash Morphology (Macule/Papule/Vesicle)\"", "\"TCM Pattern Differentiation (Wind-Heat/Damp-Heat)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `6c4a97748d6b44e692892e97da8d02a5`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, complication
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`1e9d8194508a0d5f271da6d663df776c50b00cd308ec6679282cef0c77e67ce7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `5f5efc87fd6248c98d5a667f3036405b`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Associated Symptoms (Cough/Headache/Vomiting)" AS symptom,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, symptom
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`91d21adb4a3b9cc6669146491d4ab9ed68a458755f206958c7652f50a7bfcb66`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Associated Symptoms (Cough/Headache/Vomiting)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `11b4be092830404b9c7e9f6ca362c8ad`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Hospitalization (Yes/No)" AS hospitalized,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, hospitalized
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`32b6ade9fbfaa1ed266af88dc9f4c57491aabc80d7b5def247f76667d28d5fd6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Hospitalization (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `d66f35f870b444c3bcf1ef01207c367e`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Treatment (Antiviral/Symptomatic)" AS treatment,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, treatment
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`bc54df803c80520193407a953a970da9ab6c9e90e4dd0c0de342b76d8bd7fb7d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Treatment (Antiviral/Symptomatic)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `db9a60deea764195b1b3bf6550aac3bb`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Isolation Status (Yes/No)" AS isolation,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, isolation
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`678918bb585649beeebd5c7c1111f390cf8ed7f00ec406d25b8243ed506c4c42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Isolation Status (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `fa4b690066e54040a8e532f8f2da515f`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Isolation Type (Home/Hospital)" AS iso_type,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, iso_type
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`b7be9df9565d1f50a647515d0154076a8c04914619c5baf12d787344ae789d84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\"", "\"Isolation Type (Home/Hospital)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `f89f1427bc8144519428b6db6c693f3b`；状态 `success`。

```sql
SELECT cm."Outcome (Cured/Improved/Deceased)" AS outcome,
  cpl."Complication type (pneumonia/encephalitis/hepatitis)" AS comp_type,
  cpl."Severity grading (mild/moderate/severe)" AS severity,
  cpl."Management measures (observation/treatment/referral)" AS mgmt,
  cpl."Complication outcome (recovered/sequelae)" AS comp_outcome,
  COUNT(*) AS n
FROM complication_management cpl
JOIN clinical_manifestations cm ON cpl."Case ID" = cm."Case ID"
GROUP BY outcome, comp_type, severity, mgmt, comp_outcome
ORDER BY outcome, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`05fcc30dc641f0f83a7c0de316207676bb215bccf4456af569deb9b4f3b8b4f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "clinical_manifestations AS cm", "on": "cpl.\"Case ID\" = cm.\"Case ID\"", "using": []}] | ["cm.\"Outcome (Cured/Improved/Deceased)\"", "cpl.\"Complication type (pneumonia/encephalitis/hepatitis)\"", "cpl.\"Severity grading (mild/moderate/severe)\"", "cpl.\"Management measures (observation/treatment/referral)\"", "cpl.\"Complication outcome (recovered/sequelae)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `33ca8c64a3b745a59893fec942942da0`；状态 `success`。

```sql
SELECT "Case ID", COUNT(*) AS n_records, COUNT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS n_outcomes,
  GROUP_CONCAT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS outcomes
FROM clinical_manifestations
GROUP BY "Case ID"
HAVING n_records > 1 OR n_outcomes > 1
ORDER BY n_records DESC
LIMIT 20;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e1e71544e593e3bb830899b229706472910e46b597de072f763e561df9332ee2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Outcome (Cured/Improved/Deceased)") | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | [] | False |
| B1 | GROUP_CONCAT(DISTINCT "Outcome (Cured/Improved/Deceased)") | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `f5e97e896142493e9cc7e2271a68150d`；状态 `success`。

```sql
SELECT "Case ID", COUNT(*) AS n_records, COUNT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS n_outcomes,
  GROUP_CONCAT(DISTINCT "Outcome (Cured/Improved/Deceased)") AS outcomes
FROM clinical_manifestations
GROUP BY "Case ID"
HAVING outcomes LIKE '%Deceased%'
ORDER BY n_records DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`a5b0598384d752eafe1f7cfe73c02f5147a8132acc7c1aaaf4d301edbcff163a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Outcome (Cured/Improved/Deceased)") | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | [] | False |
| B1 | GROUP_CONCAT(DISTINCT "Outcome (Cured/Improved/Deceased)") | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `ae41a093712b48a3a1078be065c693ef`；状态 `success`。

```sql
SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  COUNT(DISTINCT "Case ID") AS n_cases,
  COUNT(*) AS n_records
FROM clinical_manifestations
GROUP BY outcome;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`1762aa49920671c9342544d8595b4edbd502edc7f79cea5979042534fac1ae8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Outcome (Cured/Improved/Deceased)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Case ID") | [{"table": "clinical_manifestations", "column": "Case ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `2a6e65e73fcf41faabfeebc0cd7671ef`；状态 `success`。

```sql
SELECT "Vaccination History (Doses/Date/Type)" AS vacc, COUNT(*) AS n FROM epidemiological_investigation GROUP BY vacc ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`49a43dc4cd348bd2dc2a87e1a36b1e3adacb62a89892a5400cdf8aeee1fd44f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | ["\"Vaccination History (Doses/Date/Type)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `1f540cc2e60048439ce27dd89c1d806b`；状态 `success`。

```sql
SELECT "Contact Status (Positive/Negative/Pending)" AS contact, COUNT(*) AS n FROM epidemiological_investigation GROUP BY contact ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`49a5aaa00e5ab99d84fa8088090111c893846de045bd326f29fef32ef9058a7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | ["\"Contact Status (Positive/Negative/Pending)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `1f540cc2e60048439ce27dd89c1d806b`；状态 `success`。

```sql

SELECT "Contact Location Type (Hospital/School/Mall)" AS loc, COUNT(*) AS n FROM epidemiological_investigation GROUP BY loc ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`ae770af4adf3a93f2a1e7b055da53f3b872f7343523847c92ba59efb23daf186`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | ["\"Contact Location Type (Hospital/School/Mall)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `1f540cc2e60048439ce27dd89c1d806b`；状态 `success`。

```sql

SELECT "Shared Exposure History (Group Dining/Group Activity)" AS shared, COUNT(*) AS n FROM epidemiological_investigation GROUP BY shared ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`1c268042cab50af281c168d9b040b3305ab699db10fb26824df40ef58fc59503`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | ["\"Shared Exposure History (Group Dining/Group Activity)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `f80dfdf99a99424ab25397e61d77cbe3`；状态 `success`。

```sql
SELECT "Isolation Type (Home/Hospital/Centralized)" AS iso_type, COUNT(*) AS n FROM isolation_and_disinfection GROUP BY iso_type ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`19114ff5d40338d1d1377ca9730ccc38e5c672ea7905e4ef8774d6f1e8cc6937`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "isolation_and_disinfection", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}] | [] | ["\"Isolation Type (Home/Hospital/Centralized)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `f80dfdf99a99424ab25397e61d77cbe3`；状态 `success`。

```sql

SELECT "PPE Usage" AS ppe, COUNT(*) AS n FROM isolation_and_disinfection GROUP BY ppe ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`9c416238217b894e0e613abd9fa70cf3a649bd664f07b37e734de2cd4830c1d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "isolation_and_disinfection", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}] | [] | ["\"PPE Usage\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `f80dfdf99a99424ab25397e61d77cbe3`；状态 `success`。

```sql

SELECT "Symptom Monitoring During Isolation" AS monitor, COUNT(*) AS n FROM isolation_and_disinfection GROUP BY monitor ORDER BY n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d515207ac21515afbbab1bb89004630dc3bd1f5488614d73e993aa33c45eb1cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "isolation_and_disinfection", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}] | [] | ["\"Symptom Monitoring During Isolation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `d272cd4562254659b5784ec13eb44517`；状态 `success`。

```sql
SELECT "Initial Diagnosis (Suspected/Clinical/Confirmed)" AS init_diag,
  "Diagnostic Quality Score" AS quality,
  "Diagnostic Criteria Compliance Rate" AS compliance,
  COUNT(*) AS n
FROM diagnosis_and_classification
GROUP BY init_diag, quality, compliance
ORDER BY n DESC
LIMIT 20;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`371fe3d140faaa0a5299ead53c094183babea1f62892d3b59eb6d5f1bc09aeb4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "diagnosis_and_classification", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}] | [] | ["\"Initial Diagnosis (Suspected/Clinical/Confirmed)\"", "\"Diagnostic Quality Score\"", "\"Diagnostic Criteria Compliance Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `33348576f2174bdb95c3e4f25c626552`；状态 `success`。

```sql
SELECT "Contact Management (Yes/No)" AS contact_mgmt, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY contact_mgmt;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`732b5a4fa1fc6d002a8b72e0b1c0da824c410738f666d9927aedb04611f1f6e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Contact Management (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `5d8f250b542942c3b5b6f2c684b21b6d`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, complication ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`917eadbec89fa397b18e8c4a42fd9f6a62a5a6ea79417ca0bd37a05d53098184`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Complication Type (Pneumonia/Encephalitis/Skin Infection)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `03ede363cd1b4c0d80753627d611be6a`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Associated Symptoms (Cough/Headache/Vomiting)" AS symptom,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, symptom ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`af996e7f39a94616ba92a244b7ab7cd90ceecbcb6967d9149d58f8566aabe244`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Associated Symptoms (Cough/Headache/Vomiting)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `25f99b4bcfc74a2f93e07338fb34b833`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Hospitalization (Yes/No)" AS hosp, "Treatment (Antiviral/Symptomatic)" AS trt,
  "Isolation Status (Yes/No)" AS iso, COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, hosp, trt, iso ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`fa8fb5b99c47e52c4d971aef90c7f625244fe380bf2b060dd84383e8992c41c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Hospitalization (Yes/No)\"", "\"Treatment (Antiviral/Symptomatic)\"", "\"Isolation Status (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `3067552b3f6849c1803914332e26a622`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(DISTINCT cm."Case ID") AS n_cases,
  COUNT(*) AS n_records,
  ROUND(AVG("Highest Body Temperature (°C)"),2) AS avg_temp,
  ROUND(MIN("Highest Body Temperature (°C)"),2) AS min_temp,
  ROUND(MAX("Highest Body Temperature (°C)"),2) AS max_temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`77f28e8f4692074b447805e9a56f525268165d4440545780570bb77684a785ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT cm."Case ID") | [{"table": "clinical_manifestations", "column": "Case ID"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |
| B2 | MIN("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |
| B2 | MAX("Highest Body Temperature (°C)") | [{"table": "clinical_manifestations", "column": "Highest Body Temperature (°C)"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `ed11e3ac11694b939db85ac9a6a88652`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Rash Distribution (Head & Face/Trunk/Limbs)" AS rash_dist,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, rash_dist ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`340ea5f1cbe36c9eac726750a39a427c209bd990ebe3dd946966ae3261d37780`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Rash Distribution (Head & Face/Trunk/Limbs)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `8b2c8a2ebe6542a8ba872f9f13086703`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Rash Morphology (Macule/Papule/Vesicle)" AS rash_morph,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, rash_morph ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`b3646097590faa24415185ab76cc573cd101dea1d6fe5d8b89e4b5d948f753d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"Rash Morphology (Macule/Papule/Vesicle)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `e1ac48701502410cb4e4766ff0185fbd`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "TCM Pattern Differentiation (Wind-Heat/Damp-Heat)" AS tcm,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, tcm ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`5f37be11faa004471db916397173571fa45fcc0e2a0b894422476a0a9b6d615d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "\"TCM Pattern Differentiation (Wind-Heat/Damp-Heat)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `5aa922e87cb344acad37d3914d13935b`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Vaccination History (Doses/Date/Type)" AS vacc,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`1a27ea030beb4fb8a7e7cbd1d6b74f4e65b3b84677d066aaebda2f9c40a33138`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccination History (Doses/Date/Type)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `89442307ac844b6c9e5d88d9c1f2b85a`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Contact Status (Positive/Negative/Pending)" AS contact,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, contact ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`c94174e720f927f35b49cf2bee8c334dcfea6b3804f4760a08b855b4be2d672a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Status (Positive/Negative/Pending)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `05cdbebca5804a4b90a6a442c9efbc23`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Contact Location Type (Hospital/School/Mall)" AS loc,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, loc ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`24c85a7ac14241edcb5bee27f2937224ba261ad936777dbf488aaccc180ee4c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Location Type (Hospital/School/Mall)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `query_db`；调用 `ceff5d3260424881a8c34eb9332d9ab7`；状态 `success`。

```sql
SELECT
  CASE WHEN "Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses'
       WHEN "Vaccination History (Doses/Date/Type)" LIKE 'No%' OR "Vaccination History (Doses/Date/Type)" LIKE 'None%' THEN 'No vaccination'
       ELSE 'Other' END AS vacc_cat,
  COUNT(*) AS n
FROM epidemiological_investigation
GROUP BY vacc_cat;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`9ea4c200fe334a70cd5996c4a911bbbee169a7b4a3146ec6405ecfdd2beee753`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "epidemiological_investigation", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}] | [] | ["CASE WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '0%' THEN '0 dose/None' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '1%' THEN '1 dose' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '2%' THEN '2 doses' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE '3%' THEN '3 doses' WHEN \"Vaccination History (Doses/Date/Type)\" LIKE 'No%' OR \"Vaccination History (Doses/Date/Type)\" LIKE 'None%' THEN 'No vaccination' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `query_db`；调用 `cceff9354ff94d60a48d3d2235756e45`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  CASE WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses'
       ELSE 'No vaccination' END AS vacc_cat,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc_cat ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`bbb44d1cf28e044ee9256c2e739938006610655c8d24b261bb27dc7969f27d2f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "CASE WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '0%' THEN '0 dose/None' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '1%' THEN '1 dose' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '2%' THEN '2 doses' WHEN ei.\"Vaccination History (Doses/Date/Type)\" LIKE '3%' THEN '3 doses' ELSE 'No vaccination' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `c66ea763dc7944c3b462b186dfda4d21`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(*) AS n_records FROM epidemiological_investigation ei
JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`37f9205ea7211e5bfee543a6eb9b8c2804b28b3e09114689defe8838faf7e94b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `8da0b0cc6f6e43329a4d827a8f77e3d0`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(*) AS n_records FROM isolation_and_disinfection id
JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`f20f7f499ce87cf7c830dab70781fbe871971841b0bdd944e903b117b7939479`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "id", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "id.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `67f9a3ef909e4b31ae61f9967b769bf4`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(*) AS n_records FROM complication_management cpl
JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`bb991a0053341561d3bbdf8918a756706acf94c3cdc1be63c6df7c46335a4115`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `30204d9e96d04f3da574a73de2093ee7`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(*) AS n_records FROM diagnosis_and_classification dc
JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`4458c79f45deca56ce7fbd3deff92df8153944d2297ac4df4a0747200592c635`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S49

类别 `data`；来源 `query_db`；调用 `0f83948c322642f6aad58500c283dbee`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  id."Isolation Type (Home/Hospital/Centralized)" AS iso_type,
  id."Disinfection Frequency (times/day)" AS disinf_freq,
  id."Disinfectant Type (Chlorine-based/Peracetic Acid)" AS disinf_type,
  id."PPE Usage" AS ppe,
  id."Symptom Monitoring During Isolation" AS symp_monitor,
  COUNT(*) AS n
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp, iso_type, disinf_freq, disinf_type, ppe, symp_monitor
ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`22b8d6d33b66bebbcc0ff2379f1099d73c53b40893f9bc3a26f723fd4c824d3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "id", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "id.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"Isolation Type (Home/Hospital/Centralized)\"", "id.\"Disinfection Frequency (times/day)\"", "id.\"Disinfectant Type (Chlorine-based/Peracetic Acid)\"", "id.\"PPE Usage\"", "id.\"Symptom Monitoring During Isolation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `864bffcf8c0848a1b3c174dc7c1ba547`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  id."Isolation Type (Home/Hospital/Centralized)" AS iso_type,
  COUNT(*) AS n
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp, iso_type ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`13f453359dad3c0d9f041fa5757a48507d649831e39acea157fa178ef7ae8e00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "id", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "id.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"Isolation Type (Home/Hospital/Centralized)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `324303a9430e4638900c9dea816a9ba8`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  id."PPE Usage" AS ppe,
  id."Symptom Monitoring During Isolation" AS monitor,
  COUNT(*) AS n
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp, ppe, monitor ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`e50293b1c4867880f56e0d05671b10645596e5d25c58b0cab5d176ec56753b9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "id", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "id.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "id.\"PPE Usage\"", "id.\"Symptom Monitoring During Isolation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S52

类别 `data`；来源 `query_db`；调用 `2181403d930e43c6af96061c7c13ec9c`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(id."Disinfection Frequency (times/day)"),2) AS avg_disfreq,
  ROUND(AVG(id."Disinfected Area (m²)"),2) AS avg_area,
  ROUND(AVG(id."Isolation Cost"),2) AS avg_cost
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`a45fbeb18188624409f4dca7d292c2cd73ac48c0462b6945fc397351e81a2813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "id", "kind": "base", "block": null, "base_tables": ["isolation_and_disinfection"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "id.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | AVG(id."Disinfection Frequency (times/day)") | [{"table": "isolation_and_disinfection", "column": "Disinfection Frequency (times/day)"}] | [] | False |
| B2 | AVG(id."Disinfected Area (m²)") | [{"table": "isolation_and_disinfection", "column": "Disinfected Area (m²)"}] | [] | False |
| B2 | AVG(id."Isolation Cost") | [{"table": "isolation_and_disinfection", "column": "Isolation Cost"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `10db323ef4a54f7f90380d672635c270`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cpl."Complication type (pneumonia/encephalitis/hepatitis)" AS comp_type,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, comp_type ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`31a7be84a3ecaedb3cc80370c11aac45f3cba4a20e7b72fcb8613ab329895347`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Complication type (pneumonia/encephalitis/hepatitis)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S54

类别 `data`；来源 `query_db`；调用 `069fb45b10e341d899658f5a980ca033`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cpl."Severity grading (mild/moderate/severe)" AS severity,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, severity ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`e0f5d6a5c966b8d2b334659827a70a9a76183a7a6a26806a6aa4b9bc560f5ac8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Severity grading (mild/moderate/severe)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S55

类别 `data`；来源 `query_db`；调用 `ce800ba95ca44d78b2230a4565ba33b0`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cpl."Management measures (observation/treatment/referral)" AS mgmt,
  cpl."Complication outcome (recovered/sequelae)" AS comp_outcome,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, mgmt, comp_outcome ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`cc48f4873906ea640f1964aa3fdb11476ad4bb7fbbff2773256a48bd45ff5422`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Management measures (observation/treatment/referral)\"", "cpl.\"Complication outcome (recovered/sequelae)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `query_db`；调用 `40d65cdf459f4605876b94fb17fb37c7`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Initial Diagnosis (Suspected/Clinical/Confirmed)" AS init_diag,
  dc."Case Classification (Sporadic/Outbreak/Sudden Event)" AS case_class,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, init_diag, case_class ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`2cd5a09e192fd80a610567375c6a3bcebed44df5cb55d5dcafc4332dbc8b798a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Initial Diagnosis (Suspected/Clinical/Confirmed)\"", "dc.\"Case Classification (Sporadic/Outbreak/Sudden Event)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S57

类别 `data`；来源 `query_db`；调用 `60d6b084abc1451fa65ae33e638ce199`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(dc."Diagnostic Quality Score"),2) AS avg_quality,
  ROUND(AVG(dc."Diagnostic Criteria Compliance Rate"),2) AS avg_compliance,
  ROUND(MIN(dc."Diagnostic Quality Score"),2) AS min_quality,
  ROUND(MAX(dc."Diagnostic Quality Score"),2) AS max_quality
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`e22394d614e3ed01fae7c04363e25472e7e3cea7d621517765e3da0852dbe5c7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | AVG(dc."Diagnostic Quality Score") | [{"table": "diagnosis_and_classification", "column": "Diagnostic Quality Score"}] | [] | False |
| B2 | AVG(dc."Diagnostic Criteria Compliance Rate") | [{"table": "diagnosis_and_classification", "column": "Diagnostic Criteria Compliance Rate"}] | [] | False |
| B2 | MIN(dc."Diagnostic Quality Score") | [{"table": "diagnosis_and_classification", "column": "Diagnostic Quality Score"}] | [] | False |
| B2 | MAX(dc."Diagnostic Quality Score") | [{"table": "diagnosis_and_classification", "column": "Diagnostic Quality Score"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `df84f07c9b04446787b3e6db78999185`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Laboratory Tests (CBC/Antibody Test)" AS lab,
  cm."Imaging Studies (CT/X-ray)" AS imaging,
  cm."Medication & Dosage" AS med,
  cm."Allergic Reaction Management" AS allergy_mgmt,
  cm."Contact Management (Yes/No)" AS contact_mgmt,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, lab, imaging, med, allergy_mgmt, contact_mgmt
ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`f11ed028ecc0fd7cb1d94a142cdd0176653b966c53253654741af9647597a491`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\"", "cm.\"Imaging Studies (CT/X-ray)\"", "cm.\"Medication & Dosage\"", "cm.\"Allergic Reaction Management\"", "cm.\"Contact Management (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S59

类别 `data`；来源 `query_db`；调用 `b80d19d5964a4aa5b3bea399303794c0`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Laboratory Tests (CBC/Antibody Test)" AS lab,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, lab ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`19adda6be1604069be51bcfdacd4505304e7ecb8dc790586560fe1e8abe026a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S60

类别 `data`；来源 `query_db`；调用 `938f1e3ce2fe43809813df6fd55faff8`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Imaging Studies (CT/X-ray)" AS imaging,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, imaging ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`c64876f9bcf51702dcb33013ef5916a6a28854e2594f3a428cc364aa33a06a75`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Imaging Studies (CT/X-ray)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `query_db`；调用 `3997b10a65c542fd80d06b71b9e49987`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Allergic Reaction Management" AS allergy,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, allergy ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`18a4aa9444a47e3754ae540d63815d7e994ce0b5a9e04d7daed892dca9e6cf70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Allergic Reaction Management\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S62

类别 `data`；来源 `query_db`；调用 `9c212087a3824448a3ca69de657527e3`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Contact Management (Yes/No)" AS contact_mgmt,
  COUNT(*) AS n
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, contact_mgmt ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`fd85451480f6511826edfafcbf2b7936a62099298b0985b3444ffd1b18413c1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Contact Management (Yes/No)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S63

类别 `data`；来源 `query_db`；调用 `7cd97385286e426db9bd7f72aeb79b99`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Gender" AS gender,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, gender ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`f36fb4875a0f3f90e910879a92c174dd0d322477d947b77e52b8f520909a857a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S64

类别 `data`；来源 `query_db`；调用 `c028736b36b84421aa429696b4abe96a`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Occupation Type (Childcare/Student/Teacher)" AS occupation,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, occupation ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`9a3f01f8e6b63d962fdeadc70b1d425164eda4ceded23aee07b7edbd24cfd8b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Occupation Type (Childcare/Student/Teacher)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `f60912292a924ee4829c1f844d1b8531`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Reporting Method (App/Phone/Paper)" AS report_method,
  b."Data Source (Clinical/Laboratory/Epidemiological Investigation)" AS data_src,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, report_method, data_src ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`d997f93f65cfa2b758640f9b1e315515ee97f43ae520b55eca71ff39478752c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Reporting Method (App/Phone/Paper)\"", "b.\"Data Source (Clinical/Laboratory/Epidemiological Investigation)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S66

类别 `data`；来源 `query_db`；调用 `20aa9fe80f9344da90fd1f2cfc73fa74`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(cpl."Complication treatment cost"),2) AS avg_cost,
  ROUND(MIN(cpl."Complication treatment cost"),2) AS min_cost,
  ROUND(MAX(cpl."Complication treatment cost"),2) AS max_cost,
  ROUND(AVG(cpl."Medical Insurance Reimbursement Percentage"),2) AS avg_reimb,
  cpl."Complication reporting timeliness" AS report_time,
  cpl."Complication management timeliness" AS mgmt_time,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, report_time, mgmt_time ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`a70cda4046d85146dcfd5fc813cf1f72c9f8bcd26dcd003f8503de6b70dc1183`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cpl.\"Complication reporting timeliness\"", "cpl.\"Complication management timeliness\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cpl."Complication treatment cost") | [{"table": "complication_management", "column": "Complication treatment cost"}] | [] | False |
| B2 | MIN(cpl."Complication treatment cost") | [{"table": "complication_management", "column": "Complication treatment cost"}] | [] | False |
| B2 | MAX(cpl."Complication treatment cost") | [{"table": "complication_management", "column": "Complication treatment cost"}] | [] | False |
| B2 | AVG(cpl."Medical Insurance Reimbursement Percentage") | [{"table": "complication_management", "column": "Medical Insurance Reimbursement Percentage"}] | [] | False |


## S67

类别 `data`；来源 `query_db`；调用 `49ace16f07e844b290142433f025c686`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(cpl."Complication treatment cost"),0) AS avg_treatment_cost,
  ROUND(AVG(cpl."Medical Insurance Reimbursement Percentage"),2) AS avg_reimbursement_pct,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`2cf26ef3f4ec3d58877535cda006d23f9a8329ebf0a64ebc78839958850c910b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cpl."Complication treatment cost") | [{"table": "complication_management", "column": "Complication treatment cost"}] | [] | False |
| B2 | AVG(cpl."Medical Insurance Reimbursement Percentage") | [{"table": "complication_management", "column": "Medical Insurance Reimbursement Percentage"}] | [] | False |


## S68

类别 `data`；来源 `query_db`；调用 `d2cc130f8b4d478bb50764ce925f679f`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(cpl."Medical Insurance Reimbursement Percentage"),2) AS avg_reimb
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`3ebf5f2fa4c43176e800eadfce7b9ebfaeae1fca4d9ccbc38d4eaebbe96058ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cpl", "kind": "base", "block": null, "base_tables": ["complication_management"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cpl.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | AVG(cpl."Medical Insurance Reimbursement Percentage") | [{"table": "complication_management", "column": "Medical Insurance Reimbursement Percentage"}] | [] | False |


## S69

类别 `data`；来源 `query_db`；调用 `e7c740f0b3bb4c4d8759566b0aa4bcaf`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Vaccine Origin (Domestic/Imported)" AS vacc_origin,
  ei."Shared Exposure History (Group Dining/Group Activity)" AS shared_exposure,
  ei."Environmental Sample Test Result" AS env_result,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc_origin, shared_exposure, env_result ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`7fbf2641adff28db534776c6b87d0f266b3746235ce09aa0f38d026a17c2824d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccine Origin (Domestic/Imported)\"", "ei.\"Shared Exposure History (Group Dining/Group Activity)\"", "ei.\"Environmental Sample Test Result\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S70

类别 `data`；来源 `query_db`；调用 `6341e46056fa4a48b3edbb1f43230107`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Diagnostic Delay Analysis" AS delay,
  dc."Differential Diagnosis (Measles/Hand, Foot, and Mouth Disease)" AS diff_diag,
  dc."Diagnosis Review Flag" AS review_flag,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, delay, diff_diag, review_flag ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`ef40cbb296448ef6b37c3d19da871fcb72ae2ab33d7a88205fa0cb3f97474655`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnostic Delay Analysis\"", "dc.\"Differential Diagnosis (Measles/Hand, Foot, and Mouth Disease)\"", "dc.\"Diagnosis Review Flag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S71

类别 `data`；来源 `query_db`；调用 `7cda46c232de4b2a8dab59870e635f80`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Initial Diagnosis (Suspected/Clinical/Confirmed)" AS init_diag,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, init_diag ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`623ea161d71ea5149ce5c32e391bd1e455982c80e4aa9bf11055fd84baadfed5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Initial Diagnosis (Suspected/Clinical/Confirmed)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S72

类别 `data`；来源 `query_db`；调用 `af82a87652554587950630dd9c2bc319`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Diagnostic Delay Analysis" AS delay,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, delay ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`dd6587638f68d7b2ecaeb37fdba41e28aa776778976960016a129c8859379077`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnostic Delay Analysis\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S73

类别 `data`；来源 `query_db`；调用 `b112b4d8fdc64adfadc71561adc02dd2`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Vaccine Origin (Domestic/Imported)" AS vacc_origin,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc_origin ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`41a36e3f5b5e4424aef9973c01da2d019b8e9a99f0a475ce3c946c92e602a2b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Vaccine Origin (Domestic/Imported)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S74

类别 `data`；来源 `query_db`；调用 `1cbd9d82424948dc86d8e881f5571371`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Case Classification (Sporadic/Outbreak/Sudden Event)" AS case_class,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, case_class ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`4a0297a05e6533997c69689afb5b5dcea81f3441e60263b76d034858a3efee5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Case Classification (Sporadic/Outbreak/Sudden Event)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S75

类别 `data`；来源 `query_db`；调用 `2a1773f198a74489b0d55ded2f72df7d`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Diagnosis Review Flag" AS review_flag,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, review_flag ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`7dbcd0b0c7311417ea261fef673c0bca225826d69b6bbed418a8b00541b1ff03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Diagnosis Review Flag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `query_db`；调用 `34ef3e83ecb14612a70a7cf8899b4a97`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Allergy History (Type)" AS allergy,
  b."Past Medical History (Disease Code)" AS past_med,
  b."Contact History (Hospital/School/Home)" AS contact_hist,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, allergy, past_med, contact_hist ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`c58ab23c39698e7fa6e24c133f33b238c95b4a368e898d02e509ae9e569c12c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Allergy History (Type)\"", "b.\"Past Medical History (Disease Code)\"", "b.\"Contact History (Hospital/School/Home)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S77

类别 `data`；来源 `query_db`；调用 `a4e58cd5528b440da27119bb7978109d`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Laboratory Confirmation Basis (PCR/Antibody Test)" AS lab_conf,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, lab_conf ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`f76850596cdffe8b00571b7c0682887d5657d455f6cdbb5ff7f32676182805b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "dc", "kind": "base", "block": null, "base_tables": ["diagnosis_and_classification"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "dc.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "dc.\"Laboratory Confirmation Basis (PCR/Antibody Test)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S78

类别 `data`；来源 `query_db`；调用 `ec8df1f7c6f1453980e3511ae907bbb2`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Allergy History (Type)" AS allergy,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, allergy ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`059e60227abec2b20fd9244b4ee55674a69f304b45c6a4c8015ca6965564e0c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Allergy History (Type)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S79

类别 `data`；来源 `query_db`；调用 `1ee77cee12f1458f92fd7ba995eb8575`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Past Medical History (Disease Code)" AS past_med,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, past_med ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`2d227790821e49591f481fa041b80b9fa09dea0ed847f4806f531fea883fa6b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Past Medical History (Disease Code)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S80

类别 `data`；来源 `query_db`；调用 `5ab100b8b93a44c289b105573627f3f0`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Contact History (Hospital/School/Home)" AS contact_hist,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, contact_hist ORDER BY grp, n_cases DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`69813331e638826bc3012589938bc39fa4b0f578e601eab43c719e80159841ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "b.\"Contact History (Hospital/School/Home)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S81

类别 `data`；来源 `query_db`；调用 `abe1439bc45b482180130a7a92383205`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  MIN(b."Date of Discovery") AS min_date,
  MAX(b."Date of Discovery") AS max_date,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`b8b654a28d8d6d9f33f69930c48eb8b711dbb38bceabde2afa8534b7f8887a4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | MIN(b."Date of Discovery") | [{"table": "basic_medical_record_informatio", "column": "Date of Discovery"}] | [] | False |
| B2 | MAX(b."Date of Discovery") | [{"table": "basic_medical_record_informatio", "column": "Date of Discovery"}] | [] | False |
| B2 | COUNT(DISTINCT b."Case ID") | [{"table": "basic_medical_record_informatio", "column": "Case ID"}] | [] | False |


## S82

类别 `data`；来源 `query_db`；调用 `135aaa8e3abc4301afbedf320275396b`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Emergency Response Activation Time" AS response_time,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, response_time ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`826ddc90ef6ade97da6090d66fd44224f172f711a6e19abf2c006ad5017ad4a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Emergency Response Activation Time\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S83

类别 `data`；来源 `query_db`；调用 `15885b331b6746c4aed7fdc6101d8c5b`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Contact Location Type (Hospital/School/Mall)" AS loc_type,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, loc_type ORDER BY grp, n DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`24c85a7ac14241edcb5bee27f2937224ba261ad936777dbf488aaccc180ee4c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "ei", "kind": "base", "block": null, "base_tables": ["epidemiological_investigation"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "ei.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "ei.\"Contact Location Type (Hospital/School/Mall)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S84

类别 `data`；来源 `python`；调用 `2ff64c0b42214402945e2593743ac3ae`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`5131861596c37b7a3badb779d84ae61c872d94b6e7a383bd9ae1520944c951be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S85

类别 `data`；来源 `python`；调用 `2b4d7c4d70494ab68b73fd8a1e941925`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`5131861596c37b7a3badb779d84ae61c872d94b6e7a383bd9ae1520944c951be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S86

类别 `data`；来源 `python`；调用 `93d5cdd601ed48c8a06d6e51114586ac`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`5131861596c37b7a3badb779d84ae61c872d94b6e7a383bd9ae1520944c951be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S87

类别 `data`；来源 `python`；调用 `93d5cdd601ed48c8a06d6e51114586ac`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Data Completeness Score" AS score
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`c0cef5396b101821dcb3df8aca2ba90e50ca2d537d4735af24e68f8448f6d326`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S88

类别 `data`；来源 `python`；调用 `34fcae03813c4a708d2ef09465576573`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`5131861596c37b7a3badb779d84ae61c872d94b6e7a383bd9ae1520944c951be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S89

类别 `data`；来源 `python`；调用 `34fcae03813c4a708d2ef09465576573`；状态 `success`。

```sql

WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Data Completeness Score" AS score
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`c0cef5396b101821dcb3df8aca2ba90e50ca2d537d4735af24e68f8448f6d326`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "b.\"Case ID\" = co.\"Case ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |


## S90

类别 `data`；来源 `query_db`；调用 `054663f813ed46129c629799bc583103`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Laboratory Tests (CBC/Antibody Test)" AS lab,
  COUNT(*) AS n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END),1) AS pct
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, lab ORDER BY grp, lab;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`bf2df28740bd0fc976d30556b7fd5e61271a81a96fc86cae723171037167fa39`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Laboratory Tests (CBC/Antibody Test)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S91

类别 `data`；来源 `query_db`；调用 `49227718d7e14ea39c7b9e1bee1220ae`；状态 `success`。

```sql
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cm."Allergic Reaction Management" AS allergy,
  COUNT(*) AS n, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END),1) AS pct
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp, allergy ORDER BY grp, allergy;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-043/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`6e3c2027d0d04d6e9e6093239cd0a8566095ba78ba9c9c77d25d1dd1b2a796d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "clinical_manifestations", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}] | [] | ["\"Case ID\""] |
| B2 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["clinical_manifestations"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["clinical_manifestations"]}] | [{"type": "INNER", "right": "case_outcome AS co", "on": "cm.\"Case ID\" = co.\"Case ID\"", "using": []}] | ["CASE WHEN is_deceased = 1 THEN 'Deceased' ELSE 'Recovered' END", "cm.\"Allergic Reaction Management\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) | [] | [{"table": "clinical_manifestations", "column": "Outcome (Cured/Improved/Deceased)"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |

