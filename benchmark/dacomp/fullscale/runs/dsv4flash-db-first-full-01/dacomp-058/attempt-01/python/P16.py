import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Reload campaign health data
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
  SUM(cost) AS total_cost, AVG(roas) AS avg_roas,
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

# Comparison by campaign type
print("=== By Campaign Type ===")
ct = campaigns.groupby('campaign_type').agg(
    campaigns=('campaign_id','count'),
    avg_health=('health_score','mean'),
    avg_cost_eff=('cost_eff','mean'),
    avg_conv_quality=('conv_quality','mean'),
    avg_competitive=('competitive','mean'),
    total_cost=('total_cost','sum'),
    avg_roas=('avg_roas','mean'),
    problematic=('is_problematic','sum')
).round(1).sort_values('avg_health', ascending=False)
print(ct.to_string())

# Comparison by bidding strategy
print("\n=== By Bidding Strategy ===")
bs = campaigns.groupby('bidding_strategy').agg(
    campaigns=('campaign_id','count'),
    avg_health=('health_score','mean'),
    avg_cost_eff=('cost_eff','mean'),
    avg_conv_quality=('conv_quality','mean'),
    avg_competitive=('competitive','mean'),
    total_cost=('total_cost','sum'),
    avg_roas=('avg_roas','mean'),
    problematic=('is_problematic','sum')
).round(1).sort_values('avg_health', ascending=False)
print(bs.to_string())

# Comparison by industry
print("\n=== By Industry ===")
ind = campaigns.groupby('industry').agg(
    campaigns=('campaign_id','count'),
    avg_health=('health_score','mean'),
    avg_cost_eff=('cost_eff','mean'),
    avg_conv_quality=('conv_quality','mean'),
    avg_competitive=('competitive','mean'),
    total_cost=('total_cost','sum'),
    avg_roas=('avg_roas','mean'),
    problematic=('is_problematic','sum')
).round(1).sort_values('avg_health', ascending=False)
print(ind.to_string())

# Save comparison tables
ct.to_csv('work/campaign_type_summary.csv')
bs.to_csv('work/bidding_summary.csv')
ind.to_csv('work/industry_summary.csv')
print("\nSaved CSV files.")

# Health score distribution quartiles
print("\nHealth score quartiles:")
print(campaigns['health_score'].describe().round(2))