# dacomp-005：逐轮FAD和后续SQL

仅以严格晚于当前轮次的成功SQL作为证据。每字段分别匹配，不表示整条查询等价。过滤只比较已知条件单项，不验证AND/OR组合。

| 轮次/候选 | 数据库接受 | FAD具体内容 | 分组后来有没有查 | 聚合后来有没有查 | 已知过滤条件后来有没有查 |
|---|---|---|---|---|---|
| Q1 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.Destination","sheet1.Date","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q1 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.Destination","sheet1.Date","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"status":"unknown"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（partial） |
| Q2 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.Destination","sheet1.Date","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"status":"unknown"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（partial） |
| Q2 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Destination"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"status":"unknown"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | Q4, Q19 | Q3, Q4, Q5, Q6, Q7, Q11, Q12, Q14, Q15, Q16, Q17, Q27 | 没有提供具体项（partial） |
| Q3 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Logistics Value-Added Service Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"sheet1.Sales Quantity","function":"avg"},{"column":"sheet1.Total Logistics Revenue","function":"avg"},{"column":"sheet1.Discount Amount","function":"avg"},{"column":"sheet1.Freight Cost","function":"avg"},{"column":"sheet1.Warehousing Cost","function":"avg"},{"column":"sheet1.Other Operating Costs","function":"avg"},{"column":"sheet1.Total Logistics Cost","function":"avg"},{"column":"sheet1.Profit","function":"avg"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | Q27 | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q3 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Logistics Value-Added Service Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"ge","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"sheet1.Sales Quantity","function":"avg"},{"column":"sheet1.Total Logistics Revenue","function":"avg"},{"column":"sheet1.Discount Amount","function":"avg"},{"column":"sheet1.Freight Cost","function":"avg"},{"column":"sheet1.Warehousing Cost","function":"avg"},{"column":"sheet1.Other Operating Costs","function":"avg"},{"column":"sheet1.Total Logistics Cost","function":"avg"},{"column":"sheet1.Profit","function":"avg"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | Q27 | Q25 |
| Q4 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Destination"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Destination","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | Q19 | Q5, Q6, Q7, Q11, Q12, Q14, Q15, Q16, Q17, Q27 | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q4 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | Q6, Q18 | Q5, Q6, Q7, Q11, Q12, Q14, Q15, Q16, Q17, Q27 | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q4 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q5 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Consigned Product"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Consigned Product","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"},{"column":"sheet1.Profit Margin","function":"avg"}],"status":"known"}<br>priority: high | Q6, Q18 | Q6, Q7, Q11, Q12, Q14, Q15, Q16, Q17, Q27 | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q5 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q5 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Destination"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q6 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Customer Age","sheet1.Age Range","sheet1.Customer Gender"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q6 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q7 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Age Range","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q7 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q7 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q8 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Age Range","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q8 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q8 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.Total Logistics Revenue","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q9 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Age Range","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q9 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q9 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Consigned Product","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q10 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Age Range","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q10 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Consigned Product","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q11 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[{"column":"sheet1.Customer Gender","type":"column"}],"status":"known"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | Q12 | Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28 | 没有提供具体项（none） |
| Q11 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Age Range"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q11 / 3 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Consigned Product","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q12 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Customer Gender","sheet1.Customer Age"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q12 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Total Logistics Revenue","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Logistics Value-Added Service Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q13, Q14, Q15, Q16, Q17, Q24 |
| Q13 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Total Logistics Revenue","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[{"column":"*","function":"count"}],"status":"known"}<br>priority: high | 没有提供具体项（none） | Q14, Q15, Q16, Q17, Q18, Q19, Q21, Q22, Q23, Q24, Q25, Q26, Q27, Q28 | Q14, Q15, Q16, Q17, Q24 |
| Q13 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q14, Q15, Q16, Q17, Q24 |
| Q14 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Total Logistics Revenue","sheet1.Sales Quantity","sheet1.Logistics Unit Price"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q15, Q16, Q17, Q24 |
| Q14 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Destination","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q15, Q16, Q17, Q24 |
| Q15 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Total Logistics Revenue","sheet1.Sales Quantity","sheet1.Logistics Unit Price","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q16, Q17, Q24 |
| Q16 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Total Logistics Revenue","sheet1.Sales Quantity","sheet1.Logistics Unit Price","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q17, Q24 |
| Q17 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Sales Quantity","sheet1.Freight Cost","sheet1.Warehousing Cost","sheet1.Other Operating Costs","sheet1.Total Logistics Cost","sheet1.Total Logistics Revenue","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Profit Margin","op":"lt","type":"predicate","value":{"literal":0.3976,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q24 |
| Q18 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Consigned Product","sheet1.Age Range","sheet1.Customer Gender","sheet1.Destination","sheet1.Discount Amount","sheet1.List Price Revenue"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Sales Quantity","op":"le","type":"predicate","value":{"literal":10,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | Q23 |
| Q19 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Destination","sheet1.Sales Quantity","sheet1.Freight Cost","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q19 / 2 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Date"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q20 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Discount Amount","sheet1.Sales Quantity","sheet1.List Price Revenue","sheet1.Logistics Unit Price","sheet1.Profit Margin"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q21 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Profit","sheet1.Total Logistics Revenue","sheet1.Sales Quantity"],"status":"known"}<br>filters: {"items":[],"status":"none"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: high | 没有提供具体项（none） | 没有提供具体项（none） | 没有提供具体项（none） |
| Q23 / 1 | 否，见原始错误 | tables: ["sheet1"]<br>columns: {"items":["sheet1.Profit Margin","sheet1.Sales Quantity","sheet1.Logistics Unit Price","sheet1.Discount Amount","sheet1.List Price Revenue","sheet1.Total Logistics Revenue","sheet1.Total Logistics Cost","sheet1.Freight Cost","sheet1.Profit"],"status":"known"}<br>filters: {"items":[{"column":"sheet1.Sales Quantity","op":"le","type":"predicate","value":{"literal":10,"status":"known"}}],"status":"partial"}<br>joins: {"items":[],"status":"none"}<br>group_by: {"items":[],"status":"none"}<br>aggregations: {"items":[],"status":"none"}<br>priority: medium | 没有提供具体项（none） | 没有提供具体项（none） | 未发现对应查询 |
| Q22 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q24 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q25 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q26 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q27 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |
| Q28 / 无可分析候选 | 否 | {"candidates":[],"status":"no_further_access"} | — | — | — |

## 实际SQL

### Q1（ok）

```sql
SELECT * FROM sheet1 LIMIT 10
```

### Q2（ok）

```sql
SELECT COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, MIN("Profit Margin") AS min_pm, MAX("Profit Margin") AS max_pm FROM sheet1
```

### Q3（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low_margin' ELSE 'normal' END AS grp, COUNT(*) AS n, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Discount Amount") AS avg_disc, AVG("List Price Revenue") AS avg_list, AVG("Logistics Unit Price") AS avg_unit_price, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY grp
```

### Q4（ok）

```sql
SELECT "Destination", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY "Destination" ORDER BY low_cnt DESC LIMIT 20
```

### Q5（ok）

```sql
SELECT substr("Destination", 1, instr("Destination", '-') - 1) AS region, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY region ORDER BY low_cnt DESC
```

### Q6（ok）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Profit Margin") AS avg_pm, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 GROUP BY "Consigned Product" ORDER BY low_cnt DESC
```

### Q7（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```

### Q8（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' ELSE 'qty_>10' END AS band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, AVG("Discount Amount") AS avg_disc, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Logistics Value-Added Service Revenue") AS avg_vas, AVG("Freight Cost" / NULLIF("Total Logistics Revenue", 0)) AS freight_share_rev, AVG("Warehousing Cost" / NULLIF("Total Logistics Revenue", 0)) AS wh_share_rev, AVG("Other Operating Costs" / NULLIF("Total Logistics Revenue", 0)) AS ooc_share_rev, AVG("Total Logistics Cost" / NULLIF("Total Logistics Revenue", 0)) AS cost_share_rev FROM sheet1 GROUP BY band
```

### Q9（ok）

```sql
SELECT strftime('%Y', "Date") AS year, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY year ORDER BY year
```

### Q10（ok）

```sql
SELECT strftime('%Y-%m', "Date") AS month, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY month ORDER BY month
```

### Q11（ok）

```sql
SELECT "Age Range", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Age Range" ORDER BY low_pct DESC
```

### Q12（ok）

```sql
SELECT "Customer Gender", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Profit Margin") AS avg_pm FROM sheet1 GROUP BY "Customer Gender"
```

### Q13（ok）

```sql
SELECT SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit_cnt, SUM(CASE WHEN "Profit Margin" < 0 THEN 1 ELSE 0 END) AS neg_pm_cnt, COUNT(*) AS n, AVG("Sales Quantity") AS avg_qty, MIN("Sales Quantity") AS min_qty, MAX("Sales Quantity") AS max_qty FROM sheet1 WHERE "Profit Margin" < 0.3976
```

### Q14（ok）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Discount Amount") AS avg_disc, AVG("List Price Revenue") AS avg_list FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q15（ok）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 AND "Sales Quantity" >= 13 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q16（ok）

```sql
SELECT "Sales Quantity", COUNT(*) AS n, AVG("Profit Margin") AS avg_pm, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 AND "Sales Quantity" >= 25 GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

### Q17（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'low_qty' ELSE 'high_qty' END AS qty_group, COUNT(*) AS n, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Freight Cost" / NULLIF("Total Logistics Revenue", 0)) AS freight_pct, AVG("Warehousing Cost" / NULLIF("Total Logistics Revenue", 0)) AS wh_pct, AVG("Other Operating Costs" / NULLIF("Total Logistics Revenue", 0)) AS ooc_pct, AVG(("Freight Cost" + "Warehousing Cost" + "Other Operating Costs") / NULLIF("Total Logistics Revenue", 0)) AS total_cost_pct, AVG("Profit Margin") AS avg_pm, AVG("Profit") AS avg_profit, AVG("Logistics Value-Added Service Revenue" / NULLIF("Total Logistics Revenue", 0)) AS vas_pct_rev FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY qty_group
```

### Q18（ok）

```sql
SELECT "Consigned Product", COUNT(*) AS n, SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) AS small_cnt, ROUND(100.0 * SUM(CASE WHEN "Sales Quantity" <= 10 THEN 1 ELSE 0 END) / COUNT(*), 2) AS small_pct, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt FROM sheet1 GROUP BY "Consigned Product" ORDER BY small_pct DESC
```

### Q19（ok）

```sql
SELECT "Destination", COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.3976 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct, AVG("Sales Quantity") AS avg_qty, AVG("Freight Cost") AS avg_freight FROM sheet1 GROUP BY "Destination" HAVING COUNT(*) >= 100 ORDER BY low_pct DESC LIMIT 15
```

### Q20（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, AVG("Discount Amount") AS avg_disc_abs, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Logistics Unit Price") AS avg_unit_price, AVG("List Price Revenue" / NULLIF("Sales Quantity", 0)) AS avg_list_per_unit FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```

