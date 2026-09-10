# dacomp-006-02：每个候选到底预测了什么

只比较当前轮之后的成功SQL。忽略接口是否接收；解开JSON字符串，唯一可确定的列名补齐表前缀，并收集操作字段已明确引用的列。不从列名猜测分组或聚合。
下表逐字段列出对应查询，不等于整个候选准确；未提供不算预测成功。过滤按已知条件单项核对，复杂表达式及相近但不相同的方向见总报告人工解释。

| 提出预测的轮次/候选 | FAD具体说了什么 | 后续SQL证据（字段分别核对） |
|---|---|---|
| Q1 / 候选1 | 读取：sheet1.Date, sheet1.Destination<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Destination<br>聚合：COUNT(*) | 列：Q3、Q4、Q7、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q24、Q27、Q28、Q29、Q30<br>分组：Q14<br>聚合：Q2、Q3、Q4、Q9、Q12、Q17、Q19、Q25、Q30 |
| Q1 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit) | 列：Q3、Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>分组：Q3、Q9、Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q3、Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q2 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：未提供（none）<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit) | 列：Q3、Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>分组：Q3、Q9、Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q3、Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q3 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit) | 列：Q7、Q9、Q12、Q17、Q20<br>过滤：Q4、Q5、Q6、Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q9、Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q3 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q4、Q5、Q6、Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q4、Q14、Q22<br>聚合：Q4、Q7、Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q4 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：Q7、Q20<br>过滤：Q5、Q6、Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q7、Q13、Q15、Q21<br>聚合：Q7、Q9、Q12、Q17 |
| Q4 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Logistics Unit Price, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：AVG(sheet1.Profit Margin)、SUM(sheet1.Discount Amount)、SUM(sheet1.Logistics Unit Price) | 列：后续未找到全部所述项同时出现<br>过滤：Q5、Q6、Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q9、Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：后续未找到全部所述项同时出现 |
| Q5 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：Q7、Q20<br>过滤：Q6、Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q7、Q13、Q15、Q21<br>聚合：Q7、Q9、Q12、Q17 |
| Q6 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Discount Amount) | 列：后续未找到全部所述项同时出现<br>过滤：Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q9、Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q9 |
| Q6 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：Q7、Q20<br>过滤：Q7、Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q7、Q13、Q15、Q21<br>聚合：Q7、Q9、Q12、Q17 |
| Q7 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue) | 列：Q20<br>过滤：Q8、Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q9、Q12、Q17 |
| Q8 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q8 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q15、Q20、Q21、Q29<br>过滤：Q9、Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q9、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q9 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Discount Amount, sheet1.Freight Cost, sheet1.List Price Revenue, sheet1.Logistics Value-Added Service Revenue, sheet1.Other Operating Costs, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost)、SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Discount Amount)、SUM(sheet1.List Price Revenue)、SUM(sheet1.Logistics Value-Added Service Revenue)、SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs) | 列：后续未找到全部所述项同时出现<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q11、Q12、Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：后续未找到全部所述项同时出现 |
| Q9 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q9 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q15、Q20、Q21、Q29<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q10 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q10 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q15、Q20、Q21、Q29<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q10 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：AVG(sheet1.Profit Margin) | 列：Q20<br>过滤：Q11、Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>聚合：Q11、Q19 |
| Q11 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q11 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q15、Q20、Q21、Q29<br>过滤：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q12、Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q12 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q12 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q13、Q15、Q20、Q21、Q29<br>过滤：Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q13、Q15、Q21<br>聚合：Q13、Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q13 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q15、Q20、Q21、Q29<br>过滤：Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q15、Q21<br>聚合：Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q13 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q14、Q22<br>聚合：Q14、Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q13 / 候选3 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost) | 列：Q20<br>过滤：Q14、Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q15、Q21<br>聚合：Q17 |
| Q14 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q22<br>聚合：Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q14 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q15、Q20、Q21、Q29<br>过滤：Q15、Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q15、Q21<br>聚合：Q15、Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q15 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q20、Q21、Q29<br>过滤：Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q21<br>聚合：Q16、Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q15 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：AVG(sheet1.Profit Margin) | 列：Q20、Q29<br>过滤：Q16、Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q21<br>聚合：Q19 |
| Q16 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q17、Q18、Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q22<br>聚合：Q17、Q18、Q19、Q21、Q22、Q25、Q27、Q28 |
| Q16 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q17、Q20<br>过滤：Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q17 |
| Q16 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：AVG(sheet1.Profit Margin)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin) | 列：Q19、Q20、Q29<br>过滤：Q17、Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q17、Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q19 |
| Q17 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Sales Quantity)、COUNT(*) | 列：Q20<br>过滤：Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：后续未找到全部所述项同时出现 |
| Q17 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：AVG(sheet1.Profit Margin)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin) | 列：Q19、Q20、Q29<br>过滤：Q18、Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q19、Q21、Q22、Q24、Q27、Q28、Q30<br>聚合：Q19 |
| Q18 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q19、Q20、Q21、Q22、Q27、Q28、Q29<br>过滤：Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q22<br>聚合：Q19、Q21、Q22、Q25、Q27、Q28 |
| Q18 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q20、Q21、Q29<br>过滤：Q19、Q20、Q21、Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q21<br>聚合：Q19、Q21、Q22、Q25、Q27、Q28 |
| Q18 / 候选3 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin) | 列：Q19、Q20、Q29<br>过滤：后续未找到全部所述项同时出现<br>聚合：Q19 |
| Q19 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin) | 列：Q20、Q29<br>过滤：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q20 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue, sheet1.Waybill Number<br>过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-10-01", "2023-10-31"])<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin) | 列：Q29<br>过滤：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q21 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、AVG(sheet1.Profit Margin) | 列：后续未找到全部所述项同时出现<br>过滤：Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q21 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q22、Q27、Q28、Q29<br>过滤：Q22、Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：Q22<br>聚合：Q22、Q25、Q27、Q28 |
| Q22 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Sales Quantity<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、AVG(sheet1.Profit Margin) | 列：后续未找到全部所述项同时出现<br>过滤：Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q22 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q27、Q28、Q29<br>过滤：Q23、Q24、Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q25、Q27、Q28 |
| Q23 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q29<br>过滤：Q24、Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q25、Q27、Q28 |
| Q23 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q27、Q28、Q29<br>过滤：Q24、Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q25、Q27、Q28 |
| Q24 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q29<br>过滤：Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q25、Q27、Q28 |
| Q24 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q27、Q28、Q29<br>过滤：Q25、Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q25、Q27、Q28 |
| Q25 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q27、Q28、Q29<br>过滤：Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q27、Q28 |
| Q25 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q29<br>过滤：Q26、Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q27、Q28 |
| Q26 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Sales Quantity, sheet1.Total Logistics Cost, sheet1.Total Logistics Revenue<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit)、SUM(sheet1.Sales Quantity)、SUM(sheet1.Total Logistics Revenue)、SUM(sheet1.Total Logistics Cost) | 列：后续未找到全部所述项同时出现<br>过滤：Q27、Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q26 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、COUNT(*) | 列：Q29<br>过滤：Q27、Q29、Q30<br>分组：Q27、Q28、Q30<br>聚合：后续未找到全部所述项同时出现 |
| Q27 / 候选1 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q29<br>过滤：Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q28 |
| Q27 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Destination<br>聚合：SUM(sheet1.Profit) | 列：Q28、Q29<br>过滤：Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：Q28 |
| Q28 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Profit)、COUNT(*) | 列：Q29<br>过滤：Q29、Q30<br>分组：Q30<br>聚合：后续未找到全部所述项同时出现 |
| Q28 / 候选2 | 读取：sheet1.Consigned Product, sheet1.Date, sheet1.Destination, sheet1.Profit<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月 ＋ sheet1.Consigned Product<br>聚合：SUM(sheet1.Profit) | 列：Q29<br>过滤：Q29、Q30<br>分组：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q29 / 候选1 | 读取：sheet1.Date, sheet1.Destination, sheet1.Profit, sheet1.Profit Margin, sheet1.Total Logistics Revenue<br>过滤：(sheet1.Destination like "South China%" 且 sheet1.Date between ["2023-08-01", "2023-08-31"])<br>连接：未提供（none）<br>分组：未提供（none）<br>聚合：COUNT(*)、MIN(sheet1.Profit Margin)、MAX(sheet1.Profit Margin)、AVG(sheet1.Profit Margin) | 列：后续未找到全部所述项同时出现<br>过滤：后续未找到全部所述项同时出现<br>聚合：后续未找到全部所述项同时出现 |
| Q29 / 候选2 | 读取：sheet1.Date, sheet1.Destination, sheet1.Freight Cost, sheet1.Other Operating Costs, sheet1.Total Logistics Cost, sheet1.Warehousing Cost<br>过滤：sheet1.Destination like "South China%"<br>连接：未提供（none）<br>分组：sheet1.Date按月<br>聚合：SUM(sheet1.Freight Cost)、SUM(sheet1.Warehousing Cost)、SUM(sheet1.Other Operating Costs) | 列：后续未找到全部所述项同时出现<br>过滤：Q30<br>分组：Q30<br>聚合：Q30 |
| Q30 | 没有候选：no_further_access | — |

