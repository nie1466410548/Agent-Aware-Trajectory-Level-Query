import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Monthly conversation volume trend with bot ratio
monthly = db.frame(db.query("""
SELECT 
  strftime('%Y-%m', conversation_created_at) AS month,
  COUNT(*) AS total_convs,
  AVG(time_to_first_response_minutes) AS avg_resp_delay,
  AVG(time_to_last_close_minutes) AS avg_duration,
  100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*) AS bot_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
  AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
GROUP BY strftime('%Y-%m', conversation_created_at)
ORDER BY month
"""))
print("Monthly trends:")
print(monthly)

fig, axes = plt.subplots(2, 1, figsize=(12, 8))
axes[0].plot(monthly['month'], monthly['total_convs'], marker='o', color='steelblue', linewidth=2)
axes[0].set_title('Monthly Conversation Volume (outlier-filtered)')
axes[0].set_ylabel('Conversations')
axes[0].grid(alpha=0.3)
axes[1].plot(monthly['month'], monthly['bot_pct'], marker='o', color='darkorange', linewidth=2, label='Bot %')
axes[1].plot(monthly['month'], monthly['avg_resp_delay'], marker='s', color='green', linewidth=2, label='Avg Response Delay (min)')
axes[1].set_title('Monthly Bot Ratio & Response Delay')
axes[1].set_ylabel('% / minutes')
axes[1].legend()
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/monthly_trends.png', dpi=120)
plt.close()

# Topic-to-feature-usage: For companies, does the topic of the most recent conversation relate to post-conversation activity?
# Conversation topic composition for companies that had activity within 72h after conversation (converted) vs not
conversion_topics = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags,
         ce.last_close_at
  FROM intercom__conversation_enhanced ce
  WHERE ce.last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
),
tagged AS (
  SELECT 
    c.company_name,
    c.all_conversation_tags,
    CASE WHEN cv.company_name IS NOT NULL THEN 1 ELSE 0 END AS is_converted
  FROM conv c
  LEFT JOIN converted cv ON c.company_name = cv.company_name
)
SELECT 
  CASE 
    WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  SUM(CASE WHEN is_converted = 1 THEN 1 ELSE 0 END) AS converted_convs,
  COUNT(*) AS total_convs,
  100.0 * SUM(CASE WHEN is_converted = 1 THEN 1 ELSE 0 END) / COUNT(*) AS conv_rate_pct
FROM tagged
GROUP BY 1
ORDER BY conv_rate_pct DESC
"""))
print("\nConversation-level post-activity conversion by topic:")
print(conversion_topics)

# Also segment and SLA analysis
sla_analysis = db.frame(db.query("""
SELECT 
  CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 'breached'
       WHEN all_conversation_tags LIKE '%sla:met%' THEN 'met'
       WHEN all_conversation_tags LIKE '%sla:warning%' THEN 'warning' END AS sla_status,
  COUNT(*) AS total,
  AVG(time_to_first_response_minutes) AS avg_resp_delay,
  AVG(time_to_last_close_minutes) AS avg_duration
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
GROUP BY 1
"""))
print("\nSLA analysis:")
print(sla_analysis)

# Topic distribution for high ARR (200k+) customers
high_arr_topics = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%arr_bucket:arr:200k_plus%'
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM conv c JOIN company_dim co ON c.company_name = co.company_name
GROUP BY 1
ORDER BY total DESC
"""))
print("\nTopic distribution for ARR 200k+ customers:")
print(high_arr_topics)

# Plot conversion by topic
plt.figure(figsize=(12, 6))
topics_sorted = conversion_topics.sort_values('conv_rate_pct', ascending=False)
sns.barplot(data=topics_sorted, x='topic', y='conv_rate_pct', palette='viridis')
plt.title('Feature-Usage Conversion Rate After Conversation by Topic')
plt.ylabel('Conversion Rate (%)')
plt.xlabel('Conversation Topic')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/work/topic_conversion.png', dpi=120)
plt.close()
print("\nDone with topic analysis.")