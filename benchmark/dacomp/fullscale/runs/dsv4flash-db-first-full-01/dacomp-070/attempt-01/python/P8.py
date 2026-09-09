import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =============================================
# 3. MULTI-DIMENSIONAL USER VALUE DECAY MODEL
# =============================================
print("=" * 60)
print("ANALYSIS 3: MULTI-DIMENSIONAL USER VALUE DECAY MODEL")
print("=" * 60)

# Load daily-level data for more granular analysis
res = db.query("""
SELECT date_day, package_name, quality_score, crash_rate_per_1k, anr_rate_per_1k,
       revenue_per_active_device, active_devices, daily_churn_rate,
       daily_install_uninstall_ratio, wow_install_growth_rate, 
       daily_revenue, avg_transaction_value,
       ma_7d_quality, ma_30d_quality, ma_7d_churn,
       install_volatility_coefficient, revenue_volatility_coefficient,
       install_trend, revenue_trend, risk_growth_profile, performance_momentum,
       install_stability
FROM google_play__time_series_trends
ORDER BY package_name, date_day
""")
df_daily = db.frame(res)
df_daily['date_dt'] = pd.to_datetime(df_daily['date_day'])
df_daily['month'] = df_daily['date_dt'].dt.to_period('M').astype(str)
df_daily['days_from_start'] = (df_daily['date_dt'] - df_daily['date_dt'].min()).dt.days
print("Daily data shape:", df_daily.shape)

# Define market maturity based on install trend and active devices
# Mature: declining or stable installs, high active base
# Growing: increasing installs, rapid growth
# Emerging: early stage, low base
print("\n--- Market Maturity Classification ---")
print("Install trend distribution:")
print(df_daily['install_trend'].value_counts())
print("\nRevenue trend distribution:")
print(df_daily['revenue_trend'].value_counts())
print("\nRisk growth profile:")
print(df_daily['risk_growth_profile'].value_counts())

# Create market maturity score
# Using wow_install_growth_rate, active_devices, and install_trend
df_daily['maturity_group'] = 'unknown'
# High growth: wow_inst > 0.02
# Stable: -0.02 <= wow_inst <= 0.02
# Declining: wow_inst < -0.02
df_daily.loc[df_daily['wow_install_growth_rate'] > 0.02, 'maturity_group'] = 'growing'
df_daily.loc[(df_daily['wow_install_growth_rate'] >= -0.02) & (df_daily['wow_install_growth_rate'] <= 0.02), 'maturity_group'] = 'stable'
df_daily.loc[df_daily['wow_install_growth_rate'] < -0.02, 'maturity_group'] = 'declining'

print("\nMaturity group distribution:")
print(df_daily['maturity_group'].value_counts())

# Build multi-dimensional model for rpad
print("\n\n--- User Value Decay Model: Revenue per Active Device ---")
print("Descriptive statistics by maturity group:")
print(df_daily.groupby('maturity_group')[['revenue_per_active_device', 'quality_score', 'crash_rate_per_1k', 'active_devices', 'daily_churn_rate', 'daily_install_uninstall_ratio']].describe().round(4))

# By package, analyze rpad trends
print("\n\nRevenue per active device by package (monthly avg):")
df_pkg_monthly = df_daily.groupby(['package_name', 'month']).agg({
    'revenue_per_active_device': 'mean',
    'quality_score': 'mean',
    'crash_rate_per_1k': 'mean',
    'active_devices': 'mean',
    'daily_churn_rate': 'mean',
    'wow_install_growth_rate': 'mean'
}).reset_index()
print(df_pkg_monthly.groupby('package_name')[['revenue_per_active_device', 'quality_score', 'crash_rate_per_1k', 'active_devices']].mean().round(4))

