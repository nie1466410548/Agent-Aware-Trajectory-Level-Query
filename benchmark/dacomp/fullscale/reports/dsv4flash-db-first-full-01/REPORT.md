# DAComp-DA：数据库内优先协议下的 Agent 轨迹

计划 100 题，登记 100 题，已开始 100 题，已提交 100 题（其中未截断 98 题、截断提交 2 题）。模型 `glm-custom/DeepSeek-V4-Flash-0731`，OpenCode 1.18.29；全部官方未评分；旧四题独立保留。

数据固定 revision `2cc22149cdfe16cec41851ccae791c2d2c873bb3`；数据库合计 6,132,805,632 字节，中位数 3,745,792 字节，最大 3,524,939,776 字节。逐表实际行数见各题详情与 [数据清单](../../manifests/databases.csv)。

| 状态 | 任务数 |
| --- | --- |
| 已提交 | 100 |


并发调度：4 个任务槽；运行中的轨迹暂不计数，结束后统一审计。串行/并发边界见 state/version_boundaries.jsonl，原始查询耗时可能受并发资源竞争影响。

本批次状态持续由记录生成；提交不等于答案正确。无 FAD 组、无官方模型裁判、无成功率重跑、无金额预算。

## 轨迹有多长

表中 SQL 为尝试/成功，时长为分钟；元数据和连接设置纳入全部 SQL。

