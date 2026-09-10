# dacomp-006：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Destination","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q14 | Q2, Q3, Q4, Q9, Q12, Q17, Q19, Q25, Q30 | 没有提供具体项（none） |
| Q1 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q3, Q9, Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q3, Q4, Q7, Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | 没有提供具体项（none） |
| Q2 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Destination"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q3, Q9, Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q3, Q4, Q7, Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | 没有提供具体项（none） |
| Q3 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q9, Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q4, Q7, Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q4, Q5, Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q3 / 2 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q4, Q14, Q22 | Q4, Q7, Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q4, Q5, Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q4 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"}],"status":"known"}<br>priority: high | Q7, Q13, Q15, Q21 | Q7, Q9, Q12, Q17 | Q5, Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q4 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit Margin","function":"avg"},{"column":"sheet1.Discount Amount","function":"sum"},{"column":"sheet1.Logistics Unit Price","function":"sum"}],"status":"known"}<br>priority: medium | Q9, Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | 未发现对应查询 | Q5, Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q5 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"}],"status":"known"}<br>priority: high | Q7, Q13, Q15, Q21 | Q7, Q9, Q12, Q17 | Q6, Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q6 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Total Logistics Cost","function":"sum"},{"column":"sheet1.Discount Amount","function":"sum"}],"status":"known"}<br>priority: high | Q9, Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q9 | Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q6 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"}],"status":"known"}<br>priority: high | Q7, Q13, Q15, Q21 | Q7, Q9, Q12, Q17 | Q7, Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q7 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q9, Q12, Q17 | Q8, Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q8 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q8 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q9, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q9, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q9 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.Sales Quantity","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Logistics Value-Added Service Revenue","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Total Logistics Cost","function":"sum"},{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Discount Amount","function":"sum"},{"column":"sheet1.List Price Revenue","function":"sum"},{"column":"sheet1.Logistics Value-Added Service Revenue","function":"sum"},{"column":"sheet1.Freight Cost","function":"sum"},{"column":"sheet1.Warehousing Cost","function":"sum"},{"column":"sheet1.Other Operating Costs","function":"sum"}],"status":"known"}<br>priority: high | Q11, Q12, Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | 未发现对应查询 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q9 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q9 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q10 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q10 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q10 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | Q11, Q19 | Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q11 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q11 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q12 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q12 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q13, Q15, Q21 | Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q13 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q15, Q21 | Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q13 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q14, Q22 | Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q13 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Total Logistics Cost","function":"sum"}],"status":"known"}<br>priority: high | Q15, Q21 | Q17 | Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q14 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q22 | Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q14 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q15, Q21 | Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q15, Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q15 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q21 | Q16, Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q15 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Total Logistics Revenue","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: medium | Q21 | Q19 | Q16, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q16 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q22 | Q17, Q18, Q19, Q21, Q22, Q25, Q27, Q28 | Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q16 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q17 | Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q16 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit Margin","function":"avg"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"}],"status":"known"}<br>priority: medium | Q17, Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q19 | Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q17 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q19, Q21, Q22, Q24, Q27, Q28, Q30 | 未发现对应查询 | Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q17 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit Margin","function":"avg"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"}],"status":"known"}<br>priority: medium | Q19, Q21, Q22, Q24, Q27, Q28, Q30 | Q19 | Q18, Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q18 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q22 | Q19, Q21, Q22, Q25, Q27, Q28 | Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q18 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q21 | Q19, Q21, Q22, Q25, Q27, Q28 | Q19, Q20, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q18 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue"],"status":"known"}<br>filters: {"items":[{"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}},{"column":"sheet1.Date","op":"between","type":"predicate","value":{"literal":["2023-10-01","2023-10-31"],"status":"known"}}],"type":"and"}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | Q19 | 未发现对应查询 |
| Q19 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue"],"status":"known"}<br>filters: {"items":[{"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}},{"column":"sheet1.Date","op":"between","type":"predicate","value":{"literal":["2023-10-01","2023-10-31"],"status":"known"}}],"type":"and"}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | 未发现对应查询 | 未发现对应查询 |
| Q20 / 1 | 是 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Waybill Number","sheet1.Destination","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[{"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}},{"column":"sheet1.Date","op":"between","type":"predicate","value":{"literal":["2023-10-01","2023-10-31"],"status":"known"}}],"type":"and"}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: medium | 没有提供具体项（none） | 未发现对应查询 | 未发现对应查询 |
| Q21 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q21 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | Q22 | Q22, Q25, Q27, Q28 | Q22, Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q22 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q22 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q25, Q27, Q28 | Q23, Q24, Q25, Q26, Q27, Q29, Q30 |
| Q23 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q25, Q27, Q28 | Q24, Q25, Q26, Q27, Q29, Q30 |
| Q23 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q25, Q27, Q28 | Q24, Q25, Q26, Q27, Q29, Q30 |
| Q24 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q25, Q27, Q28 | Q25, Q26, Q27, Q29, Q30 |
| Q24 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q25, Q27, Q28 | Q25, Q26, Q27, Q29, Q30 |
| Q25 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q27, Q28 | Q26, Q27, Q29, Q30 |
| Q25 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q27, Q28 | Q26, Q27, Q29, Q30 |
| Q26 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"sheet1.Sales Quantity","function":"sum"},{"column":"sheet1.Total Logistics Revenue","function":"sum"},{"column":"sheet1.Total Logistics Cost","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | Q27, Q29, Q30 |
| Q26 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"*","function":"count"}],"status":"known"}<br>priority: medium | Q27, Q28, Q30 | 未发现对应查询 | Q27, Q29, Q30 |
| Q27 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q28 | Q29, Q30 |
| Q27 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Destination","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | Q28 | Q29, Q30 |
| Q28 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"},{"column":"*","function":"count"}],"status":"known"}<br>priority: medium | Q30 | 未发现对应查询 | Q29, Q30 |
| Q28 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Consigned Product","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"},{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Profit","function":"sum"}],"status":"known"}<br>priority: high | 未发现对应查询 | 未发现对应查询 | Q29, Q30 |
| Q29 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue"],"status":"known"}<br>filters: {"items":[{"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}},{"column":"sheet1.Date","op":"between","type":"predicate","value":{"literal":["2023-08-01","2023-08-31"],"status":"known"}}],"type":"and"}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"min"},{"column":"sheet1.Profit Margin","function":"max"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: low | 没有提供具体项（none） | 未发现对应查询 | 未发现对应查询 |
| Q29 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Date","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Destination","op":"like","type":"predicate","value":{"literal":"South China%","status":"known"}}],"status":"known"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Date","type":"time_bucket","unit":"month"}],"status":"known"}<br>aggregations: {"items":[{"column":"sheet1.Freight Cost","function":"sum"},{"column":"sheet1.Warehousing Cost","function":"sum"},{"column":"sheet1.Other Operating Costs","function":"sum"}],"status":"known"}<br>priority: low | Q30 | Q30 | Q30 |
| Q30 / 无可分析候选 | 是 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT Destination, COUNT(*) AS cnt FROM sheet1 GROUP BY Destination ORDER BY cnt DESC
```

### Q2（ok）

```sql
SELECT MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(*) AS total_rows FROM sheet1
```

### Q3（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS total_profit, COUNT(*) AS orders, SUM("Total Logistics Revenue") AS revenue, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q4（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit, COUNT(*) AS orders FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month, Destination ORDER BY month, Destination
```

