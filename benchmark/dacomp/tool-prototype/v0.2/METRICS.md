# v0.2完整统计

01为首轮；02为补充完整调用格式示例后的第二轮。未更换原题、模型、数据库、80次SQL预算或600秒时限。
每个题每个条件只有一次运行；同一候选在多轮重复出现，计数相关，不能当成独立样本。
生成脚本：`summarize.py`；底层逐轮分析：`agent_db_tool/matching.py`。

## 调用与格式

| 运行 | SQL成功/尝试 | FAD校验通过/调用 | 接受的非空FAD | 多候选调用 | 原始候选数 | 报告提交 |
|---|---|---|---|---|---|---|
| [dacomp-003-01](runs/dacomp-003-01/matching/PER-ROUND.md) | 16/18 | 0/18（0.0%） | 0 | 12 | 30 | 是 |
| [dacomp-004-01](runs/dacomp-004-01/matching/PER-ROUND.md) | 14/14 | 13/14（92.9%） | 11 | 7 | 20 | 是 |
| [dacomp-005-01](runs/dacomp-005-01/matching/PER-ROUND.md) | 28/28 | 0/28（0.0%） | 0 | 15 | 43 | 是 |
| [dacomp-006-01](runs/dacomp-006-01/matching/PER-ROUND.md) | 19/19 | 0/19（0.0%） | 0 | 18 | 50 | 是 |
| [dacomp-003-02](runs/dacomp-003-02/matching/PER-ROUND.md) | 11/11 | 5/11（45.5%） | 0 | 4 | 10 | 是 |
| [dacomp-004-02](runs/dacomp-004-02/matching/PER-ROUND.md) | 10/10 | 10/10（100.0%） | 9 | 0 | 9 | 是 |
| [dacomp-005-02](runs/dacomp-005-02/matching/PER-ROUND.md) | 21/21 | 0/21（0.0%） | 0 | 5 | 28 | 是 |
| [dacomp-006-02](runs/dacomp-006-02/matching/PER-ROUND.md) | 29/30 | 5/30（16.7%） | 4 | 24 | 58 | 是 |

## 原始内容：已填写字段后来有没有发生

分母为有具体项的候选次数，分子为该字段的全部具体项能在某一条严格后续成功SQL中找到的次数。不同字段可命中不同查询；这不是完整候选准确率。
known分组要求同一SQL作用域中完整维度集合一致，partial只要求已填维度包含其中。partial连接允许后续SQL增加等值条件。过滤只比较已知条件单项。

| 运行 | 表 | 列 | 已知过滤项 | 连接 | 分组 | 聚合 |
|---|---|---|---|---|---|---|
| dacomp-003-01 | 29/30（96.7%） | 16/26（61.5%） | 7/9（77.8%） | 11/12（91.7%） | 11/13（84.6%） | 9/17（52.9%） |
| dacomp-004-01 | 20/20（100.0%） | 15/20（75.0%） | — | — | 16/20（80.0%） | 9/20（45.0%） |
| dacomp-005-01 | 43/43（100.0%） | 24/43（55.8%） | 15/16（93.8%） | — | 5/5（100.0%） | 8/8（100.0%） |
| dacomp-006-01 | 48/50（96.0%） | 17/50（34.0%） | 47/50（94.0%） | — | 36/46（78.3%） | 31/47（66.0%） |
| dacomp-003-02 | 10/10（100.0%） | 4/10（40.0%） | 2/2（100.0%） | 10/10（100.0%） | 5/9（55.6%） | 3/7（42.9%） |
| dacomp-004-02 | 9/9（100.0%） | 8/9（88.9%） | 5/5（100.0%） | — | 5/5（100.0%） | 6/6（100.0%） |
| dacomp-005-02 | 27/28（96.4%） | 10/28（35.7%） | 1/2（50.0%） | — | 0/1（0.0%） | 2/7（28.6%） |
| dacomp-006-02 | 58/58（100.0%） | 52/58（89.7%） | 51/55（92.7%） | — | 40/53（75.5%） | 46/58（79.3%） |

## 只看数据库接受的候选

