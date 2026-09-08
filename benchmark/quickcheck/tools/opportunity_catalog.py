"""Manually reviewed, bounded opportunity families in the fixed quick-01 cohort.

Q numbers are original sql/NNN-* file numbers (metadata gaps retained).
An entry is a hypothesis with identified consumers, not measured savings.
"""
CANDIDATES = []
def add(id, group, task, tier, kind, db, members, tables, title, prepare, uses, constraints, evidence, partial=()):
    CANDIDATES.append(dict(id=id,group=group,task=task,tier=tier,kind=kind,database=db,
        members=members,tables=tables,title=title,prepare=prepare,uses=uses,
        constraints=constraints,evidence=evidence,partial=list(partial)))

add('N01','natural','bookreview/query1','A','derived','books_database',[4,5],['books_info'],
    '出版年份正则提取',
    "为 books_info 保留 book_id、details，并逐行计算 substring(details from 'on [A-Z][a-z]+ \\d{1,2}, (\\d{4})') 为 pub_year_text。",
    'Q4 从派生列计算非空数量；Q5 用派生列 IS NULL 筛选原始记录。',
    '不是缓存 Q4 的计数结果来回答 Q5；需保存行级派生列，保留 NULL 和原始文本语义。只有两次使用。',
    '两条 SQL 对同一 details 列使用完全相同的正则提取；无 WHERE 限制输入。')
add('N02','natural','bookreview/query2','A','filter','books_database',[5,6,7,8],['books_info'],
    '文学类别筛选与布尔标记',
    "对 books_info 计算 categories LIKE '%Literature & Fiction%' 标记，准备满足条件的完整行子集，保留 book_id/title/author/rating_number/details/categories。",
    'Q5/Q7/Q8 使用类别子集，保留各自 LIMIT、英语条件及投影；Q6 的 lit_fic 与 lit_fic_english 使用该子集，total 仍需全表总数。',
    'Q6 仅部分计算受益；Q5 样本结果本身不够；NOT ILIKE 的 NULL 语义必须保留。预备完整子集可能比首次 LIMIT 查询贵。',
    "四次调用都出现完全相同的类别 LIKE 条件，包括 Q6 的 FILTER 子表达式。",partial=[6])
add('N03','natural','bookreview/query3','B','profile','review_database',[5,6,8],['review'],
    '评论表的一次扫描统计准备',
    '一次完整扫描 purchase_id/review_time，同时维护总数、ID 前缀计数、日期极值、ID 数字后缀极值和精确 distinct ID 集合/计数。',
    '分别供应 Q5、Q6、Q8 的全表诊断统计；不把任何一个分组结果当成另一个结果。',
    '弱候选：主要共享扫描，不是已经识别的相同聚合状态；需要提前知道要准备哪些统计，distinct 有内存成本。',
    '三条都是 review 上无 WHERE 的完整输入统计，Q5/Q8 共同需要 purchase_id；Q5/Q6 重复全表 COUNT。')
add('N04','natural','bookreview/query3','B','profile','books_database',[7,9],['books_info'],
    '书籍 ID 的一次扫描统计准备',
    '一次扫描 book_id，维护总数、字符串 MIN/MAX、前缀计数与数字后缀 MAX。',
    '供应 Q7 的 ID 诊断和 Q9 的数字后缀上界。',
    '弱候选：复用同列扫描而非相同聚合；不能把字符串 MAX 当成数字后缀 MAX；表仅 200 行。',
    '两条都完整扫描 books_info.book_id 且没有 WHERE。')
add('N05','natural','crmarenapro/query8','A','filter','support',[4,5,6,7,8,10],['casehistory__c'],
    'Owner Assignment 历史子集',
    "准备 casehistory__c WHERE field__c='Owner Assignment'，保留 id/caseid__c/createddate/oldvalue__c/newvalue__c 的完整重复行。",
    'Q4/Q7 在此基础上继续连接 Case；Q5/Q6/Q10 的 CTE 从子集读取后保留各自窗口、分组与 Join；Q8 继续过滤 oldvalue。',
    '日期窗口不同，不能复用某一个窗口的聚合结果；这里共享不带日期约束的共同输入。保留 < 与 <= 差异和重复行。',
    '六次调用均显式包含同表同值的 field__c 等值筛选，包括 CTE 中的筛选。')
