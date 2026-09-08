# 共同准备候选及原始请求

**进度：108/108 次运行已结束。全量运行已结束。**

所有条目均为静态候选，未进行性能或改写验证。不同对象组可以重叠，不代表独立收益。

<a id="c0001"></a>
## C0001 · DEPS_DEV_V1/query1 · fad · 公共筛选

数据库：`package_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
packageinfo
```
共同表达式/条件：
```
packageinfo."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/005-62f6bec7fbfe4b86a2e9c9d7f4a4ee64.sql)、[008](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/008-8b960cc18e124b97a6bc36777e4b0c48.sql)

<a id="c0002"></a>
## C0002 · DEPS_DEV_V1/query1 · fad · 公共筛选

数据库：`project_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
project_packageversion
```
共同表达式/条件：
```
project_packageversion."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/006-ec84208a376947f38a957238c2835595.sql)、[014](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/014-32337e4405bf41a6874cc9996ffc572c.sql)

<a id="c0003"></a>
## C0003 · DEPS_DEV_V1/query1 · fad · 派生计算

数据库：`project_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
project_info
```
共同表达式/条件：
```
REGEXP_EXTRACT(project_info."project_information", 'The project ([^ ]+)', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[007](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/007-7024e07e825146a6a4c1e5166c4c765d.sql)、[009](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/009-b5d7c5681b9f4302ad4fbfabfd7a9e26.sql)

<a id="c0004"></a>
## C0004 · DEPS_DEV_V1/query1 · fad · 派生计算

数据库：`project_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
project_info
```
共同表达式/条件：
```
REGEXP_EXTRACT(project_info."project_information", '([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[010](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/010-9694a0e009d44f6eb3ef263130fc6421.sql)、[012](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/012-90923f48c9444bc0b06da881c5df5549.sql)、[015](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/015-e344e280b837462aaef95b26b2fc32e8.sql)

<a id="c0005"></a>
## C0005 · DEPS_DEV_V1/query1 · fad · 派生计算

数据库：`project_database`；任务验证：通过；涉及 5 次调用，首次之后 4 次。

共同输入：
```sql
project_info
```
共同表达式/条件：
```
REGEXP_EXTRACT(project_info."project_information", 'stars? count of\s+([\d,]+)', 1)
REGEXP_EXTRACT(project_info."project_information", '([\d,]+)\s+stars?', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[010](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/010-9694a0e009d44f6eb3ef263130fc6421.sql)、[011](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/011-71cc5a619ad446e2a42b41b391a386fa.sql)、[012](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/012-90923f48c9444bc0b06da881c5df5549.sql)、[013](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/013-924544d99d3e4d999cf6c9362cc4de57.sql)、[015](../runs/fad/DEPS_DEV_V1/query1/full-01/sql/015-e344e280b837462aaef95b26b2fc32e8.sql)

<a id="c0006"></a>
## C0006 · DEPS_DEV_V1/query2 · fad · 公共筛选

数据库：`package_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
packageinfo
```
共同表达式/条件：
```
packageinfo."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/DEPS_DEV_V1/query2/full-01/sql/004-941d2aae9cdc4f5a930d6c68288fa863.sql)、[005](../runs/fad/DEPS_DEV_V1/query2/full-01/sql/005-1e52603435ca46f8acd7a4f02e61b4c7.sql)

<a id="c0007"></a>
## C0007 · GITHUB_REPOS/query1 · fad · 公共筛选

数据库：`artifacts_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
contents
```
共同表达式/条件：
```
REGEXP_LIKE(LOWER(contents."sample_path"), '(^|/)readme\.md$')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/fad/GITHUB_REPOS/query1/full-01/sql/006-7cbe4ebbe0ba4872865bf94ae9b2e72c.sql)、[007](../runs/fad/GITHUB_REPOS/query1/full-01/sql/007-b2446bcc6ce844e5be42bc6775373eed.sql)

<a id="c0008"></a>
## C0008 · GITHUB_REPOS/query2 · fad · 公共筛选

数据库：`artifacts_database`；任务验证：未通过；涉及 4 次调用，首次之后 3 次。

共同输入：
```sql
contents
```
共同表达式/条件：
```
contents."sample_path" LIKE '%.swift'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/GITHUB_REPOS/query2/full-01/sql/004-a89945ab84d74eb68161e9d38b46a91a.sql)、[005](../runs/fad/GITHUB_REPOS/query2/full-01/sql/005-edb9b6f7a973483b919a07b93082edd8.sql)、[006](../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql)、[009](../runs/fad/GITHUB_REPOS/query2/full-01/sql/009-0d967f8891534bf68322a2f452c9752b.sql)

<a id="c0009"></a>
## C0009 · GITHUB_REPOS/query2 · fad · 派生计算

