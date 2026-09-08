# 本次实验的数据库与查看方式

以下为只读连接实测的精确 COUNT(*)。包括已经准备、但所选任务未必访问的 CRM 表；不代表每张表都出现在实验轨迹中。PostgreSQL 大小包含系统目录，SQLite/DuckDB 是文件大小，均不是纯有效载荷大小。

| 数据集 | 逻辑数据库 | 引擎 | 大小 MiB | 表数 | 总行数 |
|---|---|---|---:|---:|---:|
| bookreview | books_database | postgres | 8.22 | 1 | 200 |
| bookreview | review_database | sqlite | 1.04 | 1 | 1,833 |
| crmarenapro | core_crm | sqlite | 0.18 | 3 | 1,199 |
| crmarenapro | sales_pipeline | duckdb | 2.26 | 6 | 11,394 |
| crmarenapro | support | postgres | 16.33 | 6 | 6,499 |
| crmarenapro | products_orders | sqlite | 0.14 | 7 | 1,065 |
| crmarenapro | activities | duckdb | 20.26 | 3 | 8,870 |
| crmarenapro | territory | sqlite | 0.02 | 2 | 194 |
| stockindex | indexinfo_database | sqlite | 0.01 | 1 | 14 |
| stockindex | indextrade_database | duckdb | 4.26 | 1 | 104,224 |

## bookreview / books_database

位置：`127.0.0.1:55439/bookreview_db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"public"."books_info"` | 200 | `title`, `subtitle`, `author`, `rating_number`, `features`, `description`, `price`, `store`, `categories`, `details`, `book_id` |

## bookreview / review_database

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_bookreview/query_dataset/review_query.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"review"` | 1,833 | `rating`, `title`, `text`, `review_time`, `helpful_vote`, `verified_purchase`, `purchase_id` |

## crmarenapro / core_crm

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_crmarenapro/query_dataset/core_crm.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"User"` | 212 | `Id`, `FirstName`, `LastName`, `Email`, `Phone`, `Username`, `Alias`, `LanguageLocaleKey`, `EmailEncodingKey`, `TimeZoneSidKey`, `LocaleSidKey` |
| `"Account"` | 101 | `Id`, `Name`, `Phone`, `Industry`, `Description`, `NumberOfEmployees`, `ShippingState` |
| `"Contact"` | 886 | `Id`, `FirstName`, `LastName`, `Email`, `AccountId` |

## crmarenapro / sales_pipeline

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_crmarenapro/query_dataset/sales_pipeline.duckdb`

| 表 | 行数 | 列 |
|---|---:|---|
| `"main"."Contract"` | 163 | `Id`, `AccountId`, `Status`, `StartDate`, `CustomerSignedDate`, `CompanySignedDate`, `Description`, `ContractTerm` |
| `"main"."Lead"` | 1,465 | `Id`, `FirstName`, `LastName`, `Email`, `Phone`, `Company`, `Status`, `ConvertedContactId`, `ConvertedAccountId`, `Title`, `CreatedDate`, `ConvertedDate`, `IsConverted`, `OwnerId` |
| `"main"."Opportunity"` | 1,170 | `Id`, `ContractID__c`, `AccountId`, `ContactId`, `OwnerId`, `Probability`, `Amount`, `StageName`, `Name`, `Description`, `CreatedDate`, `CloseDate` |
| `"main"."OpportunityLineItem"` | 4,926 | `Id`, `OpportunityId`, `Product2Id`, `PricebookEntryId`, `Quantity`, `TotalPrice` |
| `"main"."Quote"` | 704 | `Id`, `OpportunityId`, `AccountId`, `ContactId`, `Name`, `Description`, `Status`, `CreatedDate`, `ExpirationDate` |
| `"main"."QuoteLineItem"` | 2,966 | `Id`, `QuoteId`, `OpportunityLineItemId`, `Product2Id`, `PricebookEntryId`, `Quantity`, `UnitPrice`, `Discount`, `TotalPrice` |

## crmarenapro / support

位置：`127.0.0.1:55439/crm_support`

| 表 | 行数 | 列 |
|---|---:|---|
| `"public"."Case"` | 153 | `id`, `priority`, `subject`, `description`, `status`, `contactid`, `createddate`, `closeddate`, `orderitemid__c`, `issueid__c`, `accountid`, `ownerid` |
| `"public"."casehistory__c"` | 393 | `id`, `caseid__c`, `oldvalue__c`, `newvalue__c`, `createddate`, `field__c` |
| `"public"."emailmessage"` | 5,686 | `id`, `subject`, `textbody`, `parentid`, `fromaddress`, `toids`, `messagedate`, `relatedtoid` |
| `"public"."issue__c"` | 15 | `id`, `name`, `description__c` |
| `"public"."knowledge__kav"` | 194 | `id`, `title`, `faq_answer__c`, `summary`, `urlname` |
| `"public"."livechattranscript"` | 58 | `id`, `caseid`, `accountid`, `ownerid`, `body`, `endtime`, `livechatvisitorid`, `contactid` |

## crmarenapro / products_orders

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_crmarenapro/query_dataset/products_orders.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"ProductCategory"` | 10 | `Id`, `Name`, `CatalogId` |
| `"Product2"` | 51 | `Id`, `Name`, `Description`, `IsActive`, `External_ID__c` |
| `"ProductCategoryProduct"` | 100 | `Id`, `ProductCategoryId`, `ProductId` |
| `"Pricebook2"` | 2 | `Id`, `Name`, `Description`, `IsActive`, `ValidFrom`, `ValidTo` |
| `"PricebookEntry"` | 50 | `Id`, `Pricebook2Id`, `Product2Id`, `UnitPrice` |
| `"Order"` | 163 | `Id`, `AccountId`, `Status`, `EffectiveDate`, `Pricebook2Id`, `OwnerId` |
| `"OrderItem"` | 689 | `Id`, `OrderId`, `Product2Id`, `Quantity`, `UnitPrice`, `PriceBookEntryId` |

