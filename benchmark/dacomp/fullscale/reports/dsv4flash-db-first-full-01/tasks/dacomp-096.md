# dacomp-096

Based on `klaviyo__campaigns` (with columns like `STATUS`/`STATUS_ID`, `SENT_AT`, `schedul…

运行：未开始。官方未评分。全部 SQL 尝试/成功 0/0；数据 SQL 0/0；Python 0 次。

完整原题：

Based on `klaviyo__campaigns` (with columns like `STATUS`/`STATUS_ID`, `SENT_AT`, `scheduled_to_send_at`, `EMAIL_TEMPLATE_ID`, `source_relation`, `count_received`, `count_opened`, `count_clicked`) and combined with activity metrics from `marts.klaviyo__persons`, build a campaign health framework.

Use Open Rate = `count_opened` ÷ `count_received` and Click-to-Open Rate = `count_clicked` ÷ `count_opened` as core metrics. Group the data by Campaign Type (e.g., Promotional/New Product/Storytelling) and audience size quantiles (< 10k, 10k–100k, > 100k, based on `count_received`). Calculate the mean and standard deviation of historical data from the last 6 months.

Set rules for anomaly detection: if a single campaign's metric falls below mean − 2σ or exceeds mean + 2σ, it should be flagged as an anomaly. Additionally, if the interval between a campaign's `updated_at` and the previous campaign's is < 24 hours, it should be identified as a high-frequency update anomaly. The analysis must trace the specific causes of anomalous campaigns, including sending time slot (weekday/weekend, morning/afternoon), template reuse frequency (percentage of the same `EMAIL_TEMPLATE_ID`), and copy theme (categorized by `source_relation`).

Finally, produce a diagnostic report that clearly outlines improvement directions for template governance (e.g., reduce reuse of templates with a >50% share), theme optimization (e.g., for theme types with low click-to-open rates), and sending cadence (e.g., avoid deployments with <24 hours between them). Propose at least one actionable A/B test plan (such as adjusting send time or replacing a template) and provide an estimated range for potential gains (e.g., projected 5–10% increase in open rate, 2–5% increase in click-to-open rate).

| 表 | 行数 | 列数 |
| --- | --- | --- |
| klaviyo__flows | 79 | 27 |
| klaviyo__person_campaign_flow | 4 | 32 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：没有可用数据查询。

数据库大小：28,672 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |


## Python 与执行位置

无 Python 分析调用。

## 优化机会

轨迹/解析不足无法判断。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |


已验证覆盖（含触发查询、候选并集去重）：0/0 条成功数据 SQL。没有发现本方法可验证的候选，不等于不存在优化。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。
