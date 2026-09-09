import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

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
  SUM(cost) AS total_cost,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score
""", parameters=[])
campaigns = db.frame(r)
campaigns['is_problematic'] = campaigns['campaign_id'].isin(problematic_ids)
def risk_level(h):
    if h < 30: return 'Critical'
    if h < 36: return 'High'
    if h < 45: return 'Medium'
    return 'Low'
campaigns['risk_level'] = campaigns['health_score'].apply(risk_level)

# Horizontal stacked bar of dimensions sorted by health score
campaigns_sorted = campaigns.sort_values('health_score', ascending=True).reset_index(drop=True)
colors = {'cost_eff': '#5B9BD5', 'conv_quality': '#ED7D31', 'competitive': '#A5A5A5'}
labels = {'cost_eff': 'Cost Efficiency (40%)', 'conv_quality': 'Conversion Quality (35%)', 'competitive': 'Competitiveness (25%)'}

fig, ax = plt.subplots(figsize=(12, 14))
bottom = np.zeros(len(campaigns_sorted))
for col, color in colors.items():
    ax.barh(campaigns_sorted.index, campaigns_sorted[col], left=bottom, color=color, label=labels[col], edgecolor='white', linewidth=0.3)
    bottom += campaigns_sorted[col].values

# Mark problematic campaigns
y_ticks = campaigns_sorted.index
y_labels = campaigns_sorted['campaign_id'].astype(str) + '-' + campaigns_sorted['campaign_type'].str[:4]
ax.set_yticks(y_ticks)
ax.set_yticklabels(y_labels, fontsize=8)
# Highlight problematic campaigns with different color on the axis labels
for idx, row in campaigns_sorted.iterrows():
    if row['is_problematic']:
        ax.get_yticklabels()[idx].set_color('red')
        ax.get_yticklabels()[idx].set_fontweight('bold')

ax.set_xlabel('Score (0-100)')
ax.set_title('Campaign Health Score Ranking (red = problematic low-ROAS campaigns)')
ax.legend(loc='lower right', fontsize=9)
ax.axvline(30, color='red', ls='--', lw=0.8)
ax.axvline(36, color='orange', ls='--', lw=0.8)
ax.axvline(45, color='green', ls='--', lw=0.8)
plt.tight_layout()
plt.savefig('health_ranking_stacked.png', dpi=100)
print("Saved health_ranking_stacked.png")

# Summary stats for report
print("Total cost:", campaigns['total_cost'].sum().round(0))
print("Problematic cost:", campaigns[campaigns['is_problematic']]['total_cost'].sum().round(0))
print("Problematic share:", (campaigns[campaigns['is_problematic']]['total_cost'].sum()/campaigns['total_cost'].sum()*100).round(1))
print("\nRisk distribution:", campaigns['risk_level'].value_counts().to_dict())
print("\nCritical+High campaigns:")
print(campaigns[campaigns['risk_level'].isin(['Critical','High'])][['campaign_id','campaign_name','health_score','risk_level','is_problematic']].round(1).to_string(index=False))