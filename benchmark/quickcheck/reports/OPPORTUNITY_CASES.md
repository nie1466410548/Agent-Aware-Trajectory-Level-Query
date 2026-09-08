# 潜在优化机会：逐项证据

所有候选仅为静态分析假设；A 为公共对象、B 为较弱的扫描准备。Q 编号对应原 SQL 文件编号。每项涉及至少两次独立成功数据调用，消费者列表不跨任务。

<a id="n01"></a>
## N01 · natural · bookreview/query1 · 出版年份正则提取

类别：A；数据库：`books_database`；任务答案：通过。

**共同输入证据：** 两条 SQL 对同一 details 列使用完全相同的正则提取；无 WHERE 限制输入。

**一次准备：** 为 books_info 保留 book_id、details，并逐行计算 substring(details from 'on [A-Z][a-z]+ \d{1,2}, (\d{4})') 为 pub_year_text。

**供后续使用：** Q4 从派生列计算非空数量；Q5 用派生列 IS NULL 筛选原始记录。

**约束和不确定性：** 不是缓存 Q4 的计数结果来回答 Q5；需保存行级派生列，保留 NULL 和原始文本语义。只有两次使用。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query1/quick-01/sql/004-52ed6163f9954d51aad68a2abd03c4f2.sql) |
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query1/quick-01/sql/005-d57a24858a8b4dedbab82d80f8cce074.sql) |

<a id="n02"></a>
## N02 · natural · bookreview/query2 · 文学类别筛选与布尔标记

类别：A；数据库：`books_database`；任务答案：通过。

**共同输入证据：** 四次调用都出现完全相同的类别 LIKE 条件，包括 Q6 的 FILTER 子表达式。

**一次准备：** 对 books_info 计算 categories LIKE '%Literature & Fiction%' 标记，准备满足条件的完整行子集，保留 book_id/title/author/rating_number/details/categories。

**供后续使用：** Q5/Q7/Q8 使用类别子集，保留各自 LIMIT、英语条件及投影；Q6 的 lit_fic 与 lit_fic_english 使用该子集，total 仍需全表总数。

**约束和不确定性：** Q6 仅部分计算受益；Q5 样本结果本身不够；NOT ILIKE 的 NULL 语义必须保留。预备完整子集可能比首次 LIMIT 查询贵。

涉及 4 次调用；若在首次使用时准备，之后还剩 3 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query2/quick-01/sql/005-7e9526581d4c417eadfae0208f45163f.sql) |
| Q6 | 1 | 部分子计算 | [SQL](../runs/natural/bookreview/query2/quick-01/sql/006-b06b68bba09d4a76bd6bba69e922dba7.sql) |
| Q7 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query2/quick-01/sql/007-2977eb4f431849288ac3dbc0621a2454.sql) |
| Q8 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query2/quick-01/sql/008-ef73e65452a14ec8867b4517ab36a87b.sql) |

<a id="n03"></a>
## N03 · natural · bookreview/query3 · 评论表的一次扫描统计准备

类别：B；数据库：`review_database`；任务答案：通过。

**共同输入证据：** 三条都是 review 上无 WHERE 的完整输入统计，Q5/Q8 共同需要 purchase_id；Q5/Q6 重复全表 COUNT。

**一次准备：** 一次完整扫描 purchase_id/review_time，同时维护总数、ID 前缀计数、日期极值、ID 数字后缀极值和精确 distinct ID 集合/计数。

**供后续使用：** 分别供应 Q5、Q6、Q8 的全表诊断统计；不把任何一个分组结果当成另一个结果。

**约束和不确定性：** 弱候选：主要共享扫描，不是已经识别的相同聚合状态；需要提前知道要准备哪些统计，distinct 有内存成本。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query3/quick-01/sql/005-aa49c2a70ea74daca5268a1e881f9722.sql) |
| Q6 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query3/quick-01/sql/006-a0811fb2b84c490e8e201bfa38ba17bc.sql) |
| Q8 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query3/quick-01/sql/008-20fb955d245145ba8e72c96eb802fcb0.sql) |

<a id="n04"></a>
## N04 · natural · bookreview/query3 · 书籍 ID 的一次扫描统计准备

类别：B；数据库：`books_database`；任务答案：通过。

**共同输入证据：** 两条都完整扫描 books_info.book_id 且没有 WHERE。

**一次准备：** 一次扫描 book_id，维护总数、字符串 MIN/MAX、前缀计数与数字后缀 MAX。

**供后续使用：** 供应 Q7 的 ID 诊断和 Q9 的数字后缀上界。

