import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# Reload device and geo data
r = db.query("""
SELECT d.year_month, d.campaign_id, d.device_type, d.cost, d.roas, d.quality_score, 
  d.impression_share, d.ctr, d.conversion_rate, d.conversions, d.conversion_value,
  d.cpc, d.cost_per_conversion
FROM google_ads__device_report d
ORDER BY d.campaign_id, d.year_month, d.device_type
""", parameters=[])
device = db.frame(r)

r = db.query("""
SELECT g.year_month, g.campaign_id, g.geo_target, g.cost, g.roas, g.quality_score,
  g.impression_share, g.ctr, g.conversion_rate, g.conversions, g.conversion_value,
  g.cpc, g.cost_per_conversion
FROM google_ads__geo_report g
ORDER BY g.campaign_id, g.year_month, g.geo_target
""", parameters=[])
geo = db.frame(r)

r = db.query("""
SELECT year_month, SUM(cost) AS total_cost, SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv, AVG(roas) AS avg_roas,
  AVG(quality_score) AS avg_qs, AVG(impression_share) AS avg_is,
  AVG(ctr) AS avg_ctr, AVG(conversion_rate) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY year_month ORDER BY year_month
""", parameters=[])
monthly = db.frame(r)

# YoY comparison
monthly['year'] = monthly['year_month'].str[:4].astype(int)
monthly['month'] = monthly['year_month'].str[5:7].astype(int)
monthly['month_label'] = monthly['year_month'].str[5:7]

yoy_23 = monthly[(monthly['year']==2023) & (monthly['month']>=2)].set_index('month')
yoy_24 = monthly[(monthly['year']==2024) & (monthly['month']<=6)].set_index('month')
overlap = sorted(set(yoy_23.index) & set(yoy_24.index))
yoy_rows = []
for m in overlap:
    r23 = yoy_23.loc[m]
    r24 = yoy_24.loc[m]
    yoy_rows.append({
        'month': f"2024-{m:02d}",
        'cost_yoy_pct': (r24['total_cost'] - r23['total_cost']) / r23['total_cost'] * 100,
        'cv_yoy_pct': (r24['total_cv'] - r23['total_cv']) / r23['total_cv'] * 100,
        'conv_yoy_pct': (r24['total_conversions'] - r23['total_conversions']) / r23['total_conversions'] * 100,
        'roas_23': r23['avg_roas'], 'roas_24': r24['avg_roas'],
    })
yoy_df = pd.DataFrame(yoy_rows)
print("YoY growth (2024 vs 2023):")
print(yoy_df.round(2))

# Figures
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Device metrics
device_agg = device.groupby('device_type').agg(
    avg_roas=('roas', 'mean'), avg_qs=('quality_score', 'mean'),
    avg_is=('impression_share', 'mean'), avg_cvr=('conversion_rate', 'mean'),
    avg_ctr=('ctr', 'mean'), total_cost=('cost', 'sum')).reset_index()
metrics = ['avg_roas', 'avg_qs', 'avg_is', 'avg_cvr', 'avg_ctr']
x = np.arange(len(device_agg['device_type']))
width = 0.15
for i, m in enumerate(metrics):
    axes[0,0].bar(x + i*width, device_agg[m], width, label=m.replace('avg_',''))
axes[0,0].set_xticks(x + width*2)
axes[0,0].set_xticklabels(device_agg['device_type'])
axes[0,0].set_title('Device Type Performance Metrics')
axes[0,0].legend(fontsize=8)
print("\nDevice aggregates:\n", device_agg.round(4))

# Geo roas
geo_agg = geo.groupby('geo_target').agg(avg_roas=('roas','mean'), avg_qs=('quality_score','mean'),
    total_cost=('cost','sum')).reset_index().sort_values('avg_roas', ascending=False)
sns.barplot(x='geo_target', y='avg_roas', data=geo_agg, ax=axes[0,1], palette='viridis')
axes[0,1].set_title('Average ROAS by Geo Target')
axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=30)
print("\nGeo aggregates:\n", geo_agg.round(4))

# Monthly trend
monthly_sorted = monthly.sort_values('year_month')
ax2 = axes[1,0]
color = 'tab:blue'
ax2.plot(monthly_sorted['year_month'], monthly_sorted['total_cost'], color=color, marker='o', label='Total Cost')
ax2.set_ylabel('Total Cost', color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax3 = ax2.twinx()
color = 'tab:red'
ax3.plot(monthly_sorted['year_month'], monthly_sorted['avg_roas'], color=color, marker='s', label='Avg ROAS')
ax3.set_ylabel('Avg ROAS', color=color)
ax3.tick_params(axis='y', labelcolor=color)
ax2.set_title('Monthly Trend: Total Cost and Average ROAS')

# Device cost for problematic vs healthy
problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]
device['is_problematic'] = device['campaign_id'].isin(problematic_ids)
device_pivot = device.groupby(['device_type', 'is_problematic'])['cost'].sum().unstack(fill_value=0)
device_pivot.columns = ['Healthy', 'Problematic']
device_pivot.plot(kind='bar', ax=axes[1,1], color=['#4C9F70', '#D9534F'])
axes[1,1].set_title('Total Cost by Device Type: Problematic vs Healthy')
axes[1,1].set_ylabel('Total Cost')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('device_geo_trend.png', dpi=100)
print("Saved device_geo_trend.png")

# Seasonal fluctuation: month-over-month index using same-year data (2023 full year)
print("\nSeasonal pattern (2023 full year cost share):")
seasonal_23 = monthly[monthly['year']==2023].sort_values('month')
seasonal_23['cost_share'] = seasonal_23['total_cost'] / seasonal_23['total_cost'].sum() * 100
seasonal_23['cv_share'] = seasonal_23['total_cv'] / seasonal_23['total_cv'].sum() * 100
print(seasonal_23[['month_label','total_cost','cost_share','cv_share']].round(2))