add('N06','natural','crmarenapro/query12','A','join','sales_pipeline',[3,4,5,8,10],['opportunity','contract'],
    '原始 ID 的 Opportunity–Contract 公共 Join',
    '准备 Opportunity o INNER JOIN Contract c ON o.ContractID__c=c.Id 的行级结果，保留 o.Id/OwnerId/CreatedDate/CloseDate/ContractID__c 和 c.Id/CompanySignedDate。',
    'Q3/Q4/Q5/Q10 在公共 Join 上保留各自日期条件与聚合/投影；Q8 仅 apr_close_with_contract 子查询可使用它。',
    'Q8 其他两个独立表统计不能用此 Join 代替；须保留 Join 多重性。全量 Join 可能比各查询谓词下推更贵；本任务未通过答案验证。',
    '五次调用的相关分支均是相同两表、相同原始等值键的 INNER JOIN。',partial=[8])
add('N07','natural','crmarenapro/query13','A','filter_join','products_orders',[11,13,14],['order','orderitem'],
    '同一订单窗口及订单明细 Join',
    "先准备 Order.EffectiveDate 在 '2022-06-25' 至 '2022-11-25'（含端点）的订单子集；另准备该子集与 OrderItem 的 OrderItem.OrderId=Order.Id Join，保留明细及原始 OwnerId，可派生 Quantity*UnitPrice。",
    'Q13 用订单子集；Q11/Q14 用明细 Join 分别按原始 OwnerId、去 # 后 OwnerId 聚合。',
    '这是一个两层准备方案，筛选和 Join 不重复算两次机会。Q13 不能从明细 Join 去重恢复订单（可能有无明细订单）。失败 Q9 不计入；不直接复用不同分组的 SUM。',
    'Q11/Q13/Q14 使用相同闭区间；Q11/Q14 使用相同 INNER JOIN 与行金额表达式。')
add('N08','natural','crmarenapro/query13','B','profile','sales_pipeline',[6,10],['opportunity'],
    '商机的全表与账户维度统计准备',
    '一次扫描 AccountId/ContractID__c/OwnerId，分别维护全局精确 distinct 状态和按 AccountId 的计数、distinct ContractID 状态。',
    '供应 Q6 的全局统计和 Q10 的账户分组统计。',
    '弱候选：共享扫描与部分状态准备；不能将每账户 distinct 计数直接相加得到全局 distinct，必须单独维护并处理 NULL。',
    '两条都完整读取 Opportunity 的 AccountId/ContractID__c，无 WHERE；分组层次不同。')
add('F01','fad','crmarenapro/query8','A','filter','support',[3,4,6],['casehistory__c'],
    'Owner Assignment 历史子集',
    "准备 field__c='Owner Assignment' 的完整行子集，保留 caseid__c/createddate/oldvalue__c/newvalue__c。",
    'Q3/Q6 施加同一日期窗口；Q4 单独施加 oldvalue 非空；保留不同排序和聚合。',
    '不能直接把 Q3 的有界结果供给不限日期的 Q4；共同准备必须覆盖三者。',
    '三条调用的直接查询或 CTE 均有同表同值 field__c 等值条件。')
add('F02','fad','crmarenapro/query12','A','join','sales_pipeline',[1,2,5],['opportunity','contract'],
    '原始 ID 的 Opportunity–Contract Join',
    '准备原始 ContractID__c=Id 的 INNER JOIN 明细，保留 OwnerId、机会原始日期、合同签署日期和 ID。',
    'Q1/Q2 分别按创建和签署日期筛选聚合；Q5 按关闭日期筛选后返回明细。',
    '不把 Q7 的 LEFT JOIN 诊断纳入此 INNER JOIN 候选；不与去 # 的键归一化 Join 混合。答案未通过。',
    '三条使用相同原始等值键 INNER JOIN，日期口径不同。')