**约束和不确定性：** 弱候选：复用同列扫描而非相同聚合；不能把字符串 MAX 当成数字后缀 MAX；表仅 200 行。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q7 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query3/quick-01/sql/007-26786887ff154a15bb8586d7a260b314.sql) |
| Q9 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/bookreview/query3/quick-01/sql/009-98af14d6a9524409b499548823b7fe57.sql) |

<a id="n05"></a>
## N05 · natural · crmarenapro/query8 · Owner Assignment 历史子集

类别：A；数据库：`support`；任务答案：未通过。

**共同输入证据：** 六次调用均显式包含同表同值的 field__c 等值筛选，包括 CTE 中的筛选。

**一次准备：** 准备 casehistory__c WHERE field__c='Owner Assignment'，保留 id/caseid__c/createddate/oldvalue__c/newvalue__c 的完整重复行。

**供后续使用：** Q4/Q7 在此基础上继续连接 Case；Q5/Q6/Q10 的 CTE 从子集读取后保留各自窗口、分组与 Join；Q8 继续过滤 oldvalue。

**约束和不确定性：** 日期窗口不同，不能复用某一个窗口的聚合结果；这里共享不带日期约束的共同输入。保留 < 与 <= 差异和重复行。

涉及 6 次调用；若在首次使用时准备，之后还剩 5 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/004-8b3740b813a94f5f8bc06013e72bd7ae.sql) |
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/005-24086fdaa6bd49cca3f142608ca584d7.sql) |
| Q6 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/006-ca91cee2d9624bb9ab4910b001039252.sql) |
| Q7 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/007-9f7c8ef90f5e48838c4e4c5e5af8138e.sql) |
| Q8 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/008-1b8576518f714f07ae709c0b590dfbc4.sql) |
| Q10 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query8/quick-01/sql/010-dda8e43c7d6d48a4a2a15518a7b5d82d.sql) |

<a id="n06"></a>
## N06 · natural · crmarenapro/query12 · 原始 ID 的 Opportunity–Contract 公共 Join

类别：A；数据库：`sales_pipeline`；任务答案：未通过。

**共同输入证据：** 五次调用的相关分支均是相同两表、相同原始等值键的 INNER JOIN。

**一次准备：** 准备 Opportunity o INNER JOIN Contract c ON o.ContractID__c=c.Id 的行级结果，保留 o.Id/OwnerId/CreatedDate/CloseDate/ContractID__c 和 c.Id/CompanySignedDate。

**供后续使用：** Q3/Q4/Q5/Q10 在公共 Join 上保留各自日期条件与聚合/投影；Q8 仅 apr_close_with_contract 子查询可使用它。

**约束和不确定性：** Q8 其他两个独立表统计不能用此 Join 代替；须保留 Join 多重性。全量 Join 可能比各查询谓词下推更贵；本任务未通过答案验证。

涉及 5 次调用；若在首次使用时准备，之后还剩 4 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q3 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query12/quick-01/sql/003-36973557214b43df99082a9acece1394.sql) |
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query12/quick-01/sql/004-90615943ec654c9394fcdb8f7e8041fc.sql) |
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query12/quick-01/sql/005-56d875618d494449b8ede6da9d81e7a2.sql) |
| Q8 | 1 | 部分子计算 | [SQL](../runs/natural/crmarenapro/query12/quick-01/sql/008-462cefe033d8463baac401b0e4673a36.sql) |
| Q10 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query12/quick-01/sql/010-e39f3371a12c4cfe84d70d0c6b4b7d98.sql) |

<a id="n07"></a>
## N07 · natural · crmarenapro/query13 · 同一订单窗口及订单明细 Join

类别：A；数据库：`products_orders`；任务答案：通过。

**共同输入证据：** Q11/Q13/Q14 使用相同闭区间；Q11/Q14 使用相同 INNER JOIN 与行金额表达式。

**一次准备：** 先准备 Order.EffectiveDate 在 '2022-06-25' 至 '2022-11-25'（含端点）的订单子集；另准备该子集与 OrderItem 的 OrderItem.OrderId=Order.Id Join，保留明细及原始 OwnerId，可派生 Quantity*UnitPrice。

**供后续使用：** Q13 用订单子集；Q11/Q14 用明细 Join 分别按原始 OwnerId、去 # 后 OwnerId 聚合。

**约束和不确定性：** 这是一个两层准备方案，筛选和 Join 不重复算两次机会。Q13 不能从明细 Join 去重恢复订单（可能有无明细订单）。失败 Q9 不计入；不直接复用不同分组的 SUM。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q11 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query13/quick-01/sql/011-b4d5bd62d74e46eebb29ad9ed73e9670.sql) |
| Q13 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query13/quick-01/sql/013-990a07634f204458809ef4845c1f2d4d.sql) |
| Q14 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query13/quick-01/sql/014-4836ecd5a6d94949ace5656f2098a7ed.sql) |

