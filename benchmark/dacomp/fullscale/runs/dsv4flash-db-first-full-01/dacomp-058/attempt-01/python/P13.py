import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Verify screening criteria
r = db.query("""
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS total_months,
  COUNT(CASE WHEN cost > 1000 AND roas < 0.8 THEN 1 END) AS screened_months
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY screened_months DESC
""", parameters=[])
screen = db.frame(r)
print("Screening results (monthly cost > 1000 AND ROAS < 0.8):")
print(screen.to_string(index=False))
print("\nTotal months screened:", screen['screened_months'].sum(), "across", (screen['screened_months']>0).sum(), "campaigns")

# All months have cost > 1000, so the screen is ROAS < 0.8
r = db.query("SELECT COUNT(DISTINCT campaign_id) AS campaigns_with_bad_roas FROM google_ads__campaign_report WHERE roas < 0.8", parameters=[])
print(db.frame(r))

# Cost share of problematic campaigns
r = db.query("""
SELECT 
  ROUND(SUM(CASE WHEN campaign_id IN ({}) THEN cost ELSE 0 END),0) AS prob_cost,
  ROUND(SUM(cost),0) AS total_cost,
  ROUND(100.0 * SUM(CASE WHEN campaign_id IN ({}) THEN cost ELSE 0 END)/SUM(cost), 1) AS pct
FROM google_ads__campaign_report
""".format(','.join(str(x) for x in problematic_ids), ','.join(str(x) for x in problematic_ids)), parameters=[])
print("\nProblematic cost share:", db.frame(r).to_string(index=False))

# Monthly trend of health score for problematic campaigns (compute health score monthly for problematic)
r = db.query("""
WITH base AS (
  SELECT year_month, campaign_id, cost, roas, cpc, cost_per_conversion, conversion_rate,
    conversions, conversion_value, quality_score, impression_share, ctr
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
SELECT year_month, campaign_id,
  100.0 * (0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS hs
FROM norm
WHERE campaign_id IN ({})
ORDER BY year_month
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
hs_monthly = db.frame(r)
print("\nHealth score monthly data shape:", hs_monthly.shape)

# Plot monthly health score trend for problematic campaigns
fig, ax = plt.subplots(figsize=(12, 6))
for cid, grp in hs_monthly.groupby('campaign_id'):
    ax.plot(grp['year_month'], grp['hs'], marker='o', ms=4, label=f"C{cid}")
ax.set_title('Monthly Health Score Trend - Problematic Campaigns')
ax.set_ylabel('Health Score')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.legend(fontsize=8, ncol=2)
ax.axhline(36, color='orange', ls='--', lw=1)
plt.tight_layout()
plt.savefig('problematic_health_trend.png', dpi=100)
print("Saved problematic_health_trend.png")

# YoY growth for problematic campaigns (cost comparison)
r = db.query("""
SELECT year_month, ROUND(SUM(cost),0) AS total_cost, ROUND(SUM(conversion_value),0) AS total_cv,
  ROUND(SUM(conversions),2) AS total_conv, ROUND(AVG(roas),3) AS avg_roas
FROM google_ads__campaign_report
WHERE campaign_id IN ({})
GROUP BY year_month ORDER BY year_month
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
prob_m = db.frame(r)
prob_m['year'] = prob_m['year_month'].str[:4].astype(int)
prob_m['month'] = prob_m['year_month'].str[5:7].astype(int)
p23 = prob_m[(prob_m['year']==2023) & (prob_m['month']>=2)].set_index('month')
p24 = prob_m[(prob_m['year']==2024) & (prob_m['month']<=6)].set_index('month')
print("\nProblematic campaigns YoY:")
for m in sorted(set(p23.index) & set(p24.index)):
    c_growth = (p24.loc[m,'total_cost'] - p23.loc[m,'total_cost'])/p23.loc[m,'total_cost']*100
    print(f"  2024-{m:02d}: cost YoY {c_growth:+.1f}%")

# Seasonal fluctuation for problematic campaigns (2023)
prob_23 = prob_m[prob_m['year']==2023]
print("\nProblematic campaigns 2023 monthly cost (seasonal pattern):")
print(prob_23[['year_month','total_cost']].to_string(index=False))