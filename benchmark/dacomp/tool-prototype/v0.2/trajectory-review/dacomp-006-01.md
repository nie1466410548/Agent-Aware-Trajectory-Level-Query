# dacomp-006-01：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Destination<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19<br>过滤：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18 |
| Q1 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Logistics Unit Price, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q4、Q9、Q14、Q18<br>聚合：Q4 |
| Q1 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"（只描述了部分）<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity) | 列：后续未找到全部所述项同时出现<br>过滤：Q2、Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q5、Q16<br>聚合：Q4、Q5、Q8、Q10、Q11、Q12、Q13、Q14、Q19 |
| Q2 / 候选1 | 读取：sheet1.Destination<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19<br>过滤：Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18 |
| Q2 / 候选2 | 读取：sheet1.Destination<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：未提供（none） | 列：Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19<br>过滤：Q3、Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18 |
| Q3 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit) | 列：Q4、Q5、Q8、Q9、Q10、Q12、Q13、Q14、Q16、Q17、Q18、Q19<br>过滤：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q4、Q9、Q14、Q18<br>聚合：Q4、Q5、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q16、Q17、Q18、Q19 |
| Q3 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount)、SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q4、Q9、Q14、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q3 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：后续未找到全部所述项同时出现<br>过滤：Q4、Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q5、Q16<br>聚合：Q4、Q8、Q11、Q14 |
| Q4 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount)、SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q9、Q14、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q4 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：后续未找到全部所述项同时出现<br>过滤：Q5、Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q5、Q16<br>聚合：Q8、Q11、Q14 |
| Q5 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q16<br>聚合：后续未找到全部所述项同时出现 |
| Q5 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q11、Q16<br>聚合：Q8、Q10、Q12、Q13、Q19 |
| Q5 / 候选3 | 读取：sheet1.Age Range, sheet1.Customer Age, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount) | 列：后续未找到全部所述项同时出现<br>过滤：Q6、Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q10<br>聚合：Q11 |
| Q6 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q14<br>过滤：Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q19<br>聚合：后续未找到全部所述项同时出现 |
| Q6 / 候选2 | 读取：sheet1.Age Range, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Discount Amount)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q10<br>聚合：后续未找到全部所述项同时出现 |
| Q6 / 候选3 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost) | 列：后续未找到全部所述项同时出现<br>过滤：Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q13<br>聚合：Q11、Q14 |
| Q6 / 候选4 | 读取：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit) | 列：Q9<br>过滤：Q7、Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q9、Q14、Q18<br>聚合：Q9 |
| Q7 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q14<br>过滤：Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q19<br>聚合：后续未找到全部所述项同时出现 |
| Q7 / 候选2 | 读取：sheet1.Age Range, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q10<br>聚合：Q8、Q10、Q12、Q13、Q19 |
| Q7 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit) | 列：Q9<br>过滤：Q8、Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q9、Q14、Q18<br>聚合：Q9 |
| Q8 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q14<br>过滤：Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q19<br>聚合：后续未找到全部所述项同时出现 |
| Q8 / 候选2 | 读取：sheet1.Age Range, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q10<br>聚合：Q10、Q12、Q13、Q19 |
| Q8 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit) | 列：Q9<br>过滤：Q9、Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q9、Q14、Q18<br>聚合：Q9 |
| Q9 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q10<br>聚合：Q10、Q12、Q13、Q19 |
| Q9 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Total Logistics Cost, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit) | 列：后续未找到全部所述项同时出现<br>过滤：Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q14、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q9 / 候选3 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q13<br>过滤：Q10、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q13<br>聚合：Q10、Q12、Q13、Q19 |
| Q10 / 候选1 | 读取：sheet1.Age Range, sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Age Range<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q12、Q13、Q19 |
| Q10 / 候选2 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q13<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q13<br>聚合：Q12、Q13、Q19 |
| Q10 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q11<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q11、Q16<br>聚合：Q12、Q13、Q19 |
| Q11 / 候选1 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q13<br>过滤：Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q13<br>聚合：Q12、Q13、Q19 |
| Q11 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Discount Amount)、SUM(sheet1.List Price Revenue)、SUM(sheet1.Total Logistics Cost) | 列：后续未找到全部所述项同时出现<br>过滤：Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q16<br>聚合：后续未找到全部所述项同时出现 |
| Q11 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q12、Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q16<br>聚合：Q12、Q13、Q19 |
| Q12 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按日<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q13、Q14、Q19<br>过滤：Q13、Q14、Q15、Q16、Q17、Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q13、Q19 |
| Q12 / 候选2 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q13<br>过滤：Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q13<br>聚合：Q13、Q19 |
| Q12 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：AVG(sheet1.Profit)、AVG(sheet1.Profit Margin)、AVG(sheet1.Logistics Unit Price) | 列：后续未找到全部所述项同时出现<br>过滤：Q13、Q14、Q15、Q16、Q17、Q18<br>分组：Q14、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q13 / 候选1 | 读取：sheet1.Customer Gender, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Customer Gender<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q14、Q15、Q16、Q17、Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q13 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：AVG(sheet1.Profit)、AVG(sheet1.Profit Margin)、AVG(sheet1.Logistics Unit Price) | 列：后续未找到全部所述项同时出现<br>过滤：Q14、Q15、Q16、Q17、Q18<br>分组：Q14、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q13 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q14、Q15、Q16、Q17、Q18<br>分组：Q14、Q18<br>聚合：Q19 |
| Q14 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost) | 列：后续未找到全部所述项同时出现<br>过滤：Q15、Q16、Q17、Q18<br>分组：Q16<br>聚合：后续未找到全部所述项同时出现 |
| Q14 / 候选2 | 读取：sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：MIN(sheet1.Profit)、MAX(sheet1.Profit)、AVG(sheet1.Profit)、COUNT(*) | 列：Q15、Q16、Q17、Q18、Q19<br>过滤：Q15、Q16、Q17、Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q14 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.List Price Revenue, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Discount Amount)、SUM(sheet1.List Price Revenue)、SUM(sheet1.Total Logistics Revenue) | 列：后续未找到全部所述项同时出现<br>过滤：Q15、Q16、Q17、Q18<br>分组：Q18<br>聚合：后续未找到全部所述项同时出现 |
| Q15 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q16、Q17、Q18<br>分组：Q16<br>聚合：Q19 |
| Q15 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q16、Q17、Q18<br>分组：Q16<br>聚合：Q19 |
| Q16 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q17、Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q16 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q17、Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q17 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q17 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：Q18<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q18 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q19 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q19 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT DISTINCT "Destination" FROM sheet1 ORDER BY "Destination"
```

### Q2（成功）

```sql
SELECT DISTINCT "Destination" FROM sheet1 WHERE "Destination" LIKE 'South%' ORDER BY "Destination"
```

### Q3（成功）

```sql
SELECT MIN("Date") as min_date, MAX("Date") as max_date FROM sheet1 WHERE "Destination" LIKE 'South%'
```

### Q4（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, SUM("Profit") as total_profit, SUM("Total Logistics Revenue") as total_revenue, SUM("Total Logistics Cost") as total_cost, SUM("Sales Quantity") as total_qty, SUM("Discount Amount") as total_discount, COUNT(*) as order_count FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month ORDER BY month
```

