import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df_rd = pd.read_csv('/work/region_device_monthly.csv')
df_rd['month_dt'] = pd.to_datetime(df_rd['month'] + '-01')
df_rd['month_num'] = (df_rd['month_dt'] - df_rd['month_dt'].min()).dt.days / 30.0
df_rd['conv_rate'] = 100.0 * df_rd['acquisitions'] / df_rd['visitors']
df_rd['cost_per_acq'] = df_rd['visitors'] / df_rd['acquisitions']
df_rd['installs_per_acq'] = df_rd['installs'] / df_rd['acquisitions']
df_rd['update_rate'] = df_rd['updates'] / df_rd['actives'] * 1000

# =============================================
# 1. Acquisition Cost-Efficiency Decay Patterns
# =============================================
print("=" * 60)
print("ANALYSIS 1: ACQUISITION COST-EFFICIENCY DECAY")
print("=" * 60)

monthly_region = df_rd.groupby(['region', 'month_num', 'month'])['conv_rate'].mean().reset_index()
print("\nMonthly conversion rate by region:")
print(monthly_region.pivot_table(index='month', columns='region', values='conv_rate').round(3))

# Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()
for i, region in enumerate(sorted(df_rd['region'].unique())):
    sub = df_rd[df_rd['region'] == region].copy()
    for dev in sub['device'].unique():
        dev_sub = sub[sub['device'] == dev]
        slope, intercept, r, p, se = stats.linregress(dev_sub['month_num'], dev_sub['conv_rate'])
        axes[i].plot(dev_sub['month_num'], dev_sub['conv_rate'], 'o-', alpha=0.3, label='_nolegend_')
        axes[i].plot(dev_sub['month_num'], intercept + slope * dev_sub['month_num'], '--', alpha=0.3)
    region_sub = sub.groupby('month_num')['conv_rate'].mean().reset_index()
    slope, intercept, r, p, se = stats.linregress(region_sub['month_num'], region_sub['conv_rate'])
    axes[i].plot(region_sub['month_num'], region_sub['conv_rate'], 'o-', color='red', linewidth=2.5, label='Region avg')
    axes[i].plot(region_sub['month_num'], intercept + slope * region_sub['month_num'], '--', color='black', linewidth=2)
    axes[i].set_title(f'{region} - Decay slope: {slope:.4f} (p={p:.4f})')
    axes[i].set_xlabel('Months from start')
    axes[i].set_ylabel('Store Listing Conversion Rate (%)')
    axes[i].legend()
    axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig1_region_decay.png', dpi=100)
plt.close()
print("Saved fig1_region_decay.png")

# Cost per acquisition
print("\n\nCost per acquisition (visitors per acquisition) by region:")
cost_reg = df_rd.groupby(['region', 'month'])['cost_per_acq'].mean().reset_index()
print(cost_reg.pivot_table(index='month', columns='region', values='cost_per_acq').round(2))

print("\nCost-per-acquisition decay slopes:")
for region in sorted(df_rd['region'].unique()):
    sub = df_rd[df_rd['region'] == region].groupby('month_num')['cost_per_acq'].mean().reset_index()
    slope, intercept, r, p, se = stats.linregress(sub['month_num'], sub['cost_per_acq'])
    print(f"  {region}: slope={slope:.4f} (p={p:.4f}) - {'increasing cost (worsening)' if slope > 0 else 'decreasing cost (improving)'}")

# Device-level metrics
print("\n\nAverage conversion rate by device type:")
dev_avg = df_rd.groupby('device')[['conv_rate', 'cost_per_acq', 'installs_per_acq', 'update_rate', 'actives']].mean().round(3)
print(dev_avg.sort_values('conv_rate', ascending=False))

# Region×Device decay slopes
print("\n\nRegion×Device decay slopes (conversion rate over time):")
decay_results = []
for region in sorted(df_rd['region'].unique()):
    for dev in sorted(df_rd['device'].unique()):
        sub = df_rd[(df_rd['region'] == region) & (df_rd['device'] == dev)]
        slope, intercept, r, p, se = stats.linregress(sub['month_num'], sub['conv_rate'])
        avg_conv = sub['conv_rate'].mean()
        decay_results.append({'region': region, 'device': dev, 'decay_slope': slope, 'p_value': p, 'avg_conv': avg_conv, 'r_squared': r**2})

df_decay = pd.DataFrame(decay_results)
print("Decay slopes (negative = efficiency declining):")
print(df_decay.pivot_table(index='device', columns='region', values='decay_slope').round(4))
print("\nP-values:")
print(df_decay.pivot_table(index='device', columns='region', values='p_value').round(4))

# Save decay results
df_decay.to_csv('/work/decay_slopes.csv', index=False)