import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the company-level data
df = db.frame(db.query("""
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         ELSE 'unknown' END AS arr_bucket,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS sla_breach_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS product_tour_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS usage_insight_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS adoption_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS escalation_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  a.*, co.segment, co.arr_bucket, co.seat_bucket,
  cm.registration_retention_7d AS ret_7d,
  cm.registration_retention_30d AS ret_30d,
  cm.contacts_active_7d AS active_7d,
  cm.contacts_active_30d AS active_30d
FROM agg a
JOIN company_dim co ON a.company_name = co.company_name
JOIN intercom__company_metrics cm ON a.company_name = cm.company_name
"""))

print(f"Loaded {len(df)} companies")
print(df.dtypes)
print(df.head())

# Correlation matrix
corr_cols = ['num_convs', 'avg_resp_delay', 'avg_duration', 'bot_ratio', 
             'sla_breach_ratio', 'product_tour_ratio', 'usage_insight_ratio',
             'adoption_ratio', 'escalation_ratio', 'ret_7d', 'ret_30d']
corr_df = df[corr_cols].dropna()
corr_matrix = corr_df.corr()

# Plot correlation heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0, 
            square=True, linewidths=0.5)
plt.title('Correlation: Conversation Metrics vs Retention', fontsize=14)
plt.tight_layout()
plt.savefig('/work/correlation_heatmap.png', dpi=120)
plt.close()

# Key correlations with retention
print("\n=== Correlations with Weekly Retention (ret_7d) ===")
for col in ['num_convs', 'avg_resp_delay', 'avg_duration', 'bot_ratio', 
            'sla_breach_ratio', 'product_tour_ratio', 'usage_insight_ratio',
            'adoption_ratio', 'escalation_ratio']:
    r, p = stats.pearsonr(df[col].dropna(), df['ret_7d'].dropna())
    print(f"{col:25s}: r={r:.4f}, p={p:.6f}")

print("\n=== Correlations with Monthly Retention (ret_30d) ===")
for col in ['num_convs', 'avg_resp_delay', 'avg_duration', 'bot_ratio', 
            'sla_breach_ratio', 'product_tour_ratio', 'usage_insight_ratio',
            'adoption_ratio', 'escalation_ratio']:
    r, p = stats.pearsonr(df[col].dropna(), df['ret_30d'].dropna())
    print(f"{col:25s}: r={r:.4f}, p={p:.6f}")

# Segment-level comparison: box plot of retention
plt.figure(figsize=(10, 6))
order = ['new_contract', 'renewal', 'expansion', 'churn_watch']
sns.boxplot(data=df, x='segment', y='ret_7d', order=order, palette='Set2')
plt.title('Weekly Retention Rate by Customer Segment', fontsize=14)
plt.xlabel('Segment')
plt.ylabel('Weekly Retention Rate')
plt.tight_layout()
plt.savefig('/work/retention_by_segment.png', dpi=120)
plt.close()

# ARR bucket vs retention
plt.figure(figsize=(10, 6))
arr_order = ['<30k', '30k_65k', '65k_110k', '110k_200k', '200k_plus']
sns.boxplot(data=df, x='arr_bucket', y='ret_7d', order=arr_order, palette='Set3')
plt.title('Weekly Retention Rate by ARR Bucket', fontsize=14)
plt.xlabel('Annual Contract Value')
plt.ylabel('Weekly Retention Rate')
plt.tight_layout()
plt.savefig('/work/retention_by_arr.png', dpi=120)
plt.close()

# Bot ratio vs retention scatter
plt.figure(figsize=(10, 6))
colors = {'new_contract': 'blue', 'renewal': 'green', 'expansion': 'orange', 'churn_watch': 'red'}
for seg in df['segment'].unique():
    mask = df['segment'] == seg
    plt.scatter(df.loc[mask, 'bot_ratio'], df.loc[mask, 'ret_7d'], 
                label=seg, alpha=0.5, s=20, c=colors.get(seg, 'gray'))
plt.xlabel('Bot Response Ratio')
plt.ylabel('Weekly Retention Rate')
plt.title('Bot Ratio vs Retention by Segment')
plt.legend()
plt.tight_layout()
plt.savefig('/work/bot_vs_retention.png', dpi=120)
plt.close()

# Topic distribution by segment
topic_cols = ['usage_insight_ratio', 'adoption_ratio', 'escalation_ratio']
topic_means = df.groupby('segment')[topic_cols].mean()
print("\n=== Topic Ratios by Segment ===")
print(topic_means)

# High-value churn_watch analysis
high_val = df[df['segment'] == 'churn_watch']
print(f"\n=== Churn Watch Companies (n={len(high_val)}) ===")
print(f"Avg ret_7d: {high_val['ret_7d'].mean():.4f}")
print(f"Avg ret_30d: {high_val['ret_30d'].mean():.4f}")

# Top and bottom quartile retention in churn_watch
high_val['ret_quartile'] = pd.qcut(high_val['ret_7d'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
top = high_val[high_val['ret_quartile'] == 'Q4']
bottom = high_val[high_val['ret_quartile'] == 'Q1']
print(f"\nTop quartile retention (Q4): {len(top)} companies")
print(f"Bottom quartile retention (Q1): {len(bottom)} companies")
print("Top quartile averages:")
print(top[['num_convs', 'avg_resp_delay', 'bot_ratio', 'sla_breach_ratio', 'product_tour_ratio']].mean())
print("Bottom quartile averages:")
print(bottom[['num_convs', 'avg_resp_delay', 'bot_ratio', 'sla_breach_ratio', 'product_tour_ratio']].mean())

print("\nDone!")