### Q5（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, "Consigned Product" as product, SUM("Profit") as profit, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month, product ORDER BY product, month
```

### Q6（成功）

```sql
SELECT substr("Destination", 1, instr("Destination", '-')-1) as region, COUNT(DISTINCT substr("Destination", instr("Destination", '-')+1, instr(substr("Destination", instr("Destination", '-')+1), '-')-1)) as provinces FROM sheet1 WHERE "Destination" LIKE 'South%'
```

### Q7（成功）

```sql
SELECT DISTINCT substr("Destination", instr("Destination", '-')+1, instr(substr("Destination", instr("Destination", '-')+1), '-')-1) as province FROM sheet1 WHERE "Destination" LIKE 'South%' ORDER BY province
```

### Q8（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, substr("Destination", instr("Destination", '-')+1, instr(substr("Destination", instr("Destination", '-')+1), '-')-1) as province, SUM("Profit") as profit, SUM("Total Logistics Revenue") as revenue, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month, province ORDER BY province, month
```

### Q9（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, SUM("Freight Cost") as freight, SUM("Warehousing Cost") as warehousing, SUM("Other Operating Costs") as other_costs, SUM("Total Logistics Cost") as total_cost, SUM("Profit") as profit FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month ORDER BY month
```

### Q10（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, "Age Range" as age, SUM("Profit") as profit, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month, age ORDER BY age, month
```

