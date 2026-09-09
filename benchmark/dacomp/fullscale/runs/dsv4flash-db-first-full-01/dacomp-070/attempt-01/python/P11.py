import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

df_daily_rp = pd.read_csv('/work/daily_region_package.csv')
df_daily_rp['date_dt'] = pd.to_datetime(df_daily_rp['date_day'])

# =============================================
# DEEPER NON-LINEAR ANALYSIS
# =============================================
print("=" * 60)
print("DEEPER: Non-linear relationship via binned means & interaction")
print("=" * 60)

# Binned means for quality
print("\n--- Binned means: conversion rate vs quality (10 bins) ---")
df_daily_rp['quality_bin'] = pd.cut(df_daily_rp['quality'], 10)
binned_q = df_daily_rp.groupby('quality_bin', observed=True)['conv_rate'].agg(['mean', 'count']).round(3)
print(binned_q)

print("\n--- Binned means: conversion rate vs crash (10 bins) ---")
df_daily_rp['crash_bin'] = pd.cut(df_daily_rp['crash'], 10)
binned_c = df_daily_rp.groupby('crash_bin', observed=True)['conv_rate'].agg(['mean', 'count']).round(3)
print(binned_c)

# Is there a combined / interaction effect? model conv ~ quality*crash
x = df_daily_rp[['quality', 'crash']].values
y = df_daily_rp['conv_rate'].values
X = np.column_stack([np.ones(len(x)), x[:,0], x[:,1], x[:,0]*x[:,1]])
beta = np.linalg.lstsq(X, y, rcond=None)[0]
y_pred = X @ beta
ss_res = np.sum((y-y_pred)**2)
ss_tot = np.sum((y-y.mean())**2)
print(f"\nInteraction model conv ~ q + c + q*c: R² = {1-ss_res/ss_tot:.4f}")
print(f"  coeffs: intercept={beta[0]:.3f}, quality={beta[1]:.3f}, crash={beta[2]:.3f}, q*c={beta[3]:.3f}")

# Full model with package/region fixed effects proxies and time
print("\n--- Full model: conv ~ q + c + q² + log(c) + active scale + time ---")
res = db.query("""
SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       SUM(cr.store_listing_visitors) AS visitors,
       SUM(cr.store_listing_acquisitions) AS acquisitions,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad, AVG(ts.active_devices) AS active_devices,
       AVG(ts.daily_churn_rate) AS churn
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name
""")
df_full = db.frame(res)
df_full['date_dt'] = pd.to_datetime(df_full['date_day'])
df_full['time_idx'] = (df_full['date_dt'] - df_full['date_dt'].min()).dt.days
df_full['region_code'] = df_full['region'].astype('category').cat.codes
df_full['pkg_code'] = df_full['package_name'].astype('category').cat.codes

# Encode region and package as dummies
region_dummies = pd.get_dummies(df_full['region'], prefix='r', drop_first=True)
pkg_dummies = pd.get_dummies(df_full['package_name'], prefix='p', drop_first=True)

X = np.column_stack([
    df_full['quality'].values,
    df_full['quality'].values**2,
    np.log(df_full['crash'].values + 0.001),
    df_full['crash'].values,
    df_full['rpad'].values,
    np.log(df_full['active_devices'].values),
    df_full['time_idx'].values,
    region_dummies.values,
    pkg_dummies.values,
])
y = df_full['conv_rate'].values
Xc = np.column_stack([np.ones(len(X)), X])
beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
y_pred = Xc @ beta
ss_res = np.sum((y-y_pred)**2)
ss_tot = np.sum((y-y.mean())**2)
n, k = Xc.shape
r2 = 1 - ss_res/ss_tot
adj_r2 = 1 - (1-r2)*(n-1)/(n-k-1)
print(f"  R² = {r2:.4f}, adj R² = {adj_r2:.4f}, n={n}")
feat_names = ['intercept', 'quality', 'quality²', 'log(crash)', 'crash', 'rpad', 'log(active)', 'time'] + list(region_dummies.columns) + list(pkg_dummies.columns)
for fn, b in zip(feat_names, beta):
    print(f"    {fn}: {b:.4f}")