分母为有具体项的候选次数，分子为该字段的全部具体项能在某一条严格后续成功SQL中找到的次数。不同字段可命中不同查询；这不是完整候选准确率。
known分组要求同一SQL作用域中完整维度集合一致，partial只要求已填维度包含其中。partial连接允许后续SQL增加等值条件。过滤只比较已知条件单项。

| 运行 | 表 | 列 | 已知过滤项 | 连接 | 分组 | 聚合 |
|---|---|---|---|---|---|---|
| dacomp-003-01 | — | — | — | — | — | — |
| dacomp-004-01 | 18/18（100.0%） | 14/18（77.8%） | — | — | 14/18（77.8%） | 8/18（44.4%） |
| dacomp-005-01 | — | — | — | — | — | — |
| dacomp-006-01 | — | — | — | — | — | — |
| dacomp-003-02 | — | — | — | — | — | — |
| dacomp-004-02 | 9/9（100.0%） | 8/9（88.9%） | 5/5（100.0%） | — | 5/5（100.0%） | 6/6（100.0%） |
| dacomp-005-02 | — | — | — | — | — | — |
| dacomp-006-02 | 6/6（100.0%） | 6/6（100.0%） | 2/3（66.7%） | — | 5/5（100.0%） | 5/6（83.3%） |

## 实际查询中的操作，有多少曾被提前提到

每条成功SQL中去重计数各操作单项，排除没有任何此前请求的首条查询。分子为任一更早FAD曾提到的项，包含原始可审核但未接受的内容。
这衡量曾经预见，不表示数据库在执行该SQL之前仍持有这些项。连接覆盖使用包含全部等值条件的完整连接模式，只有部分连接键不算完整覆盖。复杂SQL表达式无法识别的部分不在分母里，限制见下表。

| 运行 | 列 | 过滤项 | 连接 | 分组维度 | 聚合项 |
|---|---|---|---|---|---|
| dacomp-003-01 | 72/80（90.0%） | 6/12（50.0%） | 6/7（85.7%） | 7/10（70.0%） | 12/22（54.5%） |
| dacomp-004-01 | 38/46（82.6%） | 0/5（0.0%） | — | 21/22（95.5%） | 13/26（50.0%） |
| dacomp-005-01 | 144/147（98.0%） | 8/11（72.7%） | — | 5/23（21.7%） | 86/132（65.2%） |
| dacomp-006-01 | 75/75（100.0%） | 17/18（94.4%） | — | 17/20（85.0%） | 47/50（94.0%） |
| dacomp-003-02 | 51/67（76.1%） | 6/10（60.0%） | 0/9（0.0%） | 9/10（90.0%） | 1/11（9.1%） |
| dacomp-004-02 | 31/32（96.9%） | 5/6（83.3%） | — | 13/19（68.4%） | 7/18（38.9%） |
| dacomp-005-02 | 100/109（91.7%） | 1/2（50.0%） | — | 0/23（0.0%） | 16/90（17.8%） |
| dacomp-006-02 | 113/126（89.7%） | 25/33（75.8%） | — | 27/31（87.1%） | 55/66（83.3%） |

## 最近一份有效快照覆盖了多少实际操作

只使用当前SQL之前的最后一次调用所提交并通过校验的FAD；最后一次无效或空提示会清空快照，不能沿用更早预测。这里仍仅比较操作单项。

| 运行 | 列 | 过滤项 | 连接 | 分组维度 | 聚合项 |
|---|---|---|---|---|---|
| dacomp-003-01 | 0/80（0.0%） | 0/12（0.0%） | 0/7（0.0%） | 0/10（0.0%） | 0/22（0.0%） |
| dacomp-004-01 | 23/46（50.0%） | 0/5（0.0%） | — | 15/22（68.2%） | 6/26（23.1%） |
| dacomp-005-01 | 0/147（0.0%） | 0/11（0.0%） | — | 0/23（0.0%） | 0/132（0.0%） |
| dacomp-006-01 | 0/75（0.0%） | 0/18（0.0%） | — | 0/20（0.0%） | 0/50（0.0%） |
| dacomp-003-02 | 0/67（0.0%） | 0/10（0.0%） | 0/9（0.0%） | 0/10（0.0%） | 0/11（0.0%） |
| dacomp-004-02 | 23/32（71.9%） | 5/6（83.3%） | — | 7/19（36.8%） | 4/18（22.2%） |
| dacomp-005-02 | 0/109（0.0%） | 0/2（0.0%） | — | 0/23（0.0%） | 0/90（0.0%） |
| dacomp-006-02 | 11/126（8.7%） | 2/33（6.1%） | — | 3/31（9.7%） | 3/66（4.5%） |