# Multi-dimensional model: rpad ~ quality + crash + churn + active + maturity
# Fit separate models for each maturity group
print("\n\nMulti-dimensional regression by maturity group:")
results = []
for group in ['growing', 'stable', 'declining']:
    sub = df_daily[df_daily['maturity_group'] == group].copy()
    if len(sub) < 10:
        continue
    # OLS regression: rpad ~ quality + crash + churn + active + anr
    X = sub[['quality_score', 'crash_rate_per_1k', 'daily_churn_rate', 'active_devices', 'anr_rate_per_1k']].values
    y = sub['revenue_per_active_device'].values
    X_with_const = np.column_stack([np.ones(len(X)), X])
    beta = np.linalg.lstsq(X_with_const, y, rcond=None)[0]
    y_pred = X_with_const @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot
    results.append({'group': group, 'n': len(sub), 'r2': r2, 
                    'intercept': beta[0],
                    'quality': beta[1], 'crash': beta[2], 
                    'churn': beta[3], 'active': beta[4], 'anr': beta[5]})
    print(f"\n{group.upper()} (n={len(sub)}):")
    print(f"  R² = {r2:.4f}")
    print(f"  rpad = {beta[0]:.6f} + {beta[1]:.6f}*quality + {beta[2]:.6f}*crash + {beta[3]:.6f}*churn + {beta[4]:.10f}*active + {beta[5]:.6f}*anr")
    
    # Correlation matrix
    print(f"  Correlations:")
    for col in ['quality_score', 'crash_rate_per_1k', 'daily_churn_rate', 'active_devices', 'anr_rate_per_1k']:
        corr = sub[col].corr(sub['revenue_per_active_device'])
        print(f"    {col}: {corr:.4f}")

# Plot rpad trends by package and maturity
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# Subplot 1: rpad vs quality by maturity
ax = axes[0]
for group in ['growing', 'stable', 'declining']:
    sub = df_daily[df_daily['maturity_group'] == group]
    ax.scatter(sub['quality_score'], sub['revenue_per_active_device'], alpha=0.3, label=group, s=5)
ax.set_xlabel('Quality Score')
ax.set_ylabel('Revenue per Active Device')
ax.set_title('rpad vs Quality Score by Market Maturity')
ax.legend()
ax.grid(True, alpha=0.3)

# Subplot 2: rpad vs crash by maturity
ax = axes[1]
for group in ['growing', 'stable', 'declining']:
    sub = df_daily[df_daily['maturity_group'] == group]
    ax.scatter(sub['crash_rate_per_1k'], sub['revenue_per_active_device'], alpha=0.3, label=group, s=5)
ax.set_xlabel('Crash Rate per 1k')
ax.set_ylabel('Revenue per Active Device')
ax.set_title('rpad vs Crash Rate by Market Maturity')
ax.legend()
ax.grid(True, alpha=0.3)

# Subplot 3: rpad over time by package
ax = axes[2]
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    ax.plot(sub['date_dt'], sub['revenue_per_active_device'], label=pkg.split('.')[-1], alpha=0.7)
ax.set_xlabel('Date')
ax.set_ylabel('Revenue per Active Device')
ax.set_title('rpad Trends by Package')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Subplot 4: active devices over time by package
ax = axes[3]
for pkg in df_daily['package_name'].unique():
    sub = df_daily[df_daily['package_name'] == pkg]
    ax.plot(sub['date_dt'], sub['active_devices'], label=pkg.split('.')[-1], alpha=0.7)
ax.set_xlabel('Date')
ax.set_ylabel('Active Devices')
ax.set_title('Active Devices Trends by Package')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig3_user_value_decay_model.png', dpi=100)
plt.close()
print("Saved fig3_user_value_decay_model.png")

# Predict optimization strategies
print("\n\n--- Optimization Strategy Predictions ---")
print("Based on the multi-dimensional model, optimal strategies per market maturity:")
for r in results:
    group = r['group']
    q_effect = r['quality']
    c_effect = r['crash']
    churn_effect = r['churn']
    print(f"\n{group.upper()} market:")
    if q_effect > 0:
        print(f"  - Improve quality score (β={q_effect:.6f}): +1 quality → +{q_effect:.6f} rpad")
    else:
        print(f"  - Quality score has negative effect (β={q_effect:.6f}) - maintain baseline")
    if c_effect < 0:
        print(f"  - Reduce crash rate (β={c_effect:.6f}): -1 crash → +{-c_effect:.6f} rpad")
    else:
        print(f"  - Crash rate has minimal impact (β={c_effect:.6f})")
    if churn_effect < 0:
        print(f"  - Reduce churn (β={churn_effect:.6f})")
    print(f"  - Model R² = {r['r2']:.4f}")

# Save processed daily data
df_daily.to_csv('/work/daily_timeseries.csv', index=False)