### Q21（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, SUM("Profit") AS tot_profit, SUM("Total Logistics Revenue") AS tot_rev, SUM("Total Logistics Cost") AS tot_cost, SUM("Sales Quantity") AS tot_qty, ROUND(AVG("Profit"), 2) AS avg_profit FROM sheet1 GROUP BY grp
```

### Q22（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, SUM("Discount Amount") AS tot_disc, SUM("List Price Revenue") AS tot_list, SUM("Logistics Value-Added Service Revenue") AS tot_vas, SUM("Freight Cost") AS tot_freight, SUM("Warehousing Cost") AS tot_wh, SUM("Other Operating Costs") AS tot_ooc, SUM("Total Logistics Cost") AS tot_cost, SUM("Total Logistics Revenue") AS tot_rev, SUM("Profit") AS tot_profit, SUM("Sales Quantity") AS tot_qty, COUNT(*) AS n FROM sheet1 GROUP BY grp
```

### Q23（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.3976 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, AVG("Logistics Unit Price") AS avg_unit, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Total Logistics Cost") AS avg_cost, AVG("Total Logistics Revenue") AS avg_rev, AVG("Logistics Value-Added Service Revenue") AS avg_vas FROM sheet1 WHERE "Sales Quantity" <= 10 GROUP BY grp
```

### Q24（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'small' ELSE 'large' END AS sz, COUNT(*) AS n, AVG("Logistics Unit Price") AS avg_unit, AVG("Discount Amount" / NULLIF("List Price Revenue", 0)) AS avg_disc_rate, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Profit Margin" < 0.3976 GROUP BY sz
```