# Check correlation of log(active) with conversion
print("\nCorrelation: log(active_devices) vs conv_rate:", np.corrcoef(np.log(df_full['active_devices'].values), y)[0,1])

# =============================================
# USER VALUE DECAY: rpad vs scale (maturity)
# =============================================
print("\n\n--- USER VALUE DECAY: revenue per active device vs market scale ---")
# Using daily package data
df_daily = pd.read_csv('/work/daily_timeseries.csv')
df_daily['date_dt'] = pd.to_datetime(df_daily['date_dt'])

# Define market maturity by active device scale per package
print("\nPackage scale (active devices) deciles:")
df_daily['scale_bin'] = pd.qcut(df_daily['active_devices'], 10, labels=False, duplicates='drop')
print(df_daily.groupby('scale_bin')['revenue_per_active_device'].agg(['mean', 'count']).round(5))

# Correlation between rpad and active devices (log-log)
print("\nLog-log relationship: rpad vs active_devices")
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    r = np.corrcoef(np.log(sub['active_devices']), np.log(sub['revenue_per_active_device']))[0,1]
    slope = np.polyfit(np.log(sub['active_devices']), np.log(sub['revenue_per_active_device']), 1)[0]
    print(f"  {pkg.split('.')[-1]}: corr(log-active, log-rpad) = {r:.4f}, elasticity = {slope:.4f}")

# Model rpad with quality, crash, churn, active
print("\n--- Full daily rpad model (multi-dimensional) ---")
X = df_daily[['quality_score', 'crash_rate_per_1k', 'daily_churn_rate', 'anr_rate_per_1k', 'active_devices']].values
y = df_daily['revenue_per_active_device'].values
Xc = np.column_stack([np.ones(len(X)), X, np.log(df_daily['active_devices'].values)])
beta = np.linalg.lstsq(Xc, y, rcond=None)[0]
y_pred = Xc @ beta
ss_res = np.sum((y-y_pred)**2)
ss_tot = np.sum((y-y.mean())**2)
r2 = 1 - ss_res/ss_tot
n, k = Xc.shape
adj_r2 = 1 - (1-r2)*(n-1)/(n-k-1)
print(f"  R² = {r2:.4f}, adj R² = {adj_r2:.4f}")
names = ['intercept', 'quality', 'crash', 'churn', 'anr', 'active', 'log(active)']
for fn, b in zip(names, beta):
    print(f"    {fn}: {b:.6f}")

# Per-package elasticity of rpad vs active (value decay curve)
print("\n--- Value decay elasticity per package (rpad vs active) ---")
decay_curves = []
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    slope, intercept, r, p_val, se = stats.linregress(np.log(sub['active_devices']), np.log(sub['revenue_per_active_device']))
    decay_curves.append({'package': pkg.split('.')[-1], 'elasticity': slope, 'r': r, 'p': p_val})
df_decay_curves = pd.DataFrame(decay_curves)
print(df_decay_curves.round(4))

# Plot value decay curves by package
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
ax = axes[0]
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    ax.scatter(sub['active_devices'], sub['revenue_per_active_device'], alpha=0.3, s=8, label=pkg.split('.')[-1])
ax.set_xlabel('Active Devices')
ax.set_ylabel('Revenue per Active Device')
ax.set_title('User Value Decay: rpad vs Market Scale')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

ax = axes[1]
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    ax.scatter(np.log(sub['active_devices']), np.log(sub['revenue_per_active_device']), alpha=0.3, s=8, label=pkg.split('.')[-1])
ax.set_xlabel('log(Active Devices)')
ax.set_ylabel('log(rpad)')
ax.set_title('Log-Log: Value Decay Elasticity (negative slope = decay)')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig6_value_decay_curves.png', dpi=100)
plt.close()
print("Saved fig6_value_decay_curves.png")