### Q5（ok）

```sql
SELECT DISTINCT "Consigned Product" FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY 1
```

### Q6（ok）

```sql
SELECT DISTINCT Destination FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY Destination
```

### Q7（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product", SUM(Profit) AS profit, SUM("Sales Quantity") AS qty, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month, "Consigned Product" ORDER BY month, "Consigned Product"
```

### Q8（ok）

```sql
SELECT Destination FROM (SELECT DISTINCT Destination FROM sheet1 WHERE Destination LIKE 'South China%') ORDER BY Destination
```

### Q9（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, SUM("Total Logistics Revenue") AS revenue, SUM("List Price Revenue") AS list_price, SUM("Logistics Value-Added Service Revenue") AS vas_revenue, SUM("Discount Amount") AS discount, SUM("Total Logistics Cost") AS cost, SUM("Freight Cost") AS freight, SUM("Warehousing Cost") AS warehousing, SUM("Other Operating Costs") AS other_cost, SUM(Profit) AS profit, SUM("Sales Quantity") AS qty, COUNT(*) AS orders FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q10（db_error）

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

### Q11（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct, SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct, SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q12（ok）

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

### Q13（ok）

```sql
SELECT "Consigned Product", 
  ROUND(AVG(profit),0) AS avg_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct,
  MIN(profit) AS min_m, MAX(profit) AS max_m,
  ROUND(MAX(profit)-MIN(profit),0) AS range_m,
  SUM(profit) AS total_profit,
  SUM(qty) AS total_qty
FROM (
  SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY month, product
)
GROUP BY product ORDER BY std_monthly_profit DESC
```

### Q14（ok）

```sql
SELECT Destination,
  ROUND(AVG(profit),0) AS avg_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,
  ROUND(MAX(profit)-MIN(profit),0) AS range_m,
  SUM(profit) AS total_profit