| 任务 | 题意节选 | 表数/大小 | 状态 | 全 SQL | 数据 SQL | Python | 时长 | 分析状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [dacomp-001](tasks/dacomp-001.md) | Below are our bank’s collected credit and operating data for small, micro, and medium ente… | 7 / 157.24 MiB | 已提交 | 28/28 | 26/26 | 8 | 3.72 | 已验证候选 |
| [dacomp-002](tasks/dacomp-002.md) | Please analyze the growth trend of Sales Amount for each Major Category from January to Ap… | 1 / 8.97 MiB | 已提交 | 28/28 | 26/26 | 8 | 3.93 | 已验证候选 |
| [dacomp-003](tasks/dacomp-003.md) | I am studying China’s economic development and water use and have obtained the relevant da… | 2 / 0.19 MiB | 已提交 | 26/26 | 24/24 | 6 | 2.79 | 已验证候选 |
| [dacomp-004](tasks/dacomp-004.md) | For each month, determine which product has the highest Sales Amount and provide its corre… | 1 / 8.88 MiB | 已提交 | 19/19 | 17/17 | 4 | 2.46 | 已验证候选 |
| [dacomp-005](tasks/dacomp-005.md) | Orders whose `Profit Margin` in `sheet1` is lower than 50% of the dataset average are defi… | 1 / 7.16 MiB | 已提交 | 38/38 | 36/36 | 5 | 4.52 | 已验证候选 |
| [dacomp-006](tasks/dacomp-006.md) | The monthly total profit in South China is very unstable. Which aspects are causing the in… | 1 / 7.16 MiB | 已提交 | 54/51 | 52/49 | 4 | 4.8 | 已验证候选 |
| [dacomp-007](tasks/dacomp-007.md) | The Research & Development (R&D) department’s employee attrition rate is significantly low… | 1 / 0.48 MiB | 已提交 | 43/43 | 41/41 | 13 | 4.97 | 已验证候选 |
| [dacomp-008](tasks/dacomp-008.md) | Analyze the average cost deviation (Budget Amount − Actual Cost) and its distribution acro… | 1 / 0.11 MiB | 已提交 | 27/27 | 25/25 | 6 | 3.15 | 已验证候选 |
| [dacomp-009](tasks/dacomp-009.md) | If we produce an integrated ranking that considers Effective Working Hours, overall Units … | 6 / 0.95 MiB | 已提交 | 36/36 | 34/34 | 8 | 5.39 | 已验证候选 |
| [dacomp-010](tasks/dacomp-010.md) | Compare the 2024 seasonal trends in Sales Quantity (units) across agricultural product cat… | 3 / 0.38 MiB | 已提交 | 33/33 | 31/31 | 4 | 3.06 | 已验证候选 |
| [dacomp-011](tasks/dacomp-011.md) | Some people believe that the higher the parents' level of education, the better their chil… | 1 / 0.19 MiB | 已提交 | 30/27 | 28/25 | 4 | 2.22 | 已验证候选 |
| [dacomp-012](tasks/dacomp-012.md) | Analyze the trend of diamond price per carat across different carat intervals (e.g., <=0.5… | 1 / 7.17 MiB | 已提交 | 22/20 | 20/18 | 4 | 7.44 | 已验证候选 |
| [dacomp-013](tasks/dacomp-013.md) | Develop a fair and reasonable performance evaluation plan for Task Owners across different… | 1 / 0.22 MiB | 已提交 | 37/37 | 35/35 | 24 | 7.49 | 已验证候选 |
| [dacomp-014](tasks/dacomp-014.md) | I'm just starting out as a video creator. Please analyze the data from the monthly ranking… | 1 / 2.88 MiB | 已提交 | 51/51 | 49/49 | 15 | 5.1 | 已验证候选 |
| [dacomp-015](tasks/dacomp-015.md) | Based on Floor Plan, Decoration, Floor, and Orientation, analyze which combinations of hom… | 1 / 11.48 MiB | 已提交 | 29/29 | 27/27 | 9 | 3.82 | 已验证候选 |
| [dacomp-016](tasks/dacomp-016.md) | Using the `sheet1` table, compute and describe the trend in the ratio of `Surface Water Su… | 2 / 0.19 MiB | 已提交 | 17/17 | 15/15 | 3 | 2.7 | 已验证候选 |
| [dacomp-017](tasks/dacomp-017.md) | Using the metrics in `order_information`, analyze how the annual profit margin for each `P… | 3 / 27.07 MiB | 已提交 | 71/71 | 69/69 | 13 | 6.89 | 已验证候选 |
| [dacomp-018](tasks/dacomp-018.md) | I am a merchant in the Fashion category. Based on the e-commerce platform data provided to… | 3 / 27.07 MiB | 已提交 | 58/57 | 56/55 | 5 | 3.97 | 已验证候选 |
| [dacomp-019](tasks/dacomp-019.md) | Analyze, from the perspectives of inventory backlog, supply interruption, and risk of qual… | 3 / 0.48 MiB | 已提交 | 41/40 | 39/38 | 12 | 3.81 | 已验证候选 |
| [dacomp-020](tasks/dacomp-020.md) | Analyze the dataset in `sheet1` to answer the following three questions: (1) What is the o… | 1 / 0.19 MiB | 已提交 | 18/17 | 16/15 | 15 | 5.02 | 已验证候选 |
| [dacomp-021](tasks/dacomp-021.md) | Across the full year 2024, do ride bookings exhibit "peaks and troughs" (specific times of… | 1 / 44.07 MiB | 已提交 | 33/31 | 31/29 | 4 | 3.74 | 已验证候选 |
| [dacomp-022](tasks/dacomp-022.md) | I am a ride-hailing driver. Based on the platform’s 2024 data, please help me take a look … | 1 / 44.07 MiB | 已提交 | 65/61 | 63/59 | 4 | 5.85 | 已验证候选 |
| [dacomp-023](tasks/dacomp-023.md) | Analyze the sales trends from 2015 to 2018 for the three categories—Office Supplies, Techn… | 3 / 4.53 MiB | 已提交 | 37/37 | 35/35 | 5 | 3.22 | 已验证候选 |
| [dacomp-024](tasks/dacomp-024.md) | Compare the business performance of the four regions (Central, East, South, West), analyze… | 2 / 4.81 MiB | 已提交 | 25/24 | 23/22 | 3 | 3.82 | 已验证候选 |
| [dacomp-025](tasks/dacomp-025.md) | To increase total revenue, the supermarket needs to avoid loss-making sales as much as pos… | 4 / 128.82 MiB | 已提交 | 78/77 | 76/75 | 7 | 14.65 | 已验证候选 |
| [dacomp-026](tasks/dacomp-026.md) | For the Level 5 disasters in the `disaster_events` table, identify the relevant records an… | 10 / 3.52 MiB | 已提交 | 61/61 | 59/59 | 6 | 4.59 | 已验证候选 |
| [dacomp-027](tasks/dacomp-027.md) | Across disaster events at different global Disaster Levels, analyze how secondary or casca… | 10 / 3.52 MiB | 已提交 | 38/38 | 36/36 | 9 | 4.06 | 已验证候选 |
| [dacomp-028](tasks/dacomp-028.md) | What are the month-over-month growth trends of Average Price for each Product Category acr… | 1 / 0.29 MiB | 已提交 | 30/30 | 28/28 | 10 | 4.37 | 已验证候选 |
| [dacomp-029](tasks/dacomp-029.md) | I am a used car dealer. Based on the data in this table, analyze which models or configura… | 1 / 0.46 MiB | 已提交 | 52/51 | 50/49 | 8 | 6.7 | 已验证候选 |
| [dacomp-030](tasks/dacomp-030.md) | As Coca-Cola’s sales lead, which Outlet Types should I increase or reduce the contract sig… | 16 / 1.97 MiB | 已提交 | 38/37 | 32/31 | 3 | 3.7 | 有候选待验证/受限或已拒绝 |
| [dacomp-031](tasks/dacomp-031.md) | Analyze employees’ current employment status at the company across different working years… | 1 / 0.48 MiB | 已提交 | 40/39 | 38/37 | 2 | 3.48 | 已验证候选 |
| [dacomp-032](tasks/dacomp-032.md) | For customers whose `Contact priority` equals 1 in `customer_contact_table`, analyze how e… | 19 / 2.34 MiB | 已提交 | 59/58 | 54/53 | 5 | 4.07 | 已验证候选 |
| [dacomp-033](tasks/dacomp-033.md) | For customers with completed high-amount transaction behavior (cumulative over 5000), help… | 19 / 2.34 MiB | 已提交（截断） | 122/117 | 120/115 | 1 | 4.8 | 已验证候选 |
| [dacomp-034](tasks/dacomp-034.md) | At the Level 1 Category level, analyze the relationship between discount depth and sales f… | 7 / 333.31 MiB | 已提交 | 35/34 | 33/32 | 13 | 4.65 | 已验证候选 |
| [dacomp-035](tasks/dacomp-035.md) | The company is conducting a special initiative on office system security governance. Based… | 12 / 1.7 MiB | 已提交 | 82/82 | 80/80 | 5 | 4.4 | 已验证候选 |
| [dacomp-036](tasks/dacomp-036.md) | Analyze the weak points present in 2024 scenarios that combine different Login Methods and… | 12 / 1.7 MiB | 已提交 | 40/40 | 38/38 | 2 | 2.82 | 已验证候选 |
| [dacomp-037](tasks/dacomp-037.md) | I want to understand what differences exist in health checkup data between people with a m… | 2 / 2.73 MiB | 已提交 | 37/36 | 35/34 | 10 | 3.34 | 已验证候选 |
| [dacomp-038](tasks/dacomp-038.md) | Starting from July 5, we gray-released a new version of strategies such as Search Strategy… | 2 / 0.26 MiB | 已提交 | 37/37 | 35/35 | 7 | 6.2 | 已验证候选 |
| [dacomp-039](tasks/dacomp-039.md) | For levels launched in 2024, compare how Churn Rate and Level Rating change across combina… | 1 / 1.56 MiB | 已提交 | 29/27 | 27/25 | 9 | 3.86 | 已验证候选 |
| [dacomp-040](tasks/dacomp-040.md) | Based on the data for 2000, 2010, and 2020 in the tables, analyze from perspectives such a… | 24 / 0.34 MiB | 已提交 | 62/58 | 59/55 | 11 | 6.46 | 已验证候选 |
| [dacomp-041](tasks/dacomp-041.md) | Please, for Exhibition Halls with an average Daily Visitor Count exceeding 900, conduct a … | 14 / 3.35 MiB | 已提交 | 37/33 | 35/31 | 23 | 11.8 | 已验证候选 |
| [dacomp-042](tasks/dacomp-042.md) | Compare and analyze how the primary barrier factors to treatment adherence differ across p… | 9 / 2.41 MiB | 已提交 | 60/60 | 58/58 | 5 | 4.89 | 已验证候选 |
| [dacomp-043](tasks/dacomp-043.md) | To clarify the factors associated with the high case fatality rate of Hand, Foot, and Mout… | 10 / 0.92 MiB | 已提交 | 91/91 | 89/89 | 6 | 6.25 | 已验证候选 |
| [dacomp-044](tasks/dacomp-044.md) | Please summarize the health education campaign formats and locations for students that are… | 10 / 1.54 MiB | 已提交 | 32/32 | 30/30 | 5 | 3.35 | 已验证候选 |
| [dacomp-045](tasks/dacomp-045.md) | To enhance user stickiness and overall revenue, analyze and compare high-value users (Diam… | 8 / 1.04 MiB | 已提交 | 37/37 | 35/35 | 2 | 4.08 | 已验证候选 |
| [dacomp-046](tasks/dacomp-046.md) | Analyze the marketing characteristics of user groups across different age segments (churn … | 6 / 0.59 MiB | 已提交 | 68/67 | 66/65 | 9 | 5.08 | 已验证候选 |
| [dacomp-047](tasks/dacomp-047.md) | To adjust replenishment decisions, based on the interrelationships between vegetable categ… | 4 / 128.82 MiB | 已提交 | 57/56 | 55/54 | 10 | 11.13 | 已验证候选 |
| [dacomp-048](tasks/dacomp-048.md) | Please separately compute the starting salary distribution and the benefits distribution f… | 1 / 303.1 MiB | 已提交 | 37/37 | 35/35 | 10 | 5.29 | 已验证候选 |
| [dacomp-049](tasks/dacomp-049.md) | I am an HR professional in the insurance industry. I plan to conduct a competitiveness eva… | 1 / 303.1 MiB | 已提交 | 19/18 | 17/16 | 13 | 4.97 | 已验证候选 |
| [dacomp-050](tasks/dacomp-050.md) | Within the student group, what are the characteristics of those who have had suicidal thou… | 1 / 19.68 MiB | 已提交 | 32/32 | 30/30 | 16 | 5.27 | 已验证候选 |
| [dacomp-051](tasks/dacomp-051.md) | The company needs to analyze the reasons behind the decline in project delivery efficiency… | 2 / 1.79 MiB | 已提交 | 53/53 | 51/51 | 9 | 5.31 | 已验证候选 |
| [dacomp-052](tasks/dacomp-052.md) | Noticing that some teams have high project health scores but low actual completion rates, … | 1 / 0.02 MiB | 已提交 | 27/27 | 25/25 | 2 | 3.2 | 已验证候选 |
| [dacomp-053](tasks/dacomp-053.md) | We've observed a peculiar phenomenon in our company's project management: some seemingly h… | 1 / 0.25 MiB | 已提交 | 50/50 | 48/48 | 5 | 4.54 | 已验证候选 |
| [dacomp-054](tasks/dacomp-054.md) | We have identified a group of customers exhibiting specific conversion behaviors: their `m… | 4 / 211.05 MiB | 已提交 | 96/93 | 93/90 | 14 | 7.66 | 已验证候选 |
| [dacomp-055](tasks/dacomp-055.md) | The company is reassessing its customer investment strategy and needs to identify customer… | 3 / 50.88 MiB | 已提交 | 72/62 | 70/60 | 17 | 9.49 | 已验证候选 |
| [dacomp-056](tasks/dacomp-056.md) | The data team has identified a paradoxical phenomenon among high-value enterprise customer… | 3 / 2.01 MiB | 已提交 | 35/34 | 33/32 | 13 | 5.9 | 已验证候选 |
| [dacomp-057](tasks/dacomp-057.md) | The marketing team has observed complex decay patterns in the customer acquisition efficie… | 2 / 6.36 MiB | 已提交 | 74/71 | 70/67 | 7 | 10.26 | 已验证候选 |
| [dacomp-058](tasks/dacomp-058.md) | Upon discovering a severe imbalance between input and output in some high-cost campaigns, … | 7 / 0.93 MiB | 已提交 | 58/57 | 56/55 | 18 | 8.11 | 已验证候选 |
| [dacomp-059](tasks/dacomp-059.md) | In a recent analysis of ad performance, an anomaly was discovered where some ad groups exh… | 2 / 4.92 MiB | 已提交 | 58/58 | 56/56 | 16 | 8.18 | 已验证候选 |
| [dacomp-060](tasks/dacomp-060.md) | It has been observed that some ad groups exhibit a high Click-Through Rate (CTR) but a low… | 6 / 12.33 MiB | 已提交 | 22/22 | 20/20 | 13 | 4.89 | 已验证候选 |
| [dacomp-061](tasks/dacomp-061.md) | A peculiar phenomenon has been observed recently: some projects have a very short `avg_clo… | 3 / 3361.64 MiB | 已提交 | 53/53 | 51/51 | 5 | 9.57 | 已验证候选 |
| [dacomp-062](tasks/dacomp-062.md) | I want to understand the effectiveness of our cross-functional collaboration. Please analy… | 2 / 0.96 MiB | 已提交 | 33/31 | 30/28 | 5 | 4.11 | 已验证候选 |
| [dacomp-063](tasks/dacomp-063.md) | The Project Management Committee has observed a perplexing phenomenon: certain projects ex… | 3 / 1.77 MiB | 已提交 | 77/76 | 74/73 | 6 | 6.64 | 已验证候选 |
| [dacomp-064](tasks/dacomp-064.md) | In the project delivery cycle of the last 6 months, we have observed that certain key stak… | 5 / 14.01 MiB | 已提交 | 67/66 | 65/64 | 8 | 5.55 | 已验证候选 |
| [dacomp-065](tasks/dacomp-065.md) | Our CEO claims that candidates from well-known tech companies (e.g., FAANG, unicorns) perf… | 2 / 24.0 MiB | 已提交 | 62/60 | 60/58 | 5 | 5.65 | 已验证候选 |
| [dacomp-066](tasks/dacomp-066.md) | The application screening to first interview conversion rate for the company's Engineering… | 2 / 0.08 MiB | 已提交 | 44/44 | 42/42 | 7 | 3.98 | 已验证候选 |
| [dacomp-067](tasks/dacomp-067.md) | The company's CEO has tasked the Human Resources department with developing a comprehensiv… | 7 / 25.68 MiB | 已提交 | 91/90 | 89/88 | 9 | 6.65 | 已验证候选 |
| [dacomp-068](tasks/dacomp-068.md) | The finance department has allocated a Q4 marketing budget of $5,000,000, which needs to b… | 3 / 2.39 MiB | 已提交 | 41/40 | 38/37 | 8 | 7.04 | 已验证候选 |
| [dacomp-069](tasks/dacomp-069.md) | ### Capital Efficiency Issue for a High-Priority Investment Application  The CFO is concer… | 4 / 3.62 MiB | 已提交 | 46/45 | 44/43 | 5 | 6.29 | 已验证候选 |
| [dacomp-070](tasks/dacomp-070.md) | Analyze the decay patterns of user acquisition cost-efficiency for each region and device … | 4 / 6.11 MiB | 已提交 | 25/25 | 23/23 | 11 | 5.36 | 已验证候选 |
| [dacomp-071](tasks/dacomp-071.md) | Management is concerned about our hiring funnel efficiency and wants to know which stages … | 2 / 6.18 MiB | 已提交 | 38/38 | 36/36 | 19 | 6.07 | 已验证候选 |
| [dacomp-072](tasks/dacomp-072.md) | We want to establish a data-driven performance evaluation system for hiring managers. Plea… | 1 / 0.12 MiB | 已提交 | 18/18 | 16/16 | 3 | 2.2 | 已验证候选 |
| [dacomp-073](tasks/dacomp-073.md) | Given the rapid business growth, we need to forecast future hiring demand and resource all… | 2 / 0.59 MiB | 已提交 | 97/94 | 95/92 | 8 | 9.79 | 已验证候选 |
| [dacomp-074](tasks/dacomp-074.md) | The CFO wants to build a more accurate cash flow forecasting model. Analyze the historical… | 2 / 0.29 MiB | 已提交 | 26/26 | 24/24 | 9 | 6.3 | 已验证候选 |
| [dacomp-075](tasks/dacomp-075.md) | In the context of increasing uncertainty in the current global supply chain, our company i… | 1 / 0.06 MiB | 已提交 | 29/29 | 27/27 | 8 | 4.74 | 已验证候选 |
| [dacomp-076](tasks/dacomp-076.md) | We need to re-examine the effectiveness of our customer segmentation strategy. Please anal… | 1 / 0.05 MiB | 已提交 | 23/23 | 21/21 | 12 | 5.8 | 已验证候选 |
| [dacomp-077](tasks/dacomp-077.md) | The product team's statistics show that we have 180 different features, but on average, a … | 7 / 7.91 MiB | 已提交 | 45/41 | 43/39 | 6 | 11.81 | 已验证候选 |
| [dacomp-078](tasks/dacomp-078.md) | The existing customer value scoring model primarily relies on two dimensions, usage durati… | 5 / 17.03 MiB | 已提交 | 50/48 | 48/46 | 28 | 9.03 | 已验证候选 |
| [dacomp-079](tasks/dacomp-079.md) | We have observed that the proportion of users with more than 60 active days but who have c… | 4 / 10.34 MiB | 已提交 | 38/37 | 32/31 | 7 | 6.38 | 已验证候选 |
| [dacomp-080](tasks/dacomp-080.md) | We've observed a clear stratification of engagement among our user base, especially noting… | 4 / 36.82 MiB | 已提交 | 37/37 | 35/35 | 13 | 6.42 | 已验证候选 |
| [dacomp-081](tasks/dacomp-081.md) | Capital efficiency issue for high-investment priority applications. The CFO is concerned a… | 3 / 33.84 MiB | 已提交（截断） | 122/121 | 120/119 | 7 | 9.93 | 已验证候选 |
| [dacomp-082](tasks/dacomp-082.md) | We are re-evaluating the return on investment (ROI) for each distribution channel but have… | 3 / 4.08 MiB | 已提交 | 38/36 | 36/34 | 6 | 8.49 | 已验证候选 |
| [dacomp-083](tasks/dacomp-083.md) | I need you to build a comprehensive employee value and risk assessment system to support t… | 1 / 87.45 MiB | 已提交 | 65/64 | 63/62 | 2 | 6.37 | 已验证候选 |
| [dacomp-084](tasks/dacomp-084.md) | The company is redesigning its organizational structure, and I want you to identify the op… | 2 / 0.11 MiB | 已提交 | 36/34 | 34/32 | 9 | 4.55 | 已验证候选 |
| [dacomp-085](tasks/dacomp-085.md) | In light of business adjustments, we need to re-evaluate the true value of each job profil… | 3 / 87.78 MiB | 已提交 | 17/17 | 15/15 | 11 | 4.5 | 已验证候选 |
| [dacomp-086](tasks/dacomp-086.md) | We need to build a customer health score model to predict churn risk and formulate operati… | 4 / 31.56 MiB | 已提交 | 18/17 | 16/15 | 11 | 4.48 | 已验证候选 |
| [dacomp-087](tasks/dacomp-087.md) | A sales team reorganization is imminent, requiring the design of a data-driven customer re… | 7 / 52.52 MiB | 已提交 | 22/22 | 20/20 | 14 | 11.11 | 已验证候选; original verified selection retained across continuation |
| [dacomp-088](tasks/dacomp-088.md) | The Marketing Department is questioning the ROI efficiency of our investments in different… | 5 / 13.14 MiB | 已提交 | 75/75 | 73/73 | 8 | 5.19 | 已验证候选 |
| [dacomp-089](tasks/dacomp-089.md) | We need to establish a contact configuration risk monitoring system for our key accounts, … | 2 / 17.9 MiB | 已提交 | 43/43 | 41/41 | 14 | 6.85 | 已验证候选 |
| [dacomp-090](tasks/dacomp-090.md) | We have observed that the payment behavior of some customers is deteriorating. Please filt… | 4 / 4.05 MiB | 已提交 | 46/45 | 44/43 | 2 | 3.72 | 已验证候选 |
| [dacomp-091](tasks/dacomp-091.md) | From the `quickbooks__vendor_performance` table, identify 'high-quality, shrinking-spend' … | 3 / 19.5 MiB | 已提交 | 39/37 | 36/34 | 6 | 4.88 | 已验证候选; original verified selection retained across continuation |
| [dacomp-092](tasks/dacomp-092.md) | First, from the `profitability_analysis` table, identify the high-volatility customer segm… | 4 / 28.35 MiB | 已提交 | 70/68 | 67/65 | 5 | 7.72 | 已验证候选; original verified selection retained across continuation |
| [dacomp-093](tasks/dacomp-093.md) | Using behavioral data from klaviyo__campaigns and klaviyo__persons, design an analysis on … | 2 / 0.67 MiB | 已提交 | 41/40 | 38/37 | 5 | 5.22 | 已验证候选; original verified selection retained across continuation |
| [dacomp-094](tasks/dacomp-094.md) | Based on the behavioral data from `klaviyo__campaigns` and `klaviyo__persons`, design an a… | 3 / 0.48 MiB | 已提交 | 22/18 | 20/16 | 3 | 3.84 | 已验证候选 |
| [dacomp-095](tasks/dacomp-095.md) | Based on `klaviyo__persons`, `klaviyo__person_campaign_flow`, and `marts.klaviyo__events`,… | 4 / 0.57 MiB | 已提交 | 60/55 | 57/52 | 3 | 5.97 | 已验证候选 |
| [dacomp-096](tasks/dacomp-096.md) | Based on `klaviyo__campaigns` (with columns like `STATUS`/`STATUS_ID`, `SENT_AT`, `schedul… | 2 / 0.03 MiB | 已提交 | 24/24 | 22/22 | 9 | 4.26 | 已验证候选 |
| [dacomp-097](tasks/dacomp-097.md) | Using conversation, user profile, and usage event data from the past six months, compare t… | 5 / 10.62 MiB | 已提交 | 113/110 | 108/106 | 5 | 9.42 | 已验证候选 |
| [dacomp-098](tasks/dacomp-098.md) | Evaluate the impact of a bot-led first response strategy on various stages of the sales fu… | 5 / 10.04 MiB | 已提交 | 47/45 | 44/42 | 12 | 6.85 | 已验证候选 |
| [dacomp-099](tasks/dacomp-099.md) | Identify the key factors that lead customers to upgrade or downgrade. On a per-customer ba… | 4 / 8.56 MiB | 已提交 | 74/72 | 72/70 | 15 | 9.55 | 已验证候选 |
| [dacomp-100](tasks/dacomp-100.md) | For customers whose contracts are due for renewal within the next 90 days, build a renewal… | 4 / 11.41 MiB | 已提交 | 78/73 | 76/71 | 30 | 11.39 | 已验证候选 |


已提交且未截断：n=98；成功数据 SQL 均值 42.22，中位数 36.0，P25/P75/P90 27.25/55.00/70.30，范围 15–106。

已结束但截断/失败：n=2；成功数据 SQL 均值 117.00，中位数 117.0，P25/P75/P90 116.00/118.00/118.60，范围 115–119。

全批次当前记录：SQL 尝试 4711，其中数据 4485、元数据 122、连接设置 103、维护 0、未知类别 1；SQL 成功 4597、失败 111、取消 3、结果受限 0。Python 866 次，其中 666 次成功；使用 Python 的已开始任务 100/100。

执行位置审查按已结束任务列出；含违例的轨迹继续保留，不能混称严格符合数据库内优先协议。

| Python 执行位置审查状态 | 任务数 |
| --- | --- |
| database_first_partial_violation | 2 |
| database_first_violation | 74 |
| partial_violation | 11 |
| reviewed_SQL_dominant_with_chart_arithmetic | 1 |
| reviewed_SQL_dominant_with_chart_preparation_exceptions | 1 |
| reviewed_SQL_dominant_with_plot_preparation | 1 |
| reviewed_SQL_dominant_with_statistical_and_chart_exceptions | 3 |
| reviewed_SQL_dominant_with_statistical_model_preprocessing | 1 |
| reviewed_with_statistical_exceptions_and_SQL_capable_preparation | 1 |
| reviewed_with_statistical_exceptions_and_SQL_capable_summaries | 4 |
| reviewed_with_statistical_plotting_exceptions | 1 |


## SQL 具体在做什么

以下以成功数据 SQL 为分母；解析失败单列，不能把多表访问自动当成 Join。

| 任务 | 数据 SQL | 单表 | 多表 | 含 Join | 2 输入 | 3 输入 | ≥4 输入 | 未解析 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [dacomp-001](tasks/dacomp-001.md) | 26 | 18 | 8 | 8 | 5 | 1 | 2 | 0 |
| [dacomp-002](tasks/dacomp-002.md) | 26 | 26 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-003](tasks/dacomp-003.md) | 24 | 11 | 13 | 13 | 13 | 0 | 0 | 0 |
| [dacomp-004](tasks/dacomp-004.md) | 17 | 17 | 0 | 6 | 6 | 0 | 0 | 0 |
| [dacomp-005](tasks/dacomp-005.md) | 36 | 36 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-006](tasks/dacomp-006.md) | 49 | 49 | 0 | 5 | 5 | 0 | 0 | 0 |
| [dacomp-007](tasks/dacomp-007.md) | 41 | 41 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-008](tasks/dacomp-008.md) | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-009](tasks/dacomp-009.md) | 34 | 15 | 19 | 4 | 4 | 0 | 0 | 0 |
| [dacomp-010](tasks/dacomp-010.md) | 31 | 9 | 22 | 22 | 7 | 15 | 0 | 0 |
| [dacomp-011](tasks/dacomp-011.md) | 25 | 25 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-012](tasks/dacomp-012.md) | 18 | 18 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-013](tasks/dacomp-013.md) | 35 | 35 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-014](tasks/dacomp-014.md) | 49 | 49 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-015](tasks/dacomp-015.md) | 27 | 27 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-016](tasks/dacomp-016.md) | 15 | 13 | 2 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-017](tasks/dacomp-017.md) | 69 | 69 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-018](tasks/dacomp-018.md) | 55 | 21 | 29 | 29 | 29 | 0 | 0 | 5 |
| [dacomp-019](tasks/dacomp-019.md) | 38 | 17 | 21 | 21 | 20 | 1 | 0 | 0 |
| [dacomp-020](tasks/dacomp-020.md) | 15 | 15 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-021](tasks/dacomp-021.md) | 29 | 29 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-022](tasks/dacomp-022.md) | 59 | 58 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-023](tasks/dacomp-023.md) | 35 | 16 | 19 | 20 | 16 | 4 | 0 | 0 |
| [dacomp-024](tasks/dacomp-024.md) | 22 | 6 | 16 | 16 | 16 | 0 | 0 | 0 |
| [dacomp-025](tasks/dacomp-025.md) | 75 | 41 | 34 | 34 | 6 | 10 | 18 | 0 |
| [dacomp-026](tasks/dacomp-026.md) | 59 | 20 | 39 | 38 | 26 | 5 | 7 | 0 |
| [dacomp-027](tasks/dacomp-027.md) | 36 | 20 | 16 | 15 | 8 | 4 | 3 | 0 |
| [dacomp-028](tasks/dacomp-028.md) | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-029](tasks/dacomp-029.md) | 49 | 49 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-030](tasks/dacomp-030.md) | 31 | 16 | 15 | 14 | 12 | 0 | 2 | 0 |
| [dacomp-031](tasks/dacomp-031.md) | 37 | 37 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-032](tasks/dacomp-032.md) | 53 | 12 | 41 | 38 | 2 | 28 | 8 | 0 |
| [dacomp-033](tasks/dacomp-033.md) | 115 | 67 | 48 | 49 | 41 | 7 | 1 | 0 |
| [dacomp-034](tasks/dacomp-034.md) | 32 | 23 | 9 | 7 | 7 | 0 | 0 | 0 |
| [dacomp-035](tasks/dacomp-035.md) | 80 | 23 | 57 | 57 | 20 | 37 | 0 | 0 |
| [dacomp-036](tasks/dacomp-036.md) | 38 | 17 | 21 | 21 | 13 | 7 | 1 | 0 |
| [dacomp-037](tasks/dacomp-037.md) | 34 | 14 | 20 | 20 | 20 | 0 | 0 | 0 |
| [dacomp-038](tasks/dacomp-038.md) | 35 | 35 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-039](tasks/dacomp-039.md) | 25 | 25 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-040](tasks/dacomp-040.md) | 55 | 49 | 6 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-041](tasks/dacomp-041.md) | 31 | 19 | 12 | 12 | 6 | 2 | 4 | 0 |
| [dacomp-042](tasks/dacomp-042.md) | 58 | 21 | 37 | 37 | 3 | 0 | 34 | 0 |
| [dacomp-043](tasks/dacomp-043.md) | 89 | 47 | 42 | 60 | 60 | 0 | 0 | 0 |
| [dacomp-044](tasks/dacomp-044.md) | 30 | 30 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-045](tasks/dacomp-045.md) | 35 | 21 | 14 | 20 | 14 | 6 | 0 | 0 |
| [dacomp-046](tasks/dacomp-046.md) | 65 | 30 | 35 | 35 | 31 | 4 | 0 | 0 |
| [dacomp-047](tasks/dacomp-047.md) | 54 | 10 | 44 | 44 | 43 | 1 | 0 | 0 |
| [dacomp-048](tasks/dacomp-048.md) | 35 | 35 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-049](tasks/dacomp-049.md) | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-050](tasks/dacomp-050.md) | 30 | 30 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-051](tasks/dacomp-051.md) | 51 | 14 | 37 | 38 | 38 | 0 | 0 | 0 |
| [dacomp-052](tasks/dacomp-052.md) | 25 | 25 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-053](tasks/dacomp-053.md) | 48 | 48 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-054](tasks/dacomp-054.md) | 90 | 71 | 19 | 19 | 3 | 16 | 0 | 0 |
| [dacomp-055](tasks/dacomp-055.md) | 60 | 40 | 20 | 19 | 19 | 0 | 0 | 0 |
| [dacomp-056](tasks/dacomp-056.md) | 32 | 31 | 1 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-057](tasks/dacomp-057.md) | 67 | 54 | 13 | 14 | 14 | 0 | 0 | 0 |
| [dacomp-058](tasks/dacomp-058.md) | 55 | 53 | 2 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-059](tasks/dacomp-059.md) | 56 | 53 | 3 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-060](tasks/dacomp-060.md) | 20 | 17 | 3 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-061](tasks/dacomp-061.md) | 51 | 50 | 1 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-062](tasks/dacomp-062.md) | 28 | 28 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-063](tasks/dacomp-063.md) | 73 | 67 | 6 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-064](tasks/dacomp-064.md) | 64 | 43 | 21 | 21 | 18 | 3 | 0 | 0 |
| [dacomp-065](tasks/dacomp-065.md) | 58 | 45 | 13 | 18 | 18 | 0 | 0 | 0 |
| [dacomp-066](tasks/dacomp-066.md) | 42 | 31 | 11 | 11 | 11 | 0 | 0 | 0 |
| [dacomp-067](tasks/dacomp-067.md) | 88 | 79 | 9 | 7 | 7 | 0 | 0 | 0 |
| [dacomp-068](tasks/dacomp-068.md) | 37 | 37 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-069](tasks/dacomp-069.md) | 43 | 43 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-070](tasks/dacomp-070.md) | 23 | 17 | 6 | 6 | 6 | 0 | 0 | 0 |
| [dacomp-071](tasks/dacomp-071.md) | 36 | 36 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-072](tasks/dacomp-072.md) | 16 | 16 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-073](tasks/dacomp-073.md) | 92 | 78 | 14 | 9 | 9 | 0 | 0 | 0 |
| [dacomp-074](tasks/dacomp-074.md) | 24 | 23 | 1 | 1 | 0 | 1 | 0 | 0 |
| [dacomp-075](tasks/dacomp-075.md) | 27 | 27 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-076](tasks/dacomp-076.md) | 21 | 21 | 0 | 6 | 6 | 0 | 0 | 0 |
| [dacomp-077](tasks/dacomp-077.md) | 39 | 23 | 16 | 15 | 11 | 4 | 0 | 0 |
| [dacomp-078](tasks/dacomp-078.md) | 46 | 33 | 13 | 12 | 11 | 1 | 0 | 0 |
| [dacomp-079](tasks/dacomp-079.md) | 31 | 8 | 23 | 21 | 13 | 8 | 0 | 0 |
| [dacomp-080](tasks/dacomp-080.md) | 35 | 34 | 1 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-081](tasks/dacomp-081.md) | 119 | 114 | 5 | 5 | 5 | 0 | 0 | 0 |
| [dacomp-082](tasks/dacomp-082.md) | 34 | 34 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-083](tasks/dacomp-083.md) | 62 | 62 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-084](tasks/dacomp-084.md) | 32 | 32 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-085](tasks/dacomp-085.md) | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-086](tasks/dacomp-086.md) | 15 | 15 | 0 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-087](tasks/dacomp-087.md) | 20 | 17 | 3 | 5 | 2 | 2 | 1 | 0 |
| [dacomp-088](tasks/dacomp-088.md) | 73 | 68 | 5 | 5 | 5 | 0 | 0 | 0 |
| [dacomp-089](tasks/dacomp-089.md) | 41 | 31 | 10 | 2 | 2 | 0 | 0 | 0 |
| [dacomp-090](tasks/dacomp-090.md) | 43 | 37 | 6 | 6 | 6 | 0 | 0 | 0 |
| [dacomp-091](tasks/dacomp-091.md) | 34 | 23 | 11 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-092](tasks/dacomp-092.md) | 65 | 51 | 14 | 26 | 25 | 1 | 0 | 0 |
| [dacomp-093](tasks/dacomp-093.md) | 37 | 36 | 1 | 0 | 0 | 0 | 0 | 0 |
| [dacomp-094](tasks/dacomp-094.md) | 16 | 15 | 1 | 1 | 0 | 1 | 0 | 0 |
| [dacomp-095](tasks/dacomp-095.md) | 52 | 50 | 2 | 3 | 3 | 0 | 0 | 0 |
| [dacomp-096](tasks/dacomp-096.md) | 22 | 22 | 0 | 1 | 1 | 0 | 0 | 0 |
| [dacomp-097](tasks/dacomp-097.md) | 106 | 61 | 45 | 40 | 35 | 5 | 0 | 0 |
| [dacomp-098](tasks/dacomp-098.md) | 42 | 31 | 11 | 11 | 10 | 1 | 0 | 0 |
| [dacomp-099](tasks/dacomp-099.md) | 70 | 50 | 20 | 14 | 9 | 5 | 0 | 0 |
| [dacomp-100](tasks/dacomp-100.md) | 71 | 71 | 0 | 0 | 0 | 0 | 0 | 0 |


| 任务 | 含 GROUP BY | 1 维 | 2 维 | 3 维 | ≥4 维 | 含聚合 | 函数 SQL 数 | 含窗口 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [dacomp-001](tasks/dacomp-001.md) | 13 | 7 | 6 | 0 | 0 | 17 | {"COUNT": 11, "SUM": 10, "MIN": 3, "MAX": 7, "AVG": 1} | 0 |
| [dacomp-002](tasks/dacomp-002.md) | 21 | 11 | 8 | 2 | 0 | 22 | {"COUNT": 16, "MIN": 3, "MAX": 3, "SUM": 16, "AVG": 1} | 1 |
| [dacomp-003](tasks/dacomp-003.md) | 2 | 2 | 0 | 0 | 0 | 8 | {"COUNT": 8, "MIN": 4, "MAX": 4, "SUM": 1} | 0 |
| [dacomp-004](tasks/dacomp-004.md) | 16 | 3 | 13 | 0 | 0 | 17 | {"COUNT": 14, "MIN": 2, "MAX": 2, "SUM": 15, "AVG": 2} | 1 |
| [dacomp-005](tasks/dacomp-005.md) | 25 | 18 | 7 | 0 | 0 | 35 | {"COUNT": 18, "AVG": 34, "MIN": 2, "MAX": 2, "SUM": 10} | 0 |
| [dacomp-006](tasks/dacomp-006.md) | 42 | 20 | 21 | 1 | 0 | 43 | {"MIN": 5, "MAX": 6, "COUNT": 15, "SUM": 41, "AVG": 20} | 5 |
| [dacomp-007](tasks/dacomp-007.md) | 28 | 6 | 22 | 0 | 0 | 29 | {"COUNT": 26, "SUM": 21, "AVG": 3} | 8 |
| [dacomp-008](tasks/dacomp-008.md) | 15 | 10 | 5 | 0 | 0 | 18 | {"COUNT": 16, "AVG": 14, "MIN": 2, "MAX": 3, "SUM": 2} | 1 |
| [dacomp-009](tasks/dacomp-009.md) | 25 | 13 | 4 | 2 | 6 | 26 | {"COUNT": 26, "MIN": 8, "MAX": 8, "SUM": 7, "AVG": 11} | 3 |
| [dacomp-010](tasks/dacomp-010.md) | 24 | 8 | 15 | 1 | 0 | 25 | {"MIN": 1, "MAX": 1, "COUNT": 23, "SUM": 12, "AVG": 9} | 1 |
| [dacomp-011](tasks/dacomp-011.md) | 17 | 12 | 5 | 0 | 0 | 21 | {"COUNT": 19, "AVG": 19, "MIN": 3, "MAX": 3, "SUM": 2} | 0 |
| [dacomp-012](tasks/dacomp-012.md) | 10 | 7 | 3 | 0 | 0 | 15 | {"COUNT": 12, "SUM": 1, "MIN": 3, "MAX": 3, "AVG": 11} | 1 |
| [dacomp-013](tasks/dacomp-013.md) | 26 | 21 | 5 | 0 | 0 | 32 | {"COUNT": 25, "SUM": 13, "MIN": 7, "MAX": 9, "AVG": 14} | 0 |
| [dacomp-014](tasks/dacomp-014.md) | 21 | 20 | 1 | 0 | 0 | 29 | {"COUNT": 25, "MIN": 3, "MAX": 3, "AVG": 20, "SUM": 5} | 0 |
| [dacomp-015](tasks/dacomp-015.md) | 14 | 11 | 0 | 0 | 3 | 17 | {"COUNT": 16, "GROUP_CONCAT": 1, "SUM": 4, "AVG": 6, "MAX": 4, "MIN": 1} | 0 |
| [dacomp-016](tasks/dacomp-016.md) | 1 | 1 | 0 | 0 | 0 | 3 | {"SUM": 1, "COUNT": 1, "AVG": 1, "MAX": 1} | 0 |
| [dacomp-017](tasks/dacomp-017.md) | 36 | 15 | 20 | 1 | 0 | 44 | {"COUNT": 30, "SUM": 25, "MIN": 2, "MAX": 5, "AVG": 6} | 2 |
| [dacomp-018](tasks/dacomp-018.md) | 38 | 20 | 14 | 3 | 1 | 45 | {"COUNT": 44, "SUM": 34, "AVG": 12} | 2 |
| [dacomp-019](tasks/dacomp-019.md) | 21 | 20 | 1 | 0 | 0 | 26 | {"COUNT": 22, "AVG": 5, "MIN": 1, "MAX": 2} | 0 |
| [dacomp-020](tasks/dacomp-020.md) | 7 | 7 | 0 | 0 | 0 | 12 | {"COUNT": 9, "MIN": 2, "MAX": 2, "AVG": 4, "SUM": 2} | 0 |
| [dacomp-021](tasks/dacomp-021.md) | 25 | 23 | 2 | 0 | 0 | 26 | {"COUNT": 25, "MIN": 4, "MAX": 3, "SUM": 12, "AVG": 13} | 1 |
| [dacomp-022](tasks/dacomp-022.md) | 35 | 35 | 0 | 0 | 0 | 43 | {"COUNT": 38, "AVG": 30, "SUM": 24, "MIN": 9, "MAX": 3} | 2 |
| [dacomp-023](tasks/dacomp-023.md) | 31 | 3 | 19 | 9 | 0 | 32 | {"MIN": 1, "MAX": 1, "COUNT": 16, "SUM": 29, "AVG": 1} | 10 |
| [dacomp-024](tasks/dacomp-024.md) | 19 | 3 | 6 | 10 | 0 | 19 | {"COUNT": 14, "SUM": 16, "AVG": 1} | 6 |
| [dacomp-025](tasks/dacomp-025.md) | 34 | 28 | 6 | 0 | 0 | 40 | {"COUNT": 34, "AVG": 24, "SUM": 26, "MIN": 1, "MAX": 2} | 0 |
| [dacomp-026](tasks/dacomp-026.md) | 25 | 23 | 2 | 0 | 0 | 46 | {"COUNT": 36, "SUM": 10, "AVG": 25, "MIN": 2, "MAX": 2} | 0 |
| [dacomp-027](tasks/dacomp-027.md) | 20 | 15 | 5 | 0 | 0 | 22 | {"COUNT": 18, "MIN": 1, "MAX": 1, "AVG": 7} | 0 |
| [dacomp-028](tasks/dacomp-028.md) | 16 | 7 | 4 | 5 | 0 | 17 | {"MIN": 1, "MAX": 1, "COUNT": 17, "AVG": 5, "GROUP_CONCAT": 1} | 0 |
| [dacomp-029](tasks/dacomp-029.md) | 16 | 16 | 0 | 0 | 0 | 19 | {"COUNT": 18, "MIN": 2, "MAX": 2, "AVG": 15} | 0 |
| [dacomp-030](tasks/dacomp-030.md) | 23 | 22 | 1 | 0 | 0 | 24 | {"COUNT": 23, "AVG": 11, "SUM": 9, "MIN": 1, "MAX": 1} | 0 |
| [dacomp-031](tasks/dacomp-031.md) | 33 | 21 | 11 | 1 | 0 | 35 | {"COUNT": 27, "MIN": 5, "MAX": 1, "AVG": 18, "SUM": 10} | 11 |
| [dacomp-032](tasks/dacomp-032.md) | 18 | 17 | 1 | 0 | 0 | 37 | {"COUNT": 36, "SUM": 13, "AVG": 15, "MIN": 1, "MAX": 1} | 0 |
| [dacomp-033](tasks/dacomp-033.md) | 85 | 67 | 18 | 0 | 0 | 102 | {"COUNT": 97, "SUM": 44, "AVG": 15, "MIN": 3, "MAX": 3} | 0 |
| [dacomp-034](tasks/dacomp-034.md) | 6 | 5 | 1 | 0 | 0 | 21 | {"COUNT": 17, "MIN": 4, "MAX": 4, "SUM": 4, "AVG": 3} | 0 |
| [dacomp-035](tasks/dacomp-035.md) | 61 | 41 | 17 | 2 | 1 | 65 | {"COUNT": 64, "AVG": 11, "SUM": 22} | 0 |
| [dacomp-036](tasks/dacomp-036.md) | 28 | 7 | 11 | 6 | 4 | 30 | {"COUNT": 30, "SUM": 16, "AVG": 10} | 1 |
| [dacomp-037](tasks/dacomp-037.md) | 16 | 10 | 6 | 0 | 0 | 22 | {"COUNT": 16, "AVG": 4, "MIN": 1, "MAX": 1, "SUM": 5} | 0 |
| [dacomp-038](tasks/dacomp-038.md) | 17 | 8 | 9 | 0 | 0 | 19 | {"COUNT": 14, "MAX": 5, "SUM": 2, "AVG": 1} | 0 |
| [dacomp-039](tasks/dacomp-039.md) | 12 | 6 | 6 | 0 | 0 | 15 | {"MIN": 4, "MAX": 4, "COUNT": 12, "AVG": 11} | 0 |
| [dacomp-040](tasks/dacomp-040.md) | 0 | 0 | 0 | 0 | 0 | 17 | {"SUM": 17} | 0 |
| [dacomp-041](tasks/dacomp-041.md) | 0 | 0 | 0 | 0 | 0 | 9 | {"COUNT": 9, "AVG": 1, "MAX": 1, "MIN": 1} | 0 |
| [dacomp-042](tasks/dacomp-042.md) | 34 | 3 | 27 | 4 | 0 | 44 | {"MIN": 3, "MAX": 3, "AVG": 2, "COUNT": 42} | 0 |
| [dacomp-043](tasks/dacomp-043.md) | 82 | 30 | 37 | 6 | 9 | 89 | {"COUNT": 80, "AVG": 7, "MIN": 5, "MAX": 59, "GROUP_CONCAT": 2} | 2 |
| [dacomp-044](tasks/dacomp-044.md) | 13 | 4 | 7 | 2 | 0 | 14 | {"COUNT": 13, "SUM": 12, "AVG": 1} | 0 |
| [dacomp-045](tasks/dacomp-045.md) | 26 | 11 | 15 | 0 | 0 | 30 | {"COUNT": 28, "AVG": 5, "SUM": 3} | 6 |
| [dacomp-046](tasks/dacomp-046.md) | 45 | 17 | 26 | 1 | 1 | 47 | {"COUNT": 45, "SUM": 20, "AVG": 16} | 1 |
| [dacomp-047](tasks/dacomp-047.md) | 46 | 4 | 27 | 10 | 5 | 49 | {"COUNT": 21, "MIN": 2, "MAX": 2, "SUM": 40, "AVG": 8} | 0 |
| [dacomp-048](tasks/dacomp-048.md) | 18 | 18 | 0 | 0 | 0 | 25 | {"COUNT": 24, "SUM": 3, "MIN": 2, "MAX": 2, "AVG": 10} | 0 |
| [dacomp-049](tasks/dacomp-049.md) | 0 | 0 | 0 | 0 | 0 | 4 | {"COUNT": 4} | 0 |
| [dacomp-050](tasks/dacomp-050.md) | 22 | 19 | 3 | 0 | 0 | 26 | {"COUNT": 25, "AVG": 2, "SUM": 17, "MIN": 1, "MAX": 1} | 0 |
| [dacomp-051](tasks/dacomp-051.md) | 34 | 24 | 10 | 0 | 0 | 50 | {"COUNT": 43, "MIN": 1, "MAX": 1, "AVG": 43, "SUM": 17} | 8 |
| [dacomp-052](tasks/dacomp-052.md) | 14 | 10 | 4 | 0 | 0 | 19 | {"COUNT": 11, "MIN": 2, "MAX": 2, "AVG": 9, "SUM": 2} | 1 |
| [dacomp-053](tasks/dacomp-053.md) | 23 | 19 | 4 | 0 | 0 | 32 | {"COUNT": 22, "MIN": 4, "MAX": 4, "AVG": 18, "SUM": 7} | 0 |
| [dacomp-054](tasks/dacomp-054.md) | 22 | 20 | 2 | 0 | 0 | 51 | {"COUNT": 48, "AVG": 17} | 27 |
| [dacomp-055](tasks/dacomp-055.md) | 25 | 24 | 1 | 0 | 0 | 43 | {"COUNT": 39, "MIN": 15, "MAX": 18, "AVG": 11, "SUM": 9} | 11 |
| [dacomp-056](tasks/dacomp-056.md) | 11 | 6 | 5 | 0 | 0 | 16 | {"COUNT": 15, "AVG": 8, "MIN": 2, "MAX": 2, "SUM": 1} | 2 |
| [dacomp-057](tasks/dacomp-057.md) | 38 | 27 | 4 | 2 | 5 | 49 | {"COUNT": 36, "MIN": 23, "MAX": 23, "SUM": 11, "AVG": 1} | 0 |
| [dacomp-058](tasks/dacomp-058.md) | 33 | 26 | 7 | 0 | 0 | 41 | {"COUNT": 26, "MIN": 8, "MAX": 6, "SUM": 22, "AVG": 28} | 10 |
| [dacomp-059](tasks/dacomp-059.md) | 35 | 30 | 5 | 0 | 0 | 39 | {"COUNT": 27, "MIN": 3, "MAX": 3, "SUM": 24} | 2 |
| [dacomp-060](tasks/dacomp-060.md) | 13 | 7 | 1 | 1 | 4 | 19 | {"COUNT": 9, "MIN": 2, "MAX": 2, "SUM": 12} | 0 |
| [dacomp-061](tasks/dacomp-061.md) | 34 | 33 | 1 | 0 | 0 | 38 | {"COUNT": 29, "AVG": 24, "MIN": 6, "MAX": 5, "SUM": 14} | 0 |
| [dacomp-062](tasks/dacomp-062.md) | 15 | 14 | 1 | 0 | 0 | 20 | {"COUNT": 19, "AVG": 14, "MIN": 1, "MAX": 1, "SUM": 2} | 0 |
| [dacomp-063](tasks/dacomp-063.md) | 20 | 14 | 6 | 0 | 0 | 33 | {"COUNT": 31, "MIN": 2, "AVG": 14, "MAX": 2, "SUM": 1} | 0 |
| [dacomp-064](tasks/dacomp-064.md) | 29 | 23 | 5 | 0 | 1 | 46 | {"COUNT": 40, "MIN": 3, "MAX": 3, "SUM": 5, "AVG": 17} | 0 |
| [dacomp-065](tasks/dacomp-065.md) | 38 | 34 | 1 | 2 | 1 | 49 | {"COUNT": 43, "MIN": 1, "MAX": 6, "AVG": 14, "SUM": 6} | 0 |
| [dacomp-066](tasks/dacomp-066.md) | 16 | 7 | 8 | 1 | 0 | 19 | {"COUNT": 8, "SUM": 15, "MIN": 2, "MAX": 2, "AVG": 3} | 0 |
| [dacomp-067](tasks/dacomp-067.md) | 52 | 46 | 5 | 1 | 0 | 65 | {"COUNT": 53, "SUM": 36, "MIN": 6, "MAX": 6, "AVG": 24} | 0 |
| [dacomp-068](tasks/dacomp-068.md) | 10 | 10 | 0 | 0 | 0 | 14 | {"COUNT": 8, "MIN": 2, "MAX": 3, "SUM": 11, "AVG": 4} | 0 |
| [dacomp-069](tasks/dacomp-069.md) | 9 | 4 | 3 | 2 | 0 | 13 | {"MIN": 7, "MAX": 7, "AVG": 3, "COUNT": 9, "SUM": 7} | 0 |
| [dacomp-070](tasks/dacomp-070.md) | 19 | 5 | 7 | 6 | 1 | 20 | {"MIN": 5, "MAX": 5, "COUNT": 8, "SUM": 11, "AVG": 12} | 0 |
| [dacomp-071](tasks/dacomp-071.md) | 12 | 6 | 5 | 1 | 0 | 15 | {"COUNT": 15, "MAX": 2, "AVG": 3, "MIN": 1} | 0 |
| [dacomp-072](tasks/dacomp-072.md) | 3 | 3 | 0 | 0 | 0 | 9 | {"COUNT": 8, "SUM": 4, "MIN": 3, "MAX": 3, "AVG": 5} | 0 |
| [dacomp-073](tasks/dacomp-073.md) | 51 | 28 | 22 | 1 | 0 | 67 | {"MIN": 3, "MAX": 3, "COUNT": 62, "AVG": 1, "SUM": 11} | 8 |
| [dacomp-074](tasks/dacomp-074.md) | 13 | 8 | 2 | 3 | 0 | 15 | {"COUNT": 11, "MIN": 3, "MAX": 2, "SUM": 4} | 1 |
| [dacomp-075](tasks/dacomp-075.md) | 8 | 8 | 0 | 0 | 0 | 13 | {"COUNT": 9, "SUM": 4, "MIN": 2, "MAX": 2, "AVG": 2} | 1 |
| [dacomp-076](tasks/dacomp-076.md) | 9 | 8 | 1 | 0 | 0 | 12 | {"COUNT": 10, "AVG": 9, "MIN": 2, "MAX": 2, "SUM": 1} | 0 |
| [dacomp-077](tasks/dacomp-077.md) | 12 | 10 | 2 | 0 | 0 | 23 | {"COUNT": 18, "MIN": 7, "MAX": 10, "AVG": 13, "SUM": 9} | 0 |
| [dacomp-078](tasks/dacomp-078.md) | 14 | 12 | 2 | 0 | 0 | 38 | {"COUNT": 32, "MIN": 8, "MAX": 8, "AVG": 8, "SUM": 7} | 0 |
| [dacomp-079](tasks/dacomp-079.md) | 22 | 18 | 3 | 1 | 0 | 30 | {"COUNT": 29, "SUM": 5, "AVG": 17, "MIN": 4, "MAX": 5} | 0 |
| [dacomp-080](tasks/dacomp-080.md) | 19 | 15 | 4 | 0 | 0 | 30 | {"COUNT": 25, "MIN": 6, "MAX": 8, "AVG": 6, "SUM": 3} | 4 |
| [dacomp-081](tasks/dacomp-081.md) | 42 | 33 | 9 | 0 | 0 | 66 | {"COUNT": 65, "MIN": 14, "MAX": 14, "AVG": 30, "SUM": 3} | 0 |
| [dacomp-082](tasks/dacomp-082.md) | 23 | 19 | 4 | 0 | 0 | 30 | {"COUNT": 19, "SUM": 21, "MIN": 1, "AVG": 14, "MAX": 1} | 3 |
| [dacomp-083](tasks/dacomp-083.md) | 34 | 25 | 9 | 0 | 0 | 47 | {"COUNT": 44, "MIN": 4, "MAX": 3, "AVG": 14, "SUM": 21} | 46 |
| [dacomp-084](tasks/dacomp-084.md) | 11 | 7 | 4 | 0 | 0 | 15 | {"COUNT": 12, "AVG": 7, "MIN": 4, "MAX": 4, "SUM": 2} | 5 |
| [dacomp-085](tasks/dacomp-085.md) | 6 | 5 | 1 | 0 | 0 | 11 | {"COUNT": 7, "SUM": 2, "MIN": 4, "MAX": 4, "AVG": 6} | 1 |
| [dacomp-086](tasks/dacomp-086.md) | 3 | 2 | 1 | 0 | 0 | 6 | {"COUNT": 5, "MIN": 3, "MAX": 3, "AVG": 2} | 0 |
| [dacomp-087](tasks/dacomp-087.md) | 9 | 9 | 0 | 0 | 0 | 15 | {"COUNT": 14, "SUM": 7, "AVG": 5, "MIN": 2, "MAX": 2} | 0 |
| [dacomp-088](tasks/dacomp-088.md) | 42 | 30 | 12 | 0 | 0 | 48 | {"COUNT": 46, "AVG": 15, "SUM": 16, "MIN": 2, "MAX": 2} | 4 |
| [dacomp-089](tasks/dacomp-089.md) | 21 | 20 | 1 | 0 | 0 | 32 | {"COUNT": 31, "MIN": 4, "MAX": 5, "SUM": 5, "AVG": 3} | 1 |
| [dacomp-090](tasks/dacomp-090.md) | 14 | 7 | 7 | 0 | 0 | 25 | {"COUNT": 21, "AVG": 9, "MIN": 5, "MAX": 2, "SUM": 13} | 8 |
| [dacomp-091](tasks/dacomp-091.md) | 11 | 4 | 5 | 0 | 2 | 24 | {"COUNT": 17, "MIN": 6, "MAX": 6, "AVG": 7, "SUM": 16} | 0 |
| [dacomp-092](tasks/dacomp-092.md) | 41 | 23 | 15 | 3 | 0 | 50 | {"COUNT": 35, "MIN": 4, "MAX": 14, "AVG": 32, "SUM": 19} | 32 |
| [dacomp-093](tasks/dacomp-093.md) | 17 | 12 | 2 | 3 | 0 | 24 | {"COUNT": 21, "MIN": 6, "MAX": 5, "AVG": 17, "SUM": 1} | 2 |
| [dacomp-094](tasks/dacomp-094.md) | 3 | 1 | 2 | 0 | 0 | 7 | {"COUNT": 7, "MIN": 2, "MAX": 2, "AVG": 1} | 1 |
| [dacomp-095](tasks/dacomp-095.md) | 34 | 31 | 3 | 0 | 0 | 42 | {"COUNT": 34, "AVG": 32, "MIN": 4, "MAX": 5, "SUM": 4} | 2 |
| [dacomp-096](tasks/dacomp-096.md) | 13 | 4 | 6 | 3 | 0 | 17 | {"COUNT": 16, "MIN": 4, "MAX": 5, "AVG": 9, "SUM": 5} | 3 |
| [dacomp-097](tasks/dacomp-097.md) | 53 | 44 | 9 | 0 | 0 | 81 | {"MIN": 5, "MAX": 6, "COUNT": 74, "SUM": 23, "AVG": 26} | 1 |
| [dacomp-098](tasks/dacomp-098.md) | 17 | 15 | 2 | 0 | 0 | 23 | {"COUNT": 20, "MIN": 4, "MAX": 4, "SUM": 1} | 3 |
| [dacomp-099](tasks/dacomp-099.md) | 26 | 23 | 2 | 0 | 1 | 38 | {"COUNT": 35, "MIN": 7, "MAX": 6, "GROUP_CONCAT": 2, "AVG": 2, "SUM": 6} | 16 |
| [dacomp-100](tasks/dacomp-100.md) | 5 | 2 | 3 | 0 | 0 | 11 | {"COUNT": 10, "GROUP_CONCAT": 1, "MIN": 1, "MAX": 1, "SUM": 1} | 0 |


## 哪些工作能共享

精确结果复用与新增物化分别记录；结构相似只用于候选筛选，每题最多验证 3 个代表性候选。

| 任务 | 分析状态 | 已验证已有结果候选 | 已验证新增物化候选 | 去重覆盖/成功数据 SQL |
| --- | --- | --- | --- | --- |
| [dacomp-001](tasks/dacomp-001.md) | 已验证候选 | 1 | 2 | 10/26 |
| [dacomp-002](tasks/dacomp-002.md) | 已验证候选 | 2 | 1 | 14/26 |
| [dacomp-003](tasks/dacomp-003.md) | 已验证候选 | 3 | 0 | 10/24 |
| [dacomp-004](tasks/dacomp-004.md) | 已验证候选 | 0 | 3 | 12/17 |
| [dacomp-005](tasks/dacomp-005.md) | 已验证候选 | 0 | 3 | 29/36 |
| [dacomp-006](tasks/dacomp-006.md) | 已验证候选 | 0 | 3 | 25/49 |
| [dacomp-007](tasks/dacomp-007.md) | 已验证候选 | 2 | 1 | 29/41 |
| [dacomp-008](tasks/dacomp-008.md) | 已验证候选 | 0 | 3 | 15/25 |
| [dacomp-009](tasks/dacomp-009.md) | 已验证候选 | 0 | 1 | 6/34 |
| [dacomp-010](tasks/dacomp-010.md) | 已验证候选 | 1 | 1 | 6/31 |
| [dacomp-011](tasks/dacomp-011.md) | 已验证候选 | 1 | 1 | 22/25 |
| [dacomp-012](tasks/dacomp-012.md) | 已验证候选 | 0 | 3 | 15/18 |
| [dacomp-013](tasks/dacomp-013.md) | 已验证候选 | 1 | 1 | 3/35 |
| [dacomp-014](tasks/dacomp-014.md) | 已验证候选 | 1 | 1 | 30/49 |
| [dacomp-015](tasks/dacomp-015.md) | 已验证候选 | 1 | 1 | 5/27 |
| [dacomp-016](tasks/dacomp-016.md) | 已验证候选 | 0 | 2 | 4/15 |
| [dacomp-017](tasks/dacomp-017.md) | 已验证候选 | 0 | 2 | 28/69 |
| [dacomp-018](tasks/dacomp-018.md) | 已验证候选 | 0 | 3 | 20/55 |
| [dacomp-019](tasks/dacomp-019.md) | 已验证候选 | 1 | 2 | 12/38 |
| [dacomp-020](tasks/dacomp-020.md) | 已验证候选 | 1 | 0 | 2/15 |
| [dacomp-021](tasks/dacomp-021.md) | 已验证候选 | 1 | 2 | 7/29 |
| [dacomp-022](tasks/dacomp-022.md) | 已验证候选 | 0 | 3 | 32/59 |
| [dacomp-023](tasks/dacomp-023.md) | 已验证候选 | 1 | 2 | 13/35 |
| [dacomp-024](tasks/dacomp-024.md) | 已验证候选 | 1 | 2 | 6/22 |
| [dacomp-025](tasks/dacomp-025.md) | 已验证候选 | 1 | 1 | 4/75 |
| [dacomp-026](tasks/dacomp-026.md) | 已验证候选 | 0 | 2 | 5/59 |
| [dacomp-027](tasks/dacomp-027.md) | 已验证候选 | 0 | 2 | 8/36 |
| [dacomp-028](tasks/dacomp-028.md) | 已验证候选 | 2 | 1 | 22/28 |
| [dacomp-029](tasks/dacomp-029.md) | 已验证候选 | 1 | 2 | 12/49 |
| [dacomp-030](tasks/dacomp-030.md) | 有候选待验证/受限或已拒绝 | 0 | 0 | 0/31 |
| [dacomp-031](tasks/dacomp-031.md) | 已验证候选 | 0 | 3 | 21/37 |
| [dacomp-032](tasks/dacomp-032.md) | 已验证候选 | 2 | 1 | 7/53 |
| [dacomp-033](tasks/dacomp-033.md) | 已验证候选 | 0 | 2 | 9/115 |
| [dacomp-034](tasks/dacomp-034.md) | 已验证候选 | 0 | 3 | 6/32 |
| [dacomp-035](tasks/dacomp-035.md) | 已验证候选 | 2 | 1 | 7/80 |
| [dacomp-036](tasks/dacomp-036.md) | 已验证候选 | 0 | 2 | 9/38 |
| [dacomp-037](tasks/dacomp-037.md) | 已验证候选 | 1 | 2 | 14/34 |
| [dacomp-038](tasks/dacomp-038.md) | 已验证候选 | 2 | 1 | 13/35 |
| [dacomp-039](tasks/dacomp-039.md) | 已验证候选 | 1 | 2 | 18/25 |
| [dacomp-040](tasks/dacomp-040.md) | 已验证候选 | 2 | 1 | 11/55 |
| [dacomp-041](tasks/dacomp-041.md) | 已验证候选 | 2 | 1 | 6/31 |
| [dacomp-042](tasks/dacomp-042.md) | 已验证候选 | 3 | 0 | 7/58 |
| [dacomp-043](tasks/dacomp-043.md) | 已验证候选 | 0 | 3 | 75/89 |
| [dacomp-044](tasks/dacomp-044.md) | 已验证候选 | 0 | 3 | 19/30 |
| [dacomp-045](tasks/dacomp-045.md) | 已验证候选 | 0 | 3 | 24/35 |
| [dacomp-046](tasks/dacomp-046.md) | 已验证候选 | 0 | 2 | 13/65 |
| [dacomp-047](tasks/dacomp-047.md) | 已验证候选 | 3 | 0 | 10/54 |
| [dacomp-048](tasks/dacomp-048.md) | 已验证候选 | 1 | 2 | 9/35 |
| [dacomp-049](tasks/dacomp-049.md) | 已验证候选 | 0 | 3 | 8/16 |
| [dacomp-050](tasks/dacomp-050.md) | 已验证候选 | 0 | 3 | 20/30 |
| [dacomp-051](tasks/dacomp-051.md) | 已验证候选 | 1 | 2 | 12/51 |
| [dacomp-052](tasks/dacomp-052.md) | 已验证候选 | 0 | 3 | 18/25 |
| [dacomp-053](tasks/dacomp-053.md) | 已验证候选 | 1 | 2 | 25/48 |
| [dacomp-054](tasks/dacomp-054.md) | 已验证候选 | 0 | 2 | 16/90 |
| [dacomp-055](tasks/dacomp-055.md) | 已验证候选 | 0 | 2 | 10/60 |
| [dacomp-056](tasks/dacomp-056.md) | 已验证候选 | 0 | 3 | 7/32 |
| [dacomp-057](tasks/dacomp-057.md) | 已验证候选 | 0 | 2 | 7/67 |
| [dacomp-058](tasks/dacomp-058.md) | 已验证候选 | 0 | 2 | 12/55 |
| [dacomp-059](tasks/dacomp-059.md) | 已验证候选 | 1 | 1 | 4/56 |
| [dacomp-060](tasks/dacomp-060.md) | 已验证候选 | 0 | 1 | 2/20 |
| [dacomp-061](tasks/dacomp-061.md) | 已验证候选 | 0 | 1 | 6/51 |
| [dacomp-062](tasks/dacomp-062.md) | 已验证候选 | 1 | 1 | 11/28 |
| [dacomp-063](tasks/dacomp-063.md) | 已验证候选 | 2 | 0 | 12/73 |
| [dacomp-064](tasks/dacomp-064.md) | 已验证候选 | 0 | 2 | 24/64 |
| [dacomp-065](tasks/dacomp-065.md) | 已验证候选 | 0 | 3 | 30/58 |
| [dacomp-066](tasks/dacomp-066.md) | 已验证候选 | 1 | 2 | 20/42 |
| [dacomp-067](tasks/dacomp-067.md) | 已验证候选 | 0 | 3 | 30/88 |
| [dacomp-068](tasks/dacomp-068.md) | 已验证候选 | 2 | 1 | 13/37 |
| [dacomp-069](tasks/dacomp-069.md) | 已验证候选 | 0 | 3 | 32/43 |
| [dacomp-070](tasks/dacomp-070.md) | 已验证候选 | 0 | 3 | 12/23 |
| [dacomp-071](tasks/dacomp-071.md) | 已验证候选 | 1 | 2 | 21/36 |
| [dacomp-072](tasks/dacomp-072.md) | 已验证候选 | 0 | 3 | 9/16 |
| [dacomp-073](tasks/dacomp-073.md) | 已验证候选 | 1 | 2 | 38/92 |
| [dacomp-074](tasks/dacomp-074.md) | 已验证候选 | 1 | 1 | 7/24 |
| [dacomp-075](tasks/dacomp-075.md) | 已验证候选 | 0 | 3 | 12/27 |
| [dacomp-076](tasks/dacomp-076.md) | 已验证候选 | 0 | 1 | 5/21 |
| [dacomp-077](tasks/dacomp-077.md) | 已验证候选 | 2 | 1 | 6/39 |
| [dacomp-078](tasks/dacomp-078.md) | 已验证候选 | 1 | 1 | 4/46 |
| [dacomp-079](tasks/dacomp-079.md) | 已验证候选 | 0 | 1 | 4/31 |
| [dacomp-080](tasks/dacomp-080.md) | 已验证候选 | 0 | 1 | 3/35 |
| [dacomp-081](tasks/dacomp-081.md) | 已验证候选 | 0 | 3 | 26/119 |
| [dacomp-082](tasks/dacomp-082.md) | 已验证候选 | 0 | 1 | 12/34 |
| [dacomp-083](tasks/dacomp-083.md) | 已验证候选 | 0 | 2 | 48/62 |
| [dacomp-084](tasks/dacomp-084.md) | 已验证候选 | 2 | 1 | 16/32 |
| [dacomp-085](tasks/dacomp-085.md) | 已验证候选 | 0 | 1 | 2/15 |
| [dacomp-086](tasks/dacomp-086.md) | 已验证候选 | 1 | 1 | 4/15 |
| [dacomp-087](tasks/dacomp-087.md) | 已验证候选; original verified selection retained across continuation | 0 | 3 | 8/20 |
| [dacomp-088](tasks/dacomp-088.md) | 已验证候选 | 0 | 3 | 26/73 |
| [dacomp-089](tasks/dacomp-089.md) | 已验证候选 | 0 | 3 | 15/41 |
| [dacomp-090](tasks/dacomp-090.md) | 已验证候选 | 0 | 3 | 9/43 |
| [dacomp-091](tasks/dacomp-091.md) | 已验证候选; original verified selection retained across continuation | 0 | 3 | 12/34 |
| [dacomp-092](tasks/dacomp-092.md) | 已验证候选; original verified selection retained across continuation | 0 | 3 | 16/65 |
| [dacomp-093](tasks/dacomp-093.md) | 已验证候选; original verified selection retained across continuation | 0 | 1 | 2/37 |
| [dacomp-094](tasks/dacomp-094.md) | 已验证候选 | 0 | 2 | 4/16 |
| [dacomp-095](tasks/dacomp-095.md) | 已验证候选 | 0 | 1 | 3/52 |
| [dacomp-096](tasks/dacomp-096.md) | 已验证候选 | 0 | 3 | 9/22 |
| [dacomp-097](tasks/dacomp-097.md) | 已验证候选 | 0 | 3 | 15/106 |
| [dacomp-098](tasks/dacomp-098.md) | 已验证候选 | 1 | 2 | 14/42 |
| [dacomp-099](tasks/dacomp-099.md) | 已验证候选 | 1 | 2 | 18/70 |
| [dacomp-100](tasks/dacomp-100.md) | 已验证候选 | 3 | 0 | 28/71 |


暖缓存代表性性能验证（物化路径含每次构建，五次交替重复）：

| 任务/候选 | 状态 | 基线中位 ms | 构建+复用中位 ms | 基线/候选 |
| --- | --- | --- | --- | --- |
| dacomp-083/C1 | limited_or_failed | unknown | unknown | unknown |
| dacomp-025/C4 | limited_or_failed | unknown | unknown | unknown |
| dacomp-054/C6 | limited_or_failed | unknown | unknown | unknown |
| dacomp-092/C2 | measured | 11838.924922980368 | 144.1992586478591 | 82.10114971458724 |
| dacomp-080/C2 | measured | 8716.94603562355 | 3207.3902683332562 | 2.717769060312506 |
| dacomp-022/C3 | measured | 3700.186513364315 | 3612.9672741517425 | 1.0241406114681872 |
| dacomp-055/C5 | measured | 1410.5888148769736 | 420.6554042175412 | 3.3533120001175356 |
| dacomp-021/C5 | measured | 803.313422948122 | 555.9278260916471 | 1.4449958883973768 |
| dacomp-034/C2 | measured | 866.0092828795314 | 599.2158846929669 | 1.445237526243596 |
| dacomp-081/C5 | measured | 774.913964793086 | 1133.3981109783053 | 0.6837085374389854 |


## 结论边界

本报告描述当前已记录轨迹。未开始任务不参与轨迹长度分布。不能把协议或模型变化解释为受控因果效果；候选基于已知完整轨迹离线选择，不证明在线可预测性或净收益。Python 源码筛查不能代替完整语义人工审查；无法解析的列血缘明确保留 unknown。

[指标口径](METRICS.md)；[机器任务表](tasks.csv)；[逐 SQL 结构](sql_profile.jsonl)；[候选比较](verification.jsonl)；[审计](audit.json)。