## 状态与格式错误

### dacomp-003-01

错误调用分类（可重叠）：{"columns类型错误": 18}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 0 | 0 | 0 | 0 | 30 |
| filters | 9 | 0 | 0 | 21 | 0 |
| joins | 12 | 0 | 0 | 18 | 0 |
| group_by | 13 | 0 | 0 | 17 | 0 |
| aggregations | 17 | 0 | 0 | 13 | 0 |
### dacomp-004-01

错误调用分类（可重叠）：{"名称不存在或歧义": 1, "漏列操作引用列": 1}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 20 | 0 | 0 | 0 | 0 |
| filters | 0 | 0 | 0 | 20 | 0 |
| joins | 0 | 0 | 0 | 20 | 0 |
| group_by | 19 | 1 | 0 | 0 | 0 |
| aggregations | 19 | 1 | 0 | 0 | 0 |
### dacomp-005-01

错误调用分类（可重叠）：{"FAD为字符串": 28}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 43 | 0 | 0 | 0 | 0 |
| filters | 0 | 19 | 0 | 24 | 0 |
| joins | 0 | 0 | 0 | 43 | 0 |
| group_by | 5 | 0 | 0 | 38 | 0 |
| aggregations | 8 | 0 | 0 | 35 | 0 |
### dacomp-006-01

错误调用分类（可重叠）：{"FAD为字符串": 19}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 50 | 0 | 0 | 0 | 0 |
| filters | 48 | 2 | 0 | 0 | 0 |
| joins | 0 | 0 | 0 | 50 | 0 |
| group_by | 46 | 0 | 0 | 4 | 0 |
| aggregations | 47 | 0 | 0 | 3 | 0 |
### dacomp-003-02

错误调用分类（可重叠）：{"漏列操作引用列": 6}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 10 | 0 | 0 | 0 | 0 |
| filters | 2 | 0 | 0 | 8 | 0 |
| joins | 0 | 10 | 0 | 0 | 0 |
| group_by | 9 | 0 | 0 | 1 | 0 |
| aggregations | 7 | 0 | 0 | 3 | 0 |
### dacomp-004-02

错误调用分类（可重叠）：{}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 9 | 0 | 0 | 0 | 0 |
| filters | 5 | 0 | 0 | 4 | 0 |
| joins | 0 | 0 | 0 | 9 | 0 |
| group_by | 5 | 0 | 0 | 4 | 0 |
| aggregations | 6 | 0 | 0 | 3 | 0 |
### dacomp-005-02

错误调用分类（可重叠）：{"FAD为字符串": 21}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 28 | 0 | 0 | 0 | 0 |
| filters | 0 | 2 | 0 | 26 | 0 |
| joins | 0 | 0 | 0 | 28 | 0 |
| group_by | 1 | 0 | 0 | 27 | 0 |
| aggregations | 7 | 0 | 0 | 21 | 0 |
### dacomp-006-02

错误调用分类（可重叠）：{"漏列操作引用列": 25}

| 字段 | known | partial | unknown | none | 未写状态的旧数组 |
|---|---|---|---|---|---|
| columns | 58 | 0 | 0 | 0 | 0 |
| filters | 55 | 0 | 0 | 3 | 0 |
| joins | 0 | 0 | 0 | 58 | 0 |
| group_by | 53 | 0 | 0 | 5 | 0 |
| aggregations | 58 | 0 | 0 | 0 | 0 |

## 高频列是否提前说过

实际次数为首条查询之后访问该列的成功SQL条数；“曾说过”包括离线可解码的原始内容，“最近有效快照”仅包括数据库实际接受内容。这里只按columns.items统计，joins等操作字段里的引用不自动补算进列清单。