FROM (
  SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY month, Destination
)
GROUP BY Destination ORDER BY std_monthly_profit DESC LIMIT 20
```

### Q15（ok）

```sql
SELECT product AS prod, 
  ROUND(AVG(profit),0) AS avg_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_monthly_profit,
  ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/NULLIF(AVG(profit),0)*100,1) AS cv_pct,
  ROUND(MIN(profit),0) AS min_m, ROUND(MAX(profit),0) AS max_m,
  ROUND(MAX(profit)-MIN(profit),0) AS range_m,
  SUM(profit) AS total_profit, SUM(qty) AS total_qty
FROM (
  SELECT strftime('%Y-%m', Date) AS month, "Consigned Product" AS product, 
    SUM(Profit) AS profit, SUM("Sales Quantity") AS qty
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY month, product
)
GROUP BY product ORDER BY std_monthly_profit DESC
```

### Q16（ok）

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region, strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY region, month ORDER BY region, month
```

### Q17（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order, ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order, ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit, ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit, ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q18（ok）

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region, strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY region, month ORDER BY region, month
```

### Q19（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS n, ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct, ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct, ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct, ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q20（ok）

```sql
SELECT "Waybill Number", Date, Destination, "Consigned Product", "Sales Quantity", "Total Logistics Revenue", "Total Logistics Cost", Profit, "Profit Margin" FROM sheet1 WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10' ORDER BY "Profit Margin" DESC LIMIT 10
```

### Q21（ok）

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
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY month, prod
) GROUP BY month ORDER BY month
```

### Q22（ok）

```sql
SELECT month, 
  SUM(CASE WHEN dest LIKE '%Guangdong%' THEN profit END) AS guangdong,
  SUM(CASE WHEN dest LIKE '%Guangxi%' THEN profit END) AS guangxi,
  SUM(CASE WHEN dest LIKE '%Hainan%' THEN profit END) AS hainan,
  SUM(CASE WHEN dest LIKE '%Henan%' THEN profit END) AS henan,
  SUM(CASE WHEN dest NOT LIKE '%Guangdong%' AND dest NOT LIKE '%Guangxi%' AND dest NOT LIKE '%Hainan%' AND dest NOT LIKE '%Henan%' THEN profit END) AS other
FROM (
  SELECT strftime('%Y-%m', Date) AS month, Destination AS dest, SUM(Profit) AS profit
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY month, dest
) GROUP BY month ORDER BY month
```

### Q23（ok）

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY province
```

### Q24（ok）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price, ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price, SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct, SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q25（ok）

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province, COUNT(*) AS orders, ROUND(SUM(Profit),0) AS total_profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY province ORDER BY total_profit DESC
```

### Q26（ok）

```sql
SELECT "Consigned Product", ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit, ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit, ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY "Consigned Product" ORDER BY avg_profit_per_unit DESC
```

### Q27（ok）

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
  FROM sheet1 WHERE Destination LIKE 'South China%'
  GROUP BY province, month
) GROUP BY month ORDER BY month
```

### Q28（ok）

```sql
SELECT 'Guangdong' AS prov, ROUND(AVG(profit),0) AS avg_p, ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0) AS std_p, ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) AS cv_pct FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Guangdong%' GROUP BY month)
UNION ALL
SELECT 'Guangxi', ROUND(AVG(profit),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Guangxi%' GROUP BY month)
UNION ALL
SELECT 'Hainan', ROUND(AVG(profit),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Hainan%' GROUP BY month)
UNION ALL
SELECT 'Henan', ROUND(AVG(profit),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Henan%' GROUP BY month)
UNION ALL
SELECT 'Hubei', ROUND(AVG(profit),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Hubei%' GROUP BY month)
UNION ALL
SELECT 'Hunan', ROUND(AVG(profit),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit)),0), ROUND(SQRT(AVG(profit*profit)-AVG(profit)*AVG(profit))/AVG(profit)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China-Hunan%' GROUP BY month)
```

### Q29（ok）

```sql
SELECT "Waybill Number", Date, Destination, "Consigned Product", "Total Logistics Revenue", "Total Logistics Cost", Profit, "Profit Margin" FROM sheet1 WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5 ORDER BY "Profit Margin" LIMIT 5
```

### Q30（ok）

```sql
SELECT 'Freight' AS cost_type, ROUND(AVG(val),0) AS avg, ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std, ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Warehousing', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Other Costs', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Orders', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
```
