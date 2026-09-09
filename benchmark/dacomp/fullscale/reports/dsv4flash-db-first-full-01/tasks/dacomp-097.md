# dacomp-097

Using conversation, user profile, and usage event data from the past six months, compare t…

运行：未开始。官方未评分。全部 SQL 尝试/成功 0/0；数据 SQL 0/0；Python 0 次。

完整原题：

Using conversation, user profile, and usage event data from the past six months, compare the structural differences in Intercom conversation and product usage behavior among paying customers. The analysis should be sliced by customer segmentation (new_contract/renewal/churn_watch) and account size (seat count, annual contract value).

Calculate the following metrics:
- Message Response Delay = `first_response_at` − `initiated_at` (in minutes)
- First Response Bot Ratio = Count of conversations where responder_type = 'bot' ÷ Total conversations
- Conversation-to-Feature-Usage Conversion Rate = Number of customers with a feature event within 72 hours after a conversation ends ÷ Total customers
- Weekly/Monthly Retention Rate = Percentage of active customers in the current week/month who remain active in the next week/month (where 'active' is defined as having ≥1 core feature event).

The analysis must unify timezones and exclude outlier conversations (response time/duration > P99 or < P1). The output should be a reproducible metrics dashboard. The conclusion should focus on identifying key operational touchpoints and feature paths that can enhance the long-term activity of high-value customers.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__contact_enhanced | 2707 | 22 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：没有可用数据查询。

数据库大小：11,137,024 字节。

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