| 运行 | 高频列 | 实际访问次数 | 曾提前提到 | 上一轮提到 | 最近有效快照提到 |
|---|---|---|---|---|---|
| dacomp-003-01 | sheet1.Year | 10 | 10 | 9 | 0 |
| dacomp-003-01 | sheet1.Region Name | 9 | 9 | 6 | 0 |
| dacomp-003-01 | sheet1.Total Water Consumption (100 million m³)  | 9 | 9 | 8 | 0 |
| dacomp-003-01 | sheet1.Industrial Water Consumption (100 million m³) | 8 | 8 | 6 | 0 |
| dacomp-003-01 | sheet1.Region Code | 8 | 8 | 1 | 0 |
| dacomp-003-01 | economic_indicator_data.Year | 8 | 8 | 3 | 0 |
| dacomp-003-01 | economic_indicator_data.Per capita GDP (yuan/person) | 7 | 7 | 5 | 0 |
| dacomp-003-01 | economic_indicator_data.Region Code | 7 | 7 | 0 | 0 |
| dacomp-004-01 | sheet1.Product Code | 12 | 12 | 11 | 10 |
| dacomp-004-01 | sheet1.Sales Amount | 11 | 11 | 4 | 4 |
| dacomp-004-01 | sheet1.Sales Month | 10 | 10 | 5 | 4 |
| dacomp-004-01 | sheet1.Customer ID | 6 | 5 | 5 | 5 |
| dacomp-004-01 | sheet1.Is Promotional | 1 | 0 | 0 | 0 |
| dacomp-004-01 | sheet1.Major Category Name | 1 | 0 | 0 | 0 |
| dacomp-004-01 | sheet1.Middle Category Name | 1 | 0 | 0 | 0 |
| dacomp-004-01 | sheet1.Minor Category Name | 1 | 0 | 0 | 0 |
| dacomp-005-01 | sheet1.Profit Margin | 26 | 26 | 21 | 0 |
| dacomp-005-01 | sheet1.Sales Quantity | 20 | 20 | 15 | 0 |
| dacomp-005-01 | sheet1.Profit | 13 | 13 | 6 | 0 |
| dacomp-005-01 | sheet1.Total Logistics Revenue | 13 | 13 | 7 | 0 |
| dacomp-005-01 | sheet1.Total Logistics Cost | 12 | 12 | 3 | 0 |
| dacomp-005-01 | sheet1.Freight Cost | 10 | 10 | 3 | 0 |
| dacomp-005-01 | sheet1.Discount Amount | 9 | 9 | 4 | 0 |
| dacomp-005-01 | sheet1.Warehousing Cost | 9 | 9 | 2 | 0 |
| dacomp-006-01 | sheet1.Destination | 18 | 18 | 18 | 0 |
| dacomp-006-01 | sheet1.Profit | 14 | 14 | 14 | 0 |
| dacomp-006-01 | sheet1.Date | 13 | 13 | 12 | 0 |
| dacomp-006-01 | sheet1.Sales Quantity | 9 | 9 | 9 | 0 |
| dacomp-006-01 | sheet1.Total Logistics Cost | 5 | 5 | 3 | 0 |
| dacomp-006-01 | sheet1.Total Logistics Revenue | 5 | 5 | 4 | 0 |
| dacomp-006-01 | sheet1.Consigned Product | 3 | 3 | 3 | 0 |
| dacomp-006-01 | sheet1.Discount Amount | 2 | 2 | 2 | 0 |
| dacomp-003-02 | economic_indicator_data.Year | 9 | 9 | 2 | 0 |
| dacomp-003-02 | sheet1.Region Name | 9 | 9 | 5 | 0 |
| dacomp-003-02 | economic_indicator_data.Per capita GDP (yuan/person) | 8 | 8 | 4 | 0 |
| dacomp-003-02 | economic_indicator_data.Region Code | 8 | 0 | 0 | 0 |
| dacomp-003-02 | sheet1.Industrial Water Consumption (100 million m³) | 8 | 8 | 4 | 0 |
| dacomp-003-02 | sheet1.Region Code | 8 | 0 | 0 | 0 |
| dacomp-003-02 | sheet1.Total Water Consumption (100 million m³)  | 8 | 8 | 4 | 0 |
| dacomp-003-02 | sheet1.Year | 8 | 8 | 3 | 0 |
| dacomp-004-02 | sheet1.Product Code | 9 | 9 | 9 | 9 |
| dacomp-004-02 | sheet1.Sales Month | 8 | 8 | 7 | 7 |
| dacomp-004-02 | sheet1.Sales Amount | 5 | 5 | 4 | 4 |
| dacomp-004-02 | sheet1.Customer ID | 4 | 4 | 3 | 3 |
| dacomp-004-02 | sheet1.Major Category Name | 1 | 1 | 0 | 0 |
| dacomp-004-02 | sheet1.Middle Category Name | 1 | 1 | 0 | 0 |
| dacomp-004-02 | sheet1.Minor Category Name | 1 | 1 | 0 | 0 |
| dacomp-004-02 | sheet1.Product Type | 1 | 1 | 0 | 0 |
| dacomp-005-02 | sheet1.Sales Quantity | 17 | 16 | 16 | 0 |
| dacomp-005-02 | sheet1.Profit Margin | 16 | 16 | 16 | 0 |
| dacomp-005-02 | sheet1.Profit | 10 | 9 | 8 | 0 |
| dacomp-005-02 | sheet1.Discount Amount | 10 | 9 | 8 | 0 |
| dacomp-005-02 | sheet1.List Price Revenue | 10 | 9 | 4 | 0 |
| dacomp-005-02 | sheet1.Total Logistics Revenue | 9 | 8 | 8 | 0 |
| dacomp-005-02 | sheet1.Total Logistics Cost | 7 | 6 | 6 | 0 |
| dacomp-005-02 | sheet1.Freight Cost | 6 | 5 | 4 | 0 |
| dacomp-006-02 | sheet1.Destination | 27 | 27 | 19 | 3 |
| dacomp-006-02 | sheet1.Date | 22 | 22 | 22 | 4 |
| dacomp-006-02 | sheet1.Profit | 20 | 20 | 20 | 3 |
| dacomp-006-02 | sheet1.Sales Quantity | 10 | 9 | 2 | 0 |
| dacomp-006-02 | sheet1.Total Logistics Revenue | 10 | 9 | 5 | 0 |
| dacomp-006-02 | sheet1.Total Logistics Cost | 8 | 7 | 1 | 0 |
| dacomp-006-02 | sheet1.Consigned Product | 8 | 7 | 6 | 1 |
| dacomp-006-02 | sheet1.Profit Margin | 4 | 3 | 3 | 0 |