## 实际SQL（保留失败轮次，失败SQL不作为发生证据）

### Q1（成功）

```sql
SELECT Destination, COUNT(*) AS cnt FROM sheet1 GROUP BY Destination ORDER BY cnt DESC
```

### Q2（成功）

```sql
SELECT MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(*) AS total_rows FROM sheet1
```

### Q3（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, SUM(Profit) AS total_profit, COUNT(*) AS orders, SUM("Total Logistics Revenue") AS revenue, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q4（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, Destination, SUM(Profit) AS profit, COUNT(*) AS orders FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month, Destination ORDER BY month, Destination
```

### Q5（成功）

```sql
SELECT DISTINCT "Consigned Product" FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY 1
```

### Q6（成功）

```sql
SELECT DISTINCT Destination FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY Destination
```

### Q7（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, "Consigned Product", SUM(Profit) AS profit, SUM("Sales Quantity") AS qty, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month, "Consigned Product" ORDER BY month, "Consigned Product"
```

### Q8（成功）

```sql
SELECT Destination FROM (SELECT DISTINCT Destination FROM sheet1 WHERE Destination LIKE 'South China%') ORDER BY Destination
```

### Q9（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, SUM("Total Logistics Revenue") AS revenue, SUM("List Price Revenue") AS list_price, SUM("Logistics Value-Added Service Revenue") AS vas_revenue, SUM("Discount Amount") AS discount, SUM("Total Logistics Cost") AS cost, SUM("Freight Cost") AS freight, SUM("Warehousing Cost") AS warehousing, SUM("Other Operating Costs") AS other_cost, SUM(Profit) AS profit, SUM("Sales Quantity") AS qty, COUNT(*) AS orders FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q10（失败）

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

