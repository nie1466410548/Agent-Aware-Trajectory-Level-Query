import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load segment-level conversation metrics
seg_conv = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  AVG(c.resp_delay) AS avg_resp_delay_min,
  AVG(c.duration) AS avg_duration_min,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*) AS bot_ratio_pct,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*) AS sla_breach_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
ORDER BY co.segment
"""))

# Load retention by segment
seg_ret = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  cd.segment,
  COUNT(*) AS companies,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.segment
ORDER BY cd.segment
"""))

# Load conversion rate by segment
seg_conv_rate = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.segment,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.segment
ORDER BY cd.segment
"""))

# Merge for visualization
df = seg_conv.merge(seg_ret, on='segment', how='left').merge(seg_conv_rate, on='segment', how='left')
order = ['new_contract', 'renewal', 'expansion', 'churn_watch']
df['segment'] = pd.Categorical(df['segment'], categories=order, ordered=True)
df = df.sort_values('segment')
print(df)

# Dashboard figure: 2x2
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
colors = {'new_contract': '#4C72B0', 'renewal': '#55A868', 'expansion': '#C44E52', 'churn_watch': '#8172B2'}

# Panel 1: Avg response delay
axes[0,0].bar(df['segment'].astype(str), df['avg_resp_delay_min'], color=[colors[s] for s in df['segment']], alpha=0.85)
axes[0,0].set_title('Message Response Delay (avg, minutes)')
axes[0,0].set_ylabel('Minutes')
axes[0,0].set_ylim(0, 35)
for i, v in enumerate(df['avg_resp_delay_min']):
    axes[0,0].text(i, v + 0.3, f'{v:.2f}', ha='center', fontsize=10)

# Panel 2: Bot ratio
axes[0,1].bar(df['segment'].astype(str), df['bot_ratio_pct'], color=[colors[s] for s in df['segment']], alpha=0.85)
axes[0,1].set_title('First Response Bot Ratio (%)')
axes[0,1].set_ylabel('%')
for i, v in enumerate(df['bot_ratio_pct']):
    axes[0,1].text(i, v + 0.3, f'{v:.2f}%', ha='center', fontsize=10)

# Panel 3: Retention
x = np.arange(len(df))
w = 0.35
axes[1,0].bar(x - w/2, df['weekly_retention']*100, w, label='Weekly', color='steelblue', alpha=0.85)
axes[1,0].bar(x + w/2, df['monthly_retention']*100, w, label='Monthly', color='lightcoral', alpha=0.85)
axes[1,0].set_xticks(x)
axes[1,0].set_xticklabels(df['segment'].astype(str))
axes[1,0].set_title('Retention Rate (%)')
axes[1,0].set_ylabel('%')
axes[1,0].legend()
for i in range(len(df)):
    axes[1,0].text(i - w/2, df['weekly_retention'].iloc[i]*100 + 1, f"{df['weekly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)
    axes[1,0].text(i + w/2, df['monthly_retention'].iloc[i]*100 + 1, f"{df['monthly_retention'].iloc[i]*100:.1f}", ha='center', fontsize=8)

# Panel 4: Conversion rate
axes[1,1].bar(df['segment'].astype(str), df['conversion_rate_pct'], color=[colors[s] for s in df['segment']], alpha=0.85)
axes[1,1].set_title('Conversation-to-Feature-Usage Conversion Rate (%)')
axes[1,1].set_ylabel('%')
for i, v in enumerate(df['conversion_rate_pct']):
    axes[1,1].text(i, v + 0.05, f'{v:.2f}%', ha='center', fontsize=10)

fig.suptitle('Customer Engagement Metrics by Segmentation (Outlier-filtered)', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/work/dashboard_metrics_by_segment.png', dpi=130, bbox_inches='tight')
plt.close()

# Save the dashboard data
df.to_csv('/work/dashboard_metrics_by_segment.csv', index=False)
print("\nSaved dashboard data and figure.")