数据库：`artifacts_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
contents
```
共同表达式/条件：
```
REGEXP_EXTRACT(contents."repo_data_description", '(\d+) times', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[006](../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql)、[009](../runs/fad/GITHUB_REPOS/query2/full-01/sql/009-0d967f8891534bf68322a2f452c9752b.sql)

<a id="c0010"></a>
## C0010 · GITHUB_REPOS/query3 · fad · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
licenses
```
共同表达式/条件：
```
licenses."license" = 'apache-2.0'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql)、[003](../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

<a id="c0011"></a>
## C0011 · GITHUB_REPOS/query3 · fad · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
languages
```
共同表达式/条件：
```
languages."language_description" LIKE '%Shell (%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql)、[003](../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

<a id="c0012"></a>
## C0012 · GITHUB_REPOS/query3 · fad · 公共内连接

数据库：`metadata_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```
共同表达式/条件：
```
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[002](../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql)、[003](../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

<a id="c0013"></a>
## C0013 · PANCANCER_ATLAS/query1 · fad · 公共筛选

数据库：`clinical_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."patient_description" ILIKE '%lower grade glioma%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/005-30cb7a44269948ed8834b3c3d95050e3.sql)、[006](../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/006-a0a4d62dd3db40c6b5b8c31d8b5d2ff1.sql)、[007](../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/007-54dc369fd7514b48bbf0d6f09b2fd1f3.sql)

<a id="c0014"></a>
## C0014 · PANCANCER_ATLAS/query1 · fad · 公共筛选

数据库：`clinical_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."histological_type" IS NOT NULL
clinical_info."histological_type" NOT LIKE '[%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/006-a0a4d62dd3db40c6b5b8c31d8b5d2ff1.sql)、[007](../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/007-54dc369fd7514b48bbf0d6f09b2fd1f3.sql)

<a id="c0015"></a>
## C0015 · PANCANCER_ATLAS/query2 · fad · 公共筛选

数据库：`clinical_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."patient_description" ILIKE '%breast invasive carcinoma%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/005-3cf67fa1971944dc810ac193152b3daa.sql)、[006](../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/006-d26814ac52d94904b89d408404365116.sql)

<a id="c0016"></a>
## C0016 · PANCANCER_ATLAS/query3 · fad · 公共筛选

数据库：`clinical_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."patient_description" ILIKE '%Breast invasive carcinoma%'
clinical_info."patient_description" ILIKE '%FEMALE%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/005-8c24ff8d7b314760ab8e0f5f4543731a.sql)、[007](../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/007-27979943806b4743ba1654259e35f8c5.sql)

<a id="c0017"></a>
## C0017 · PATENTS/query1 · fad · 同输入同分组聚合状态

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "publicationinfo"
```
共同表达式/条件：
```
COUNT(*)
```

准备方式：在完全相同输入与分组上准备此聚合的完整结果/状态，保留全部分组后再施加各自 HAVING、排序和 LIMIT。

边界：基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

消费者：[004](../runs/fad/PATENTS/query1/full-01/sql/004-3fab454f877040a3add2f789ac4d5365.sql)、[005](../runs/fad/PATENTS/query1/full-01/sql/005-8509fe9ef5294f41a8c8efef14965af6.sql)

<a id="c0018"></a>
## C0018 · PATENTS/query1 · fad · 派生计算

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
SUBSTRING(TRIM(publicationinfo."filing_date"), -4)
SUBSTRING(TRIM(publicationinfo."filing_date"), 1, 4)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[007](../runs/fad/PATENTS/query1/full-01/sql/007-a792b04e7f6042eb82b84cedce751659.sql)、[011](../runs/fad/PATENTS/query1/full-01/sql/011-a35028c05c3d48d990e8729ea7decdb3.sql)

<a id="c0019"></a>
## C0019 · PATENTS/query1 · fad · 公共筛选

数据库：`CPCDefinition_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
cpc_definition
```
共同表达式/条件：
```
cpc_definition."level" = 5
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[010](../runs/fad/PATENTS/query1/full-01/sql/010-5e808f70c0f14ce88f66f5a17dc2ece0.sql)、[012](../runs/fad/PATENTS/query1/full-01/sql/012-f07147bb9bc7448cbfba90888ef75193.sql)

<a id="c0020"></a>
## C0020 · PATENTS/query2 · fad · 公共筛选

数据库：`publication_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."patents_info" LIKE '%DE-%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/fad/PATENTS/query2/full-01/sql/006-fb12f62e4dbb42d9ad516a36177ce767.sql)、[007](../runs/fad/PATENTS/query2/full-01/sql/007-de75e1c1822040b69867dff18c1f286a.sql)

<a id="c0021"></a>
## C0021 · PATENTS/query3 · fad · 同输入同分组聚合状态

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "publicationinfo"
```
共同表达式/条件：
```
COUNT(*)
```

准备方式：在完全相同输入与分组上准备此聚合的完整结果/状态，保留全部分组后再施加各自 HAVING、排序和 LIMIT。

边界：基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

消费者：[004](../runs/fad/PATENTS/query3/full-01/sql/004-c28490c05cb9409eacfcbc88b2dea807.sql)、[006](../runs/fad/PATENTS/query3/full-01/sql/006-8270c2b274744d80bdd287f52cd08708.sql)

<a id="c0022"></a>
## C0022 · PATENTS/query3 · fad · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."patents_info" LIKE 'UNIV CALIFORNIA%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/PATENTS/query3/full-01/sql/004-c28490c05cb9409eacfcbc88b2dea807.sql)、[007](../runs/fad/PATENTS/query3/full-01/sql/007-872a86d27ca546aab3fec5d8b84fbda4.sql)、[008](../runs/fad/PATENTS/query3/full-01/sql/008-6496653b63d041b0baf9eba8b3bf0d62.sql)

<a id="c0023"></a>
## C0023 · PATENTS/query3 · fad · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."citation" LIKE '%1212462%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[009](../runs/fad/PATENTS/query3/full-01/sql/009-14841ac64dfa4b9f86528e172a0f22d5.sql)、[010](../runs/fad/PATENTS/query3/full-01/sql/010-7a4ec8af45844cffa8741ccee2b36a26.sql)

<a id="c0024"></a>
## C0024 · PATENTS/query3 · fad · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."patents_info" LIKE '%UNIV CALIFORNIA%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[011](../runs/fad/PATENTS/query3/full-01/sql/011-72e794cc0ab14201ab7a6ebd71250530.sql)、[012](../runs/fad/PATENTS/query3/full-01/sql/012-4fc69af1481e4f55b5201caede99dd3e.sql)

<a id="c0025"></a>
## C0025 · agnews/query3 · fad · 公共筛选

数据库：`metadata_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
article_metadata
```
共同表达式/条件：
```
article_metadata."region" = 'Europe'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[003](../runs/fad/agnews/query3/full-01/sql/003-2b626d1a70284ed4b99ab99e0fe2ea6e.sql)、[004](../runs/fad/agnews/query3/full-01/sql/004-484c741ebf5746aabd07411f3413d056.sql)

<a id="c0026"></a>
## C0026 · agnews/query3 · fad · 派生计算

数据库：`metadata_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
article_metadata
```
共同表达式/条件：
```
SUBSTRING(article_metadata."publication_date", 1, 4)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[003](../runs/fad/agnews/query3/full-01/sql/003-2b626d1a70284ed4b99ab99e0fe2ea6e.sql)、[004](../runs/fad/agnews/query3/full-01/sql/004-484c741ebf5746aabd07411f3413d056.sql)

<a id="c0027"></a>
## C0027 · bookreview/query2 · fad · 公共筛选

数据库：`books_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
books_info
```
共同表达式/条件：
```
books_info."categories" LIKE '%Literature & Fiction%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/bookreview/query2/full-01/sql/004-081a7ca6b6084c78b026a5719530f397.sql)、[005](../runs/fad/bookreview/query2/full-01/sql/005-38e30bb3230740d381cf2de5dea8b7dc.sql)

<a id="c0028"></a>
## C0028 · crmarenapro/query10 · fad · 公共筛选

数据库：`support`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
casehistory__c
```
共同表达式/条件：
```
casehistory__c."field__c" = 'Owner Assignment'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/crmarenapro/query10/full-01/sql/004-cbfd1bba72ca483ca37db1cc48f0eba9.sql)、[005](../runs/fad/crmarenapro/query10/full-01/sql/005-b068645d811849edb63d3d34bdd062da.sql)、[007](../runs/fad/crmarenapro/query10/full-01/sql/007-a791c08b30a4452c894506874b295a12.sql)

<a id="c0029"></a>
## C0029 · crmarenapro/query11 · fad · 公共筛选

数据库：`products_orders`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
order
```
共同表达式/条件：
```
order."accountid" = '#001Wt00000PGXrNIAX'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/fad/crmarenapro/query11/full-01/sql/002-19d0a6d433474cc78b730eced521f35a.sql)、[003](../runs/fad/crmarenapro/query11/full-01/sql/003-0ce7fcbfcb97479d96f47f0d592ac0d3.sql)

<a id="c0030"></a>
## C0030 · crmarenapro/query12 · fad · 公共内连接

数据库：`sales_pipeline`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```
共同表达式/条件：
```
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[001](../runs/fad/crmarenapro/query12/full-01/sql/001-fb319174901a4c9888ad85ebcbdaa965.sql)、[002](../runs/fad/crmarenapro/query12/full-01/sql/002-1a05cc1a94244f4896285e7ef7009389.sql)

<a id="c0031"></a>
## C0031 · crmarenapro/query4 · fad · 公共筛选

数据库：`products_orders`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
orderitem
```
共同表达式/条件：
```
orderitem."product2id" = '01tWt000006hVJdIAM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[001](../runs/fad/crmarenapro/query4/full-01/sql/001-7e3a1c2101354d1bb83be10790493c96.sql)、[004](../runs/fad/crmarenapro/query4/full-01/sql/004-615e605901a64c83923eb439aa45721b.sql)、[006](../runs/fad/crmarenapro/query4/full-01/sql/006-62344aff78f2461ba2f47a230f0e2552.sql)

<a id="c0032"></a>
## C0032 · crmarenapro/query6 · fad · 公共筛选

数据库：`sales_pipeline`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
quote
```
共同表达式/条件：
```
quote."id" = '0Q0Wt000001WRAzKAO'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[001](../runs/fad/crmarenapro/query6/full-01/sql/001-ce51debc166b4b74ad40f76ba83836f9.sql)、[002](../runs/fad/crmarenapro/query6/full-01/sql/002-99448368616649bebe274d3db090bfed.sql)

<a id="c0033"></a>
## C0033 · crmarenapro/query7 · fad · 公共筛选

数据库：`support`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
casehistory__c
```
共同表达式/条件：
```
casehistory__c."caseid__c" LIKE '%500Wt00000DDyznIAD%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[010](../runs/fad/crmarenapro/query7/full-01/sql/010-98ddb2561f6e42e7b021bba84c5c822e.sql)、[011](../runs/fad/crmarenapro/query7/full-01/sql/011-a869be984a254094b6b47f751866563d.sql)

<a id="c0034"></a>
## C0034 · crmarenapro/query7 · fad · 公共筛选

数据库：`support`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
emailmessage
```
共同表达式/条件：
```
emailmessage."parentid" LIKE '%500Wt00000DDyznIAD%' OR emailmessage."relatedtoid" LIKE '%500Wt00000DDyznIAD%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[010](../runs/fad/crmarenapro/query7/full-01/sql/010-98ddb2561f6e42e7b021bba84c5c822e.sql)、[012](../runs/fad/crmarenapro/query7/full-01/sql/012-a2adad4df29a4db099b6563d30f7f532.sql)

<a id="c0035"></a>
## C0035 · crmarenapro/query8 · fad · 公共筛选

数据库：`support`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
casehistory__c
```
共同表达式/条件：
```
casehistory__c."field__c" = 'Owner Assignment'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/fad/crmarenapro/query8/full-01/sql/002-bb0f03a3a13d4b248923f8833d866155.sql)、[003](../runs/fad/crmarenapro/query8/full-01/sql/003-814416a199f14106b3245afe35947247.sql)、[004](../runs/fad/crmarenapro/query8/full-01/sql/004-475b9e44709c4b199411ad7a8ee40cdc.sql)

<a id="c0036"></a>
## C0036 · googlelocal/query3 · fad · 公共筛选

数据库：`business_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
business_description
```
共同表达式/条件：
```
business_description."hours" IS NOT NULL
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/googlelocal/query3/full-01/sql/004-61b536c39cc249a09f7712e67097e377.sql)、[006](../runs/fad/googlelocal/query3/full-01/sql/006-4962efe96a4e4fbcb0986a5d46f2de22.sql)

<a id="c0037"></a>
## C0037 · music_brainz_20k/query3 · fad · 同输入同分组聚合状态

数据库：`sales_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "sales"  GROUP BY sales."track_id"
```
共同表达式/条件：
```
SUM(sales."revenue_usd")
SUM(sales."units_sold")
```

