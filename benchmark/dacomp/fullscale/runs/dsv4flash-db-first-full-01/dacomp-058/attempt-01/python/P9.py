import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os, warnings
warnings.filterwarnings('ignore')

# Device-level analysis: compute health-like metrics by device type
r = db.query("""
SELECT d.year_month, d.campaign_id, d.device_type, d.cost, d.roas, d.quality_score, 
  d.impression_share, d.ctr, d.conversion_rate, d.conversions, d.conversion_value,
  d.cpc, d.cost_per_conversion
FROM google_ads__device_report d
ORDER BY d.campaign_id, d.year_month, d.device_type
""", parameters=[])
device = db.frame(r)
print("Device data shape:", device.shape)
print("Device types:", device['device_type'].value_counts())

# Geo-level analysis
r = db.query("""
SELECT g.year_month, g.campaign_id, g.geo_target, g.cost, g.roas, g.quality_score,
  g.impression_share, g.ctr, g.conversion_rate, g.conversions, g.conversion_value,
  g.cpc, g.cost_per_conversion
FROM google_ads__geo_report g
ORDER BY g.campaign_id, g.year_month, g.geo_target
""", parameters=[])
geo = db.frame(r)
print("Geo data shape:", geo.shape)
print("Geo targets:", geo['geo_target'].value_counts())

# Monthly trend data
r = db.query("""
SELECT year_month, 
  SUM(cost) AS total_cost,
  SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv,
  AVG(roas) AS avg_roas,
  AVG(quality_score) AS avg_qs,
  AVG(impression_share) AS avg_is,
  AVG(ctr) AS avg_ctr,
  AVG(conversion_rate) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY year_month
ORDER BY year_month
""", parameters=[])
monthly = db.frame(r)
print("Monthly data shape:", monthly.shape)
print(monthly.head(20))

# Compute YoY growth rates (compare 2024 months to 2023 same months)
# Data spans 2023-02 to 2024-06
monthly['year'] = monthly['year_month'].str[:4].astype(int)
monthly['month'] = monthly['year_month'].str[5:7].astype(int)
monthly['month_label'] = monthly['year_month'].str[5:7]

# YoY comparison - only months that exist in both years
# 2023 months: 02-12, 2024 months: 01-06
# For YoY, we need same month: 2023-02 vs 2024-02, 2023-03 vs 2024-03, etc.
yoy = monthly[monthly['year'] == 2023].copy()
yoy24 = monthly[monthly['year'] == 2024].copy()
yoy = yoy[yoy['month'].isin([2,3,4,5,6])].sort_values('month')
yoy24 = yoy24[yoy24['month'].isin([2,3,4,5,6])].sort_values('month')

print("\nYoY comparison (Feb-Jun):")
for i, (_, r23) in enumerate(yoy.iterrows()):
    _, r24 = yoy24.iloc[i]
    m = r23['month_label']
    cost_growth = (r24['total_cost'] - r23['total_cost']) / r23['total_cost'] * 100
    cv_growth = (r24['total_cv'] - r23['total_cv']) / r23['total_cv'] * 100
    print(f"Month {m}: Cost YoY: {cost_growth:+.1f}%, CV YoY: {cv_growth:+.1f}%")

# Figures: Device and Geo comparisons
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Device: avg roas by device type
device_agg = device.groupby('device_type').agg(
    avg_roas=('roas', 'mean'),
    avg_qs=('quality_score', 'mean'),
    avg_is=('impression_share', 'mean'),
    avg_cvr=('conversion_rate', 'mean'),
    avg_ctr=('ctr', 'mean'),
    total_cost=('cost', 'sum')
).reset_index()
print("\nDevice-level aggregates:")
print(device_agg)

# Plot device metrics
metrics = ['avg_roas', 'avg_qs', 'avg_is', 'avg_cvr', 'avg_ctr']
x = np.arange(len(device_agg['device_type']))
width = 0.15
for i, m in enumerate(metrics):
    axes[0,0].bar(x + i*width, device_agg[m], width, label=m.replace('avg_',''))
axes[0,0].set_xticks(x + width*2)
axes[0,0].set_xticklabels(device_agg['device_type'])
axes[0,0].set_title('Device Type Performance Metrics')
axes[0,0].legend()

# Geo: roas by geo target
geo_agg = geo.groupby('geo_target').agg(
    avg_roas=('roas', 'mean'),
    avg_qs=('quality_score', 'mean'),
    total_cost=('cost', 'sum')
).reset_index().sort_values('avg_roas', ascending=False)
print("\nGeo-level aggregates:")
print(geo_agg)

sns.barplot(x='geo_target', y='avg_roas', data=geo_agg, ax=axes[0,1], palette='viridis')
axes[0,1].set_title('Average ROAS by Geo Target')
axes[0,1].set_xticklabels(axes[0,1].get_xticklabels(), rotation=30)

# Monthly trend: cost and avg_roas
monthly_sorted = monthly.sort_values('year_month')
ax2 = axes[1,0]
color = 'tab:blue'
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Cost', color=color)
ax2.plot(monthly_sorted['year_month'], monthly_sorted['total_cost'], color=color, marker='o', label='Total Cost')
ax2.tick_params(axis='y', labelcolor=color)
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
ax3 = ax2.twinx()
color = 'tab:red'
ax3.set_ylabel('Avg ROAS', color=color)
ax3.plot(monthly_sorted['year_month'], monthly_sorted['avg_roas'], color=color, marker='s', label='Avg ROAS')
ax3.tick_params(axis='y', labelcolor=color)
ax2.set_title('Monthly Trend: Total Cost and Average ROAS')
plt.tight_layout()

# Cost by device type for problematic vs healthy
# We need to join device data with campaign info
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