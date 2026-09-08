# 逐项证据

下列证据均在各自任务、组内部。候选和数值匹配尚非语义改写或因果验证。

## 分组演化

- GITHUB_REPOS/query2 / fad / same_keys / 同筛选=False：`['contents."id"']` → `['contents."id"']`；[前序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [后序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/009-0d967f8891534bf68322a2f452c9752b.sql)
- PANCANCER_ATLAS/query1 / fad / sibling / 同筛选=False：`['clinical_info."patient_description"']` → `['clinical_info."histological_type"']`；[前序](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/004-162c697713064bcf9a5438f98b5c576d.sql) → [后序](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/005-30cb7a44269948ed8834b3c3d95050e3.sql)
- PANCANCER_ATLAS/query3 / fad / sibling / 同筛选=False：`['clinical_info."patient_description"']` → `['clinical_info."histological_type"']`；[前序](../../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/004-875d56e6df074f569e6c5c9f87c48632.sql) → [后序](../../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/005-8c24ff8d7b314760ab8e0f5f4543731a.sql)
- crmarenapro/query10 / fad / sibling / 同筛选=False：`['casehistory__c."field__c"']` → `['casehistory__c."caseid__c"']`；[前序](../../runs/fad/crmarenapro/query10/full-01/sql/002-051467edb03c4db5af5d8d6870d59cf1.sql) → [后序](../../runs/fad/crmarenapro/query10/full-01/sql/004-cbfd1bba72ca483ca37db1cc48f0eba9.sql)
- crmarenapro/query12 / fad / same_keys / 同筛选=False：`['opportunity."ownerid"']` → `['opportunity."ownerid"']`；[前序](../../runs/fad/crmarenapro/query12/full-01/sql/001-fb319174901a4c9888ad85ebcbdaa965.sql) → [后序](../../runs/fad/crmarenapro/query12/full-01/sql/002-1a05cc1a94244f4896285e7ef7009389.sql)
- music_brainz_20k/query3 / fad / same_keys / 同筛选=True：`['sales."track_id"']` → `['sales."track_id"']`；[前序](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [后序](../../runs/fad/music_brainz_20k/query3/full-01/sql/005-dd8f3354db5d4de5adca29b3abf3edae.sql)
- stockindex/query1 / fad / sibling / 同筛选=False：`['index_trade."index"']` → `['index_trade."date"']`；[前序](../../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql) → [后序](../../runs/fad/stockindex/query1/full-01/sql/006-076a198afc1a46ce9ae82b5ba5d6329b.sql)
- stockindex/query2 / fad / same_keys / 同筛选=False：`['index_trade."index"']` → `['index_trade."index"']`；[前序](../../runs/fad/stockindex/query2/full-01/sql/005-3d65729c6fd641fda5f7cb025ecfcaad.sql) → [后序](../../runs/fad/stockindex/query2/full-01/sql/006-e2bb12301fef491ca659562d38daea17.sql)
- stockindex/query3 / fad / sibling / 同筛选=True：`['index_trade."index"']` → `['CASE WHEN REGEXP_FULL_MATCH(index_trade."date", \'^[0-9]{2} [A-Za-z]{3} [0-9]{4}\') THEN \'DD Mon YYYY\' WHEN REGEXP_FULL_MATCH(index_trade."date", \'^[A-Za-z]+ [0-9]{1,2}, [0-9]{4}\') THEN \'Month D, YYYY\' ELSE \'OTHER\' END']`；[前序](../../runs/fad/stockindex/query3/full-01/sql/005-7a9647a497cc4ed4bc5f453edd57c407.sql) → [后序](../../runs/fad/stockindex/query3/full-01/sql/006-e545d30c0a3a4181bc3dbfa495e3eeb0.sql)
- yelp/query1 / fad / same_keys / 同筛选=False：`['review."business_ref"']` → `['review."business_ref"']`；[前序](../../runs/fad/yelp/query1/full-01/sql/002-7ba4c269f043448c89cdb19471d8066e.sql) → [后序](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql)
- GITHUB_REPOS/query2 / natural / same_keys / 同筛选=False：`['files."id"']` → `['files."id"']`；[前序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql) → [后序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/016-29d8fde5f6b2417ab64a22f5a1353250.sql)
- PANCANCER_ATLAS/query1 / natural / sibling / 同筛选=True：`['clinical_info."patient_description"']` → `['clinical_info."diagnosis"']`；[前序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/003-546fb960098c4868af02b4afe3e0aff6.sql) → [后序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/004-eee66c952d9c4dcdae57499f18016504.sql)
- PANCANCER_ATLAS/query1 / natural / sibling / 同筛选=False：`['clinical_info."patient_description"']` → `['clinical_info."histological_type"']`；[前序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/003-546fb960098c4868af02b4afe3e0aff6.sql) → [后序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/005-0911b7f14f5e4e76ba6b8ccfde2c8992.sql)
- PANCANCER_ATLAS/query1 / natural / sibling / 同筛选=False：`['clinical_info."diagnosis"']` → `['clinical_info."histological_type"']`；[前序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/004-eee66c952d9c4dcdae57499f18016504.sql) → [后序](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/005-0911b7f14f5e4e76ba6b8ccfde2c8992.sql)
- PANCANCER_ATLAS/query3 / natural / sibling / 同筛选=True：`['clinical_info."histological_type"']` → `['CASE WHEN clinical_info."patient_description" LIKE \'%FEMALE%\' THEN \'FEMALE\' WHEN clinical_info."patient_description" LIKE \'%MALE%\' THEN \'MALE\' ELSE \'UNKNOWN\' END']`；[前序](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/005-6ab3b6aaca974643858a815b39c2cf32.sql) → [后序](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/006-7a6409ae1a4e49d6a25fbada077c5230.sql)
- PATENTS/query2 / natural / sibling / 同筛选=False：`['SUBSTRING(publicationinfo."patents_info", STR_POSITION(publicationinfo."patents_info", \'publication number\'), 40)']` → `['publicationinfo."grant_date"']`；[前序](../../runs/natural/PATENTS/query2/full-01/sql/004-aad920458c024dea9bb76817b75c41ce.sql) → [后序](../../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql)
- PATENTS/query2 / natural / sibling / 同筛选=False：`['SUBSTRING(publicationinfo."patents_info", STR_POSITION(publicationinfo."patents_info", \'publication number\'), 40)']` → `['publicationinfo."grant_date"']`；[前序](../../runs/natural/PATENTS/query2/full-01/sql/004-aad920458c024dea9bb76817b75c41ce.sql) → [后序](../../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)
- PATENTS/query2 / natural / same_keys / 同筛选=False：`['publicationinfo."grant_date"']` → `['publicationinfo."grant_date"']`；[前序](../../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql) → [后序](../../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)
- crmarenapro/query10 / natural / sibling / 同筛选=False：`['casehistory__c."field__c"']` → `['casehistory__c."caseid__c"']`；[前序](../../runs/natural/crmarenapro/query10/full-01/sql/004-d6e09356035a409fa8bf84d0a8f2bca6.sql) → [后序](../../runs/natural/crmarenapro/query10/full-01/sql/008-52c1727e9424487e966229b11f44384b.sql)
- crmarenapro/query12 / natural / same_keys / 同筛选=False：`['opportunity."ownerid"']` → `['opportunity."ownerid"']`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/003-63d12b98ec8843c685107011d07ebcd8.sql)
- crmarenapro/query12 / natural / same_keys / 同筛选=False：`['opportunity."ownerid"']` → `['opportunity."ownerid"']`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql)
- crmarenapro/query12 / natural / same_keys / 同筛选=False：`['opportunity."ownerid"']` → `['opportunity."ownerid"']`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/003-63d12b98ec8843c685107011d07ebcd8.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql)
- crmarenapro/query12 / natural / same_keys / 同筛选=False：`['REPLACE(opportunity."ownerid", \'#\', \'\')']` → `['REPLACE(opportunity."ownerid", \'#\', \'\')']`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)
- crmarenapro/query4 / natural / same_keys / 同筛选=False：`['SUBSTRING(case."createddate", 1, 7)']` → `['SUBSTRING(case."createddate", 1, 7)']`；[前序](../../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql) → [后序](../../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql)
- crmarenapro/query4 / natural / same_keys / 同筛选=False：`['SUBSTRING(case."createddate", 1, 7)']` → `['SUBSTRING(case."createddate", 1, 7)']`；[前序](../../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql) → [后序](../../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)
- crmarenapro/query4 / natural / same_keys / 同筛选=False：`['SUBSTRING(case."createddate", 1, 7)']` → `['SUBSTRING(case."createddate", 1, 7)']`；[前序](../../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql) → [后序](../../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)
- music_brainz_20k/query3 / natural / same_keys / 同筛选=True：`['sales."track_id"']` → `['sales."track_id"']`；[前序](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [后序](../../runs/natural/music_brainz_20k/query3/full-01/sql/003-b77bf2b2ae1b49949a8f9249756cb310.sql)
- stockindex/query1 / natural / same_keys / 同筛选=False：`['index_trade."index"']` → `['index_trade."index"']`；[前序](../../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/007-3ee02b5bd5234a138217eba651f8a024.sql)
- yelp/query1 / natural / same_keys / 同筛选=False：`['review."business_ref"']` → `['review."business_ref"']`；[前序](../../runs/natural/yelp/query1/full-01/sql/001-82342ca44777410a98e72fec59902999.sql) → [后序](../../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql)

## 结果值匹配（每个查询对最多展示 3 个值，JSON 保留全部）

- DEPS_DEV_V1/query2 / fad：结果列 `System` 第 0 行值 `NPM` 匹配后序 `System`；[前序](../../runs/fad/DEPS_DEV_V1/query2/full-01/sql/004-941d2aae9cdc4f5a930d6c68288fa863.sql) → [后序](../../runs/fad/DEPS_DEV_V1/query2/full-01/sql/005-1e52603435ca46f8acd7a4f02e61b4c7.sql)。新谓词值=False，prompt含值=True。
- GITHUB_REPOS/query1 / fad：结果列 `sample_repo_name` 第 53 行值 `3ventic/DiscordServers` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/007-b2446bcc6ce844e5be42bc6775373eed.sql) → [后序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/008-cd03e21956cd4457af46c89ce18fe156.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query1 / fad：结果列 `sample_repo_name` 第 100 行值 `AcyOrt/acyort` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/007-b2446bcc6ce844e5be42bc6775373eed.sql) → [后序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/008-cd03e21956cd4457af46c89ce18fe156.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query1 / fad：结果列 `sample_repo_name` 第 130 行值 `Ali-Razmjoo/OWASP-ZSC` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/007-b2446bcc6ce844e5be42bc6775373eed.sql) → [后序](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/008-cd03e21956cd4457af46c89ce18fe156.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query2 / fad：结果列 `sample_repo_name` 第 0 行值 `uacaps/PageMenu` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [后序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/007-1d65b42b24cd4c3aa38eeeb7fb00b28e.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query2 / fad：结果列 `sample_repo_name` 第 1 行值 `kostiakoval/Mirror` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [后序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/007-1d65b42b24cd4c3aa38eeeb7fb00b28e.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query2 / fad：结果列 `sample_repo_name` 第 2 行值 `apple/swift` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [后序](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/007-1d65b42b24cd4c3aa38eeeb7fb00b28e.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query4 / fad：结果列 `repo_name` 第 0 行值 `torvalds/linux` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/004-d82421f2e18643f381d3cdedefb9e26d.sql) → [后序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/005-6b72dc5076ce4ccd81c8ece53cd1a99e.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query4 / fad：结果列 `repo_name` 第 1 行值 `apple/swift` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/004-d82421f2e18643f381d3cdedefb9e26d.sql) → [后序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/005-6b72dc5076ce4ccd81c8ece53cd1a99e.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query4 / fad：结果列 `repo_name` 第 2 行值 `twbs/bootstrap` 匹配后序 `repo_name`；[前序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/004-d82421f2e18643f381d3cdedefb9e26d.sql) → [后序](../../runs/fad/GITHUB_REPOS/query4/full-01/sql/005-6b72dc5076ce4ccd81c8ece53cd1a99e.sql)。新谓词值=True，prompt含值=False。
- PANCANCER_ATLAS/query2 / fad：结果列 `days_to_death` 第 0 行值 `[Not Applicable]` 匹配后序 `days_to_death`；[前序](../../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/004-e736389193e94d9ba6f59191eab82bde.sql) → [后序](../../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/005-3cf67fa1971944dc810ac193152b3daa.sql)。新谓词值=True，prompt含值=False。
- PATENTS/query1 / fad：结果列 `n` 第 42 行值 `5` 匹配后序 `level`；[前序](../../runs/fad/PATENTS/query1/full-01/sql/011-a35028c05c3d48d990e8729ea7decdb3.sql) → [后序](../../runs/fad/PATENTS/query1/full-01/sql/012-f07147bb9bc7448cbfba90888ef75193.sql)。新谓词值=False，prompt含值=True。
- agnews/query2 / fad：结果列 `author_id` 第 0 行值 `218` 匹配后序 `author_id`；[前序](../../runs/fad/agnews/query2/full-01/sql/003-fc15464eda3949649d0d46f4187aa5ad.sql) → [后序](../../runs/fad/agnews/query2/full-01/sql/004-38cd4fc28cc34d239cf6fb5cbc0a4094.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query1 / fad：结果列 `Id` 第 0 行值 `00QWt0000089AekMAE` 匹配后序 `LeadId__c`；[前序](../../runs/fad/crmarenapro/query1/full-01/sql/001-d4dabf62c5fa421a9c4f432d0295dca8.sql) → [后序](../../runs/fad/crmarenapro/query1/full-01/sql/002-81def6184f644ec1b15c0a4a7b504f6d.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query11 / fad：结果列 `AccountId` 第 0 行值 `#001Wt00000PGXrNIAX` 匹配后序 `o.AccountId`；[前序](../../runs/fad/crmarenapro/query11/full-01/sql/001-b0736c0ecef24efcbc595d1d063f7e51.sql) → [后序](../../runs/fad/crmarenapro/query11/full-01/sql/002-19d0a6d433474cc78b730eced521f35a.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query11 / fad：结果列 `Id` 第 0 行值 `801Wt00000PHRYWIA5` 匹配后序 `oi.OrderId`；[前序](../../runs/fad/crmarenapro/query11/full-01/sql/004-681d9e847835493fbefc7a9a78937752.sql) → [后序](../../runs/fad/crmarenapro/query11/full-01/sql/005-14f9d4c5e1fb4fc9b2485fe4ea2c9b04.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query12 / fad：结果列 `OwnerId` 第 0 行值 `005Wt000003NDEBIA4` 匹配后序 `Id`；[前序](../../runs/fad/crmarenapro/query12/full-01/sql/002-1a05cc1a94244f4896285e7ef7009389.sql) → [后序](../../runs/fad/crmarenapro/query12/full-01/sql/003-273d1e88190f4cca824b14b02843e775.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query13 / fad：结果列 `OwnerId` 第 94 行值 `005Wt000003NHw5IAG` 匹配后序 `Id`；[前序](../../runs/fad/crmarenapro/query13/full-01/sql/004-40119010292543b486fbc63bea393d6c.sql) → [后序](../../runs/fad/crmarenapro/query13/full-01/sql/005-b052774f62ce4362a7ae5a25575df9b7.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query3 / fad：结果列 `Id` 第 0 行值 `006Wt000007BGGjIAO` 匹配后序 `WhatId`；[前序](../../runs/fad/crmarenapro/query3/full-01/sql/001-4f2136e842a34b68abeb0191e06358ed.sql) → [后序](../../runs/fad/crmarenapro/query3/full-01/sql/002-bb33b6267c1d4f358166ef64761a44af.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query3 / fad：结果列 `WhatId` 第 0 行值 `006Wt000007BGGjIAO` 匹配后序 `OpportunityId`；[前序](../../runs/fad/crmarenapro/query3/full-01/sql/002-bb33b6267c1d4f358166ef64761a44af.sql) → [后序](../../runs/fad/crmarenapro/query3/full-01/sql/003-b97cb780607d4bb6b43407321dba665e.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query4 / fad：结果列 `Id` 第 0 行值 `#802Wt0000078yuGIAQ` 匹配后序 `orderitemid__c`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/001-7e3a1c2101354d1bb83be10790493c96.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/002-7f8d6a994bf54feba5d418da0b693cb8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query4 / fad：结果列 `Id` 第 1 行值 `802Wt00000790mOIAQ` 匹配后序 `orderitemid__c`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/001-7e3a1c2101354d1bb83be10790493c96.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/002-7f8d6a994bf54feba5d418da0b693cb8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query4 / fad：结果列 `Id` 第 2 行值 `802Wt00000790zGIAQ` 匹配后序 `orderitemid__c`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/001-7e3a1c2101354d1bb83be10790493c96.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/002-7f8d6a994bf54feba5d418da0b693cb8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query4 / fad：结果列 `AccountId` 第 0 行值 `#001Wt00000PGHsyIAH` 匹配后序 `accountid`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/004-615e605901a64c83923eb439aa45721b.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/005-563996ce436b4cfbbb64ad6b1ea71c3d.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query4 / fad：结果列 `AccountId` 第 1 行值 `001Wt00000PGSwYIAX` 匹配后序 `accountid`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/004-615e605901a64c83923eb439aa45721b.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/005-563996ce436b4cfbbb64ad6b1ea71c3d.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query4 / fad：结果列 `AccountId` 第 2 行值 `001Wt00000PHVkAIAX` 匹配后序 `accountid`；[前序](../../runs/fad/crmarenapro/query4/full-01/sql/004-615e605901a64c83923eb439aa45721b.sql) → [后序](../../runs/fad/crmarenapro/query4/full-01/sql/005-563996ce436b4cfbbb64ad6b1ea71c3d.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `Id` 第 0 行值 `#0Q0Wt000001WRAzKAO` 匹配后序 `QuoteId`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/003-25d78ec337214f06ad19949fb4510cd4.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/004-94b451cb0f984d5a88d5e5b9b024cb78.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `Product2Id` 第 0 行值 `#01tWt000006hV6jIAE` 匹配后序 `p.Id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/005-ccc81f2c763245218ffeb079297d4da1.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/006-c3193b1842b34b77981f711b83521d49.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `Product2Id` 第 1 行值 `01tWt000006hV8LIAU` 匹配后序 `p.Id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/005-ccc81f2c763245218ffeb079297d4da1.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/006-c3193b1842b34b77981f711b83521d49.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `Product2Id` 第 2 行值 `#01tWt000006hPffIAE` 匹配后序 `p.Id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/005-ccc81f2c763245218ffeb079297d4da1.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/006-c3193b1842b34b77981f711b83521d49.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `id` 第 6 行值 `ka0Wt000000Eq0MIAS` 匹配后序 `id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/008-257756a8d28b4504a2d45d24456d1561.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/009-852aa5f17fc944bcbee4adfbe8215b95.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `id` 第 188 行值 `#ka0Wt000000EnwvIAC` 匹配后序 `id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/008-257756a8d28b4504a2d45d24456d1561.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/009-852aa5f17fc944bcbee4adfbe8215b95.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / fad：结果列 `id` 第 191 行值 `ka0Wt000000Ens5IAC` 匹配后序 `id`；[前序](../../runs/fad/crmarenapro/query6/full-01/sql/008-257756a8d28b4504a2d45d24456d1561.sql) → [后序](../../runs/fad/crmarenapro/query6/full-01/sql/009-852aa5f17fc944bcbee4adfbe8215b95.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query7 / fad：结果列 `id` 第 0 行值 `#500Wt00000DDyznIAD` 匹配后序 `id`；[前序](../../runs/fad/crmarenapro/query7/full-01/sql/007-3928fa79e94f426b98a8907171ad67d0.sql) → [后序](../../runs/fad/crmarenapro/query7/full-01/sql/008-d6ffb3733bd241f29a57a1482b69b202.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query7 / fad：结果列 `id` 第 0 行值 `#500Wt00000DDyznIAD` 匹配后序 `caseid`；[前序](../../runs/fad/crmarenapro/query7/full-01/sql/008-d6ffb3733bd241f29a57a1482b69b202.sql) → [后序](../../runs/fad/crmarenapro/query7/full-01/sql/009-5aad60b4d4334f209fc6b74ade9c7ca1.sql)。新谓词值=False，prompt含值=False。
- crmarenapro/query7 / fad：结果列 `id` 第 0 行值 `#500Wt00000DDyznIAD` 匹配后序 `caseid__c`；[前序](../../runs/fad/crmarenapro/query7/full-01/sql/008-d6ffb3733bd241f29a57a1482b69b202.sql) → [后序](../../runs/fad/crmarenapro/query7/full-01/sql/009-5aad60b4d4334f209fc6b74ade9c7ca1.sql)。新谓词值=False，prompt含值=False。
- crmarenapro/query7 / fad：结果列 `id` 第 0 行值 `#500Wt00000DDyznIAD` 匹配后序 `parentid`；[前序](../../runs/fad/crmarenapro/query7/full-01/sql/008-d6ffb3733bd241f29a57a1482b69b202.sql) → [后序](../../runs/fad/crmarenapro/query7/full-01/sql/009-5aad60b4d4334f209fc6b74ade9c7ca1.sql)。新谓词值=False，prompt含值=False。
- crmarenapro/query8 / fad：结果列 `field__c` 第 2 行值 `Owner Assignment` 匹配后序 `field__c`；[前序](../../runs/fad/crmarenapro/query8/full-01/sql/001-e9ef5b54932e4998aaa3634ab42ab61b.sql) → [后序](../../runs/fad/crmarenapro/query8/full-01/sql/002-bb0f03a3a13d4b248923f8833d866155.sql)。新谓词值=True，prompt含值=True。
- googlelocal/query1 / fad：结果列 `gmap_id` 第 0 行值 `gmap_44` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query1/full-01/sql/005-97d8540b54ed45d083f0098169bfda40.sql) → [后序](../../runs/fad/googlelocal/query1/full-01/sql/006-58ababad37c14e6c888f8bfdba41c17b.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query1 / fad：结果列 `gmap_id` 第 1 行值 `gmap_41` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query1/full-01/sql/005-97d8540b54ed45d083f0098169bfda40.sql) → [后序](../../runs/fad/googlelocal/query1/full-01/sql/006-58ababad37c14e6c888f8bfdba41c17b.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query1 / fad：结果列 `gmap_id` 第 2 行值 `gmap_43` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query1/full-01/sql/005-97d8540b54ed45d083f0098169bfda40.sql) → [后序](../../runs/fad/googlelocal/query1/full-01/sql/006-58ababad37c14e6c888f8bfdba41c17b.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / fad：结果列 `gmap_id` 第 0 行值 `gmap_72` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query4/full-01/sql/002-a2e294bd47e14c2080b9de667242e617.sql) → [后序](../../runs/fad/googlelocal/query4/full-01/sql/003-9a7c2d2bac6b4930841472fb96a0715b.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / fad：结果列 `gmap_id` 第 1 行值 `gmap_35` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query4/full-01/sql/002-a2e294bd47e14c2080b9de667242e617.sql) → [后序](../../runs/fad/googlelocal/query4/full-01/sql/003-9a7c2d2bac6b4930841472fb96a0715b.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / fad：结果列 `gmap_id` 第 2 行值 `gmap_20` 匹配后序 `gmap_id`；[前序](../../runs/fad/googlelocal/query4/full-01/sql/002-a2e294bd47e14c2080b9de667242e617.sql) → [后序](../../runs/fad/googlelocal/query4/full-01/sql/003-9a7c2d2bac6b4930841472fb96a0715b.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / fad：结果列 `track_id` 第 0 行值 `4233` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query1/full-01/sql/003-857af3b59ccc447ea4807fc4a04d4f96.sql) → [后序](../../runs/fad/music_brainz_20k/query1/full-01/sql/004-a7181c7f33c14c308e4c7e0e549d52b6.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / fad：结果列 `track_id` 第 1 行值 `12954` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query1/full-01/sql/003-857af3b59ccc447ea4807fc4a04d4f96.sql) → [后序](../../runs/fad/music_brainz_20k/query1/full-01/sql/004-a7181c7f33c14c308e4c7e0e549d52b6.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / fad：结果列 `track_id` 第 2 行值 `15158` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query1/full-01/sql/003-857af3b59ccc447ea4807fc4a04d4f96.sql) → [后序](../../runs/fad/music_brainz_20k/query1/full-01/sql/004-a7181c7f33c14c308e4c7e0e549d52b6.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query2 / fad：结果列 `track_id` 第 0 行值 `4122` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query2/full-01/sql/001-40f4c6136b964919b5dbb09dddcef3cd.sql) → [后序](../../runs/fad/music_brainz_20k/query2/full-01/sql/002-54f352036e584985978908025a678d49.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / fad：结果列 `track_id` 第 0 行值 `14719` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [后序](../../runs/fad/music_brainz_20k/query3/full-01/sql/004-080ed3f1a74246b982767cfdc14ce40f.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / fad：结果列 `track_id` 第 1 行值 `5124` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [后序](../../runs/fad/music_brainz_20k/query3/full-01/sql/004-080ed3f1a74246b982767cfdc14ce40f.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / fad：结果列 `track_id` 第 2 行值 `1344` 匹配后序 `track_id`；[前序](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [后序](../../runs/fad/music_brainz_20k/query3/full-01/sql/004-080ed3f1a74246b982767cfdc14ce40f.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / fad：结果列 `Index` 第 4 行值 `HSI` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query1/full-01/sql/004-108a0efb9a92455c8b2e78ab3bdeab6a.sql) → [后序](../../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / fad：结果列 `Index` 第 0 行值 `000001.SS` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query1/full-01/sql/004-108a0efb9a92455c8b2e78ab3bdeab6a.sql) → [后序](../../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / fad：结果列 `Index` 第 1 行值 `399001.SZ` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query1/full-01/sql/004-108a0efb9a92455c8b2e78ab3bdeab6a.sql) → [后序](../../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql)。新谓词值=True，prompt含值=False。
- stockindex/query2 / fad：结果列 `Index` 第 10 行值 `NYA` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query2/full-01/sql/006-e2bb12301fef491ca659562d38daea17.sql) → [后序](../../runs/fad/stockindex/query2/full-01/sql/007-38a885e2fb0d4b68aabe57c6cd05d801.sql)。新谓词值=True，prompt含值=False。
- stockindex/query2 / fad：结果列 `Index` 第 5 行值 `IXIC` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query2/full-01/sql/006-e2bb12301fef491ca659562d38daea17.sql) → [后序](../../runs/fad/stockindex/query2/full-01/sql/007-38a885e2fb0d4b68aabe57c6cd05d801.sql)。新谓词值=True，prompt含值=False。
- stockindex/query2 / fad：结果列 `Index` 第 3 行值 `GSPTSE` 匹配后序 `"Index"`；[前序](../../runs/fad/stockindex/query2/full-01/sql/006-e2bb12301fef491ca659562d38daea17.sql) → [后序](../../runs/fad/stockindex/query2/full-01/sql/007-38a885e2fb0d4b68aabe57c6cd05d801.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query2 / fad：结果列 `Listing Exchange` 第 2 行值 `P` 匹配后序 `"Listing Exchange"`；[前序](../../runs/fad/stockmarket/query2/full-01/sql/003-984d674d50274727a67ed783e76372bc.sql) → [后序](../../runs/fad/stockmarket/query2/full-01/sql/004-f4d81bf2f6c243c1af0def39562c9f6f.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query3 / fad：结果列 `val` 第 7 行值 `Q` 匹配后序 `"Listing Exchange"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/003-ea1a5a29b3b24fd38063bd0d161ad8be.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/004-f23c3a8ee6cc449094f60868c6e8ad71.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query3 / fad：结果列 `val` 第 1 行值 `D` 匹配后序 `"Financial Status"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/003-ea1a5a29b3b24fd38063bd0d161ad8be.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/004-f23c3a8ee6cc449094f60868c6e8ad71.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query3 / fad：结果列 `val` 第 2 行值 `H` 匹配后序 `"Financial Status"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/003-ea1a5a29b3b24fd38063bd0d161ad8be.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/004-f23c3a8ee6cc449094f60868c6e8ad71.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query3 / fad：结果列 `symbol` 第 2 行值 `APEX` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/006-d87cf9224e09478d8cf4a38dbb1c6c31.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/007-b3f2dd5ebb8740a2bf22e68b7c2ac2d9.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query3 / fad：结果列 `symbol` 第 4 行值 `BKYI` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/006-d87cf9224e09478d8cf4a38dbb1c6c31.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/007-b3f2dd5ebb8740a2bf22e68b7c2ac2d9.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query3 / fad：结果列 `symbol` 第 5 行值 `CBAT` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query3/full-01/sql/006-d87cf9224e09478d8cf4a38dbb1c6c31.sql) → [后序](../../runs/fad/stockmarket/query3/full-01/sql/007-b3f2dd5ebb8740a2bf22e68b7c2ac2d9.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query4 / fad：结果列 `Listing Exchange` 第 4 行值 `N` 匹配后序 `"Listing Exchange"`；[前序](../../runs/fad/stockmarket/query4/full-01/sql/003-e12f4c1335874cc8b11e6da9a46b5564.sql) → [后序](../../runs/fad/stockmarket/query4/full-01/sql/004-6e9e4ba4a4aa4132824e267e2d1a0f75.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query4 / fad：结果列 `Listing Exchange` 第 4 行值 `N` 匹配后序 `"ETF"`；[前序](../../runs/fad/stockmarket/query4/full-01/sql/003-e12f4c1335874cc8b11e6da9a46b5564.sql) → [后序](../../runs/fad/stockmarket/query4/full-01/sql/004-6e9e4ba4a4aa4132824e267e2d1a0f75.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query5 / fad：结果列 `Market Category` 第 5 行值 `S` 匹配后序 `"Market Category"`；[前序](../../runs/fad/stockmarket/query5/full-01/sql/003-8304708d2637432495145354c8b494dd.sql) → [后序](../../runs/fad/stockmarket/query5/full-01/sql/004-877057d055ae48c3850feb36f95b3a02.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query5 / fad：结果列 `Listing Exchange` 第 1 行值 `Q` 匹配后序 `"Listing Exchange"`；[前序](../../runs/fad/stockmarket/query5/full-01/sql/003-8304708d2637432495145354c8b494dd.sql) → [后序](../../runs/fad/stockmarket/query5/full-01/sql/004-877057d055ae48c3850feb36f95b3a02.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query5 / fad：结果列 `symbol` 第 0 行值 `SES` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query5/full-01/sql/005-eb169fce95b349f08fc930a5fbaa48f4.sql) → [后序](../../runs/fad/stockmarket/query5/full-01/sql/006-66fc145f826c4ea3b8a87b1a7016380f.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query5 / fad：结果列 `symbol` 第 1 行值 `GLG` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query5/full-01/sql/005-eb169fce95b349f08fc930a5fbaa48f4.sql) → [后序](../../runs/fad/stockmarket/query5/full-01/sql/006-66fc145f826c4ea3b8a87b1a7016380f.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query5 / fad：结果列 `symbol` 第 2 行值 `TMSR` 匹配后序 `"Symbol"`；[前序](../../runs/fad/stockmarket/query5/full-01/sql/005-eb169fce95b349f08fc930a5fbaa48f4.sql) → [后序](../../runs/fad/stockmarket/query5/full-01/sql/006-66fc145f826c4ea3b8a87b1a7016380f.sql)。新谓词值=True，prompt含值=False。
- yelp/query1 / fad：结果列 `business_ref` 第 4 行值 `businessref_16` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query1/full-01/sql/003-e32a6dff90db409c9f4891a88f7a24f2.sql) → [后序](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql)。新谓词值=True，prompt含值=False。
- yelp/query1 / fad：结果列 `business_ref` 第 1 行值 `businessref_52` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql) → [后序](../../runs/fad/yelp/query1/full-01/sql/005-ceeb4c2d6d104325b327b8be83d7b988.sql)。新谓词值=False，prompt含值=False。
- yelp/query1 / fad：结果列 `business_ref` 第 4 行值 `businessref_84` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql) → [后序](../../runs/fad/yelp/query1/full-01/sql/005-ceeb4c2d6d104325b327b8be83d7b988.sql)。新谓词值=False，prompt含值=False。
- yelp/query1 / fad：结果列 `business_ref` 第 3 行值 `businessref_76` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql) → [后序](../../runs/fad/yelp/query1/full-01/sql/005-ceeb4c2d6d104325b327b8be83d7b988.sql)。新谓词值=False，prompt含值=False。
- yelp/query5 / fad：结果列 `business_ref` 第 1 行值 `businessref_67` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query5/full-01/sql/002-30646c582fb04b2bbec6d0b2e408e2ad.sql) → [后序](../../runs/fad/yelp/query5/full-01/sql/003-e70cbfcd80cb437388ebe0cbc20dac52.sql)。新谓词值=True，prompt含值=False。
- yelp/query5 / fad：结果列 `business_ref` 第 16 行值 `businessref_77` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query5/full-01/sql/002-30646c582fb04b2bbec6d0b2e408e2ad.sql) → [后序](../../runs/fad/yelp/query5/full-01/sql/003-e70cbfcd80cb437388ebe0cbc20dac52.sql)。新谓词值=True，prompt含值=False。
- yelp/query5 / fad：结果列 `business_ref` 第 0 行值 `businessref_86` 匹配后序 `business_ref`；[前序](../../runs/fad/yelp/query5/full-01/sql/002-30646c582fb04b2bbec6d0b2e408e2ad.sql) → [后序](../../runs/fad/yelp/query5/full-01/sql/003-e70cbfcd80cb437388ebe0cbc20dac52.sql)。新谓词值=True，prompt含值=False。
- DEPS_DEV_V1/query1 / natural：结果列 `RelationType` 第 1 行值 `SOURCE_REPO_TYPE` 匹配后序 `ppv.RelationType`；[前序](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/012-0b726662f08d4931a79cbdacd2869ab8.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/013-8f39780a9c91476f8049aec18951828b.sql)。新谓词值=True，prompt含值=False。
- DEPS_DEV_V1/query2 / natural：结果列 `System` 第 0 行值 `NPM` 匹配后序 `System`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/004-0f1bbbf3a84741db8d562083652f6e8a.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/005-3b2c0e630df84ff7a8e9dcde693eaa05.sql)。新谓词值=True，prompt含值=True。
- DEPS_DEV_V1/query2 / natural：结果列 `System` 第 0 行值 `NPM` 匹配后序 `System`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/005-3b2c0e630df84ff7a8e9dcde693eaa05.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/006-a8d60bd81720489fbf580187eb35451b.sql)。新谓词值=False，prompt含值=True。
- DEPS_DEV_V1/query2 / natural：结果列 `Name` 第 9094 行值 `@discourse/virtual-dom` 匹配后序 `Name`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)。新谓词值=True，prompt含值=False。
- DEPS_DEV_V1/query2 / natural：结果列 `Name` 第 3037 行值 `@discovery-dao/ui` 匹配后序 `Name`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)。新谓词值=True，prompt含值=False。
- DEPS_DEV_V1/query2 / natural：结果列 `Name` 第 3346 行值 `@discovery-dni/shaka-player` 匹配后序 `Name`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)。新谓词值=True，prompt含值=False。
- DEPS_DEV_V1/query2 / natural：结果列 `ProjectName` 第 2 行值 `wizards-lab/routing` 匹配后序 `ProjectName`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/014-23b2be50dd774a86ac7f2825ea4791d2.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql)。新谓词值=False，prompt含值=False。
- DEPS_DEV_V1/query2 / natural：结果列 `ProjectName` 第 11386 行值 `semantic-org/semantic-ui` 匹配后序 `ProjectName`；[前序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql) → [后序](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/016-cbeb44409c774ad6b65321a77347aba3.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query1 / natural：结果列 `sample_repo_name` 第 53 行值 `3ventic/DiscordServers` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/008-665c02b536b54d818800744da2ca9027.sql) → [后序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/009-b3b6fe03509a47feb7a832ec13779f44.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query1 / natural：结果列 `sample_repo_name` 第 100 行值 `AcyOrt/acyort` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/008-665c02b536b54d818800744da2ca9027.sql) → [后序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/009-b3b6fe03509a47feb7a832ec13779f44.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query1 / natural：结果列 `sample_repo_name` 第 130 行值 `Ali-Razmjoo/OWASP-ZSC` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/008-665c02b536b54d818800744da2ca9027.sql) → [后序](../../runs/natural/GITHUB_REPOS/query1/full-01/sql/009-b3b6fe03509a47feb7a832ec13779f44.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query2 / natural：结果列 `id` 第 0 行值 `6f4cdb70f044b0486a24a07403600cb964a02672` 匹配后序 `id`；[前序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/007-28663d17f2dc4fe5a85eaca518fdc05d.sql) → [后序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/008-018182ee667245c1ac8baf2d957e7b76.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query2 / natural：结果列 `id` 第 0 行值 `71a17ce92451858f3eb01aa8082551e48bc5550d` 匹配后序 `id`；[前序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/016-29d8fde5f6b2417ab64a22f5a1353250.sql) → [后序](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/017-7eccd824219d477088d092bf21cf7991.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 0 行值 `twbs/bootstrap` 匹配后序 `la.repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/012-f66eee8c72974b6c8810a8f8e732a8db.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/013-f689c3534bc049278f37234a54d7210d.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 1 行值 `facebook/react` 匹配后序 `la.repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/012-f66eee8c72974b6c8810a8f8e732a8db.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/013-f689c3534bc049278f37234a54d7210d.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 2 行值 `Microsoft/vscode` 匹配后序 `la.repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/012-f66eee8c72974b6c8810a8f8e732a8db.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/013-f689c3534bc049278f37234a54d7210d.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 0 行值 `tensorflow/tensorflow` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/013-f689c3534bc049278f37234a54d7210d.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 2 行值 `apple/swift` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/013-f689c3534bc049278f37234a54d7210d.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 0 行值 `tensorflow/tensorflow` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/015-8c2c935d46744e8291f00620c81ebc25.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query3 / natural：结果列 `repo_name` 第 1 行值 `apple/swift` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql) → [后序](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/015-8c2c935d46744e8291f00620c81ebc25.sql)。新谓词值=False，prompt含值=False。
- GITHUB_REPOS/query4 / natural：结果列 `repo_name` 第 0 行值 `torvalds/linux` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/004-702f66af53b046c58417f38e2f6763a9.sql) → [后序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/005-f2479e8985c04c31b3543cc7659c8e30.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query4 / natural：结果列 `repo_name` 第 1 行值 `apple/swift` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/004-702f66af53b046c58417f38e2f6763a9.sql) → [后序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/005-f2479e8985c04c31b3543cc7659c8e30.sql)。新谓词值=True，prompt含值=False。
- GITHUB_REPOS/query4 / natural：结果列 `repo_name` 第 2 行值 `twbs/bootstrap` 匹配后序 `repo_name`；[前序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/004-702f66af53b046c58417f38e2f6763a9.sql) → [后序](../../runs/natural/GITHUB_REPOS/query4/full-01/sql/005-f2479e8985c04c31b3543cc7659c8e30.sql)。新谓词值=True，prompt含值=False。
- PATENTS/query1 / natural：结果列 `cnt` 第 0 行值 `5` 匹配后序 `level`；[前序](../../runs/natural/PATENTS/query1/full-01/sql/013-960b572783834a45a1ffda3046245e1e.sql) → [后序](../../runs/natural/PATENTS/query1/full-01/sql/014-7de1a1ef05664a21aeb1cc0a80a1423a.sql)。新谓词值=False，prompt含值=True。
- bookreview/query1 / natural：结果列 `book_id` 第 195 行值 `bookid_196` 匹配后序 `book_id`；[前序](../../runs/natural/bookreview/query1/full-01/sql/005-f00079fe297e4114a2943386d14643e7.sql) → [后序](../../runs/natural/bookreview/query1/full-01/sql/006-e6101bcc278a4d5f9c8bb99151f380cb.sql)。新谓词值=True，prompt含值=False。
- bookreview/query1 / natural：结果列 `book_id` 第 178 行值 `bookid_178` 匹配后序 `book_id`；[前序](../../runs/natural/bookreview/query1/full-01/sql/005-f00079fe297e4114a2943386d14643e7.sql) → [后序](../../runs/natural/bookreview/query1/full-01/sql/006-e6101bcc278a4d5f9c8bb99151f380cb.sql)。新谓词值=True，prompt含值=False。
- bookreview/query1 / natural：结果列 `book_id` 第 2 行值 `bookid_3` 匹配后序 `book_id`；[前序](../../runs/natural/bookreview/query1/full-01/sql/005-f00079fe297e4114a2943386d14643e7.sql) → [后序](../../runs/natural/bookreview/query1/full-01/sql/006-e6101bcc278a4d5f9c8bb99151f380cb.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query1 / natural：结果列 `LeadId__c` 第 0 行值 `00QWt0000089AekMAE` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query1/full-01/sql/001-de67ecc613504a05b9d8f0d949d68ca3.sql) → [后序](../../runs/natural/crmarenapro/query1/full-01/sql/002-742bb455944a45d7b76dd97f2a5bc8ed.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query1 / natural：结果列 `Id` 第 0 行值 `00QWt0000089AekMAE` 匹配后序 `LeadId__c`；[前序](../../runs/natural/crmarenapro/query1/full-01/sql/002-742bb455944a45d7b76dd97f2a5bc8ed.sql) → [后序](../../runs/natural/crmarenapro/query1/full-01/sql/003-3782911cf788489a8dbfb88f0ae12ce2.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query10 / natural：结果列 `agent_id` 第 5 行值 `005Wt000003NDqDIAW` 匹配后序 `c.ownerid`；[前序](../../runs/natural/crmarenapro/query10/full-01/sql/009-17c1c992295c4d209643176f9e518a11.sql) → [后序](../../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query11 / natural：结果列 `Product2Id` 第 0 行值 `01tWt000006hV8LIAU` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query11/full-01/sql/004-3465f03a9a834809a69ba4db6180a241.sql) → [后序](../../runs/natural/crmarenapro/query11/full-01/sql/005-5bebb56b0de94aedb131847368fcb006.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query12 / natural：结果列 `ContractID__c` 第 16 行值 `800Wt00000DE9FFIA1` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/005-181d1bc1c63e46a8a5396d55ac0a26e8.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/006-c4b4c9d836244f8c8d89d7b31f940ba8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query12 / natural：结果列 `ContractID__c` 第 17 行值 `800Wt00000DE8sgIAD` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/005-181d1bc1c63e46a8a5396d55ac0a26e8.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/006-c4b4c9d836244f8c8d89d7b31f940ba8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query12 / natural：结果列 `ContractID__c` 第 26 行值 `800Wt00000DE9ryIAD` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/005-181d1bc1c63e46a8a5396d55ac0a26e8.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/006-c4b4c9d836244f8c8d89d7b31f940ba8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query12 / natural：结果列 `OwnerId` 第 1 行值 `005Wt000003NJgAIAW` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql) → [后序](../../runs/natural/crmarenapro/query12/full-01/sql/009-ccca2b612217407c80c7bf2f41ea99ae.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Product2Id` 第 0 行值 `#01tWt000006hV6jIAE` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/003-136671a3baab48f485acb9540a032b0f.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/004-d3af33ccf6d84e068b3418fd345c0ad8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Product2Id` 第 1 行值 `01tWt000006hV57IAE` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/003-136671a3baab48f485acb9540a032b0f.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/004-d3af33ccf6d84e068b3418fd345c0ad8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Product2Id` 第 2 行值 `#01tWt000006hVQ5IAM` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/003-136671a3baab48f485acb9540a032b0f.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/004-d3af33ccf6d84e068b3418fd345c0ad8.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Product2Id` 第 1 行值 `01tWt000006hVQ5IAM` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/005-1d78862b719a41759ca36b6b542f7ccf.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/006-3adaea75a0ab4ee3bc0bccc9d0cd4b1a.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Product2Id` 第 0 行值 `01tWt000006hV57IAE` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/005-1d78862b719a41759ca36b6b542f7ccf.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/006-3adaea75a0ab4ee3bc0bccc9d0cd4b1a.sql)。新谓词值=False，prompt含值=False。
- crmarenapro/query2 / natural：结果列 `Id` 第 0 行值 `006Wt000007BHHfIAO` 匹配后序 `WhatId`；[前序](../../runs/natural/crmarenapro/query2/full-01/sql/007-f1b0b926360d4ccd8a1d303f876cea79.sql) → [后序](../../runs/natural/crmarenapro/query2/full-01/sql/008-aeab157c640a40479ae0b4178f4b391a.sql)。新谓词值=False，prompt含值=False。
- crmarenapro/query3 / natural：结果列 `Id` 第 0 行值 `006Wt000007BGGjIAO` 匹配后序 `WhatId`；[前序](../../runs/natural/crmarenapro/query3/full-01/sql/001-e8c84c1555ac4788b2e395190ffc2a1f.sql) → [后序](../../runs/natural/crmarenapro/query3/full-01/sql/002-5712e0e55d874149b85d59f6a65d79ef.sql)。新谓词值=False，prompt含值=True。
- crmarenapro/query6 / natural：结果列 `PricebookEntryId` 第 0 行值 `01uWt0000027P8bIAE` 匹配后序 `pe.Id`；[前序](../../runs/natural/crmarenapro/query6/full-01/sql/002-1be55f55b64242f582b678b577b356eb.sql) → [后序](../../runs/natural/crmarenapro/query6/full-01/sql/003-9c141f707ac54be497d386078a24957c.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / natural：结果列 `PricebookEntryId` 第 1 行值 `01uWt0000027P8cIAE` 匹配后序 `pe.Id`；[前序](../../runs/natural/crmarenapro/query6/full-01/sql/002-1be55f55b64242f582b678b577b356eb.sql) → [后序](../../runs/natural/crmarenapro/query6/full-01/sql/003-9c141f707ac54be497d386078a24957c.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query6 / natural：结果列 `PricebookEntryId` 第 2 行值 `01uWt0000027PADIA2` 匹配后序 `pe.Id`；[前序](../../runs/natural/crmarenapro/query6/full-01/sql/002-1be55f55b64242f582b678b577b356eb.sql) → [后序](../../runs/natural/crmarenapro/query6/full-01/sql/003-9c141f707ac54be497d386078a24957c.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query8 / natural：结果列 `oldvalue__c` 第 8 行值 `005Wt000003NIliIAG` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query8/full-01/sql/005-bb3f1da59e0a4cb089c4cc6c6df343a5.sql) → [后序](../../runs/natural/crmarenapro/query8/full-01/sql/006-d11aeb784fb644fc9634ef13bb3f72e2.sql)。新谓词值=True，prompt含值=False。
- crmarenapro/query8 / natural：结果列 `newvalue__c` 第 8 行值 `005Wt000003NGjuIAG` 匹配后序 `Id`；[前序](../../runs/natural/crmarenapro/query8/full-01/sql/005-bb3f1da59e0a4cb089c4cc6c6df343a5.sql) → [后序](../../runs/natural/crmarenapro/query8/full-01/sql/006-d11aeb784fb644fc9634ef13bb3f72e2.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query1 / natural：结果列 `gmap_id` 第 0 行值 `gmap_44` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query1/full-01/sql/005-7f46b0bac3874f42a97d94b9e207431f.sql) → [后序](../../runs/natural/googlelocal/query1/full-01/sql/006-30e085b7bfc744fc82ea1e018dd17a66.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query1 / natural：结果列 `gmap_id` 第 1 行值 `gmap_41` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query1/full-01/sql/005-7f46b0bac3874f42a97d94b9e207431f.sql) → [后序](../../runs/natural/googlelocal/query1/full-01/sql/006-30e085b7bfc744fc82ea1e018dd17a66.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query1 / natural：结果列 `gmap_id` 第 2 行值 `gmap_43` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query1/full-01/sql/005-7f46b0bac3874f42a97d94b9e207431f.sql) → [后序](../../runs/natural/googlelocal/query1/full-01/sql/006-30e085b7bfc744fc82ea1e018dd17a66.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query2 / natural：结果列 `gmap_id` 第 0 行值 `gmap_22` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query2/full-01/sql/003-75c4e51b02754c97825a0d5258a476cd.sql) → [后序](../../runs/natural/googlelocal/query2/full-01/sql/004-fcb781d2448b44d19096e62b90615224.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query2 / natural：结果列 `gmap_id` 第 1 行值 `gmap_25` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query2/full-01/sql/003-75c4e51b02754c97825a0d5258a476cd.sql) → [后序](../../runs/natural/googlelocal/query2/full-01/sql/004-fcb781d2448b44d19096e62b90615224.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query2 / natural：结果列 `gmap_id` 第 2 行值 `gmap_33` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query2/full-01/sql/003-75c4e51b02754c97825a0d5258a476cd.sql) → [后序](../../runs/natural/googlelocal/query2/full-01/sql/004-fcb781d2448b44d19096e62b90615224.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / natural：结果列 `gmap_id` 第 0 行值 `gmap_35` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query4/full-01/sql/004-0948e49757ff4be9a0806fbd06f56313.sql) → [后序](../../runs/natural/googlelocal/query4/full-01/sql/005-246c7691ce144ff192cbd4e1137d6823.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / natural：结果列 `gmap_id` 第 1 行值 `gmap_53` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query4/full-01/sql/004-0948e49757ff4be9a0806fbd06f56313.sql) → [后序](../../runs/natural/googlelocal/query4/full-01/sql/005-246c7691ce144ff192cbd4e1137d6823.sql)。新谓词值=True，prompt含值=False。
- googlelocal/query4 / natural：结果列 `gmap_id` 第 2 行值 `gmap_20` 匹配后序 `gmap_id`；[前序](../../runs/natural/googlelocal/query4/full-01/sql/004-0948e49757ff4be9a0806fbd06f56313.sql) → [后序](../../runs/natural/googlelocal/query4/full-01/sql/005-246c7691ce144ff192cbd4e1137d6823.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / natural：结果列 `track_id` 第 0 行值 `4233` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query1/full-01/sql/001-5d3fd2b4764c448f9b579500c5c20bfb.sql) → [后序](../../runs/natural/music_brainz_20k/query1/full-01/sql/002-394a0fdaecec4c68b686a1df614c652e.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / natural：结果列 `track_id` 第 1 行值 `12954` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query1/full-01/sql/001-5d3fd2b4764c448f9b579500c5c20bfb.sql) → [后序](../../runs/natural/music_brainz_20k/query1/full-01/sql/002-394a0fdaecec4c68b686a1df614c652e.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query1 / natural：结果列 `track_id` 第 2 行值 `15158` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query1/full-01/sql/001-5d3fd2b4764c448f9b579500c5c20bfb.sql) → [后序](../../runs/natural/music_brainz_20k/query1/full-01/sql/002-394a0fdaecec4c68b686a1df614c652e.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query2 / natural：结果列 `track_id` 第 0 行值 `4122` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query2/full-01/sql/001-b4ddce40b03d4f5298fc5c2e2c27bb78.sql) → [后序](../../runs/natural/music_brainz_20k/query2/full-01/sql/002-67a82748c7394387bf0fe5daf1080043.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / natural：结果列 `track_id` 第 0 行值 `14719` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [后序](../../runs/natural/music_brainz_20k/query3/full-01/sql/002-daa9a1b599ef445eb27ad0a057775871.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / natural：结果列 `track_id` 第 1 行值 `5124` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [后序](../../runs/natural/music_brainz_20k/query3/full-01/sql/002-daa9a1b599ef445eb27ad0a057775871.sql)。新谓词值=True，prompt含值=False。
- music_brainz_20k/query3 / natural：结果列 `track_id` 第 2 行值 `1344` 匹配后序 `track_id`；[前序](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [后序](../../runs/natural/music_brainz_20k/query3/full-01/sql/002-daa9a1b599ef445eb27ad0a057775871.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 1 行值 `N225` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/004-d4f83b30ea6a47efafd306554874ef6c.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 3 行值 `NSEI` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/004-d4f83b30ea6a47efafd306554874ef6c.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 6 行值 `HSI` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/004-d4f83b30ea6a47efafd306554874ef6c.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql)。新谓词值=True，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 8 行值 `N225` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/007-3ee02b5bd5234a138217eba651f8a024.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/008-115bbcc37df243ab8f6c8f07d38807b8.sql)。新谓词值=False，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 9 行值 `NSEI` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/007-3ee02b5bd5234a138217eba651f8a024.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/008-115bbcc37df243ab8f6c8f07d38807b8.sql)。新谓词值=False，prompt含值=False。
- stockindex/query1 / natural：结果列 `Index` 第 4 行值 `HSI` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query1/full-01/sql/007-3ee02b5bd5234a138217eba651f8a024.sql) → [后序](../../runs/natural/stockindex/query1/full-01/sql/008-115bbcc37df243ab8f6c8f07d38807b8.sql)。新谓词值=False，prompt含值=False。
- stockindex/query2 / natural：结果列 `Index` 第 0 行值 `IXIC` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query2/full-01/sql/006-1e12c8957f724d24ab9779113909f160.sql) → [后序](../../runs/natural/stockindex/query2/full-01/sql/007-8524f90f24b846da831a5df4f33bbd20.sql)。新谓词值=True，prompt含值=False。
- stockindex/query2 / natural：结果列 `Index` 第 7 行值 `NYA` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query2/full-01/sql/006-1e12c8957f724d24ab9779113909f160.sql) → [后序](../../runs/natural/stockindex/query2/full-01/sql/007-8524f90f24b846da831a5df4f33bbd20.sql)。新谓词值=True，prompt含值=False。
- stockindex/query2 / natural：结果列 `Index` 第 2 行值 `GSPTSE` 匹配后序 `"Index"`；[前序](../../runs/natural/stockindex/query2/full-01/sql/006-1e12c8957f724d24ab9779113909f160.sql) → [后序](../../runs/natural/stockindex/query2/full-01/sql/007-8524f90f24b846da831a5df4f33bbd20.sql)。新谓词值=True，prompt含值=False。
- stockmarket/query2 / natural：结果列 `Listing Exchange` 第 0 行值 `P` 匹配后序 `"Listing Exchange"`；[前序](../../runs/natural/stockmarket/query2/full-01/sql/003-a9542be353ce429e96696250c9f51098.sql) → [后序](../../runs/natural/stockmarket/query2/full-01/sql/004-2139e60ca48748c3ae0e31b0e8df1aa0.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query2 / natural：结果列 `ETF` 第 0 行值 `Y` 匹配后序 `"ETF"`；[前序](../../runs/natural/stockmarket/query2/full-01/sql/003-a9542be353ce429e96696250c9f51098.sql) → [后序](../../runs/natural/stockmarket/query2/full-01/sql/004-2139e60ca48748c3ae0e31b0e8df1aa0.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query3 / natural：结果列 `Listing Exchange` 第 4 行值 `Q` 匹配后序 `"Listing Exchange"`；[前序](../../runs/natural/stockmarket/query3/full-01/sql/003-97253af0c90941ddb956f31160248bd0.sql) → [后序](../../runs/natural/stockmarket/query3/full-01/sql/004-ac7e2a69960e4f2aaf634d4f3bbcd063.sql)。新谓词值=True，prompt含值=True。
- stockmarket/query4 / natural：结果列 `Listing Exchange` 第 0 行值 `N` 匹配后序 `"Listing Exchange"`；[前序](../../runs/natural/stockmarket/query4/full-01/sql/003-2bca31d5327b4fb6a5c58f78274d41be.sql) → [后序](../../runs/natural/stockmarket/query4/full-01/sql/004-a4e65db3630f47f3bd96492d4fd7a6c0.sql)。新谓词值=False，prompt含值=True。
- stockmarket/query4 / natural：结果列 `Listing Exchange` 第 0 行值 `N` 匹配后序 `"ETF"`；[前序](../../runs/natural/stockmarket/query4/full-01/sql/003-2bca31d5327b4fb6a5c58f78274d41be.sql) → [后序](../../runs/natural/stockmarket/query4/full-01/sql/004-a4e65db3630f47f3bd96492d4fd7a6c0.sql)。新谓词值=False，prompt含值=True。
- stockmarket/query5 / natural：结果列 `Market Category` 第 3 行值 `S` 匹配后序 `"Market Category"`；[前序](../../runs/natural/stockmarket/query5/full-01/sql/003-7fc0a5defbc74faba7719b2cfae63ec6.sql) → [后序](../../runs/natural/stockmarket/query5/full-01/sql/004-d373a3cc68d04ace801c4c5d16cfa2ae.sql)。新谓词值=True，prompt含值=True。
- yelp/query1 / natural：结果列 `business_ref` 第 1 行值 `businessref_52` 匹配后序 `business_ref`；[前序](../../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql) → [后序](../../runs/natural/yelp/query1/full-01/sql/004-f005e6191e5a4b87a6e15842069f443d.sql)。新谓词值=False，prompt含值=False。
- yelp/query1 / natural：结果列 `business_ref` 第 4 行值 `businessref_84` 匹配后序 `business_ref`；[前序](../../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql) → [后序](../../runs/natural/yelp/query1/full-01/sql/004-f005e6191e5a4b87a6e15842069f443d.sql)。新谓词值=False，prompt含值=False。
- yelp/query1 / natural：结果列 `business_ref` 第 3 行值 `businessref_76` 匹配后序 `business_ref`；[前序](../../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql) → [后序](../../runs/natural/yelp/query1/full-01/sql/004-f005e6191e5a4b87a6e15842069f443d.sql)。新谓词值=False，prompt含值=False。
- yelp/query5 / natural：结果列 `business_ref` 第 0 行值 `businessref_89` 匹配后序 `business_ref`；[前序](../../runs/natural/yelp/query5/full-01/sql/004-c6c3eac0b4a14f9dadbfbd58c59afcc9.sql) → [后序](../../runs/natural/yelp/query5/full-01/sql/005-447dc217f8124451b1706aedafbe43df.sql)。新谓词值=True，prompt含值=False。

## 共同准备候选

### ME0001 · DEPS_DEV_V1/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
packageinfo

packageinfo."system" = 'NPM'
```

[005](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/005-62f6bec7fbfe4b86a2e9c9d7f4a4ee64.sql) → [008](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/008-8b960cc18e124b97a6bc36777e4b0c48.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0002 · DEPS_DEV_V1/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
project_packageversion

project_packageversion."system" = 'NPM'
```

[006](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/006-ec84208a376947f38a957238c2835595.sql) → [014](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/014-32337e4405bf41a6874cc9996ffc572c.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0003 · DEPS_DEV_V1/query1 · fad · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
project_info

REGEXP_EXTRACT(project_info."project_information", 'The project ([^ ]+)', 1)
```

[007](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/007-7024e07e825146a6a4c1e5166c4c765d.sql) → [009](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/009-b5d7c5681b9f4302ad4fbfabfd7a9e26.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0004 · DEPS_DEV_V1/query1 · fad · derived

使用 3 次，首次后 2 次；仅共享子计算候选。

```
project_info

REGEXP_EXTRACT(project_info."project_information", '([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)', 1)
```

[010](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/010-9694a0e009d44f6eb3ef263130fc6421.sql) → [012](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/012-90923f48c9444bc0b06da881c5df5549.sql) → [015](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/015-e344e280b837462aaef95b26b2fc32e8.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0005 · DEPS_DEV_V1/query1 · fad · derived

使用 5 次，首次后 4 次；仅共享子计算候选。

```
project_info

REGEXP_EXTRACT(project_info."project_information", 'stars? count of\s+([\d,]+)', 1)
REGEXP_EXTRACT(project_info."project_information", '([\d,]+)\s+stars?', 1)
```

[010](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/010-9694a0e009d44f6eb3ef263130fc6421.sql) → [011](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/011-71cc5a619ad446e2a42b41b391a386fa.sql) → [012](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/012-90923f48c9444bc0b06da881c5df5549.sql) → [013](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/013-924544d99d3e4d999cf6c9362cc4de57.sql) → [015](../../runs/fad/DEPS_DEV_V1/query1/full-01/sql/015-e344e280b837462aaef95b26b2fc32e8.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0006 · DEPS_DEV_V1/query2 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
packageinfo

packageinfo."system" = 'NPM'
```

[004](../../runs/fad/DEPS_DEV_V1/query2/full-01/sql/004-941d2aae9cdc4f5a930d6c68288fa863.sql) → [005](../../runs/fad/DEPS_DEV_V1/query2/full-01/sql/005-1e52603435ca46f8acd7a4f02e61b4c7.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0007 · GITHUB_REPOS/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
contents

REGEXP_LIKE(LOWER(contents."sample_path"), '(^|/)readme\.md$')
```

[006](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/006-7cbe4ebbe0ba4872865bf94ae9b2e72c.sql) → [007](../../runs/fad/GITHUB_REPOS/query1/full-01/sql/007-b2446bcc6ce844e5be42bc6775373eed.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0008 · GITHUB_REPOS/query2 · fad · filter

使用 4 次，首次后 3 次；仅共享子计算候选。

```
contents

contents."sample_path" LIKE '%.swift'
```

[004](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/004-a89945ab84d74eb68161e9d38b46a91a.sql) → [005](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/005-edb9b6f7a973483b919a07b93082edd8.sql) → [006](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [009](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/009-0d967f8891534bf68322a2f452c9752b.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0009 · GITHUB_REPOS/query2 · fad · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
contents

REGEXP_EXTRACT(contents."repo_data_description", '(\d+) times', 1)
```

[006](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/006-a8fa11a6975b42289adf9cf8a5c0e44b.sql) → [009](../../runs/fad/GITHUB_REPOS/query2/full-01/sql/009-0d967f8891534bf68322a2f452c9752b.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0010 · GITHUB_REPOS/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
licenses

licenses."license" = 'apache-2.0'
```

[002](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql) → [003](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0011 · GITHUB_REPOS/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
languages

languages."language_description" LIKE '%Shell (%'
```

[002](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql) → [003](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0012 · GITHUB_REPOS/query3 · fad · join

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"

FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```

[002](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/002-b332ef6fca0a4ba1adb7eead15fecb0a.sql) → [003](../../runs/fad/GITHUB_REPOS/query3/full-01/sql/003-00a32c7f78df4ae380fd00d0877c08a1.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0013 · PANCANCER_ATLAS/query1 · fad · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
clinical_info

clinical_info."patient_description" ILIKE '%lower grade glioma%'
```

[005](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/005-30cb7a44269948ed8834b3c3d95050e3.sql) → [006](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/006-a0a4d62dd3db40c6b5b8c31d8b5d2ff1.sql) → [007](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/007-54dc369fd7514b48bbf0d6f09b2fd1f3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0014 · PANCANCER_ATLAS/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
clinical_info

clinical_info."histological_type" IS NOT NULL
clinical_info."histological_type" NOT LIKE '[%'
```

[006](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/006-a0a4d62dd3db40c6b5b8c31d8b5d2ff1.sql) → [007](../../runs/fad/PANCANCER_ATLAS/query1/full-01/sql/007-54dc369fd7514b48bbf0d6f09b2fd1f3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0015 · PANCANCER_ATLAS/query2 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
clinical_info

clinical_info."patient_description" ILIKE '%breast invasive carcinoma%'
```

[005](../../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/005-3cf67fa1971944dc810ac193152b3daa.sql) → [006](../../runs/fad/PANCANCER_ATLAS/query2/full-01/sql/006-d26814ac52d94904b89d408404365116.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0016 · PANCANCER_ATLAS/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
clinical_info

clinical_info."patient_description" ILIKE '%Breast invasive carcinoma%'
clinical_info."patient_description" ILIKE '%FEMALE%'
```

[005](../../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/005-8c24ff8d7b314760ab8e0f5f4543731a.sql) → [007](../../runs/fad/PANCANCER_ATLAS/query3/full-01/sql/007-27979943806b4743ba1654259e35f8c5.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0017 · PATENTS/query1 · fad · aggregate_state

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "publicationinfo"

COUNT(*)
```

[004](../../runs/fad/PATENTS/query1/full-01/sql/004-3fab454f877040a3add2f789ac4d5365.sql) → [005](../../runs/fad/PATENTS/query1/full-01/sql/005-8509fe9ef5294f41a8c8efef14965af6.sql)

基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

### ME0018 · PATENTS/query1 · fad · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
publicationinfo

SUBSTRING(TRIM(publicationinfo."filing_date"), -4)
SUBSTRING(TRIM(publicationinfo."filing_date"), 1, 4)
```

[007](../../runs/fad/PATENTS/query1/full-01/sql/007-a792b04e7f6042eb82b84cedce751659.sql) → [011](../../runs/fad/PATENTS/query1/full-01/sql/011-a35028c05c3d48d990e8729ea7decdb3.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0019 · PATENTS/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
cpc_definition

cpc_definition."level" = 5
```

[010](../../runs/fad/PATENTS/query1/full-01/sql/010-5e808f70c0f14ce88f66f5a17dc2ece0.sql) → [012](../../runs/fad/PATENTS/query1/full-01/sql/012-f07147bb9bc7448cbfba90888ef75193.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0020 · PATENTS/query2 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."patents_info" LIKE '%DE-%'
```

[006](../../runs/fad/PATENTS/query2/full-01/sql/006-fb12f62e4dbb42d9ad516a36177ce767.sql) → [007](../../runs/fad/PATENTS/query2/full-01/sql/007-de75e1c1822040b69867dff18c1f286a.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0021 · PATENTS/query3 · fad · aggregate_state

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "publicationinfo"

COUNT(*)
```

[004](../../runs/fad/PATENTS/query3/full-01/sql/004-c28490c05cb9409eacfcbc88b2dea807.sql) → [006](../../runs/fad/PATENTS/query3/full-01/sql/006-8270c2b274744d80bdd287f52cd08708.sql)

基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

### ME0022 · PATENTS/query3 · fad · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."patents_info" LIKE 'UNIV CALIFORNIA%'
```

[004](../../runs/fad/PATENTS/query3/full-01/sql/004-c28490c05cb9409eacfcbc88b2dea807.sql) → [007](../../runs/fad/PATENTS/query3/full-01/sql/007-872a86d27ca546aab3fec5d8b84fbda4.sql) → [008](../../runs/fad/PATENTS/query3/full-01/sql/008-6496653b63d041b0baf9eba8b3bf0d62.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0023 · PATENTS/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."citation" LIKE '%1212462%'
```

[009](../../runs/fad/PATENTS/query3/full-01/sql/009-14841ac64dfa4b9f86528e172a0f22d5.sql) → [010](../../runs/fad/PATENTS/query3/full-01/sql/010-7a4ec8af45844cffa8741ccee2b36a26.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0024 · PATENTS/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."patents_info" LIKE '%UNIV CALIFORNIA%'
```

[011](../../runs/fad/PATENTS/query3/full-01/sql/011-72e794cc0ab14201ab7a6ebd71250530.sql) → [012](../../runs/fad/PATENTS/query3/full-01/sql/012-4fc69af1481e4f55b5201caede99dd3e.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0025 · agnews/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
article_metadata

article_metadata."region" = 'Europe'
```

[003](../../runs/fad/agnews/query3/full-01/sql/003-2b626d1a70284ed4b99ab99e0fe2ea6e.sql) → [004](../../runs/fad/agnews/query3/full-01/sql/004-484c741ebf5746aabd07411f3413d056.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0026 · agnews/query3 · fad · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
article_metadata

SUBSTRING(article_metadata."publication_date", 1, 4)
```

[003](../../runs/fad/agnews/query3/full-01/sql/003-2b626d1a70284ed4b99ab99e0fe2ea6e.sql) → [004](../../runs/fad/agnews/query3/full-01/sql/004-484c741ebf5746aabd07411f3413d056.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0027 · bookreview/query2 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
books_info

books_info."categories" LIKE '%Literature & Fiction%'
```

[004](../../runs/fad/bookreview/query2/full-01/sql/004-081a7ca6b6084c78b026a5719530f397.sql) → [005](../../runs/fad/bookreview/query2/full-01/sql/005-38e30bb3230740d381cf2de5dea8b7dc.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0028 · crmarenapro/query10 · fad · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
casehistory__c

casehistory__c."field__c" = 'Owner Assignment'
```

[004](../../runs/fad/crmarenapro/query10/full-01/sql/004-cbfd1bba72ca483ca37db1cc48f0eba9.sql) → [005](../../runs/fad/crmarenapro/query10/full-01/sql/005-b068645d811849edb63d3d34bdd062da.sql) → [007](../../runs/fad/crmarenapro/query10/full-01/sql/007-a791c08b30a4452c894506874b295a12.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0029 · crmarenapro/query11 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
order

order."accountid" = '#001Wt00000PGXrNIAX'
```

[002](../../runs/fad/crmarenapro/query11/full-01/sql/002-19d0a6d433474cc78b730eced521f35a.sql) → [003](../../runs/fad/crmarenapro/query11/full-01/sql/003-0ce7fcbfcb97479d96f47f0d592ac0d3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0030 · crmarenapro/query12 · fad · join

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"

FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```

[001](../../runs/fad/crmarenapro/query12/full-01/sql/001-fb319174901a4c9888ad85ebcbdaa965.sql) → [002](../../runs/fad/crmarenapro/query12/full-01/sql/002-1a05cc1a94244f4896285e7ef7009389.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0031 · crmarenapro/query4 · fad · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
orderitem

orderitem."product2id" = '01tWt000006hVJdIAM'
```

[001](../../runs/fad/crmarenapro/query4/full-01/sql/001-7e3a1c2101354d1bb83be10790493c96.sql) → [004](../../runs/fad/crmarenapro/query4/full-01/sql/004-615e605901a64c83923eb439aa45721b.sql) → [006](../../runs/fad/crmarenapro/query4/full-01/sql/006-62344aff78f2461ba2f47a230f0e2552.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0032 · crmarenapro/query6 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
quote

quote."id" = '0Q0Wt000001WRAzKAO'
```

[001](../../runs/fad/crmarenapro/query6/full-01/sql/001-ce51debc166b4b74ad40f76ba83836f9.sql) → [002](../../runs/fad/crmarenapro/query6/full-01/sql/002-99448368616649bebe274d3db090bfed.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0033 · crmarenapro/query7 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
casehistory__c

casehistory__c."caseid__c" LIKE '%500Wt00000DDyznIAD%'
```

[010](../../runs/fad/crmarenapro/query7/full-01/sql/010-98ddb2561f6e42e7b021bba84c5c822e.sql) → [011](../../runs/fad/crmarenapro/query7/full-01/sql/011-a869be984a254094b6b47f751866563d.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0034 · crmarenapro/query7 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
emailmessage

emailmessage."parentid" LIKE '%500Wt00000DDyznIAD%' OR emailmessage."relatedtoid" LIKE '%500Wt00000DDyznIAD%'
```

[010](../../runs/fad/crmarenapro/query7/full-01/sql/010-98ddb2561f6e42e7b021bba84c5c822e.sql) → [012](../../runs/fad/crmarenapro/query7/full-01/sql/012-a2adad4df29a4db099b6563d30f7f532.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0035 · crmarenapro/query8 · fad · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
casehistory__c

casehistory__c."field__c" = 'Owner Assignment'
```

[002](../../runs/fad/crmarenapro/query8/full-01/sql/002-bb0f03a3a13d4b248923f8833d866155.sql) → [003](../../runs/fad/crmarenapro/query8/full-01/sql/003-814416a199f14106b3245afe35947247.sql) → [004](../../runs/fad/crmarenapro/query8/full-01/sql/004-475b9e44709c4b199411ad7a8ee40cdc.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0036 · googlelocal/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
business_description

business_description."hours" IS NOT NULL
```

[004](../../runs/fad/googlelocal/query3/full-01/sql/004-61b536c39cc249a09f7712e67097e377.sql) → [006](../../runs/fad/googlelocal/query3/full-01/sql/006-4962efe96a4e4fbcb0986a5d46f2de22.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0037 · music_brainz_20k/query3 · fad · aggregate_mv_extended

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "sales" WHERE 
sales."track_id"
COUNT(*)
SUM(sales."revenue_usd")
SUM(sales."units_sold")
```

[003](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [005](../../runs/fad/music_brainz_20k/query3/full-01/sql/005-dd8f3354db5d4de5adca29b3abf3edae.sql)

Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.

### ME0038 · music_brainz_20k/query3 · fad · aggregate_state

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "sales"  GROUP BY sales."track_id"

SUM(sales."revenue_usd")
SUM(sales."units_sold")
```

[003](../../runs/fad/music_brainz_20k/query3/full-01/sql/003-ad7c1908f40b4f739f4f697ba8fe6e3b.sql) → [005](../../runs/fad/music_brainz_20k/query3/full-01/sql/005-dd8f3354db5d4de5adca29b3abf3edae.sql)

基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

### ME0039 · stockindex/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
index_trade

index_trade."index" IN ('HSI', '000001.SS', '399001.SZ', 'N225', 'NSEI', 'TWII')
```

[005](../../runs/fad/stockindex/query1/full-01/sql/005-7840c3b62deb41f6a340469ecb2cebe0.sql) → [007](../../runs/fad/stockindex/query1/full-01/sql/007-1678feef9bfb4902a48185f0ca405ed2.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0040 · stockindex/query3 · fad · aggregate_mv_extended

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "index_trade" WHERE 
CASE WHEN REGEXP_FULL_MATCH(index_trade."date", '^[0-9]{2} [A-Za-z]{3} [0-9]{4}') THEN 'DD Mon YYYY' WHEN REGEXP_FULL_MATCH(index_trade."date", '^[A-Za-z]+ [0-9]{1,2}, [0-9]{4}') THEN 'Month D, YYYY' ELSE 'OTHER' END
index_trade."index"
COUNT(*)
MAX(index_trade."date")
MIN(index_trade."date")
```

[005](../../runs/fad/stockindex/query3/full-01/sql/005-7a9647a497cc4ed4bc5f453edd57c407.sql) → [006](../../runs/fad/stockindex/query3/full-01/sql/006-e545d30c0a3a4181bc3dbfa495e3eeb0.sql)

Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.

### ME0041 · yelp/query1 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
review

review."business_ref" IN ('businessref_52', 'businessref_84', 'businessref_76', 'businessref_87', 'businessref_65', 'businessref_94', 'businessref_90', 'businessref_16')
```

[004](../../runs/fad/yelp/query1/full-01/sql/004-2e7cf2e472f04809a613857f63d82a66.sql) → [005](../../runs/fad/yelp/query1/full-01/sql/005-ceeb4c2d6d104325b327b8be83d7b988.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0042 · yelp/query3 · fad · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
review

review."date" >= '2018-01-01'
review."date" < '2019-01-01'
```

[002](../../runs/fad/yelp/query3/full-01/sql/002-9450824df55a4f2bb109cd847fff92e9.sql) → [003](../../runs/fad/yelp/query3/full-01/sql/003-3ef9cd02c2334f2587cb305c74b66417.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0043 · DEPS_DEV_V1/query1 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
packageinfo

packageinfo."system" = 'NPM'
```

[006](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/006-a5bb89312e0d448cb255b1451afd469e.sql) → [007](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/007-4164a10ca28741d095ee7b9f5583819b.sql) → [009](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/009-a46400c1ac19499d934e4518e65ae405.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0044 · DEPS_DEV_V1/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
project_packageversion

project_packageversion."system" = 'NPM'
```

[008](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/008-2982192d5f29437b8cc1507584f17c5f.sql) → [012](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/012-0b726662f08d4931a79cbdacd2869ab8.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0045 · DEPS_DEV_V1/query1 · natural · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
project_info

REGEXP_EXTRACT(project_info."project_information", 'The project ([^ ]+)', 1)
REGEXP_EXTRACT(project_info."project_information", '([0-9]+) stars', 1)
```

[011](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/011-caabc4aa663a4ec3b1ba92fa4836207a.sql) → [013](../../runs/natural/DEPS_DEV_V1/query1/full-01/sql/013-8f39780a9c91476f8049aec18951828b.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0046 · DEPS_DEV_V1/query2 · natural · filter

使用 4 次，首次后 3 次；仅共享子计算候选。

```
packageinfo

packageinfo."system" = 'NPM'
```

[005](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/005-3b2c0e630df84ff7a8e9dcde693eaa05.sql) → [006](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/006-a8d60bd81720489fbf580187eb35451b.sql) → [008](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/008-cdae6aacd2f047c39deba46ac6e5b804.sql) → [011](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0047 · DEPS_DEV_V1/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
project_packageversion

project_packageversion."system" = 'NPM'
```

[007](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/007-bc6169bc8e5e49db8ab11b95b3cc8328.sql) → [010](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql) → [015](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0048 · DEPS_DEV_V1/query2 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
packageinfo

packageinfo."licenses" LIKE '%"MIT"%'
packageinfo."versioninfo" LIKE '%"IsRelease": true%'
```

[008](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/008-cdae6aacd2f047c39deba46ac6e5b804.sql) → [011](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/011-35c29264c83a461e80850bd873f0b112.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0049 · DEPS_DEV_V1/query2 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
project_packageversion

project_packageversion."projecttype" = 'GITHUB'
project_packageversion."projectname" IN ('lberrocal/npm-packages-template', 'leaflet/leaflet', 'leaflet/leaflet.fullscreen', 'leaflet/leaflet.markercluster', 'leandrowd/react-responsive-carousel', 'learnfrontend-dc/product-cart', 'ledgerproject/keypairoom', 'leebyron/jasmine-check', 'leebyron/testcheck-js', 'leecade/react-native-swiper', 'legendjaden/aftablecolumn', 'lekoarts/gatsby-themes', 'lenconda/dollie', 'leo-ran/easy-node-reflect', 'leo-ran/easy-node-server', 'leofelix077/bunchofnothing', 'leoilab/react-native-analytics-segment-io', 'leonardparisi/easy-express-server', 'leoroese/template-cli', 'letrungdo/react-ui-component-lib', 'levelkdev/dxswap-sdk', 'leviticusmb/divine-amd-loader', 'leviticusmb/divine-synchronization', 'leviticusmb/esxx-2', 'leviticusmb/ghostly', 'leviticusmb/sysconsole', 'lfujiwara/dnausp-core', 'libertydsnp/activity-content', 'libertydsnp/contracts', 'libertydsnp/parquetjs', 'libertydsnp/sdk-ts', 'libertydsnp/test-generators', 'libertyequalitydata/dynamic-data', 'liivevideo/react-native-web-webrtc', 'linkshare/service-container', 'lisiadito/checksslcertificate', 'litejs/natural-compare-lite', 'ljharb/define-properties', 'ljharb/has-symbols', 'ljharb/object-keys', 'ljharb/object.assign', 'ljharb/qs', 'ln-zap/node-lnd-grpc', 'locize/fluent_conv', 'lodash/lodash', 'logflare/winston-logflare', 'lohfu/dom-append-to', 'lohfu/dom-children', 'lohfu/dom-closest', 'lohfu/dom-insert-after', 'lohfu/domp', 'lohfu/domp-create', 'lohfu/domp-create-many', 'lohfu/domp-is', 'loktor/image-compressor', 'lonelycpp/react-native-youtube-iframe', 'lrembacz/dragndrop', 'lrembacz/vue-dragndrop.', 'ltsfran/dreamtec-ui', 'lucasferreira/react-native-flash-message', 'lucassifoni/ondif-js', 'luckylooke/dragon', 'luehang/react-native-masonry-list', 'lukasz-galka/ngx-gallery', 'lukeed/escalade', 'luzzif/ethereum-contacts-registry', 'lxg1992/sharedlotide', 'lydell/js-tokens', 'lzrski/node-damerau-levenshtein', 'm1212e/easy-rpc-browser', 'maddijoyce/serverless-ses-mjml', 'mafintosh/generate-function', 'mafintosh/generate-object-property', 'mafintosh/is-my-json-valid', 'mafintosh/tar-fs', 'magnusdanielson/au-fluent-ui', 'magnusdanielson/au-office-ui', 'magnusdanielson/aureactwrapper', 'maksimovicdanijel/vue-countdown', 'malte-wessel/react-custom-scrollbars', 'mammadataei/dom-assertions', 'mapbox/mapbox-gl-draw', 'mapbox/mapbox-gl-js', 'mapbox/node-pre-gyp', 'mapbox/node-sqlite3', 'mapbox/shp-write', 'marak/colors.js', 'marcbachmann/node-html-pdf', 'marcelklehr/toposort', 'march08/duik', 'marijnh/moduleserve', 'mariuszfoltak/angular2-datatable', 'mark-shark/edge-scss', 'markcellus/wait-for-element-transition', 'markhughes/droppy', 'marknotton/doggistyle', 'markormesher/dragonlabs-eslint-config', 'markormesher/dragonlabs-redux-cache-key-util', 'marmelab/gremlins.js', 'maronato/vue-toastification', 'martinalmlof/homebridge-pioneer-vsx527', 'martinpagesaal/ngx-ace-editor-wrapper', 'marvin-j97/tunisia', 'marvin-j97/yxc', 'master-atul/react-native-exception-handler', 'matejlauko/duotone', 'mathe42/vite-plugin-serviceworker', 'mathiasbynens/cssesc', 'mathiasbynens/he', 'mathiasbynens/jsesc', 'mathiasbynens/regenerate', 'mathiasbynens/regenerate-unicode-properties', 'mathiasbynens/regexpu-core', 'mathiasbynens/string.prototype.codepointat', 'mathiasbynens/unicode-canonical-property-names-ecmascript', 'mathiasbynens/unicode-match-property-ecmascript', 'mathiasbynens/unicode-match-property-value-ecmascript', 'mathiasbynens/unicode-property-aliases-ecmascript', 'mathiasgheno/ducto', 'maticnetwork/matic.js', 'matoseb/musee-de-la-main-2022-scripts', 'matt-esch/virtual-dom', 'mattdesl/ghpages', 'matthiaaas/express-file-routing', 'mattilehtinen/postgrator-cli', 'mattlewis92/angular-confirmation-popover', 'mattphillips/deep-object-diff', 'mauriciohernancabrera/tymo-utils', 'maxinminax/node-mihome', 'maxogden/concat-stream', 'maxwellsquared/lotide', 'mbrn/material-table', 'mcavage/node-asn1', 'mcavage/node-assert-plus', 'mchlbrnd/normalizr-decorators', 'mcicheick/dd-react-lib', 'mdevils/node-html-entities', 'medelman17/edel.monster', 'medikoo/d', 'medikoo/es5-ext', 'medikoo/es6-iterator', 'medikoo/es6-map', 'medikoo/es6-set', 'medikoo/es6-symbol', 'medikoo/es6-weak-map', 'medikoo/event-emitter', 'medusajs/medusa', 'meetearnest/eslint-config-earnest', 'meetearnest/eslint-config-earnest-es7', 'meettya/whet.extend', 'megafetis/vue3-treeselect', 'meganz/jodid25519', 'mengxiong10/vue2-datepicker', 'menudocs/erela.js', 'meryn/performance-now', 'mhart/aws4', 'mhart/stringstream', 'miaowing/schedule', 'michael-ciniawsky/postcss-load-config', 'michael-ciniawsky/postcss-load-options', 'michael-ciniawsky/postcss-load-plugins', 'michaeljier/easy-messenger', 'micky2be/superlogin-client', 'microlinkhq/youtube-dl-exec', 'microsoft/monaco-editor', 'microsoft/monaco-editor-webpack-plugin', 'microsoft/typescript', 'microsoft/typescript-website', 'microsoft/web-build-tools', 'miguelfernandez008/test-npm-package', 'mikaelbr/marked-terminal', 'mikaelbr/node-notifier', 'mike-dax/gatsby-plugin-ffmpeg', 'mike-dax/gatsby-remark-videos', 'mike-spainhower/querystring', 'mikeal/aws-sign', 'mikeal/caseless', 'mikeal/forever-agent', 'mikeal/oauth-sign', 'mikeal/tunnel-agent', 'mikeal/watch', 'mikemcl/big.js', 'mikolalysenko/is-property', 'mikolalysenko/uniq', 'milanovic-dusan/bb-model', 'mindary/drpc', 'mindoktor/material-ui', 'mindoktor/pulse', 'mioriaty/duong-custom-ckeditor5', 'mirrorjs/mirror', 'mirrorthink/vue-wow', 'mirumee/saleor-sdk', 'mishoo/uglifyjs2', 'mixer/arcade-machine', 'mixu/markdown-styles', 'mjmlio/mjml', 'mkayander/easyenv', 'mklabs/node-fileset', 'mmaakkii/dmanz-connector', 'mmende/homebridge-samsungtv-control2', 'mnasyrov/ditox', 'mobilereality/react-native-select-pro', 'mobxjs/mobx', 'mokkabonna/inquirer-autocomplete-prompt', 'moment/moment', 'momsfriendlydevco/doop-avatar', 'momsfriendlydevco/doop-cache', 'momsfriendlydevco/doop-core-vue', 'momsfriendlydevco/doop-dates', 'momsfriendlydevco/doop-debug', 'momsfriendlydevco/doop-deepstream', 'momsfriendlydevco/doop-deloy', 'momsfriendlydevco/doop-deploy', 'momsfriendlydevco/doop-digest', 'momsfriendlydevco/doop-directive-jump', 'momsfriendlydevco/doop-docs', 'momsfriendlydevco/doop-drag-drop', 'momsfriendlydevco/doop-dynamic-component', 'momsfriendlydevco/doop-eslint-plugin-doop', 'momsfriendlydevco/doop-eval', 'momsfriendlydevco/doop-files', 'momsfriendlydevco/doop-http', 'momsfriendlydevco/doop-locking', 'momsfriendlydevco/doop-permissions', 'momsfriendlydevco/doop-polyfills', 'momsfriendlydevco/doop-prompt', 'momsfriendlydevco/doop-search', 'momsfriendlydevco/doop-service-clipboard', 'momsfriendlydevco/doop-service-code-alloc', 'momsfriendlydevco/doop-service-components', 'momsfriendlydevco/doop-service-config', 'momsfriendlydevco/doop-service-data', 'momsfriendlydevco/doop-service-db', 'momsfriendlydevco/doop-service-debug', 'momsfriendlydevco/doop-service-dirty-checker', 'momsfriendlydevco/doop-service-emit', 'momsfriendlydevco/doop-service-eval', 'momsfriendlydevco/doop-service-files', 'momsfriendlydevco/doop-service-git', 'momsfriendlydevco/doop-service-http', 'momsfriendlydevco/doop-service-lifecycle', 'momsfriendlydevco/doop-service-loader', 'momsfriendlydevco/doop-service-locking', 'momsfriendlydevco/doop-service-lodash', 'momsfriendlydevco/doop-service-log-change', 'momsfriendlydevco/doop-service-morph', 'momsfriendlydevco/doop-service-oid', 'momsfriendlydevco/doop-service-prompt', 'momsfriendlydevco/doop-service-pub-sub', 'momsfriendlydevco/doop-service-replace', 'momsfriendlydevco/doop-service-router', 'momsfriendlydevco/doop-service-screen', 'momsfriendlydevco/doop-service-slack', 'momsfriendlydevco/doop-service-throttle', 'momsfriendlydevco/doop-service-timeout', 'momsfriendlydevco/doop-service-timestamps', 'momsfriendlydevco/doop-service-toast', 'momsfriendlydevco/doop-service-transitions', 'momsfriendlydevco/doop-service-watch-all', 'momsfriendlydevco/doop-table', 'momsfriendlydevco/doop-throttle', 'momsfriendlydevco/doop-timeout', 'momsfriendlydevco/doop-validate', 'mono/mono', 'moonshotcollective/scaffold-moonshot-starter', 'mooory/ckeditor5-custom', 'moox/eslint-loader', 'moox/postcss-message-helpers', 'moox/reduce-css-calc', 'moox/reduce-function-call', 'moregidge/parsley.js', 'morgbillingsley/mailer-domain', 'moribvndvs/ng2-idle', 'mormubis/elo', 'mormubis/pgn', 'morphatic/v-stripe-elements', 'motdotla/dotenv', 'mousumidutta136/lotide', 'mozilla-services/react-jsonschema-form', 'mozilla/pdf.js', 'mozilla/pdfjs-dist', 'mozilla/source-map', 'mpetroff/pannellum', 'mpoiriert/service-container', 'mr-strike/react-native-advance-draggable-view', 'mr-strike/react-native-advance-image-cropper', 'mrdannael/easy-eva-icons', 'ms-dg/api-typings', 'ms-dg/create-dg-react', 'ms-dg/miniprogram-storage', 'mui-org/material-ui', 'muniftanjim/draft-js-modules', 'murhafsousli/ngx-sharebuttons', 'mweststrate/relative-deps', 'mybabysexy/react-sip-phone', 'mythie/dockite', 'myzhangdong/log-collect', 'n05ae/react-virtual-scroll-list', 'n0sae/react-virtual-list', 'n43/easyapp', 'n4kz/react-native-material-textfield', 'naknode/test', 'namespace-ee/react-calendar-timeline', 'nandorojo/dripsy', 'nandorojo/expo-theme-ui', 'nanzm/dora', 'naoufal/react-native-payments', 'naoufal/react-native-touch-id', 'napthedev/react-tuby', 'nartc/react-native-barcode-mask', 'nasa8x/html-metadata-parser', 'nativescript/plugins', 'natural-apptitude/ngrx-store-ionic-storage', 'naugtur/xhr', 'ndmitry/grunt-postcss', 'nebulouslabs/nodejs-sia', 'nedredmond/dsa-ui', 'nehr/ws-scss-mixins', 'quangbuule/extract-hoc', 'quartzjer/ecc-jsbn', 'quentinsvn/react-native-fix', 'quilljs/quill', 'qyjs/captchajs', 'ra-protocol/ra-protocol', 'rackt/async-props', 'rahuldream11/react-native-analytics-segment-io', 'rails/rails', 'rajdee/postcss-autoimport', 'rajneeshraghav/resumable-file-uploads', 'rajneeshraghav/wexer-videojs', 'ramdan123/default-token-list', 'rampnetwork/crypto-address-validator', 'rangoo94/easen-tools', 'rashagu/dnd-kit-vue', 'rauldeheer/use-async-effect', 'raynos/console-browserify', 'raynos/duplexer', 'raynos/function-bind', 'raynos/xtend', 'react-component/dropdown', 'react-component/picker', 'react-component/select', 'react-component/slider', 'react-component/tabs', 'react-csv/react-csv', 'react-icons/react-icons', 'react-materialize/react-materialize', 'react-native-admob/admob', 'react-native-community/react-native-tab-view', 'react-native-community/react-native-webview', 'react-native-device-info/react-native-device-info', 'react-native-elements/react-native-elements', 'react-native-webrtc/react-native-webrtc', 'react-navigation/react-navigation', 'react-qr-reader/react-qr-reader', 'react-toolbox/react-toolbox', 'reactive-extensions/rxjs', 'reactjs-ui/reactjs-pull-refresh', 'reactjs/react-art', 'realdolos/node-jpegoptim', 'realtymaps/promise-ftp', 'reasonml-community/bs-express', 'reasonml-community/bs-webapi-incubator', 'reasonml-community/graphql_ppx', 'rebilly/redoc', 'redpandatronicsuk/react-native-check-app-install', 'redux-observable/redux-observable', 'reg2005/adonis5-scheduler', 'regexps/filename-regex', 'release-it/conventional-changelog', 'remarkjs/remark-github', 'remaxjs/remax', 'renddslow/dunsany', 'reposilite-playground/jsonforms', 'request/promise-core', 'request/request', 'request/request-promise', 'resembli/docusolid', 'rethinkdb/rethinkdb-ts', 'revsoul12/lotide', 'rhumaric/express-mount-files', 'ribeiro-tiago/bundletool', 'richmccartney/design-system-monorepo', 'riophae/vue-treeselect', 'rishabh09/duffle-bag', 'rjsf-team/react-jsonschema-form', 'rjw57/grib.js', 'rmartone/missionlog', 'robbederks/downzip', 'robbiesdream/ci-tests', 'robinbiao/dw', 'robinfehr/react-portal', 'rojer95/dslate', 'royriojas/file-entry-cache', 'royriojas/flat-cache', 'rrag/react-stockcharts', 'rrdelaney/reason', 'rreverser/acorn-jsx', 'rs/node-netmask', 'rstiller/inspector-elasticsearch', 'rstiller/inspector-vm', 'rubengrill/apollo-typed-documents', 'ruimarinho/bitcoin-core', 'ruinouscheng/share-config', 'run-z/rollup-plugin-flat-dts', 'rustwasm/create-wasm-app', 'rvagg/bl', 'rvagg/isstream', 'rvagg/node-errno', 'rvagg/node-worker-farm', 'rvagg/prr', 'rvagg/string_decoder', 'ryan-lau314/modularscale-sass', 'sabakihq/gtp', 'saiya/dsps', 'salesforce/lwc', 'salesforce/tough-cookie', 'salesforceeng/tough-cookie', 'samsaffron/message_bus', 'samuelgoto/docscript', 'samverschueren/generator-alfred', 'sanity-io/cross-dataset-duplicator', 'sanity-io/gatsby-source-sanity', 'santiment/san-ui', 'sarin-dotin/eslint-config-react-native', 'sass/node-sass', 'sastan/distilt', 'satya164/react-simple-code-editor', 'savokiss/vue-raven', 'sboudrias/inquirer.js', 'sboudrias/readline2', 'sboudrias/run-async', 'scarlatum/eccheuma-crusoris', 'schickling/gulp-webserver', 'schmich/instascan', 'scnale/openzeppelin-upgrades', 'scniro/react-codemirror2', 'scravy/node-macaddress', 'seansobey/markdown-preprocessor', 'searchkit/searchkit', 'sebinsua/docco-next', 'sebmaster/tr46.js', 'secretmapper/react-image-annotation', 'securingsincity/react-ace', 'segmentio/analytics-node', 'segmentio/helpscout', 'seishun/node-steam-crypto', 'selkkie/nodebb-plugin-sso-discord-with-logo', 'semantic-org/semantic-ui', 'semantic-org/semantic-ui-css', 'semantic-release/git', 'semantic-release/npm', 'senecajs/seneca-mesh', 'sentrei/dogan', 'serverless-nextjs/serverless-next.js', 'sethsandaru/vue-form-builder', 'sethvincent/dxv', 'sfundomhlungu/-dot.product-createlib', 'sgguo/dc-datatable', 'shahen94/react-native-switch', 'shaka-project/shaka-player', 'shama/gaze', 'shanebo/balm', 'shanebo/coerce', 'shanebo/cors', 'shanebo/csrf', 'shanebo/engines', 'shanebo/forcessl', 'shanebo/ip-limiter', 'shanebo/parser', 'shanebo/session', 'shanebo/slashless', 'shanebo/static', 'shanebo/swap-redirect', 'sharaal/dnode', 'sharaal/maxdome-rssfeeds', 'sharaal/sharaal', 'shelljs/shelljs', 'shinnn/is-resolvable', 'shinnn/spdx-license-ids', 'shopify/polaris-icons', 'shopify/polaris-react', 'shopify/quilt', 'shtylman/node-browser-resolve', 'shtylman/node-process', 'shwetdream11/react-native-fast-image', 'shwetdream11/react-native-google-analytics-bridge', 'shwetdream11/react-native-shimmer', 'signal-noise/index-core', 'signavio/react-mentions', 'siimon/prom-client', 'simeonackermann/rdform', 'sindresorhus/active-win', 'sindresorhus/ansi-escapes', 'sindresorhus/ansi-regex', 'sindresorhus/array-differ', 'sindresorhus/array-find-index', 'sindresorhus/array-union', 'sindresorhus/array-uniq', 'sindresorhus/arrify', 'sindresorhus/binary-extensions', 'sindresorhus/builtin-modules', 'sindresorhus/caller-path', 'sindresorhus/callsites', 'sindresorhus/camelcase', 'sindresorhus/camelcase-keys', 'sindresorhus/cli-cursor', 'sindresorhus/code-point-at', 'sindresorhus/decamelize', 'sindresorhus/del', 'sindresorhus/detect-indent', 'sindresorhus/escape-string-regexp', 'sindresorhus/exit-hook', 'sindresorhus/figures', 'sindresorhus/find-up', 'sindresorhus/get-stdin', 'sindresorhus/globals', 'sindresorhus/globby', 'sindresorhus/gzip-size', 'sindresorhus/has-ansi', 'sindresorhus/has-color', 'sindresorhus/has-flag', 'sindresorhus/home-or-tmp', 'sindresorhus/indent-string', 'sindresorhus/invert-kv', 'sindresorhus/is-absolute-url', 'sindresorhus/is-binary-path', 'sindresorhus/is-builtin-module', 'sindresorhus/is-finite', 'sindresorhus/is-fullwidth-code-point', 'sindresorhus/is-path-cwd', 'sindresorhus/is-path-in-cwd', 'sindresorhus/is-path-inside', 'sindresorhus/is-plain-obj', 'sindresorhus/is-svg', 'sindresorhus/lcid', 'sindresorhus/leven', 'sindresorhus/load-json-file', 'sindresorhus/loud-rejection', 'sindresorhus/map-obj', 'sindresorhus/meow', 'sindresorhus/multimatch', 'sindresorhus/ncname', 'sindresorhus/normalize-url', 'sindresorhus/number-is-nan', 'sindresorhus/object-assign', 'sindresorhus/onetime', 'sindresorhus/opn', 'sindresorhus/os-homedir', 'sindresorhus/os-locale', 'sindresorhus/os-tmpdir', 'sindresorhus/p-filter', 'sindresorhus/p-limit', 'sindresorhus/p-map', 'sindresorhus/parse-json', 'sindresorhus/path-exists', 'sindresorhus/path-is-absolute', 'sindresorhus/path-key', 'sindresorhus/path-type', 'sindresorhus/pify', 'sindresorhus/pkg-dir', 'sindresorhus/pkg-up', 'sindresorhus/prepend-http', 'sindresorhus/query-string', 'sindresorhus/read-pkg', 'sindresorhus/read-pkg-up', 'sindresorhus/redent', 'sindresorhus/repeating', 'sindresorhus/require-uncached', 'sindresorhus/resolve-from', 'sindresorhus/restore-cursor', 'sindresorhus/set-immediate-shim', 'sindresorhus/shebang-regex', 'sindresorhus/slash', 'sindresorhus/sort-keys', 'sindresorhus/string-width', 'sindresorhus/strip-bom', 'sindresorhus/strip-indent', 'sindresorhus/strip-json-comments', 'sindresorhus/to-fast-properties', 'sindresorhus/trim-newlines', 'sindresorhus/user-home', 'sindresorhus/xml-char-classes', 'sindresorhus/yocto-queue', 'skeleton-metal/apollo-server-express', 'skick1234/discord-ytdl-core', 'skick1234/node-youtube-dl', 'skick1234/node-ytpl', 'skick1234/node-ytsr', 'sky111144/easyregexp', 'sky111144/easytype', 'slorber/responsive-loader', 'snowpackjs/snowpack', 'sockjs/sockjs-client', 'sockjs/sockjs-node', 'softwarebrothers/adminjs-mongoose', 'solana-labs/wallet-adapter', 'soliantconsulting/fm-data-api-client', 'solinor/react-native-bluetooth-status', 'soluto/dynamico', 'sortablejs/vue.draggable', 'soumyatiwari392/ds-awesome', 'sourcey/spectacle', 'spautz/dynamic-selectors', 'spike-the-coder/electron-privacy', 'spite/three.meshline', 'spruceid/siwe', 'sridharsathasivam/data-lib', 'sscfaith/avue-form-design', 'sstur/draft-js-export-html', 'stabzs/angular2-toaster', 'stackbithq/datocms-plugin-typed-list', 'stacktical/stacktical-dsla-contracts', 'starchup/node-converge', 'stardustapp/javascript-client', 'starnutoditopo/react-typescript-flight-indicators', 'stefanpenner/get-caller-file', 'steffeydev/react-native-popover-view', 'stephenliu1944/beancommons-define', 'stephenliu1944/beancommons-http', 'stephenliu1944/beancommons-proxy', 'stephenliu1944/beanreact-permission', 'stephenliu1944/easytool-define-config', 'stephenliu1944/easytool-http', 'stephenliu1944/easytool-react-carousel', 'stephenliu1944/easytool-react-permission', 'stephenliu1944/easytool-react-types', 'stephenliu1944/mock-server', 'stevelacy/browser-info', 'stevemao/html-comment-regex', 'stevenvachon/http-equiv-refresh', 'stevenvachon/relateurl', 'stidges/laravel-mix-mjml', 'stimulcross/donation-alerts', 'stoneqq11/react-dialog', 'stoneqq11/react-lazy-img', 'stoneqq11/react-load-more', 'stoneqq11/react-loading', 'stoneqq11/react-trans-btn', 'storybookjs/react-treebeard', 'strapi/strapi', 'stream-utils/destroy', 'stream-utils/unpipe', 'strongholdmedia/react-vs-calendar', 'strongholdmedia/react-vs-tagger', 'strongholdmedia/react-vs-tree', 'strongholdmedia/usable', 'strongloop/fsevents', 'styled-components/styled-components', 'substack/defined', 'substack/http-browserify', 'substack/https-browserify', 'substack/json-stable-stringify', 'substack/jsonify', 'substack/minimist', 'substack/node-commondir', 'substack/node-concat-map', 'substack/node-mkdirp', 'substack/node-optimist', 'substack/node-resolve', 'substack/node-wordwrap', 'substack/path-browserify', 'substack/stream-browserify', 'substack/text-table', 'substack/tty-browserify', 'substack/typedarray', 'substack/vm-browserify', 'sudomaker/dominative-solid', 'sudomaker/dominative-vue', 'suminksudhi/nativescript-notification', 'suminksudhi/react-media-loader', 'supasate/connected-react-router', 'surnet/graphql-amqp-subscriptions', 'suryacandra/cratail', 'sushiswap/sushiswap-sdk', 'suweya/react-verification-code-input', 'sveltejs/prettier-plugin-svelte', 'sveltejs/sapper', 'sveltejs/site-kit', 'sveltejs/svelte', 'svenchristian/react-progressive-loader', 'svg/svgo', 'swagger-api/swagger-ui', 'swdenglian/dva-rn', 'sweetiq/schemats', 'swolf88/types-4-strapi', 'swuecho/camelsnakekebab_bs', 'swuecho/jinja_bin', 'synw/docdundee', 'sysgears/domain-schema', 'szpadel/chrome-headless-render-pdf', 'szymmis/vite-express', 't3dkich/smart-order-router-maistestsubnet-modded', 'tabookey-dev/tabookey-gasless', 'tada5hi/ebec', 'tadejgasparovic/multer-storage-google-cloud', 'taidomi-sapi-de-cv/domitai-sdk', 'tailwindcss/tailwindcss', 'tailwindcss/typography', 'taixw2/dx', 'tanhauhau/levenary', 'tapjs/signal-exit', 'tappleby/redux-batched-subscribe', 'tarruda/has', 'teambank/easycredit-ratenkauf-webcomponents', 'teamdock/password-cli', 'techroad-community/dooda-swap-core', 'techroad-community/dooda-swap-sdk', 'techroad-community/dooda-toolkit', 'tencent/vconsole', 'terkelg/prompts', 'ternjs/acorn', 'tetther1122/job-board', 'th3rdwave/react-native-safe-area-context', 'the-eater/grunt-po2mo', 'the-economist-editorial/component-404', 'the-economist-editorial/component-ad-panel', 'the-economist-editorial/component-articletemplate', 'the-economist-editorial/component-gallery', 'the-economist-editorial/component-imagecaption', 'the-economist-editorial/component-scenechanger', 'the-economist-editorial/component-silver-bullet', 'the-economist-editorial/component-video', 'the-economist-editorial/sharebar', 'the-front-distillery/stylelint-config-distillery', 'theabraham/growly', 'thebigbrain/dora.js', 'theboringschool/toast-notify', 'thedeeno/web-component-tester-istanbul', 'theia-ide/theia', 'thejameskyle/pretty-format', 'thejameskyle/react-loadable', 'thejameskyle/spectacle-code-slide', 'then/promise', 'theodo-uk/nestjs-admin', 'theprateinteractives/common-lists', 'theprateinteractives/generation-game', 'thesoftwarehouse/react-router-permissions', 'thinkjs/think-sequelize', 'thlorenz/ansicolors', 'thlorenz/cardinal', 'thlorenz/convert-source-map', 'thlorenz/deep-is', 'thlorenz/readdirp', 'thlorenz/redeyed', 'thomasdondorf/puppeteer-cluster', 'thomwright/postgres-migrations', 'thoughtsunificator/domodel-chat', 'thoughtsunificator/domodel-form', 'thoughtsunificator/domodel-paginator', 'thoughtsunificator/domodel-popup', 'thoughtsunificator/domodel-resizable', 'thoughtsunificator/domodel-router', 'thoughtsunificator/domodel-steps', 'thoughtsunificator/domodel-tabs', 'tigthor/associated-token', 'tigthor/borsh', 'tigthor/dvst', 'tigthor/pool', 'timhall/svelte-apollo', 'timpaulaskasds/sfparty', 'tirupatibalaji-dev/djs-handler', 'titel-media/node-fetch', 'tj/co', 'tj/commander.js', 'tjatse/ansi-html', 'tkellen/node-interpret', 'tmpvar/jsdom', 'toilal/ng-pickadate', 'wizards-lab/routing')
```

[010](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/010-add329c0d8af4331841ebf4ed8df7442.sql) → [015](../../runs/natural/DEPS_DEV_V1/query2/full-01/sql/015-43ac636561c74708a6ee449f3bb299a2.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0050 · GITHUB_REPOS/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
languages

languages."language_description" LIKE '%Swift%'
```

[004](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/004-ba83de1dba9d4d5cb42a837e90671e9c.sql) → [005](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/005-c4b0bd63b6004ccc832b096c28c942dd.sql) → [013](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/013-72dd1f7f2fed4c1cbae168634d642bb3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0051 · GITHUB_REPOS/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
contents

LOWER(contents."repo_data_description") LIKE '%non-binary%'
```

[007](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/007-28663d17f2dc4fe5a85eaca518fdc05d.sql) → [012](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql) → [014](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0052 · GITHUB_REPOS/query2 · natural · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
contents

REGEXP_EXTRACT(contents."repo_data_description", '(\d+) times', 1)
```

[007](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/007-28663d17f2dc4fe5a85eaca518fdc05d.sql) → [012](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0053 · GITHUB_REPOS/query2 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
files

files."path" LIKE '%.swift'
```

[012](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql) → [014](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0054 · GITHUB_REPOS/query2 · natural · join

使用 3 次，首次后 2 次；仅共享子计算候选。

```
FROM "files" JOIN "contents" ON files."id" = contents."id"

FROM "files" JOIN "contents" ON files."id" = contents."id"
```

[012](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/012-2956253b54b0483590a60fb90d93fe18.sql) → [014](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/014-d0a8fbe1c5654c4ca4c1a4eb63902a2a.sql) → [016](../../runs/natural/GITHUB_REPOS/query2/full-01/sql/016-29d8fde5f6b2417ab64a22f5a1353250.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0055 · GITHUB_REPOS/query3 · natural · filter

使用 4 次，首次后 3 次；仅共享子计算候选。

```
languages

languages."language_description" LIKE '%Shell%'
```

[004](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/004-8c7f674562584430bdf7657a7315e37c.sql) → [007](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/007-be8a2c6eb15f4ebab8e4bf7634c6b9a7.sql) → [009](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql) → [010](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0056 · GITHUB_REPOS/query3 · natural · filter

使用 4 次，首次后 3 次；仅共享子计算候选。

```
languages

languages."language_description" NOT LIKE '%PowerShell%'
```

[007](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/007-be8a2c6eb15f4ebab8e4bf7634c6b9a7.sql) → [008](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/008-8afe57c746fd4367acbf2d22ce260003.sql) → [009](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql) → [010](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0057 · GITHUB_REPOS/query3 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
licenses

licenses."license" = 'apache-2.0'
```

[009](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql) → [010](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0058 · GITHUB_REPOS/query3 · natural · join

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"

FROM "languages" JOIN "licenses" ON languages."repo_name" = licenses."repo_name"
```

[009](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/009-8179d09e20374b64a0f658170aef7447.sql) → [010](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/010-2e111ba678304934b55805397e53ab15.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0059 · GITHUB_REPOS/query3 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
commits

commits."repo_name" IN ('tensorflow/tensorflow', 'apple/swift')
```

[014](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/014-d97fc3bd463547159a3eb5e67f7ae66b.sql) → [015](../../runs/natural/GITHUB_REPOS/query3/full-01/sql/015-8c2c935d46744e8291f00620c81ebc25.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0060 · PANCANCER_ATLAS/query1 · natural · aggregate_mv_extended

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "clinical_info" WHERE 
clinical_info."diagnosis"
clinical_info."patient_description"
COUNT(*)
```

[003](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/003-546fb960098c4868af02b4afe3e0aff6.sql) → [004](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/004-eee66c952d9c4dcdae57499f18016504.sql)

Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.

### ME0061 · PANCANCER_ATLAS/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
clinical_info

clinical_info."patient_description" ILIKE '%lower grade glioma%'
```

[005](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/005-0911b7f14f5e4e76ba6b8ccfde2c8992.sql) → [006](../../runs/natural/PANCANCER_ATLAS/query1/full-01/sql/006-0eb1aa77de8f4859b1d1a4335ab1dbc3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0062 · PANCANCER_ATLAS/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
mutation_data

mutation_data."hugo_symbol" = 'CDH1'
```

[008](../../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/008-464cda910a6b47f88a8a9215ecb00610.sql) → [009](../../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/009-70e1c9ab1adc42f891de9509aefddf8d.sql) → [010](../../runs/natural/PANCANCER_ATLAS/query2/full-01/sql/010-f97a9dc6c955445aab5e99d51a34facb.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0063 · PANCANCER_ATLAS/query3 · natural · aggregate_mv_extended

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "clinical_info" WHERE clinical_info."patient_description" ILIKE '%Breast invasive carcinoma%'
CASE WHEN clinical_info."patient_description" LIKE '%FEMALE%' THEN 'FEMALE' WHEN clinical_info."patient_description" LIKE '%MALE%' THEN 'MALE' ELSE 'UNKNOWN' END
clinical_info."histological_type"
COUNT(*)
```

[005](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/005-6ab3b6aaca974643858a815b39c2cf32.sql) → [006](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/006-7a6409ae1a4e49d6a25fbada077c5230.sql)

Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.

### ME0064 · PANCANCER_ATLAS/query3 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
clinical_info

clinical_info."patient_description" ILIKE '%Breast invasive carcinoma%'
```

[005](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/005-6ab3b6aaca974643858a815b39c2cf32.sql) → [006](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/006-7a6409ae1a4e49d6a25fbada077c5230.sql) → [008](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/008-1f0cd54a021a45e3b2969c67fce770c4.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0065 · PANCANCER_ATLAS/query3 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
mutation_data

mutation_data."hugo_symbol" = 'CDH1'
```

[007](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/007-2131f8f97c9d4b09b2f5b401b9ed561b.sql) → [009](../../runs/natural/PANCANCER_ATLAS/query3/full-01/sql/009-fcaf927c69a242c5aca8c3894b75c3a9.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0066 · PATENTS/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
cpc_definition

cpc_definition."level" = 5
```

[007](../../runs/natural/PATENTS/query1/full-01/sql/007-536111fd0d1249e8a9599126827ff697.sql) → [014](../../runs/natural/PATENTS/query1/full-01/sql/014-7de1a1ef05664a21aeb1cc0a80a1423a.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0067 · PATENTS/query2 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."patents_info" LIKE '% DE-%'
```

[007](../../runs/natural/PATENTS/query2/full-01/sql/007-1fdadd328f4e4cd38767c256e6c22ca0.sql) → [008](../../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0068 · PATENTS/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."grant_date" LIKE '%2019%'
```

[008](../../runs/natural/PATENTS/query2/full-01/sql/008-0eb6d4d4787145299e89e690f8503216.sql) → [014](../../runs/natural/PATENTS/query2/full-01/sql/014-f53248ce62bb4a58a74c036bdb9ec427.sql) → [015](../../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0069 · PATENTS/query2 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
publicationinfo

publicationinfo."patents_info" LIKE '%DE-%'
```

[013](../../runs/natural/PATENTS/query2/full-01/sql/013-e1f4aa9fef1f4c6bad6d18e29df02301.sql) → [014](../../runs/natural/PATENTS/query2/full-01/sql/014-f53248ce62bb4a58a74c036bdb9ec427.sql) → [015](../../runs/natural/PATENTS/query2/full-01/sql/015-54993bf9cc064863aa646ef430d0bb5b.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0070 · bookreview/query2 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
books_info

books_info."categories" LIKE '%Literature & Fiction%'
```

[003](../../runs/natural/bookreview/query2/full-01/sql/003-acbc168cfd0440a1964a2aa049d19c9a.sql) → [004](../../runs/natural/bookreview/query2/full-01/sql/004-bf45e97a9a8a42a2b015542d56e394e6.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0071 · bookreview/query3 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
books_info

books_info."categories" LIKE '%Children''s Books%'
```

[004](../../runs/natural/bookreview/query3/full-01/sql/004-ca59a07d3dd8462f83ad8d8ffd1e481b.sql) → [006](../../runs/natural/bookreview/query3/full-01/sql/006-6cb64f355c544ccf842b3ce8abccb9c9.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0072 · crmarenapro/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
voicecalltranscript__c

voicecalltranscript__c."leadid__c" = '00QWt0000089AekMAE'
```

[001](../../runs/natural/crmarenapro/query1/full-01/sql/001-de67ecc613504a05b9d8f0d949d68ca3.sql) → [003](../../runs/natural/crmarenapro/query1/full-01/sql/003-3782911cf788489a8dbfb88f0ae12ce2.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0073 · crmarenapro/query10 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
casehistory__c

casehistory__c."field__c" = 'Owner Assignment'
```

[007](../../runs/natural/crmarenapro/query10/full-01/sql/007-5d1c770653334d8cb49af843c02e5432.sql) → [008](../../runs/natural/crmarenapro/query10/full-01/sql/008-52c1727e9424487e966229b11f44384b.sql) → [010](../../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0074 · crmarenapro/query10 · natural · derived

使用 3 次，首次后 2 次；仅共享子计算候选。

```
case

SUBSTRING(case."createddate", 1, 19)
```

[008](../../runs/natural/crmarenapro/query10/full-01/sql/008-52c1727e9424487e966229b11f44384b.sql) → [009](../../runs/natural/crmarenapro/query10/full-01/sql/009-17c1c992295c4d209643176f9e518a11.sql) → [010](../../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0075 · crmarenapro/query10 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
case

CAST(SUBSTRING(case."createddate", 1, 19) AS TIMESTAMP) >= CAST('2023-05-02' AS TIMESTAMP)
```

[009](../../runs/natural/crmarenapro/query10/full-01/sql/009-17c1c992295c4d209643176f9e518a11.sql) → [010](../../runs/natural/crmarenapro/query10/full-01/sql/010-b5522c9279d5458e9238ee6507e15347.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0076 · crmarenapro/query12 · natural · filter

使用 3 次，首次后 2 次；仅共享子计算候选。

```
opportunity

opportunity."createddate" >= '2023-04-01'
opportunity."createddate" < '2023-05-01'
```

[002](../../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql) → [005](../../runs/natural/crmarenapro/query12/full-01/sql/005-181d1bc1c63e46a8a5396d55ac0a26e8.sql) → [007](../../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0077 · crmarenapro/query12 · natural · join

使用 3 次，首次后 2 次；仅共享子计算候选。

```
FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"

FROM "opportunity" JOIN "contract" ON opportunity."contractid__c" = contract."id"
```

[002](../../runs/natural/crmarenapro/query12/full-01/sql/002-7be9739b47744297a80f5aa86fd73964.sql) → [003](../../runs/natural/crmarenapro/query12/full-01/sql/003-63d12b98ec8843c685107011d07ebcd8.sql) → [004](../../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0078 · crmarenapro/query12 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
opportunity

opportunity."closedate" >= '2023-04-01'
opportunity."closedate" < '2023-05-01'
```

[004](../../runs/natural/crmarenapro/query12/full-01/sql/004-b7be2280e05a49718b95c110b4f5acac.sql) → [008](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0079 · crmarenapro/query12 · natural · join

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "opportunity" JOIN "contract" ON REPLACE(opportunity."contractid__c", '#', '') = REPLACE(contract."id", '#', '')

FROM "opportunity" JOIN "contract" ON REPLACE(opportunity."contractid__c", '#', '') = REPLACE(contract."id", '#', '')
```

[007](../../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql) → [008](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。

### ME0080 · crmarenapro/query12 · natural · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
opportunity

REPLACE(opportunity."ownerid", '#', '')
REPLACE(opportunity."contractid__c", '#', '')
```

[007](../../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql) → [008](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0081 · crmarenapro/query12 · natural · derived

使用 2 次，首次后 1 次；仅共享子计算候选。

```
contract

REPLACE(contract."id", '#', '')
```

[007](../../runs/natural/crmarenapro/query12/full-01/sql/007-efa00aeb276f495d97268c9e785418aa.sql) → [008](../../runs/natural/crmarenapro/query12/full-01/sql/008-5d507853f8004210b8e44234a7c2f7e3.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0082 · crmarenapro/query4 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
orderitem

orderitem."product2id" = '01tWt000006hVJdIAM'
```

[001](../../runs/natural/crmarenapro/query4/full-01/sql/001-eb3de57c639d46978deb379d8793a12e.sql) → [006](../../runs/natural/crmarenapro/query4/full-01/sql/006-252cd6e35c954309b0354245df4293c5.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0083 · crmarenapro/query4 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
case

case."orderitemid__c" IN ('#802Wt0000078yuGIAQ', '802Wt0000078yuGIAQ', '802Wt00000790mOIAQ', '802Wt00000790zGIAQ', '802Wt00000794F2IAI', '802Wt000007968eIAA', '802Wt00000796bfIAA', '802Wt00000796qFIAQ', '802Wt0000079734IAA', '802Wt00000797W5IAI', '802Wt00000797z7IAA', '802Wt00000798YdIAI', '802Wt00000798okIAA', '802Wt0000079B0EIAU')
```

[004](../../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql) → [008](../../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0084 · crmarenapro/query4 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
case

case."createddate" >= '2020-06-10'
case."createddate" <= '2021-04-10'
```

[004](../../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql) → [005](../../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0085 · crmarenapro/query4 · natural · derived

使用 3 次，首次后 2 次；仅共享子计算候选。

```
case

SUBSTRING(case."createddate", 1, 7)
```

[004](../../runs/natural/crmarenapro/query4/full-01/sql/004-f8d956d9a9e94d278a86634a47f0fdb0.sql) → [005](../../runs/natural/crmarenapro/query4/full-01/sql/005-3d2370b79d6b46d198c8d3be8d95dfe0.sql) → [008](../../runs/natural/crmarenapro/query4/full-01/sql/008-f3773b91c3d44e5b98ffba429e3473e2.sql)

需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。

### ME0086 · crmarenapro/query8 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
casehistory__c

casehistory__c."field__c" = 'Owner Assignment'
```

[003](../../runs/natural/crmarenapro/query8/full-01/sql/003-7712a5339f6445909a124d51013bf46c.sql) → [005](../../runs/natural/crmarenapro/query8/full-01/sql/005-bb3f1da59e0a4cb089c4cc6c6df343a5.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0087 · googlelocal/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
business_description

business_description."description" ILIKE '%Los Angeles%'
```

[004](../../runs/natural/googlelocal/query1/full-01/sql/004-bbb802d64adb44ec99cece581cd449c2.sql) → [005](../../runs/natural/googlelocal/query1/full-01/sql/005-7f46b0bac3874f42a97d94b9e207431f.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0088 · music_brainz_20k/query3 · natural · aggregate_mv_extended

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "sales" WHERE 
sales."track_id"
COUNT(*)
SUM(sales."revenue_usd")
SUM(sales."units_sold")
```

[001](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [003](../../runs/natural/music_brainz_20k/query3/full-01/sql/003-b77bf2b2ae1b49949a8f9249756cb310.sql)

Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.

### ME0089 · music_brainz_20k/query3 · natural · aggregate_state

使用 2 次，首次后 1 次；仅共享子计算候选。

```
FROM "sales"  GROUP BY sales."track_id"

SUM(sales."revenue_usd")
```

[001](../../runs/natural/music_brainz_20k/query3/full-01/sql/001-ca792eef7a5348d6a2d68054fc015eda.sql) → [003](../../runs/natural/music_brainz_20k/query3/full-01/sql/003-b77bf2b2ae1b49949a8f9249756cb310.sql)

基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。

### ME0090 · stockindex/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
index_trade

index_trade."index" IN ('N225', 'NSEI', 'HSI', '000001.SS', '399001.SZ', 'TWII')
```

[006](../../runs/natural/stockindex/query1/full-01/sql/006-a129a6c8aa7b475c8a783013b4c769b3.sql) → [008](../../runs/natural/stockindex/query1/full-01/sql/008-115bbcc37df243ab8f6c8f07d38807b8.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0091 · yelp/query1 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
review

review."business_ref" IN ('businessref_52', 'businessref_84', 'businessref_76', 'businessref_87', 'businessref_65', 'businessref_94', 'businessref_90', 'businessref_16')
```

[003](../../runs/natural/yelp/query1/full-01/sql/003-e1c22f39d383456993f8360526b4b4a7.sql) → [004](../../runs/natural/yelp/query1/full-01/sql/004-f005e6191e5a4b87a6e15842069f443d.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0092 · yelp/query3 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
review

review."date" LIKE '%2018%'
```

[003](../../runs/natural/yelp/query3/full-01/sql/003-99e14da782ee459f828e270dc269acce.sql) → [004](../../runs/natural/yelp/query3/full-01/sql/004-d525231640b442f6936af5cfa84c9ed5.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

### ME0093 · yelp/query7 · natural · filter

使用 2 次，首次后 1 次；仅共享子计算候选。

```
user

user."yelping_since" LIKE '%2016%'
```

[004](../../runs/natural/yelp/query7/full-01/sql/004-5527eb8911ed4a18a539109f67bf45fb.sql) → [006](../../runs/natural/yelp/query7/full-01/sql/006-eb152856605544129147da66dcb425f3.sql)

仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。