准备方式：在完全相同输入与分组上准备此聚合的完整结果/状态，保留全部分组后再施加各自 HAVING、排序和 LIMIT。

边界：基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

消费者：[003](../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql)、[005](../runs/fad/music_brainz_20k/query3/full-01/sql/005-dd8f3354db5d4de5adca29b3abf3edae.sql)

<a id="c0038"></a>
## C0038 · stockindex/query1 · fad · 公共筛选

数据库：`indextrade_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
index_trade
```
共同表达式/条件：
```
index_trade."index" IN ('HSI', '000001.SS', '399001.SZ', 'N225', 'NSEI', 'TWII')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql)、[007](../runs/fad/stockindex/query1/full-01/sql/007-1678feef9bfb4902a48185f0ca405ed2.sql)

<a id="c0039"></a>
## C0039 · yelp/query1 · fad · 公共筛选

数据库：`user_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
review
```
共同表达式/条件：
```
review."business_ref" IN ('businessref_52', 'businessref_84', 'businessref_76', 'businessref_87', 'businessref_65', 'businessref_94', 'businessref_90', 'businessref_16')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql)、[005](../runs/fad/yelp/query1/full-01/sql/005-ceeb4c2d6d104325b327b8be83d7b988.sql)

<a id="c0040"></a>
## C0040 · yelp/query3 · fad · 公共筛选

数据库：`user_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
review
```
共同表达式/条件：
```
review."date" >= '2018-01-01'
review."date" < '2019-01-01'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/fad/yelp/query3/full-01/sql/002-9450824df55a4f2bb109cd847fff92e9.sql)、[003](../runs/fad/yelp/query3/full-01/sql/003-3ef9cd02c2334f2587cb305c74b66417.sql)

<a id="c0041"></a>
## C0041 · DEPS_DEV_V1/query1 · natural · 公共筛选

数据库：`package_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
packageinfo
```
共同表达式/条件：
```
packageinfo."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/006-a5bb89312e0d448cb255b1451afd469e.sql)、[007](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/007-4164a10ca28741d095ee7b9f5583819b.sql)、[009](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/009-a46400c1ac19499d934e4518e65ae405.sql)

<a id="c0042"></a>
## C0042 · DEPS_DEV_V1/query1 · natural · 公共筛选