### Q11（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(AVG("Profit Margin")*100, 2) AS avg_profit_margin_pct, SUM("Discount Amount")/SUM("Total Logistics Revenue")*100 AS discount_rate_pct, SUM("Logistics Value-Added Service Revenue")/SUM("Total Logistics Revenue")*100 AS vas_rate_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q12（成功）

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

### Q13（成功）

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

### Q14（成功）

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

### Q15（成功）

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

### Q16（成功）

```sql
SELECT substr(Destination, 1, instr(substr(Destination, 14), '-')+13) AS region, strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY region, month ORDER BY region, month
```

### Q17（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(SUM("Total Logistics Revenue")/COUNT(*),2) AS rev_per_order, ROUND(SUM("Sales Quantity")/COUNT(*),2) AS qty_per_order, ROUND(SUM("Total Logistics Revenue")/SUM("Sales Quantity"),3) AS rev_per_unit, ROUND(SUM(Profit)/SUM("Sales Quantity"),3) AS profit_per_unit, ROUND(SUM("Total Logistics Cost")/SUM("Sales Quantity"),3) AS cost_per_unit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q18（成功）

```sql
SELECT CASE WHEN Destination LIKE 'South China-Guangdong%' THEN 'Guangdong' WHEN Destination LIKE 'South China-Guangxi%' THEN 'Guangxi' WHEN Destination LIKE 'South China-Hainan%' THEN 'Hainan' ELSE 'Henan' END AS region, strftime('%Y-%m', Date) AS month, SUM(Profit) AS profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY region, month ORDER BY region, month
```