## 解析范围与开销

SQLGlot识别原始列、strftime年/月/日分组、常见简单聚合、已知WHERE条件单项和ON等值连接。CASE分组、聚合后的再聚合、比值、窗口语义、HAVING、复杂条件及连接暂不作完整等价判断。
所有运行SQL解析失败数及具体未支持表达式保存在各运行detail.json。SQLITE_READ列引用不受这些表达式识别限制影响。
耗时为四题并发运行时的观测值，不用于性能比较。token字段按服务原口径保存，可能含重叠项，不能当作FAD增量成本。

| 运行 | SQL解析失败 | 候选无法分析 | 未支持表达式次数（按类别） | 运行秒数 | 平均提示校验毫秒 |
|---|---|---|---|---|---|
| dacomp-003-01 | 0 | 0 | {"aggregations": 43, "group_by": 2} | 226.1 | 1.20 |
| dacomp-004-01 | 0 | 0 | {"window": 6, "filters": 4, "aggregations": 24, "group_by": 1} | 153.3 | 2.03 |
| dacomp-005-01 | 0 | 0 | {"group_by": 12, "aggregations": 42, "filters": 1} | 318.9 | 0.31 |
| dacomp-006-01 | 0 | 0 | {"aggregations": 33, "group_by": 3} | 301.4 | 0.38 |
| dacomp-003-02 | 0 | 0 | {"aggregations": 9, "filters": 5} | 309.2 | 1.79 |
| dacomp-004-02 | 0 | 0 | {"window": 4, "filters": 1, "aggregations": 2} | 86.3 | 1.68 |
| dacomp-005-02 | 0 | 0 | {"group_by": 17, "aggregations": 31} | 221.4 | 0.35 |
| dacomp-006-02 | 0 | 0 | {"aggregations": 182, "group_by": 4, "filters": 2} | 364.4 | 3.82 |