### Q25（ok）

```sql
SELECT COUNT(*) AS n_between FROM sheet1 WHERE "Profit Margin" >= 0.3976 AND "Profit Margin" < 0.3976434082191792
```

### Q26（ok）

```sql
SELECT COUNT(*) AS low_cnt_exact, SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit FROM sheet1 WHERE "Profit Margin" < 0.7952868164383584 * 0.5
```

### Q27（ok）

```sql
SELECT CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 'low' ELSE 'normal' END AS grp, COUNT(*) AS n, SUM("Profit") AS tot_profit, SUM("Total Logistics Revenue") AS tot_rev, SUM("Total Logistics Cost") AS tot_cost, SUM("Sales Quantity") AS tot_qty, AVG("Sales Quantity") AS avg_qty, AVG("Total Logistics Revenue") AS avg_rev, AVG("Total Logistics Cost") AS avg_cost, AVG("Profit") AS avg_profit, AVG("Profit Margin") AS avg_pm, AVG("Discount Amount") AS avg_disc, AVG("Logistics Unit Price") AS avg_unit, AVG("Freight Cost") AS avg_freight, AVG("Warehousing Cost") AS avg_wh, AVG("Other Operating Costs") AS avg_ooc, AVG("Logistics Value-Added Service Revenue") AS avg_vas FROM sheet1 GROUP BY grp
```

### Q28（ok）

```sql
SELECT CASE WHEN "Sales Quantity" <= 10 THEN 'qty_<=10' WHEN "Sales Quantity" <= 20 THEN 'qty_11-20' WHEN "Sales Quantity" <= 50 THEN 'qty_21-50' ELSE 'qty_>50' END AS qty_band, COUNT(*) AS n, SUM(CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 1 ELSE 0 END) AS low_cnt, ROUND(100.0 * SUM(CASE WHEN "Profit Margin" < 0.7952868164383584 * 0.5 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct FROM sheet1 GROUP BY qty_band ORDER BY MIN("Sales Quantity")
```