<a id="n08"></a>
## N08 · natural · crmarenapro/query13 · 商机的全表与账户维度统计准备

类别：B；数据库：`sales_pipeline`；任务答案：通过。

**共同输入证据：** 两条都完整读取 Opportunity 的 AccountId/ContractID__c，无 WHERE；分组层次不同。

**一次准备：** 一次扫描 AccountId/ContractID__c/OwnerId，分别维护全局精确 distinct 状态和按 AccountId 的计数、distinct ContractID 状态。

**供后续使用：** 供应 Q6 的全局统计和 Q10 的账户分组统计。

**约束和不确定性：** 弱候选：共享扫描与部分状态准备；不能将每账户 distinct 计数直接相加得到全局 distinct，必须单独维护并处理 NULL。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q6 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query13/quick-01/sql/006-4b888f4c13004a43986ff88031205063.sql) |
| Q10 | 1 | 所述公共对象相关部分 | [SQL](../runs/natural/crmarenapro/query13/quick-01/sql/010-87ec80621e674725b4709099e349d1a5.sql) |

<a id="f01"></a>
## F01 · fad · crmarenapro/query8 · Owner Assignment 历史子集

类别：A；数据库：`support`；任务答案：通过。

**共同输入证据：** 三条调用的直接查询或 CTE 均有同表同值 field__c 等值条件。

**一次准备：** 准备 field__c='Owner Assignment' 的完整行子集，保留 caseid__c/createddate/oldvalue__c/newvalue__c。

**供后续使用：** Q3/Q6 施加同一日期窗口；Q4 单独施加 oldvalue 非空；保留不同排序和聚合。

**约束和不确定性：** 不能直接把 Q3 的有界结果供给不限日期的 Q4；共同准备必须覆盖三者。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q3 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query8/quick-01/sql/003-2b8e4f5207854706adad96225f32edbf.sql) |
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query8/quick-01/sql/004-a387634c961943e0adab45fbcd5ee7d9.sql) |
| Q6 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query8/quick-01/sql/006-dc13858a46704f5d803a8fcc574224bf.sql) |

<a id="f02"></a>
## F02 · fad · crmarenapro/query12 · 原始 ID 的 Opportunity–Contract Join

类别：A；数据库：`sales_pipeline`；任务答案：未通过。

**共同输入证据：** 三条使用相同原始等值键 INNER JOIN，日期口径不同。

**一次准备：** 准备原始 ContractID__c=Id 的 INNER JOIN 明细，保留 OwnerId、机会原始日期、合同签署日期和 ID。

**供后续使用：** Q1/Q2 分别按创建和签署日期筛选聚合；Q5 按关闭日期筛选后返回明细。

**约束和不确定性：** 不把 Q7 的 LEFT JOIN 诊断纳入此 INNER JOIN 候选；不与去 # 的键归一化 Join 混合。答案未通过。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q1 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/001-d50925ad9c8b4ffdaa8b344ef3f68e81.sql) |
| Q2 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/002-9e6aa8e4e69a4900aa19221f8f16c2a9.sql) |
| Q5 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/005-3b2146be0b8845aa814455c3306686bd.sql) |

<a id="f03"></a>
## F03 · fad · crmarenapro/query12 · 去 # 的连接键与归一化 Join

类别：A；数据库：`sales_pipeline`；任务答案：未通过。

**共同输入证据：** 三条均在相同两表的相同键列使用相同 replace 去 # 连接表达式。

**一次准备：** 分别预计算 Contract.Id 和 Opportunity.ContractID__c 的 replace(...,'#','')；以归一键构建关联访问结构，并可准备归一键 INNER JOIN 行结果。

**供后续使用：** Q7 的 c2 LEFT JOIN 分支使用预计算键/访问结构，保留外连接；Q8/Q9 可用归一键 INNER JOIN 明细。

**约束和不确定性：** Q7 只部分受益，不能用 INNER JOIN 改写整个 LEFT JOIN 诊断；归一化可能产生重复键，必须保留多重性。这是一个关联准备方案，不把键与 Join 另算两个机会。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q7 | 1 | 部分子计算 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/007-2aa9db066b664ff2bba1dba9fcdaa74c.sql) |
| Q8 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/008-c5e7dcacc4c94f32a110248f073138cf.sql) |
| Q9 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/009-5d11c21e0e624339b325b42b7a91c8a4.sql) |

<a id="f04"></a>
## F04 · fad · crmarenapro/query12 · 商机诊断的一次扫描统计准备

类别：B；数据库：`sales_pipeline`；任务答案：未通过。

**共同输入证据：** 三次调用中的 Opportunity 统计分支均无 WHERE；Q3/Q4 有完全相同的 MIN/MAX、COUNT 和非空计数。

