import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]

# Geo breakdown for problematic campaigns
r = db.query("""
SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr, ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN ({})
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, cost DESC
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
geo_prob = db.frame(r)
print("Geo breakdown for problematic campaigns:")
print(geo_prob.to_string(index=False))

# Geo ROAS by geo_target for problematic campaigns
geo_prob['roas_computed'] = geo_prob['cv'] / geo_prob['cost'].clip(lower=1)
print("\nGeo-level computed ROAS (cv/cost):")
print(geo_prob[['campaign_id','geo_target','cost','roas_computed','avg_roas']].round(3).to_string(index=False))

# Keyword optimization analysis
r = db.query("""
SELECT k.* FROM google_ads__keyword_report k
WHERE k.campaign_id IN ({})
ORDER BY k.campaign_id, k.year_quarter
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
kw_prob = db.frame(r)

if len(kw_prob) > 0:
    kw_agg = kw_prob.groupby(['campaign_id','keyword_text','match_type']).agg(
        impressions=('impressions','sum'), clicks=('clicks','sum'), cost=('cost','sum'),
        conversions=('conversions','sum'), cv=('conversion_value','sum'),
        qs=('quality_score','mean'), avg_pos=('avg_position','mean')).reset_index()
    kw_agg['cost_per_conv'] = kw_agg['cost'] / kw_agg['conversions'].clip(lower=0.001)
    kw_agg['roas'] = kw_agg['cv'] / kw_agg['cost'].clip(lower=1)
    kw_agg = kw_agg.sort_values(['campaign_id','cost'], ascending=[True,False])
    print("\nKeyword-level metrics for problematic campaigns:")
    print(kw_agg[['campaign_id','keyword_text','match_type','cost','conversions','cost_per_conv','roas','qs','avg_pos']].round(2).to_string(index=False))

# Monthly trend for problematic campaigns specifically
r = db.query("""
SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  cost, roas, quality_score, impression_share, ctr, conversion_rate, conversions, conversion_value
FROM google_ads__campaign_report
WHERE campaign_id IN ({})
ORDER BY campaign_id, year_month
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
prob_monthly = db.frame(r)
print("\n\nProblematic campaigns monthly data shape:", prob_monthly.shape)
print(prob_monthly.head(20))

# Monthly trend for problematic campaigns
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Cost trend per problematic campaign
for cid, grp in prob_monthly.groupby('campaign_id'):
    axes[0,0].plot(grp['year_month'], grp['cost'], marker='o', label=f"Campaign {cid} ({grp['campaign_type'].iloc[0]})")
axes[0,0].set_title('Monthly Cost Trend - Problematic Campaigns')
axes[0,0].set_xticklabels(axes[0,0].get_xticklabels(), rotation=45)
axes[0,0].legend(fontsize=7)

# ROAS (roas field) trend
for cid, grp in prob_monthly.groupby('campaign_id'):
    axes[0,1].plot(grp['year_month'], grp['roas'], marker='s', label=f"Campaign {cid}")
axes[0,1].set_title('Monthly ROAS Trend - Problematic Campaigns')
axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=45)
axes[0,1].legend(fontsize=7)

# Geo cost for problematic - stacked bar
geo_pivot = geo_prob.pivot_table(index='geo_target', columns='campaign_id', values='cost', aggfunc='sum', fill_value=0)
geo_pivot.plot(kind='bar', stacked=True, ax=axes[1,0], colormap='tab10')
axes[1,0].set_title('Cost by Geo Target (Problematic Campaigns)')
axes[1,0].set_xticklabels(axes[1,0].get_xticklabels(), rotation=30)

# Device cost for problematic - stacked bar
dev_prob_res = db.query("""
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost
FROM google_ads__device_report
WHERE campaign_id IN ({})
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type
""".format(','.join(str(x) for x in problematic_ids)), parameters=[])
dev_prob = db.frame(dev_prob_res)
dev_pivot = dev_prob.pivot_table(index='device_type', columns='campaign_id', values='cost', aggfunc='sum', fill_value=0)
dev_pivot.plot(kind='bar', stacked=True, ax=axes[1,1], colormap='tab10')
axes[1,1].set_title('Cost by Device Type (Problematic Campaigns)')
axes[1,1].set_xticklabels(axes[1,1].get_xticklabels(), rotation=0)

plt.tight_layout()
plt.savefig('problematic_breakdown.png', dpi=100)
print("Saved problematic_breakdown.png")