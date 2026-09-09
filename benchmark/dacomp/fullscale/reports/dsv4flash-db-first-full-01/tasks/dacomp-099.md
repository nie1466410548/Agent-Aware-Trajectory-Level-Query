# dacomp-099

Identify the key factors that lead customers to upgrade or downgrade. On a per-customer ba…

运行：未开始。官方未评分。全部 SQL 尝试/成功 0/0；数据 SQL 0/0；Python 0 次。

完整原题：

Identify the key factors that lead customers to upgrade or downgrade. On a per-customer basis, construct an event timeline based on subscription change times (hypothetical `upgrade_at`, `downgrade_at`). Within a 30-day observation window before and after the change, compare changes in feature usage intensity (e.g., call counts, frequency changes relative to a baseline) with the occurrence of support incidents (e.g., outages, Bug tickets, support conversations). The goal is to analyze which experiences best explain the occurrence of upgrades or downgrades and to provide actionable business recommendations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：没有可用数据查询。

数据库大小：8,978,432 字节。

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