## crmarenapro / activities

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_crmarenapro/query_dataset/activities.duckdb`

| 表 | 行数 | 列 |
|---|---:|---|
| `"main"."Event"` | 54 | `Id`, `WhatId`, `OwnerId`, `StartDateTime`, `Subject`, `Description`, `DurationInMinutes`, `Location`, `IsAllDayEvent` |
| `"main"."Task"` | 4,783 | `Id`, `WhatId`, `OwnerId`, `Priority`, `Status`, `ActivityDate`, `Subject`, `Description` |
| `"main"."VoiceCallTranscript__c"` | 4,033 | `Id`, `OpportunityId__c`, `LeadId__c`, `Body__c`, `CreatedDate`, `EndTime__c` |

## crmarenapro / territory

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_crmarenapro/query_dataset/territory.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"Territory2"` | 10 | `Id`, `Name`, `Description` |
| `"UserTerritory2Association"` | 184 | `Id`, `UserId`, `Territory2Id` |

## stockindex / indexinfo_database

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_stockindex/query_dataset/indexInfo_query.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"index_info"` | 14 | `Exchange`, `Currency` |

## stockindex / indextrade_database

位置：`/data/nly/Agent-Aware-Trajectory-Level-Query/benchmark/quickcheck/upstream/query_stockindex/query_dataset/indextrade_query.db`

| 表 | 行数 | 列 |
|---|---:|---|
| `"main"."index_trade"` | 104,224 | `Index`, `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `CloseUSD` |

## 查看命令

在项目根目录执行。此工具独立于实验记录，以只读连接查看数据库，不会把人工查询追加到已有 Agent 轨迹。SQL 预览请使用 LIMIT；没有指定 SQL 时输出表名、精确行数、列名及数据库大小。

```bash
# 所有数据库的清单
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/inspect_data.py

# 查看 CRM 的销售数据库结构与行数
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/inspect_data.py crmarenapro sales_pipeline

# 预览 Opportunity
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/inspect_data.py crmarenapro sales_pipeline --sql 'SELECT * FROM "Opportunity" LIMIT 5'

# 预览书籍（PostgreSQL）
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/inspect_data.py bookreview books_database --sql 'SELECT * FROM books_info LIMIT 5'

# 预览股票交易数据（DuckDB）
benchmark/bookreview/.venv/bin/python benchmark/quickcheck/tools/inspect_data.py stockindex indextrade_database --sql 'SELECT * FROM index_trade LIMIT 5'
```

PostgreSQL：容器 `dab-bookreview-pg`，主机 `127.0.0.1`，端口 `55439`，只读用户 `dab_reader`，数据库分别为 `bookreview_db` 和 `crm_support`。当前本地配置连接无需密码。也可从容器执行：

```bash
docker exec -i dab-bookreview-pg psql -U dab_reader -d bookreview_db -c 'SELECT * FROM books_info LIMIT 5'
```

SQLite/DuckDB 可直接用支持对应引擎的数据库客户端打开上述文件，建议使用只读模式。PostgreSQL 原始导入文件分别位于 `upstream/query_bookreview/query_dataset/books_info.sql` 和 `upstream/query_crmarenapro/query_dataset/support.sql`。

机器可读清单：[data-inventory.json](data-inventory.json)。

本次为小规模可行性实验，31 张表共 135,492 行，最大表 index_trade 为 104,224 行。适合观察 Agent 的访问模式；不能据此声称大规模数据库上的优化收益。
