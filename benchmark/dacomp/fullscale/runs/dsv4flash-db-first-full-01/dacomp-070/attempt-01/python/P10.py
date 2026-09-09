import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =============================================
# ADDITIONAL: Daily-level non-linear relationship
# =============================================
print("=" * 60)
print("SUPPLEMENTAL: Daily Non-linear Relationship Analysis")
print("=" * 60)

# Fetch daily data: conversion rate, quality, crash
res = db.query("""
SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name
HAVING SUM(cr.store_listing_visitors) > 0
ORDER BY cr.date_day, cr.region, cr.package_name
""")
df_daily_rp = db.frame(res)
df_daily_rp['date_dt'] = pd.to_datetime(df_daily_rp['date_day'])
print("Daily region×package data shape:", df_daily_rp.shape)

# Check non-linear relationship at daily level
print("\n--- Daily-level correlation ---")
print("Pearson: conv_rate vs quality:", df_daily_rp['conv_rate'].corr(df_daily_rp['quality']))
print("Pearson: conv_rate vs crash:", df_daily_rp['conv_rate'].corr(df_daily_rp['crash']))

# By region
print("\n--- By region ---")
for region in df_daily_rp['region'].unique():
    sub = df_daily_rp[df_daily_rp['region'] == region]
    print(f"\n{region}:")
    r_q = sub['conv_rate'].corr(sub['quality'])
    r_c = sub['conv_rate'].corr(sub['crash'])
    print(f"  conv vs quality: r={r_q:.4f}")
    print(f"  conv vs crash: r={r_c:.4f}")
    
    # Quadratic fit for quality
    x = sub['quality'].values
    y = sub['conv_rate'].values
    coeffs = np.polyfit(x, y, 2)
    p = np.poly1d(coeffs)
    y_pred = p(x)
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2_q = 1 - ss_res/ss_tot
    print(f"  Quadratic (quality) R² = {r2_q:.4f}: conv = {coeffs[2]:.3f} + {coeffs[1]:.3f}*q + {coeffs[0]:.4f}*q²")
    
    # Log fit for crash
    x2 = sub['crash'].values
    log_x = np.log(x2 + 0.001)
    slope, intercept, r, p_val, se = stats.linregress(log_x, y)
    y_pred_log = intercept + slope * log_x
    ss_res_log = np.sum((y - y_pred_log)**2)
    r2_c_log = 1 - ss_res_log/ss_tot
    print(f"  Log(crash) R² = {r2_c_log:.4f}: conv = {intercept:.3f} + {slope:.3f}*log(crash)")

# By package
print("\n--- By package ---")
for pkg in df_daily_rp['package_name'].unique():
    sub = df_daily_rp[df_daily_rp['package_name'] == pkg]
    r_q = sub['conv_rate'].corr(sub['quality'])
    r_c = sub['conv_rate'].corr(sub['crash'])
    print(f"{pkg.split('.')[-1]}: conv vs quality r={r_q:.4f}, vs crash r={r_c:.4f}")

# Visualize by region-package combination
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
axes = axes.flatten()
idx = 0
for region in sorted(df_daily_rp['region'].unique()):
    for pkg in sorted(df_daily_rp['package_name'].unique()):
        sub = df_daily_rp[(df_daily_rp['region'] == region) & (df_daily_rp['package_name'] == pkg)]
        if len(sub) < 5:
            continue
        ax = axes[idx]
        ax.scatter(sub['quality'], sub['conv_rate'], alpha=0.5, s=5, label='quality')
        ax.scatter(sub['crash'], sub['conv_rate'], alpha=0.3, s=5, c='red', label='crash')
        ax.set_title(f'{region} - {pkg.split(".")[-1]}')
        ax.set_xlabel('Score')
        ax.set_ylabel('Conv Rate (%)')
        ax.legend(fontsize=6)
        ax.grid(True, alpha=0.3)
        idx += 1
        if idx >= 8:
            break
    if idx >= 8:
        break

plt.tight_layout()
plt.savefig('/work/fig5_daily_nonlinear_detailed.png', dpi=100)
plt.close()
print("Saved fig5_daily_nonlinear_detailed.png")

# Let me also look at the relationship between quality and crash more carefully
print("\n\n--- Quality vs Crash relationship ---")
print("Pearson correlation between quality_score and crash_rate_per_1k:", df_daily_rp['quality'].corr(df_daily_rp['crash']))

# Check if there's a threshold effect
print("\n--- Threshold analysis: conversion rate by quality quartiles ---")
df_daily_rp['quality_q'] = pd.qcut(df_daily_rp['quality'], 4, labels=['Q1_low', 'Q2', 'Q3', 'Q4_high'])
print(df_daily_rp.groupby('quality_q', observed=True)['conv_rate'].describe().round(3))

print("\n--- Threshold analysis: conversion rate by crash quartiles ---")
df_daily_rp['crash_q'] = pd.qcut(df_daily_rp['crash'], 4, labels=['Q1_low', 'Q2', 'Q3', 'Q4_high'])
print(df_daily_rp.groupby('crash_q', observed=True)['conv_rate'].describe().round(3))

# Save daily data
df_daily_rp.to_csv('/work/daily_region_package.csv', index=False)