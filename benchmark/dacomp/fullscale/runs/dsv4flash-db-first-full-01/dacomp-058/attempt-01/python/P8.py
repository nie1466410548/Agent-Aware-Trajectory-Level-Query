import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# Reload campaign data
r = db.query("""
WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, AVG(cost) AS avg_monthly_cost, SUM(cost) AS total_cost,
  AVG(roas) AS avg_roas,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score
""", parameters=[])
campaigns = db.frame(r)
problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]
campaigns['is_problematic'] = campaigns['campaign_id'].isin(problematic_ids)

def risk_level(h):
    if h < 30: return 'Critical'
    if h < 36: return 'High'
    if h < 45: return 'Medium'
    return 'Low'
campaigns['risk_level'] = campaigns['health_score'].apply(risk_level)

# Figure 1: Health score distribution
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(campaigns['health_score'], bins=15, kde=True, ax=axes[0], color='steelblue')
axes[0].axvline(30, color='red', ls='--', label='Critical threshold')
axes[0].axvline(36, color='orange', ls='--', label='High threshold')
axes[0].axvline(45, color='green', ls='--', label='Medium threshold')
axes[0].set_title('Health Score Distribution (50 campaigns)')
axes[0].set_xlabel('Health Score')
axes[0].legend()

# Risk level by problematic status
risk_counts = campaigns.groupby(['risk_level', 'is_problematic']).size().unstack(fill_value=0)
risk_counts.columns = ['Healthy', 'Problematic']
risk_counts.plot(kind='bar', ax=axes[1], color=['#4C9F70', '#D9534F'])
axes[1].set_title('Risk Level by Campaign Classification')
axes[1].set_xlabel('Risk Level')
axes[1].set_ylabel('Number of Campaigns')
plt.tight_layout()
plt.savefig('health_score_distribution.png', dpi=100)
print("Saved health_score_distribution.png")

# Figure 2: Dimension comparison - problematic vs healthy
dim_cols = ['cost_eff', 'conv_quality', 'competitive']
fig, ax = plt.subplots(figsize=(8, 6))
dim_data = campaigns.groupby('is_problematic')[dim_cols].mean().T
dim_data.columns = ['Healthy campaigns', 'Problematic (low-ROAS) campaigns']
dim_data.plot(kind='bar', ax=ax, color=['#4C9F70', '#D9534F'])
ax.set_title('Average Dimension Scores: Problematic vs Healthy Campaigns')
ax.set_ylabel('Dimension Score (0-100)')
ax.set_ylim(0, 60)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('dimension_compare.png', dpi=100)
print("Saved dimension_compare.png")
print(dim_data)

# Figure 3: Health score by campaign type
fig, ax = plt.subplots(figsize=(12, 5))
order = campaigns.groupby('campaign_type')['health_score'].mean().sort_values().index
sns.boxplot(x='campaign_type', y='health_score', data=campaigns, ax=ax, order=order, palette='Set2')
sns.stripplot(x='campaign_type', y='health_score', data=campaigns, ax=ax, order=order, color='black', alpha=0.5, size=6)
ax.set_title('Health Score Distribution by Campaign Type')
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
plt.tight_layout()
plt.savefig('health_by_type.png', dpi=100)
print("Saved health_by_type.png")

# Figure 4: Health score by industry
fig, ax = plt.subplots(figsize=(12, 5))
order = campaigns.groupby('industry')['health_score'].mean().sort_values().index
sns.boxplot(x='industry', y='health_score', data=campaigns, ax=ax, order=order, palette='Set2')
sns.stripplot(x='industry', y='health_score', data=campaigns, ax=ax, order=order, color='black', alpha=0.5, size=6)
ax.set_title('Health Score Distribution by Industry')
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
plt.tight_layout()
plt.savefig('health_by_industry.png', dpi=100)
print("Saved health_by_industry.png")

# Figure 5: Health score by bidding strategy
fig, ax = plt.subplots(figsize=(12, 5))
order = campaigns.groupby('bidding_strategy')['health_score'].mean().sort_values().index
sns.boxplot(x='bidding_strategy', y='health_score', data=campaigns, ax=ax, order=order, palette='Set2')
sns.stripplot(x='bidding_strategy', y='health_score', data=campaigns, ax=ax, order=order, color='black', alpha=0.5, size=6)
ax.set_title('Health Score Distribution by Bidding Strategy')
ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
plt.tight_layout()
plt.savefig('health_by_bidding.png', dpi=100)
print("Saved health_by_bidding.png")