### Q19（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS n, ROUND(AVG("Profit Margin")*100,1) AS avg_margin_pct, ROUND(MIN("Profit Margin")*100,1) AS min_margin_pct, ROUND(MAX("Profit Margin")*100,1) AS max_margin_pct, ROUND(SUM(Profit)/SUM("Total Logistics Revenue")*100,1) AS weighted_margin_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q20（成功）

```sql
SELECT "Waybill Number", Date, Destination, "Consigned Product", "Sales Quantity", "Total Logistics Revenue", "Total Logistics Cost", Profit, "Profit Margin" FROM sheet1 WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-10' ORDER BY "Profit Margin" DESC LIMIT 10
```

### Q21（成功）

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

### Q22（成功）

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

### Q23（成功）

```sql
SELECT DISTINCT substr(Destination, 14, instr(substr(Destination||'-', 14), '-')-1) AS province FROM sheet1 WHERE Destination LIKE 'South China%' ORDER BY province
```

### Q24（成功）

```sql
SELECT strftime('%Y-%m', Date) AS month, ROUND(AVG("List Price Revenue"/"Sales Quantity"),3) AS avg_unit_list_price, ROUND(AVG("Logistics Unit Price"),3) AS avg_logistics_unit_price, SUM("Discount Amount")/SUM("List Price Revenue")*100 AS discount_rate_pct, SUM("Logistics Value-Added Service Revenue")/(SUM("List Price Revenue")-SUM("Discount Amount"))*100 AS vas_effective_rate_pct FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month ORDER BY month
```

### Q25（成功）

```sql
SELECT substr(Destination, 13, instr(substr(Destination, 13)||'-', '-')-1) AS province, COUNT(*) AS orders, ROUND(SUM(Profit),0) AS total_profit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY province ORDER BY total_profit DESC
```

### Q26（成功）

```sql
SELECT "Consigned Product", ROUND(AVG("Total Logistics Revenue"/"Sales Quantity"),3) AS avg_price_per_unit, ROUND(AVG("Total Logistics Cost"/"Sales Quantity"),3) AS avg_cost_per_unit, ROUND(AVG("Profit"/"Sales Quantity"),3) AS avg_profit_per_unit FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY "Consigned Product" ORDER BY avg_profit_per_unit DESC
```

### Q27（成功）

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

### Q28（成功）

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

### Q29（成功）

```sql
SELECT "Waybill Number", Date, Destination, "Consigned Product", "Total Logistics Revenue", "Total Logistics Cost", Profit, "Profit Margin" FROM sheet1 WHERE Destination LIKE 'South China%' AND strftime('%Y-%m', Date)='2023-08' AND "Profit Margin" < -5 ORDER BY "Profit Margin" LIMIT 5
```

### Q30（成功）

```sql
SELECT 'Freight' AS cost_type, ROUND(AVG(val),0) AS avg, ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0) AS std, ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) AS cv_pct FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Freight Cost") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Warehousing', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Warehousing Cost") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Other Costs', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, SUM("Other Operating Costs") AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
UNION ALL
SELECT 'Orders', ROUND(AVG(val),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val)),0), ROUND(SQRT(AVG(val*val)-AVG(val)*AVG(val))/AVG(val)*100,1) FROM (SELECT strftime('%Y-%m', Date) AS month, COUNT(*) AS val FROM sheet1 WHERE Destination LIKE 'South China%' GROUP BY month)
```