### Q11（成功）

```sql
SELECT "Consigned Product" as product, SUM("Profit") as profit, SUM("Sales Quantity") as qty, SUM("List Price Revenue") as list_rev, SUM("Discount Amount") as discount, SUM("Total Logistics Revenue") as rev, SUM("Total Logistics Cost") as cost FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY product ORDER BY profit DESC
```

### Q12（成功）

```sql
SELECT "Date" as day, SUM("Profit") as profit, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY day ORDER BY profit DESC LIMIT 30
```

### Q13（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, "Customer Gender" as gender, SUM("Profit") as profit, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month, gender ORDER BY gender, month
```

### Q14（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, SUM("Profit") as profit, SUM("Sales Quantity") as qty, SUM("Total Logistics Revenue") as rev, SUM("Total Logistics Cost") as cost, ROUND(SUM("Profit")*1.0/SUM("Sales Quantity"), 2) as profit_per_unit FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY month ORDER BY month
```

### Q15（成功）

```sql
SELECT COUNT(*) as total_rows, SUM(CASE WHEN ABS(("Profit" + "Total Logistics Cost") - "Total Logistics Revenue") > 0.01 THEN 1 ELSE 0 END) as inconsistent, MIN("Profit") as min_profit, MAX("Profit") as max_profit, SUM(CASE WHEN "Profit" <= 0 THEN 1 ELSE 0 END) as non_positive_profit_rows FROM sheet1 WHERE "Destination" LIKE 'South%'
```

### Q16（成功）

```sql
SELECT product, COUNT(*) as n, MIN(p) as min_p, MAX(p) as max_p, ROUND(AVG(p),0) as avg_p, ROUND(SQRT(AVG(p*p) - AVG(p)*AVG(p)),0) as std_p, ROUND((SQRT(AVG(p*p) - AVG(p)*AVG(p)))/AVG(p)*100,1) as cv_pct FROM (SELECT "Consigned Product" as product, strftime('%Y-%m', "Date") as m, SUM("Profit") as p FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY product, m) GROUP BY product ORDER BY cv_pct DESC
```

### Q17（成功）

```sql
SELECT province, COUNT(*) as n, MIN(p) as min_p, MAX(p) as max_p, ROUND(AVG(p),0) as avg_p, ROUND(SQRT(AVG(p*p) - AVG(p)*AVG(p)),0) as std_p, ROUND((SQRT(AVG(p*p) - AVG(p)*AVG(p)))/AVG(p)*100,1) as cv_pct FROM (SELECT substr("Destination", instr("Destination", '-')+1, instr(substr("Destination", instr("Destination", '-')+1), '-')-1) as province, strftime('%Y-%m', "Date") as m, SUM("Profit") as p FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY province, m) GROUP BY province ORDER BY avg_p DESC
```

### Q18（成功）

```sql
SELECT ROUND(AVG(p),0) as avg_profit, ROUND(MIN(p),0) as min_profit, ROUND(MAX(p),0) as max_profit, ROUND(SQRT(AVG(p*p) - AVG(p)*AVG(p)),0) as std_profit, ROUND((SQRT(AVG(p*p) - AVG(p)*AVG(p)))/AVG(p)*100,1) as cv_pct FROM (SELECT strftime('%Y-%m', "Date") as m, SUM("Profit") as p FROM sheet1 WHERE "Destination" LIKE 'South%' GROUP BY m)
```

### Q19（成功）

```sql
SELECT strftime('%Y-%m', "Date") as month, "Destination" as city, SUM("Profit") as profit, SUM("Sales Quantity") as qty, COUNT(*) as orders FROM sheet1 WHERE "Destination" LIKE 'South China-Guangdong%' GROUP BY month, city ORDER BY profit DESC LIMIT 60
```