add('F03','fad','crmarenapro/query12','A','key_join','sales_pipeline',[7,8,9],['opportunity','contract'],
    '去 # 的连接键与归一化 Join',
    "分别预计算 Contract.Id 和 Opportunity.ContractID__c 的 replace(...,'#','')；以归一键构建关联访问结构，并可准备归一键 INNER JOIN 行结果。",
    'Q7 的 c2 LEFT JOIN 分支使用预计算键/访问结构，保留外连接；Q8/Q9 可用归一键 INNER JOIN 明细。',
    'Q7 只部分受益，不能用 INNER JOIN 改写整个 LEFT JOIN 诊断；归一化可能产生重复键，必须保留多重性。这是一个关联准备方案，不把键与 Join 另算两个机会。',
    '三条均在相同两表的相同键列使用相同 replace 去 # 连接表达式。',partial=[7])
add('F04','fad','crmarenapro/query12','B','profile','sales_pipeline',[3,4,6],['opportunity'],
    '商机诊断的一次扫描统计准备',
    '对 Opportunity 无过滤完整输入，一次维护日期极值、总数、合同非空计数、月份和 # 前缀诊断计数。',
    'Q3 第一条语句、Q4 和 Q6 第一条语句使用其统计；Q3/Q6 的 Contract 语句仍独立执行。',
    'Q3/Q6 是多语句调用，不能把合同统计与商机统计混合；末条结果才被适配器返回，因此前面的统计工作是否值得保留本身也存疑。弱候选。',
    '三次调用中的 Opportunity 统计分支均无 WHERE；Q3/Q4 有完全相同的 MIN/MAX、COUNT 和非空计数。',partial=[3,6])
add('F05','fad','crmarenapro/query13','A','filter_join','products_orders',[3,4],['order','orderitem'],
    '多个销售时间窗口的共同明细',
    "准备日期 '2022-06-01' 至 '2022-11-30' 的订单及其 OrderItem 等值 Join，保留 OwnerId/Order.Id/EffectiveDate/Quantity/UnitPrice。",
    'Q3 保留滚动窗口筛选；Q4 三个 UNION ALL 分支分别筛选各自窗口后分组。',
    '只算两次跨调用使用，不将 Q4 三个分支算三条未来 SQL。Q3 的 LIMIT 10 聚合结果不能代替 Q4 全分组；共同明细可以。',
    '两次调用各分支 Join 键相同，三个日期窗口都包含于六月至十一月共同范围，滚动窗口分支还相同。')
add('F06','fad','stockindex/query1','A','derived','indextrade_database',[8,9],['index_trade'],
    '股票日期解析及共同分析输入',
    '对 index_trade 预计算两条 CTE 中完全相同的 COALESCE(try_strptime(...))::DATE，保留 Index/High/Low/Open/Close；可进一步准备相同六个指数且解析日期 >=2020-01-01 的行子集。',
    'Q8 从该输入计算 close 分母波动率及日期统计；Q9 计算 open/mid 等其他波动指标。',
    '只计 Q8/Q9；Q6 使用原始日期字符串比较，与解析日期过滤不等价，不能合并。保留 try_strptime 的 NULL 行为。',
    'Q8/Q9 日期解析表达式、解析后日期下界和指数集合完全相同；仅额外投影及最终统计不同。')
add('F07','fad','stockindex/query2','A','filter','indextrade_database',[6,7],['index_trade'],
    '北美指数窗口输入',
    "按原 SQL 字符串比较语义，准备三个指数、Date >= '2017-11-01' 且 Date < '2019-01-01' 的原始行，保留 Index/Date/Open/Close；可在原排序语义下组织数据。",
    'Q6 再筛 2018 下界后比较 Open/Close；Q7 在宽窗口上先算 LAG，再筛 2018。',
    '不可先裁到 2018 再算 LAG，会丢前驱行；原 SQL 字符串日期比较的业务正确性存疑，任务未通过，本候选仅讨论保留实际 SQL 语义。相同日期键的排序不唯一性仍需重放核对。',
    '两条指数集合及上界相同；Q6 窗口包含于 Q7 LAG 前的宽窗口。')