数据库：`project_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
project_packageversion
```
共同表达式/条件：
```
project_packageversion."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[008](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/008-2982192d5f29437b8cc1507584f17c5f.sql)、[012](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/012-0b726662f08d4931a79cbdacd2869ab8.sql)

<a id="c0043"></a>
## C0043 · DEPS_DEV_V1/query1 · natural · 派生计算

数据库：`project_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
project_info
```
共同表达式/条件：
```
REGEXP_EXTRACT(project_info."project_information", 'The project ([^ ]+)', 1)
REGEXP_EXTRACT(project_info."project_information", '([0-9]+) stars', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[011](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/011-caabc4aa663a4ec3b1ba92fa4836207a.sql)、[013](../runs/natural/DEPS_DEV_V1/query1/full-01/sql/013-8f39780a9c91476f8049aec18951828b.sql)

<a id="c0044"></a>
## C0044 · DEPS_DEV_V1/query2 · natural · 公共筛选

数据库：`package_database`；任务验证：未通过；涉及 4 次调用，首次之后 3 次。

共同输入：
```sql
packageinfo
```
共同表达式/条件：
```
packageinfo."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/005-3b2c0e630df84ff7a8e9dcde693eaa05.sql)、[006](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/006-a8d60bd81720489fbf580187eb35451b.sql)、[008](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/008-cdae6aacd2f047c39deba46ac6e5b804.sql)、[011](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)

<a id="c0045"></a>
## C0045 · DEPS_DEV_V1/query2 · natural · 公共筛选

数据库：`project_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
project_packageversion
```
共同表达式/条件：
```
project_packageversion."system" = 'NPM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/007-bc6169bc8e5e49db8ab11b95b3cc8328.sql)、[010](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql)、[015](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql)

<a id="c0046"></a>
## C0046 · DEPS_DEV_V1/query2 · natural · 公共筛选

数据库：`package_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
packageinfo
```
共同表达式/条件：
```
packageinfo."licenses" LIKE '%"MIT"%'
packageinfo."versioninfo" LIKE '%"IsRelease": true%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[008](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/008-cdae6aacd2f047c39deba46ac6e5b804.sql)、[011](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)

<a id="c0047"></a>
## C0047 · DEPS_DEV_V1/query2 · natural · 公共筛选

数据库：`project_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
project_packageversion
```
共同表达式/条件：
```
project_packageversion."projecttype" = 'GITHUB'
project_packageversion."projectname" IN ('lberrocal/npm-packages-template', 'leaflet/leaflet', 'leaflet/leaflet.fullscreen', 'leaflet/leaflet.markercluster', 'leandrowd/react-responsive-carousel', 'learnfrontend-dc/product-cart', 'ledgerproject/keypairoom', 'leebyron/jasmine-check', 'leebyron/testcheck-js', 'leecade/react-native-swiper', 'legendjaden/aftablecolumn', 'lekoarts/gatsby-themes', 'lenconda/dollie', 'leo-ran/easy-node-reflect', 'leo-ran/easy-node-server', 'leofelix077/bunchofnothing', 'leoilab/react-native-analytics-segment-io', 'leonardparisi/easy-express-server', 'leoroese/template-cli', 'letrungdo/react-ui-component-lib', 'levelkdev/dxswap-sdk', 'leviticusmb/divine-amd-loader', 'leviticusmb/divine-synchronization', 'leviticusmb/esxx-2', 'leviticusmb/ghostly', 'leviticusmb/sysconsole', 'lfujiwara/dnausp-core', 'libertydsnp/activity-content', 'libertydsnp/contracts', 'libertydsnp/parquetjs', 'libertydsnp/sdk-ts', 'libertydsnp/test-generators', 'libertyequalitydata/dynamic-data', 'liivevideo/react-native-web-webrtc', 'linkshare/service-container', 'lisiadito/checksslcertificate', 'litejs/natural-compare-lite', 'ljharb/define-properties', 'ljharb/has-symbols', 'ljharb/object-keys', 'ljharb/object.assign', 'ljharb/qs', 'ln-zap/node-lnd-grpc', 'locize/fluent_conv', 'lodash/lodash', 'logflare/winston-logflare', 'lohfu/dom-append-to', 'lohfu/dom-children', 'lohfu/dom-closest', 'lohfu/dom-insert-after', 'lohfu/domp', 'lohfu/domp-create', 'lohfu/domp-create-many', 'lohfu/domp-is', 'loktor/image-compressor', 'lonelycpp/react-native-youtube-iframe', 'lrembacz/dragndrop', 'lrembacz/vue-dragndrop.', 'ltsfran/dreamtec-ui', 'lucasferreira/react-native-flash-message', 'lucassifoni/ondif-js', 'luckylooke/dragon', 'luehang/react-native-masonry-list', 'lukasz-galka/ngx-gallery', 'lukeed/escalade', 'luzzif/ethereum-contacts-registry', 'lxg1992/sharedlotide', 'lydell/js-tokens', 'lzrski/node-damerau-levenshtein', 'm1212e/easy-rpc-browser', 'maddijoyce/serverless-ses-mjml', 'mafintosh/generate-function', 'mafintosh/generate-object-property', 'mafintosh/is-my-json-valid', 'mafintosh/tar-fs', 'magnusdanielson/au-fluent-ui', 'magnusdanielson/au-office-ui', 'magnusdanielson/aureactwrapper', 'maksimovicdanijel/vue-countdown', 'malte-wessel/react-custom-scrollbars', 'mammadataei/dom-assertions', 'mapbox/mapbox-gl-draw', 'mapbox/mapbox-gl-js', 'mapbox/node-pre-gyp', 'mapbox/node-sqlite3', 'mapbox/shp-write', 'marak/colors.js', 'marcbachmann/node-html-pdf', 'marcelklehr/toposort', 'march08/duik', 'marijnh/moduleserve', 'mariuszfoltak/angular2-datatable', 'mark-shark/edge-scss', 'markcellus/wait-for-element-transition', 'markhughes/droppy', 'marknotton/doggistyle', 'markormesher/dragonlabs-eslint-config', 'markormesher/dragonlabs-redux-cache-key-util', 'marmelab/gremlins.js', 'maronato/vue-toastification', 'martinalmlof/homebridge-pioneer-vsx527', 'martinpagesaal/ngx-ace-editor-wrapper', 'marvin-j97/tunisia', 'marvin-j97/yxc', 'master-atul/react-native-exception-handler', 'matejlauko/duotone', 'mathe42/vite-plugin-serviceworker', 'mathiasbynens/cssesc', 'mathiasbynens/he', 'mathiasbynens/jsesc', 'mathiasbynens/regenerate', 'mathiasbynens/regenerate-unicode-properties', 'mathiasbynens/regexpu-core', 'mathiasbynens/string.prototype.codepointat', 'mathiasbynens/unicode-canonical-property-names-ecmascript', 'mathiasbynens/unicode-match-property-ecmascript', 'mathiasbynens/unicode-match-property-value-ecmascript', 'mathiasbynens/unicode-property-aliases-ecmascript', 'mathiasgheno/ducto', 'maticnetwork/matic.js', 'matoseb/musee-de-la-main-2022-scripts', 'matt-esch/virtual-dom', 'mattdesl/ghpages', 'matthiaaas/express-file-routing', 'mattilehtinen/postgrator-cli', 'mattlewis92/angular-confirmation-popover', 'mattphillips/deep-object-diff', 'mauriciohernancabrera/tymo-utils', 'maxinminax/node-mihome', 'maxogden/concat-stream', 'maxwellsquared/lotide', 'mbrn/material-table', 'mcavage/node-asn1', 'mcavage/node-assert-plus', 'mchlbrnd/normalizr-decorators', 'mcicheick/dd-react-lib', 'mdevils/node-html-entities', 'medelman17/edel.monster', 'medikoo/d', 'medikoo/es5-ext', 'medikoo/es6-iterator', 'medikoo/es6-map', 'medikoo/es6-set', 'medikoo/es6-symbol', 'medikoo/es6-weak-map', 'medikoo/event-emitter', 'medusajs/medusa', 'meetearnest/eslint-config-earnest', 'meetearnest/eslint-config-earnest-es7', 'meettya/whet.extend', 'megafetis/vue3-treeselect', 'meganz/jodid25519', 'mengxiong10/vue2-datepicker', 'menudocs/erela.js', 'meryn/performance-now', 'mhart/aws4', 'mhart/stringstream', 'miaowing/schedule', 'michael-ciniawsky/postcss-load-config', 'michael-ciniawsky/postcss-load-options', 'michael-ciniawsky/postcss-load-plugins', 'michaeljier/easy-messenger', 'micky2be/superlogin-client', 'microlinkhq/youtube-dl-exec', 'microsoft/monaco-editor', 'microsoft/monaco-editor-webpack-plugin', 'microsoft/typescript', 'microsoft/typescript-website', 'microsoft/web-build-tools', 'miguelfernandez008/test-npm-package', 'mikaelbr/marked-terminal', 'mikaelbr/node-notifier', 'mike-dax/gatsby-plugin-ffmpeg', 'mike-dax/gatsby-remark-videos', 'mike-spainhower/querystring', 'mikeal/aws-sign', 'mikeal/caseless', 'mikeal/forever-agent', 'mikeal/oauth-sign', 'mikeal/tunnel-agent', 'mikeal/watch', 'mikemcl/big.js', 'mikolalysenko/is-property', 'mikolalysenko/uniq', 'milanovic-dusan/bb-model', 'mindary/drpc', 'mindoktor/material-ui', 'mindoktor/pulse', 'mioriaty/duong-custom-ckeditor5', 'mirrorjs/mirror', 'mirrorthink/vue-wow', 'mirumee/saleor-sdk', 'mishoo/uglifyjs2', 'mixer/arcade-machine', 'mixu/markdown-styles', 'mjmlio/mjml', 'mkayander/easyenv', 'mklabs/node-fileset', 'mmaakkii/dmanz-connector', 'mmende/homebridge-samsungtv-control2', 'mnasyrov/ditox', 'mobilereality/react-native-select-pro', 'mobxjs/mobx', 'mokkabonna/inquirer-autocomplete-prompt', 'moment/moment', 'momsfriendlydevco/doop-avatar', 'momsfriendlydevco/doop-cache', 'momsfriendlydevco/doop-core-vue', 'momsfriendlydevco/doop-dates', 'momsfriendlydevco/doop-debug', 'momsfriendlydevco/doop-deepstream', 'momsfriendlydevco/doop-deloy', 'momsfriendlydevco/doop-deploy', 'momsfriendlydevco/doop-digest', 'momsfriendlydevco/doop-directive-jump', 'momsfriendlydevco/doop-docs', 'momsfriendlydevco/doop-drag-drop', 'momsfriendlydevco/doop-dynamic-component', 'momsfriendlydevco/doop-eslint-plugin-doop', 'momsfriendlydevco/doop-eval', 'momsfriendlydevco/doop-files', 'momsfriendlydevco/doop-http', 'momsfriendlydevco/doop-locking', 'momsfriendlydevco/doop-permissions', 'momsfriendlydevco/doop-polyfills', 'momsfriendlydevco/doop-prompt', 'momsfriendlydevco/doop-search', 'momsfriendlydevco/doop-service-clipboard', 'momsfriendlydevco/doop-service-code-alloc', 'momsfriendlydevco/doop-service-components', 'momsfriendlydevco/doop-service-config', 'momsfriendlydevco/doop-service-data', 'momsfriendlydevco/doop-service-db', 'momsfriendlydevco/doop-service-debug', 'momsfriendlydevco/doop-service-dirty-checker', 'momsfriendlydevco/doop-service-emit', 'momsfriendlydevco/doop-service-eval', 'momsfriendlydevco/doop-service-files', 'momsfriendlydevco/doop-service-git', 'momsfriendlydevco/doop-service-http', 'momsfriendlydevco/doop-service-lifecycle', 'momsfriendlydevco/doop-service-loader', 'momsfriendlydevco/doop-service-locking', 'momsfriendlydevco/doop-service-lodash', 'momsfriendlydevco/doop-service-log-change', 'momsfriendlydevco/doop-service-morph', 'momsfriendlydevco/doop-service-oid', 'momsfriendlydevco/doop-service-prompt', 'momsfriendlydevco/doop-service-pub-sub', 'momsfriendlydevco/doop-service-replace', 'momsfriendlydevco/doop-service-router', 'momsfriendlydevco/doop-service-screen', 'momsfriendlydevco/doop-service-slack', 'momsfriendlydevco/doop-service-throttle', 'momsfriendlydevco/doop-service-timeout', 'momsfriendlydevco/doop-service-timestamps', 'momsfriendlydevco/doop-service-toast', 'momsfriendlydevco/doop-service-transitions', 'momsfriendlydevco/doop-service-watch-all', 'momsfriendlydevco/doop-table', 'momsfriendlydevco/doop-throttle', 'momsfriendlydevco/doop-timeout', 'momsfriendlydevco/doop-validate', 'mono/mono', 'moonshotcollective/scaffold-moonshot-starter', 'mooory/ckeditor5-custom', 'moox/eslint-loader', 'moox/postcss-message-helpers', 'moox/reduce-css-calc', 'moox/reduce-function-call', 'moregidge/parsley.js', 'morgbillingsley/mailer-domain', 'moribvndvs/ng2-idle', 'mormubis/elo', 'mormubis/pgn', 'morphatic/v-stripe-elements', 'motdotla/dotenv', 'mousumidutta136/lotide', 'mozilla-services/react-jsonschema-form', 'mozilla/pdf.js', 'mozilla/pdfjs-dist', 'mozilla/source-map', 'mpetroff/pannellum', 'mpoiriert/service-container', 'mr-strike/react-native-advance-draggable-view', 'mr-strike/react-native-advance-image-cropper', 'mrdannael/easy-eva-icons', 'ms-dg/api-typings', 'ms-dg/create-dg-react', 'ms-dg/miniprogram-storage', 'mui-org/material-ui', 'muniftanjim/draft-js-modules', 'murhafsousli/ngx-sharebuttons', 'mweststrate/relative-deps', 'mybabysexy/react-sip-phone', 'mythie/dockite', 'myzhangdong/log-collect', 'n05ae/react-virtual-scroll-list', 'n0sae/react-virtual-list', 'n43/easyapp', 'n4kz/react-native-material-textfield', 'naknode/test', 'namespace-ee/react-calendar-timeline', 'nandorojo/dripsy', 'nandorojo/expo-theme-ui', 'nanzm/dora', 'naoufal/react-native-payments', 'naoufal/react-native-touch-id', 'napthedev/react-tuby', 'nartc/react-native-barcode-mask', 'nasa8x/html-metadata-parser', 'nativescript/plugins', 'natural-apptitude/ngrx-store-ionic-storage', 'naugtur/xhr', 'ndmitry/grunt-postcss', 'nebulouslabs/nodejs-sia', 'nedredmond/dsa-ui', 'nehr/ws-scss-mixins', 'quangbuule/extract-hoc', 'quartzjer/ecc-jsbn', 'quentinsvn/react-native-fix', 'quilljs/quill', 'qyjs/captchajs', 'ra-protocol/ra-protocol', 'rackt/async-props', 'rahuldream11/react-native-analytics-segment-io', 'rails/rails', 'rajdee/postcss-autoimport', 'rajneeshraghav/resumable-file-uploads', 'rajneeshraghav/wexer-videojs', 'ramdan123/default-token-list', 'rampnetwork/crypto-address-validator', 'rangoo94/easen-tools', 'rashagu/dnd-kit-vue', 'rauldeheer/use-async-effect', 'raynos/console-browserify', 'raynos/duplexer', 'raynos/function-bind', 'raynos/xtend', 'react-component/dropdown', 'react-component/picker', 'react-component/select', 'react-component/slider', 'react-component/tabs', 'react-csv/react-csv', 'react-icons/react-icons', 'react-materialize/react-materialize', 'react-native-admob/admob', 'react-native-community/react-native-tab-view', 'react-native-community/react-native-webview', 'react-native-device-info/react-native-device-info', 'react-native-elements/react-native-elements', 'react-native-webrtc/react-native-webrtc', 'react-navigation/react-navigation', 'react-qr-reader/react-qr-reader', 'react-toolbox/react-toolbox', 'reactive-extensions/rxjs', 'reactjs-ui/reactjs-pull-refresh', 'reactjs/react-art', 'realdolos/node-jpegoptim', 'realtymaps/promise-ftp', 'reasonml-community/bs-express', 'reasonml-community/bs-webapi-incubator', 'reasonml-community/graphql_ppx', 'rebilly/redoc', 'redpandatronicsuk/react-native-check-app-install', 'redux-observable/redux-observable', 'reg2005/adonis5-scheduler', 'regexps/filename-regex', 'release-it/conventional-changelog', 'remarkjs/remark-github', 'remaxjs/remax', 'renddslow/dunsany', 'reposilite-playground/jsonforms', 'request/promise-core', 'request/request', 'request/request-promise', 'resembli/docusolid', 'rethinkdb/rethinkdb-ts', 'revsoul12/lotide', 'rhumaric/express-mount-files', 'ribeiro-tiago/bundletool', 'richmccartney/design-system-monorepo', 'riophae/vue-treeselect', 'rishabh09/duffle-bag', 'rjsf-team/react-jsonschema-form', 'rjw57/grib.js', 'rmartone/missionlog', 'robbederks/downzip', 'robbiesdream/ci-tests', 'robinbiao/dw', 'robinfehr/react-portal', 'rojer95/dslate', 'royriojas/file-entry-cache', 'royriojas/flat-cache', 'rrag/react-stockcharts', 'rrdelaney/reason', 'rreverser/acorn-jsx', 'rs/node-netmask', 'rstiller/inspector-elasticsearch', 'rstiller/inspector-vm', 'rubengrill/apollo-typed-documents', 'ruimarinho/bitcoin-core', 'ruinouscheng/share-config', 'run-z/rollup-plugin-flat-dts', 'rustwasm/create-wasm-app', 'rvagg/bl', 'rvagg/isstream', 'rvagg/node-errno', 'rvagg/node-worker-farm', 'rvagg/prr', 'rvagg/string_decoder', 'ryan-lau314/modularscale-sass', 'sabakihq/gtp', 'saiya/dsps', 'salesforce/lwc', 'salesforce/tough-cookie', 'salesforceeng/tough-cookie', 'samsaffron/message_bus', 'samuelgoto/docscript', 'samverschueren/generator-alfred', 'sanity-io/cross-dataset-duplicator', 'sanity-io/gatsby-source-sanity', 'santiment/san-ui', 'sarin-dotin/eslint-config-react-native', 'sass/node-sass', 'sastan/distilt', 'satya164/react-simple-code-editor', 'savokiss/vue-raven', 'sboudrias/inquirer.js', 'sboudrias/readline2', 'sboudrias/run-async', 'scarlatum/eccheuma-crusoris', 'schickling/gulp-webserver', 'schmich/instascan', 'scnale/openzeppelin-upgrades', 'scniro/react-codemirror2', 'scravy/node-macaddress', 'seansobey/markdown-preprocessor', 'searchkit/searchkit', 'sebinsua/docco-next', 'sebmaster/tr46.js', 'secretmapper/react-image-annotation', 'securingsincity/react-ace', 'segmentio/analytics-node', 'segmentio/helpscout', 'seishun/node-steam-crypto', 'selkkie/nodebb-plugin-sso-discord-with-logo', 'semantic-org/semantic-ui', 'semantic-org/semantic-ui-css', 'semantic-release/git', 'semantic-release/npm', 'senecajs/seneca-mesh', 'sentrei/dogan', 'serverless-nextjs/serverless-next.js', 'sethsandaru/vue-form-builder', 'sethvincent/dxv', 'sfundomhlungu/-dot.product-createlib', 'sgguo/dc-datatable', 'shahen94/react-native-switch', 'shaka-project/shaka-player', 'shama/gaze', 'shanebo/balm', 'shanebo/coerce', 'shanebo/cors', 'shanebo/csrf', 'shanebo/engines', 'shanebo/forcessl', 'shanebo/ip-limiter', 'shanebo/parser', 'shanebo/session', 'shanebo/slashless', 'shanebo/static', 'shanebo/swap-redirect', 'sharaal/dnode', 'sharaal/maxdome-rssfeeds', 'sharaal/sharaal', 'shelljs/shelljs', 'shinnn/is-resolvable', 'shinnn/spdx-license-ids', 'shopify/polaris-icons', 'shopify/polaris-react', 'shopify/quilt', 'shtylman/node-browser-resolve', 'shtylman/node-process', 'shwetdream11/react-native-fast-image', 'shwetdream11/react-native-google-analytics-bridge', 'shwetdream11/react-native-shimmer', 'signal-noise/index-core', 'signavio/react-mentions', 'siimon/prom-client', 'simeonackermann/rdform', 'sindresorhus/active-win', 'sindresorhus/ansi-escapes', 'sindresorhus/ansi-regex', 'sindresorhus/array-differ', 'sindresorhus/array-find-index', 'sindresorhus/array-union', 'sindresorhus/array-uniq', 'sindresorhus/arrify', 'sindresorhus/binary-extensions', 'sindresorhus/builtin-modules', 'sindresorhus/caller-path', 'sindresorhus/callsites', 'sindresorhus/camelcase', 'sindresorhus/camelcase-keys', 'sindresorhus/cli-cursor', 'sindresorhus/code-point-at', 'sindresorhus/decamelize', 'sindresorhus/del', 'sindresorhus/detect-indent', 'sindresorhus/escape-string-regexp', 'sindresorhus/exit-hook', 'sindresorhus/figures', 'sindresorhus/find-up', 'sindresorhus/get-stdin', 'sindresorhus/globals', 'sindresorhus/globby', 'sindresorhus/gzip-size', 'sindresorhus/has-ansi', 'sindresorhus/has-color', 'sindresorhus/has-flag', 'sindresorhus/home-or-tmp', 'sindresorhus/indent-string', 'sindresorhus/invert-kv', 'sindresorhus/is-absolute-url', 'sindresorhus/is-binary-path', 'sindresorhus/is-builtin-module', 'sindresorhus/is-finite', 'sindresorhus/is-fullwidth-code-point', 'sindresorhus/is-path-cwd', 'sindresorhus/is-path-in-cwd', 'sindresorhus/is-path-inside', 'sindresorhus/is-plain-obj', 'sindresorhus/is-svg', 'sindresorhus/lcid', 'sindresorhus/leven', 'sindresorhus/load-json-file', 'sindresorhus/loud-rejection', 'sindresorhus/map-obj', 'sindresorhus/meow', 'sindresorhus/multimatch', 'sindresorhus/ncname', 'sindresorhus/normalize-url', 'sindresorhus/number-is-nan', 'sindresorhus/object-assign', 'sindresorhus/onetime', 'sindresorhus/opn', 'sindresorhus/os-homedir', 'sindresorhus/os-locale', 'sindresorhus/os-tmpdir', 'sindresorhus/p-filter', 'sindresorhus/p-limit', 'sindresorhus/p-map', 'sindresorhus/parse-json', 'sindresorhus/path-exists', 'sindresorhus/path-is-absolute', 'sindresorhus/path-key', 'sindresorhus/path-type', 'sindresorhus/pify', 'sindresorhus/pkg-dir', 'sindresorhus/pkg-up', 'sindresorhus/prepend-http', 'sindresorhus/query-string', 'sindresorhus/read-pkg', 'sindresorhus/read-pkg-up', 'sindresorhus/redent', 'sindresorhus/repeating', 'sindresorhus/require-uncached', 'sindresorhus/resolve-from', 'sindresorhus/restore-cursor', 'sindresorhus/set-immediate-shim', 'sindresorhus/shebang-regex', 'sindresorhus/slash', 'sindresorhus/sort-keys', 'sindresorhus/string-width', 'sindresorhus/strip-bom', 'sindresorhus/strip-indent', 'sindresorhus/strip-json-comments', 'sindresorhus/to-fast-properties', 'sindresorhus/trim-newlines', 'sindresorhus/user-home', 'sindresorhus/xml-char-classes', 'sindresorhus/yocto-queue', 'skeleton-metal/apollo-server-express', 'skick1234/discord-ytdl-core', 'skick1234/node-youtube-dl', 'skick1234/node-ytpl', 'skick1234/node-ytsr', 'sky111144/easyregexp', 'sky111144/easytype', 'slorber/responsive-loader', 'snowpackjs/snowpack', 'sockjs/sockjs-client', 'sockjs/sockjs-node', 'softwarebrothers/adminjs-mongoose', 'solana-labs/wallet-adapter', 'soliantconsulting/fm-data-api-client', 'solinor/react-native-bluetooth-status', 'soluto/dynamico', 'sortablejs/vue.draggable', 'soumyatiwari392/ds-awesome', 'sourcey/spectacle', 'spautz/dynamic-selectors', 'spike-the-coder/electron-privacy', 'spite/three.meshline', 'spruceid/siwe', 'sridharsathasivam/data-lib', 'sscfaith/avue-form-design', 'sstur/draft-js-export-html', 'stabzs/angular2-toaster', 'stackbithq/datocms-plugin-typed-list', 'stacktical/stacktical-dsla-contracts', 'starchup/node-converge', 'stardustapp/javascript-client', 'starnutoditopo/react-typescript-flight-indicators', 'stefanpenner/get-caller-file', 'steffeydev/react-native-popover-view', 'stephenliu1944/beancommons-define', 'stephenliu1944/beancommons-http', 'stephenliu1944/beancommons-proxy', 'stephenliu1944/beanreact-permission', 'stephenliu1944/easytool-define-config', 'stephenliu1944/easytool-http', 'stephenliu1944/easytool-react-carousel', 'stephenliu1944/easytool-react-permission', 'stephenliu1944/easytool-react-types', 'stephenliu1944/mock-server', 'stevelacy/browser-info', 'stevemao/html-comment-regex', 'stevenvachon/http-equiv-refresh', 'stevenvachon/relateurl', 'stidges/laravel-mix-mjml', 'stimulcross/donation-alerts', 'stoneqq11/react-dialog', 'stoneqq11/react-lazy-img', 'stoneqq11/react-load-more', 'stoneqq11/react-loading', 'stoneqq11/react-trans-btn', 'storybookjs/react-treebeard', 'strapi/strapi', 'stream-utils/destroy', 'stream-utils/unpipe', 'strongholdmedia/react-vs-calendar', 'strongholdmedia/react-vs-tagger', 'strongholdmedia/react-vs-tree', 'strongholdmedia/usable', 'strongloop/fsevents', 'styled-components/styled-components', 'substack/defined', 'substack/http-browserify', 'substack/https-browserify', 'substack/json-stable-stringify', 'substack/jsonify', 'substack/minimist', 'substack/node-commondir', 'substack/node-concat-map', 'substack/node-mkdirp', 'substack/node-optimist', 'substack/node-resolve', 'substack/node-wordwrap', 'substack/path-browserify', 'substack/stream-browserify', 'substack/text-table', 'substack/tty-browserify', 'substack/typedarray', 'substack/vm-browserify', 'sudomaker/dominative-solid', 'sudomaker/dominative-vue', 'suminksudhi/nativescript-notification', 'suminksudhi/react-media-loader', 'supasate/connected-react-router', 'surnet/graphql-amqp-subscriptions', 'suryacandra/cratail', 'sushiswap/sushiswap-sdk', 'suweya/react-verification-code-input', 'sveltejs/prettier-plugin-svelte', 'sveltejs/sapper', 'sveltejs/site-kit', 'sveltejs/svelte', 'svenchristian/react-progressive-loader', 'svg/svgo', 'swagger-api/swagger-ui', 'swdenglian/dva-rn', 'sweetiq/schemats', 'swolf88/types-4-strapi', 'swuecho/camelsnakekebab_bs', 'swuecho/jinja_bin', 'synw/docdundee', 'sysgears/domain-schema', 'szpadel/chrome-headless-render-pdf', 'szymmis/vite-express', 't3dkich/smart-order-router-maistestsubnet-modded', 'tabookey-dev/tabookey-gasless', 'tada5hi/ebec', 'tadejgasparovic/multer-storage-google-cloud', 'taidomi-sapi-de-cv/domitai-sdk', 'tailwindcss/tailwindcss', 'tailwindcss/typography', 'taixw2/dx', 'tanhauhau/levenary', 'tapjs/signal-exit', 'tappleby/redux-batched-subscribe', 'tarruda/has', 'teambank/easycredit-ratenkauf-webcomponents', 'teamdock/password-cli', 'techroad-community/dooda-swap-core', 'techroad-community/dooda-swap-sdk', 'techroad-community/dooda-toolkit', 'tencent/vconsole', 'terkelg/prompts', 'ternjs/acorn', 'tetther1122/job-board', 'th3rdwave/react-native-safe-area-context', 'the-eater/grunt-po2mo', 'the-economist-editorial/component-404', 'the-economist-editorial/component-ad-panel', 'the-economist-editorial/component-articletemplate', 'the-economist-editorial/component-gallery', 'the-economist-editorial/component-imagecaption', 'the-economist-editorial/component-scenechanger', 'the-economist-editorial/component-silver-bullet', 'the-economist-editorial/component-video', 'the-economist-editorial/sharebar', 'the-front-distillery/stylelint-config-distillery', 'theabraham/growly', 'thebigbrain/dora.js', 'theboringschool/toast-notify', 'thedeeno/web-component-tester-istanbul', 'theia-ide/theia', 'thejameskyle/pretty-format', 'thejameskyle/react-loadable', 'thejameskyle/spectacle-code-slide', 'then/promise', 'theodo-uk/nestjs-admin', 'theprateinteractives/common-lists', 'theprateinteractives/generation-game', 'thesoftwarehouse/react-router-permissions', 'thinkjs/think-sequelize', 'thlorenz/ansicolors', 'thlorenz/cardinal', 'thlorenz/convert-source-map', 'thlorenz/deep-is', 'thlorenz/readdirp', 'thlorenz/redeyed', 'thomasdondorf/puppeteer-cluster', 'thomwright/postgres-migrations', 'thoughtsunificator/domodel-chat', 'thoughtsunificator/domodel-form', 'thoughtsunificator/domodel-paginator', 'thoughtsunificator/domodel-popup', 'thoughtsunificator/domodel-resizable', 'thoughtsunificator/domodel-router', 'thoughtsunificator/domodel-steps', 'thoughtsunificator/domodel-tabs', 'tigthor/associated-token', 'tigthor/borsh', 'tigthor/dvst', 'tigthor/pool', 'timhall/svelte-apollo', 'timpaulaskasds/sfparty', 'tirupatibalaji-dev/djs-handler', 'titel-media/node-fetch', 'tj/co', 'tj/commander.js', 'tjatse/ansi-html', 'tkellen/node-interpret', 'tmpvar/jsdom', 'toilal/ng-pickadate', 'wizards-lab/routing')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[010](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql)、[015](../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql)

<a id="c0048"></a>
## C0048 · GITHUB_REPOS/query2 · natural · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
languages
```
共同表达式/条件：
```
languages."language_description" LIKE '%Swift%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/GITHUB_REPOS/query2/full-01/sql/004-ba83de1dba9d4d5cb42a837e90671e9c.sql)、[005](../runs/natural/GITHUB_REPOS/query2/full-01/sql/005-c4b0bd63b6004ccc832b096c28c942dd.sql)、[013](../runs/natural/GITHUB_REPOS/query2/full-01/sql/013-72dd1f7f2fed4c1cbae168634d642bb3.sql)

<a id="c0049"></a>
## C0049 · GITHUB_REPOS/query2 · natural · 公共筛选

数据库：`artifacts_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
contents
```
共同表达式/条件：
```
LOWER(contents."repo_data_description") LIKE '%non-binary%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/GITHUB_REPOS/query2/full-01/sql/007-28663d17f2dc4fe5a85eaca518fdc05d.sql)、[012](../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql)、[014](../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql)

<a id="c0050"></a>
## C0050 · GITHUB_REPOS/query2 · natural · 派生计算

数据库：`artifacts_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
contents
```
共同表达式/条件：
```
REGEXP_EXTRACT(contents."repo_data_description", '(\d+) times', 1)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[007](../runs/natural/GITHUB_REPOS/query2/full-01/sql/007-28663d17f2dc4fe5a85eaca518fdc05d.sql)、[012](../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql)

<a id="c0051"></a>
## C0051 · GITHUB_REPOS/query2 · natural · 公共筛选

数据库：`artifacts_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
files
```
共同表达式/条件：
```
files."path" LIKE '%.swift'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[012](../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql)、[014](../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql)

<a id="c0052"></a>
## C0052 · GITHUB_REPOS/query2 · natural · 公共内连接

数据库：`artifacts_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
FROM "files" JOIN "contents" ON files."id" = contents."id"
```
共同表达式/条件：
```
FROM "files" JOIN "contents" ON files."id" = contents."id"
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[012](../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql)、[014](../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql)、[016](../runs/natural/GITHUB_REPOS/query2/full-01/sql/016-29d8fde5f6b2417ab64a22f5a1353250.sql)

<a id="c0053"></a>
## C0053 · GITHUB_REPOS/query3 · natural · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 4 次调用，首次之后 3 次。

共同输入：
```sql
languages
```
共同表达式/条件：
```
languages."language_description" LIKE '%Shell%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/GITHUB_REPOS/query3/full-01/sql/004-8c7f674562584430bdf7657a7315e37c.sql)、[007](../runs/natural/GITHUB_REPOS/query3/full-01/sql/007-be8a2c6eb15f4ebab8e4bf7634c6b9a7.sql)、[009](../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql)、[010](../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

<a id="c0054"></a>
## C0054 · GITHUB_REPOS/query3 · natural · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 4 次调用，首次之后 3 次。

共同输入：
```sql
languages
```
共同表达式/条件：
```
languages."language_description" NOT LIKE '%PowerShell%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/GITHUB_REPOS/query3/full-01/sql/007-be8a2c6eb15f4ebab8e4bf7634c6b9a7.sql)、[008](../runs/natural/GITHUB_REPOS/query3/full-01/sql/008-8afe57c746fd4367acbf2d22ce260003.sql)、[009](../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql)、[010](../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

<a id="c0055"></a>
## C0055 · GITHUB_REPOS/query3 · natural · 公共筛选

数据库：`metadata_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
licenses
```
共同表达式/条件：
```
licenses."license" = 'apache-2.0'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[009](../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql)、[010](../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

<a id="c0056"></a>
## C0056 · GITHUB_REPOS/query3 · natural · 公共内连接

数据库：`metadata_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```
共同表达式/条件：
```
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[009](../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql)、[010](../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

<a id="c0057"></a>
## C0057 · GITHUB_REPOS/query3 · natural · 公共筛选

数据库：`artifacts_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
commits
```
共同表达式/条件：
```
commits."repo_name" IN ('tensorflow/tensorflow', 'apple/swift')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[014](../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql)、[015](../runs/natural/GITHUB_REPOS/query3/full-01/sql/015-8c2c935d46744e8291f00620c81ebc25.sql)

<a id="c0058"></a>
## C0058 · PANCANCER_ATLAS/query1 · natural · 公共筛选

数据库：`clinical_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."patient_description" ILIKE '%lower grade glioma%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/005-0911b7f14f5e4e76ba6b8ccfde2c8992.sql)、[006](../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/006-0eb1aa77de8f4859b1d1a4335ab1dbc3.sql)

<a id="c0059"></a>
## C0059 · PANCANCER_ATLAS/query2 · natural · 公共筛选

数据库：`molecular_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
mutation_data
```
共同表达式/条件：
```
mutation_data."hugo_symbol" = 'CDH1'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[008](../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/008-464cda910a6b47f88a8a9215ecb00610.sql)、[009](../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/009-70e1c9ab1adc42f891de9509aefddf8d.sql)、[010](../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/010-f97a9dc6c955445aab5e99d51a34facb.sql)

<a id="c0060"></a>
## C0060 · PANCANCER_ATLAS/query3 · natural · 公共筛选

数据库：`clinical_database`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
clinical_info
```
共同表达式/条件：
```
clinical_info."patient_description" ILIKE '%Breast invasive carcinoma%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[005](../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/005-6ab3b6aaca974643858a815b39c2cf32.sql)、[006](../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/006-7a6409ae1a4e49d6a25fbada077c5230.sql)、[008](../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/008-1f0cd54a021a45e3b2969c67fce770c4.sql)

<a id="c0061"></a>
## C0061 · PANCANCER_ATLAS/query3 · natural · 公共筛选

数据库：`molecular_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
mutation_data
```
共同表达式/条件：
```
mutation_data."hugo_symbol" = 'CDH1'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/007-2131f8f97c9d4b09b2f5b401b9ed561b.sql)、[009](../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/009-fcaf927c69a242c5aca8c3894b75c3a9.sql)

<a id="c0062"></a>
## C0062 · PATENTS/query1 · natural · 公共筛选

数据库：`CPCDefinition_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
cpc_definition
```
共同表达式/条件：
```
cpc_definition."level" = 5
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/PATENTS/query1/full-01/sql/007-536111fd0d1249e8a9599126827ff697.sql)、[014](../runs/natural/PATENTS/query1/full-01/sql/014-7de1a1ef05664a21aeb1cc0a80a1423a.sql)

<a id="c0063"></a>
## C0063 · PATENTS/query2 · natural · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."patents_info" LIKE '% DE-%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/PATENTS/query2/full-01/sql/007-1fdadd328f4e4cd38767c256e6c22ca0.sql)、[008](../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql)

<a id="c0064"></a>
## C0064 · PATENTS/query2 · natural · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."grant_date" LIKE '%2019%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[008](../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql)、[014](../runs/natural/PATENTS/query2/full-01/sql/014-f53248ce62bb4a58a74c036bdb9ec427.sql)、[015](../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)

<a id="c0065"></a>
## C0065 · PATENTS/query2 · natural · 公共筛选

数据库：`publication_database`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
publicationinfo
```
共同表达式/条件：
```
publicationinfo."patents_info" LIKE '%DE-%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[013](../runs/natural/PATENTS/query2/full-01/sql/013-e1f4aa9fef1f4c6bad6d18e29df02301.sql)、[014](../runs/natural/PATENTS/query2/full-01/sql/014-f53248ce62bb4a58a74c036bdb9ec427.sql)、[015](../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)

<a id="c0066"></a>
## C0066 · bookreview/query2 · natural · 公共筛选

数据库：`books_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
books_info
```
共同表达式/条件：
```
books_info."categories" LIKE '%Literature & Fiction%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[003](../runs/natural/bookreview/query2/full-01/sql/003-acbc168cfd0440a1964a2aa049d19c9a.sql)、[004](../runs/natural/bookreview/query2/full-01/sql/004-bf45e97a9a8a42a2b015542d56e394e6.sql)

<a id="c0067"></a>
## C0067 · bookreview/query3 · natural · 公共筛选

数据库：`books_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
books_info
```
共同表达式/条件：
```
books_info."categories" LIKE '%Children''s Books%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/bookreview/query3/full-01/sql/004-ca59a07d3dd8462f83ad8d8ffd1e481b.sql)、[006](../runs/natural/bookreview/query3/full-01/sql/006-6cb64f355c544ccf842b3ce8abccb9c9.sql)

<a id="c0068"></a>
## C0068 · crmarenapro/query1 · natural · 公共筛选

数据库：`activities`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
voicecalltranscript__c
```
共同表达式/条件：
```
voicecalltranscript__c."leadid__c" = '00QWt0000089AekMAE'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[001](../runs/natural/crmarenapro/query1/full-01/sql/001-de67ecc613504a05b9d8f0d949d68ca3.sql)、[003](../runs/natural/crmarenapro/query1/full-01/sql/003-3782911cf788489a8dbfb88f0ae12ce2.sql)

<a id="c0069"></a>
## C0069 · crmarenapro/query10 · natural · 公共筛选

数据库：`support`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
casehistory__c
```
共同表达式/条件：
```
casehistory__c."field__c" = 'Owner Assignment'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[007](../runs/natural/crmarenapro/query10/full-01/sql/007-5d1c770653334d8cb49af843c02e5432.sql)、[008](../runs/natural/crmarenapro/query10/full-01/sql/008-52c1727e9424487e966229b11f44384b.sql)、[010](../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

<a id="c0070"></a>
## C0070 · crmarenapro/query10 · natural · 派生计算

数据库：`support`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
case
```
共同表达式/条件：
```
SUBSTRING(case."createddate", 1, 19)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[008](../runs/natural/crmarenapro/query10/full-01/sql/008-52c1727e9424487e966229b11f44384b.sql)、[009](../runs/natural/crmarenapro/query10/full-01/sql/009-17c1c992295c4d209643176f9e518a11.sql)、[010](../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

<a id="c0071"></a>
## C0071 · crmarenapro/query10 · natural · 公共筛选

数据库：`support`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
case
```
共同表达式/条件：
```
CAST(SUBSTRING(case."createddate", 1, 19) AS TIMESTAMP) >= CAST('2023-05-02' AS TIMESTAMP)
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[009](../runs/natural/crmarenapro/query10/full-01/sql/009-17c1c992295c4d209643176f9e518a11.sql)、[010](../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

<a id="c0072"></a>
## C0072 · crmarenapro/query12 · natural · 公共筛选

数据库：`sales_pipeline`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
opportunity
```
共同表达式/条件：
```
opportunity."createddate" >= '2023-04-01'
opportunity."createddate" < '2023-05-01'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[002](../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql)、[005](../runs/natural/crmarenapro/query12/full-01/sql/005-181d1bc1c63e46a8a5396d55ac0a26e8.sql)、[007](../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql)

<a id="c0073"></a>
## C0073 · crmarenapro/query12 · natural · 公共内连接

数据库：`sales_pipeline`；任务验证：未通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```
共同表达式/条件：
```
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[002](../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql)、[003](../runs/natural/crmarenapro/query12/full-01/sql/003-63d12b98ec8843c685107011d07ebcd8.sql)、[004](../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql)

<a id="c0074"></a>
## C0074 · crmarenapro/query12 · natural · 公共筛选

数据库：`sales_pipeline`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
opportunity
```
共同表达式/条件：
```
opportunity."closedate" >= '2023-04-01'
opportunity."closedate" < '2023-05-01'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql)、[008](../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

<a id="c0075"></a>
## C0075 · crmarenapro/query12 · natural · 公共内连接

数据库：`sales_pipeline`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "opportunity" JOIN "contract" ON REPLACE(opportunity."contractid__c", '#', '') = REPLACE(contract."id", '#', '')
```
共同表达式/条件：
```
FROM "opportunity" JOIN "contract" ON REPLACE(opportunity."contractid__c", '#', '') = REPLACE(contract."id", '#', '')
```

准备方式：准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。

边界：只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

消费者：[007](../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql)、[008](../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

<a id="c0076"></a>
## C0076 · crmarenapro/query12 · natural · 派生计算

数据库：`sales_pipeline`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
opportunity
```
共同表达式/条件：
```
REPLACE(opportunity."ownerid", '#', '')
REPLACE(opportunity."contractid__c", '#', '')
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[007](../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql)、[008](../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

<a id="c0077"></a>
## C0077 · crmarenapro/query12 · natural · 派生计算

数据库：`sales_pipeline`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
contract
```
共同表达式/条件：
```
REPLACE(contract."id", '#', '')
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[007](../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql)、[008](../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

<a id="c0078"></a>
## C0078 · crmarenapro/query4 · natural · 公共筛选

数据库：`products_orders`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
orderitem
```
共同表达式/条件：
```
orderitem."product2id" = '01tWt000006hVJdIAM'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[001](../runs/natural/crmarenapro/query4/full-01/sql/001-eb3de57c639d46978deb379d8793a12e.sql)、[006](../runs/natural/crmarenapro/query4/full-01/sql/006-252cd6e35c954309b0354245df4293c5.sql)

<a id="c0079"></a>
## C0079 · crmarenapro/query4 · natural · 公共筛选

数据库：`support`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
case
```
共同表达式/条件：
```
case."orderitemid__c" IN ('#802Wt0000078yuGIAQ', '802Wt0000078yuGIAQ', '802Wt00000790mOIAQ', '802Wt00000790zGIAQ', '802Wt00000794F2IAI', '802Wt000007968eIAA', '802Wt00000796bfIAA', '802Wt00000796qFIAQ', '802Wt0000079734IAA', '802Wt00000797W5IAI', '802Wt00000797z7IAA', '802Wt00000798YdIAI', '802Wt00000798okIAA', '802Wt0000079B0EIAU')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql)、[008](../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)

<a id="c0080"></a>
## C0080 · crmarenapro/query4 · natural · 公共筛选

数据库：`support`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
case
```
共同表达式/条件：
```
case."createddate" >= '2020-06-10'
case."createddate" <= '2021-04-10'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql)、[005](../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql)

<a id="c0081"></a>
## C0081 · crmarenapro/query4 · natural · 派生计算

数据库：`support`；任务验证：通过；涉及 3 次调用，首次之后 2 次。

共同输入：
```sql
case
```
共同表达式/条件：
```
SUBSTRING(case."createddate", 1, 7)
```

准备方式：对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。

边界：需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

消费者：[004](../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql)、[005](../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql)、[008](../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)

<a id="c0082"></a>
## C0082 · crmarenapro/query8 · natural · 公共筛选

数据库：`support`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
casehistory__c
```
共同表达式/条件：
```
casehistory__c."field__c" = 'Owner Assignment'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[003](../runs/natural/crmarenapro/query8/full-01/sql/003-7712a5339f6445909a124d51013bf46c.sql)、[005](../runs/natural/crmarenapro/query8/full-01/sql/005-bb3f1da59e0a4cb089c4cc6c6df343a5.sql)

<a id="c0083"></a>
## C0083 · googlelocal/query1 · natural · 公共筛选

数据库：`business_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
business_description
```
共同表达式/条件：
```
business_description."description" ILIKE '%Los Angeles%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/googlelocal/query1/full-01/sql/004-bbb802d64adb44ec99cece581cd449c2.sql)、[005](../runs/natural/googlelocal/query1/full-01/sql/005-7f46b0bac3874f42a97d94b9e207431f.sql)

<a id="c0084"></a>
## C0084 · music_brainz_20k/query3 · natural · 同输入同分组聚合状态

数据库：`sales_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
FROM "sales"  GROUP BY sales."track_id"
```
共同表达式/条件：
```
SUM(sales."revenue_usd")
```

准备方式：在完全相同输入与分组上准备此聚合的完整结果/状态，保留全部分组后再施加各自 HAVING、排序和 LIMIT。

边界：基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

消费者：[001](../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql)、[003](../runs/natural/music_brainz_20k/query3/full-01/sql/003-b77bf2b2ae1b49949a8f9249756cb310.sql)

<a id="c0085"></a>
## C0085 · stockindex/query1 · natural · 公共筛选

数据库：`indextrade_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
index_trade
```
共同表达式/条件：
```
index_trade."index" IN ('N225', 'NSEI', 'HSI', '000001.SS', '399001.SZ', 'TWII')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[006](../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql)、[008](../runs/natural/stockindex/query1/full-01/sql/008-115bbcc37df243ab8f6c8f07d38807b8.sql)

<a id="c0086"></a>
## C0086 · yelp/query1 · natural · 公共筛选

数据库：`user_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
review
```
共同表达式/条件：
```
review."business_ref" IN ('businessref_52', 'businessref_84', 'businessref_76', 'businessref_87', 'businessref_65', 'businessref_94', 'businessref_90', 'businessref_16')
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[003](../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql)、[004](../runs/natural/yelp/query1/full-01/sql/004-f005e6191e5a4b87a6e15842069f443d.sql)

<a id="c0087"></a>
## C0087 · yelp/query3 · natural · 公共筛选

数据库：`user_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
review
```
共同表达式/条件：
```
review."date" LIKE '%2018%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[003](../runs/natural/yelp/query3/full-01/sql/003-99e14da782ee459f828e270dc269acce.sql)、[004](../runs/natural/yelp/query3/full-01/sql/004-d525231640b442f6936af5cfa84c9ed5.sql)

<a id="c0088"></a>
## C0088 · yelp/query7 · natural · 公共筛选

数据库：`user_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
user
```
共同表达式/条件：
```
user."yelping_since" LIKE '%2016%'
```

准备方式：保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。

边界：仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

消费者：[004](../runs/natural/yelp/query7/full-01/sql/004-5527eb8911ed4a18a539109f67bf45fb.sql)、[006](../runs/natural/yelp/query7/full-01/sql/006-eb152856605544129147da66dcb425f3.sql)

<a id="c0089"></a>
## C0089 · agnews/query3 · fad · Mongo 公共筛选

数据库：`articles_database`；任务验证：未通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
articles
```
共同表达式/条件：
```
{"$or": [{"title": {"$options": "i", "$regex": "business"}}, {"description": {"$options": "i", "$regex": "business"}}]}
```

准备方式：准备同一集合上相同原生筛选条件的完整文档子集，继续保留消费者各自的管道、投影和 LIMIT。

边界：只匹配非空 find/count/distinct filter 或管道首个 $match，不把任意全集合读取当成机会；未测缓存成本。

消费者：[003](../runs/fad/agnews/query3/full-01/mongo/003-2e825beeea9e4cda9f6348a56a46a73b.json)、[004](../runs/fad/agnews/query3/full-01/mongo/004-5e32d3c9fd0f4c5bbd59e5ff2e783019.json)

<a id="c0090"></a>
## C0090 · yelp/query4 · natural · Mongo 公共筛选

数据库：`businessinfo_database`；任务验证：通过；涉及 2 次调用，首次之后 1 次。

共同输入：
```sql
business
```
共同表达式/条件：
```
{"attributes.BusinessAcceptsCreditCards": "True"}
```

准备方式：准备同一集合上相同原生筛选条件的完整文档子集，继续保留消费者各自的管道、投影和 LIMIT。

边界：只匹配非空 find/count/distinct filter 或管道首个 $match，不把任意全集合读取当成机会；未测缓存成本。

消费者：[003](../runs/natural/yelp/query4/full-01/mongo/003-84d2aa41782448c9bf6f9e78db986b2b.json)、[005](../runs/natural/yelp/query4/full-01/mongo/005-604e6e7e916d4e7abcb7e2ce011c42d0.json)