**一次准备：** 对 Opportunity 无过滤完整输入，一次维护日期极值、总数、合同非空计数、月份和 # 前缀诊断计数。

**供后续使用：** Q3 第一条语句、Q4 和 Q6 第一条语句使用其统计；Q3/Q6 的 Contract 语句仍独立执行。

**约束和不确定性：** Q3/Q6 是多语句调用，不能把合同统计与商机统计混合；末条结果才被适配器返回，因此前面的统计工作是否值得保留本身也存疑。弱候选。

涉及 3 次调用；若在首次使用时准备，之后还剩 2 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q3 | 2 | 部分子计算 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/003-598f0ac9f96143c0ab93e4082625127d.sql) |
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/004-e66fde8c074e4abd8e16e6bc1008c1c7.sql) |
| Q6 | 2 | 部分子计算 | [SQL](../runs/fad/crmarenapro/query12/quick-01/sql/006-3313c6d48e5d4b26ae1bb68613adadbf.sql) |

<a id="f05"></a>
## F05 · fad · crmarenapro/query13 · 多个销售时间窗口的共同明细

类别：A；数据库：`products_orders`；任务答案：通过。

**共同输入证据：** 两次调用各分支 Join 键相同，三个日期窗口都包含于六月至十一月共同范围，滚动窗口分支还相同。

**一次准备：** 准备日期 '2022-06-01' 至 '2022-11-30' 的订单及其 OrderItem 等值 Join，保留 OwnerId/Order.Id/EffectiveDate/Quantity/UnitPrice。

**供后续使用：** Q3 保留滚动窗口筛选；Q4 三个 UNION ALL 分支分别筛选各自窗口后分组。

**约束和不确定性：** 只算两次跨调用使用，不将 Q4 三个分支算三条未来 SQL。Q3 的 LIMIT 10 聚合结果不能代替 Q4 全分组；共同明细可以。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q3 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query13/quick-01/sql/003-fdb801d358584ee9a60aa7247afbfe25.sql) |
| Q4 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/crmarenapro/query13/quick-01/sql/004-c36250a3c302443a844f7c4b2359f4f1.sql) |

<a id="f06"></a>
## F06 · fad · stockindex/query1 · 股票日期解析及共同分析输入

类别：A；数据库：`indextrade_database`；任务答案：通过。

**共同输入证据：** Q8/Q9 日期解析表达式、解析后日期下界和指数集合完全相同；仅额外投影及最终统计不同。

**一次准备：** 对 index_trade 预计算两条 CTE 中完全相同的 COALESCE(try_strptime(...))::DATE，保留 Index/High/Low/Open/Close；可进一步准备相同六个指数且解析日期 >=2020-01-01 的行子集。

**供后续使用：** Q8 从该输入计算 close 分母波动率及日期统计；Q9 计算 open/mid 等其他波动指标。

**约束和不确定性：** 只计 Q8/Q9；Q6 使用原始日期字符串比较，与解析日期过滤不等价，不能合并。保留 try_strptime 的 NULL 行为。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q8 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/stockindex/query1/quick-01/sql/008-4bb579f1f33d49aa8938451a46e68da1.sql) |
| Q9 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/stockindex/query1/quick-01/sql/009-7f7a16a1a51142e68eb39e057c3265e0.sql) |

<a id="f07"></a>
## F07 · fad · stockindex/query2 · 北美指数窗口输入

类别：A；数据库：`indextrade_database`；任务答案：未通过。

**共同输入证据：** 两条指数集合及上界相同；Q6 窗口包含于 Q7 LAG 前的宽窗口。

**一次准备：** 按原 SQL 字符串比较语义，准备三个指数、Date >= '2017-11-01' 且 Date < '2019-01-01' 的原始行，保留 Index/Date/Open/Close；可在原排序语义下组织数据。

**供后续使用：** Q6 再筛 2018 下界后比较 Open/Close；Q7 在宽窗口上先算 LAG，再筛 2018。

**约束和不确定性：** 不可先裁到 2018 再算 LAG，会丢前驱行；原 SQL 字符串日期比较的业务正确性存疑，任务未通过，本候选仅讨论保留实际 SQL 语义。相同日期键的排序不唯一性仍需重放核对。

涉及 2 次调用；若在首次使用时准备，之后还剩 1 次潜在使用。

| 调用 | 语句数 | 受益范围 | 原始 SQL |
|---|---:|---|---|
| Q6 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/stockindex/query2/quick-01/sql/006-da98cb49014841e8be6c4ebfa13a72ea.sql) |
| Q7 | 1 | 所述公共对象相关部分 | [SQL](../runs/fad/stockindex/query2/quick-01/sql/007-12d21c9d97564f8db6482b8c0b2eddc0.sql) |

