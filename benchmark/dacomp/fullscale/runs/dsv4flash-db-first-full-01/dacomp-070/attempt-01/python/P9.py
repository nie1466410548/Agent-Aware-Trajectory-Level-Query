import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# =============================================
# 4. INTERACTION EFFECT OF APP UPDATE FREQUENCY
# =============================================
print("=" * 60)
print("ANALYSIS 4: INTERACTION EFFECT OF APP UPDATE FREQUENCY")
print("=" * 60)

# Fetch daily-level update data from country_report
res = db.query("""
SELECT date_day, country_short, region, package_name,
       update_events, active_devices_last_30_days, 
       rolling_total_average_rating, device_installs, net_device_installs
FROM google_play__country_report
ORDER BY region, package_name, date_day
""")
df_cr = db.frame(res)
df_cr['date_dt'] = pd.to_datetime(df_cr['date_day'])
df_cr['month'] = df_cr['date_dt'].dt.to_period('M').astype(str)
print("Country report daily shape:", df_cr.shape)

# Compute update frequency metrics
df_cr['update_intensity'] = df_cr['update_events'] / (df_cr['active_devices_last_30_days'] + 1) * 1000  # per 1000 active
df_cr['update_to_installs'] = df_cr['update_events'] / (df_cr['device_installs'] + 1)

print("\nUpdate intensity distribution (per 1000 active devices):")
print(df_cr['update_intensity'].describe())

# Aggregate by region-month
df_rm = df_cr.groupby(['region', 'month']).agg({
    'update_events': 'sum',
    'active_devices_last_30_days': 'sum',
    'rolling_total_average_rating': 'mean',
    'update_intensity': 'mean',
    'device_installs': 'sum',
    'net_device_installs': 'sum'
}).reset_index()
df_rm['update_rate'] = df_rm['update_events'] / df_rm['active_devices_last_30_days'] * 1000

print("\n\nMonthly update rate by region:")
print(df_rm.pivot_table(index='month', columns='region', values='update_rate').round(2))

# Correlation: update frequency vs active devices
print("\n\nCorrelation: Update frequency vs Active Devices (by region):")
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region]
    # Daily aggregation
    daily = sub.groupby('date_dt').agg({
        'update_intensity': 'mean',
        'active_devices_last_30_days': 'sum',
        'rolling_total_average_rating': 'mean'
    }).reset_index()
    r1 = daily['update_intensity'].corr(daily['active_devices_last_30_days'])
    r2 = daily['update_intensity'].corr(daily['rolling_total_average_rating'])
    print(f"  {region}: update_intensity vs active_devices: r={r1:.4f}, vs rating: r={r2:.4f}")

# Interaction effect: Use regression to test interaction
# model: active_devices ~ update_intensity * rating 
# (does update frequency effect on active devices depend on rating?)
print("\n\n--- Interaction Regression Models ---")
print("Model 1: active_devices ~ update_intensity + rating + update_intensity*rating")
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region].copy()
    daily = sub.groupby('date_dt').agg({
        'update_intensity': 'mean',
        'active_devices_last_30_days': 'sum',
        'rolling_total_average_rating': 'mean'
    }).reset_index()
    
    X = daily[['update_intensity', 'rolling_total_average_rating']].values
    X = np.column_stack([np.ones(len(X)), X, X[:, 0] * X[:, 1]])  # add interaction
    y = daily['active_devices_last_30_days'].values / 1e6  # scale to millions
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot
    print(f"\n  {region}: R² = {r2:.4f}")
    print(f"  active_devices(M) = {beta[0]:.4f} + {beta[1]:.4f}*upd_intensity + {beta[2]:.4f}*rating + {beta[3]:.4f}*upd_intensity*rating")
    
    # Test if interaction term is significant (simplified: compare with no-interaction model)
    X_noi = daily[['update_intensity', 'rolling_total_average_rating']].values
    X_noi = np.column_stack([np.ones(len(X_noi)), X_noi])
    beta_noi = np.linalg.lstsq(X_noi, y, rcond=None)[0]
    y_pred_noi = X_noi @ beta_noi
    ss_res_noi = np.sum((y - y_pred_noi)**2)
    r2_noi = 1 - ss_res_noi/ss_tot
    f_stat = ((ss_res_noi - ss_res) / 1) / (ss_res / (len(y) - 4))
    p_val = 1 - stats.f.cdf(f_stat, 1, len(y) - 4)
    print(f"  Interaction F-test: F={f_stat:.4f}, p={p_val:.4f}")

# Model 2: rating ~ update_intensity + active_devices + update_intensity*active_devices
print("\n\nModel 2: rating ~ update_intensity + active_devices + update_intensity*active_devices")
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region].copy()
    daily = sub.groupby('date_dt').agg({
        'update_intensity': 'mean',
        'active_devices_last_30_days': 'sum',
        'rolling_total_average_rating': 'mean'
    }).reset_index()
    
    X = daily[['update_intensity', 'active_devices_last_30_days']].values
    X = np.column_stack([np.ones(len(X)), X, X[:, 0] * X[:, 1] / 1e6])  # interaction
    y = daily['rolling_total_average_rating'].values
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    y_pred = X @ beta
    ss_res = np.sum((y - y_pred)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot
    print(f"\n  {region}: R² = {r2:.4f}")
    print(f"  rating = {beta[0]:.4f} + {beta[1]:.4f}*upd_intensity + {beta[2]:.10f}*active + {beta[3]:.4f}*upd_intensity*active")
    
    # Test interaction significance
    X_noi = daily[['update_intensity', 'active_devices_last_30_days']].values
    X_noi = np.column_stack([np.ones(len(X_noi)), X_noi])
    beta_noi = np.linalg.lstsq(X_noi, y, rcond=None)[0]
    y_pred_noi = X_noi @ beta_noi
    ss_res_noi = np.sum((y - y_pred_noi)**2)
    r2_noi = 1 - ss_res_noi/ss_tot
    f_stat = ((ss_res_noi - ss_res) / 1) / (ss_res / (len(y) - 4))
    p_val = 1 - stats.f.cdf(f_stat, 1, len(y) - 4)
    print(f"  Interaction F-test: F={f_stat:.4f}, p={p_val:.4f}")

# Device-level analysis
print("\n\n--- Device-Level Update Frequency Analysis ---")
res = db.query("""
SELECT date_day, device, package_name,
       update_events, active_devices_last_30_days,
       rolling_total_average_rating, device_installs, device_uninstalls
FROM google_play__device_report
ORDER BY device, package_name, date_day
""")
df_dr = db.frame(res)
df_dr['date_dt'] = pd.to_datetime(df_dr['date_day'])
df_dr['update_intensity'] = df_dr['update_events'] / (df_dr['active_devices_last_30_days'] + 1) * 1000
print("Device report daily shape:", df_dr.shape)

# Device-level correlation
print("\nCorrelation: Update intensity vs Active devices (by device):")
dev_corr = df_dr.groupby('device').apply(
    lambda g: pd.Series({
        'r_active': g['update_intensity'].corr(g['active_devices_last_30_days']),
        'r_rating': g['update_intensity'].corr(g['rolling_total_average_rating']),
        'avg_upd_rate': g['update_intensity'].mean(),
        'avg_active': g['active_devices_last_30_days'].mean()
    })
).reset_index()
print(dev_corr.sort_values('r_active', ascending=False).round(4))

# Plot interaction effects
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

# Subplot 1: Update intensity vs active devices by region
ax = axes[0]
colors = {'Asia': 'blue', 'Europe': 'green', 'North America': 'orange', 'South America': 'red'}
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region]
    daily = sub.groupby('date_dt').agg({'update_intensity': 'mean', 'active_devices_last_30_days': 'sum'}).reset_index()
    ax.scatter(daily['update_intensity'], daily['active_devices_last_30_days']/1e6, alpha=0.5, s=10, c=colors[region], label=region)
ax.set_xlabel('Update Intensity (per 1000 active devices)')
ax.set_ylabel('Active Devices (Millions)')
ax.set_title('Update Intensity vs Active Devices by Region')
ax.legend()
ax.grid(True, alpha=0.3)

# Subplot 2: Update intensity vs rating by region
ax = axes[1]
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region]
    daily = sub.groupby('date_dt').agg({'update_intensity': 'mean', 'rolling_total_average_rating': 'mean'}).reset_index()
    ax.scatter(daily['update_intensity'], daily['rolling_total_average_rating'], alpha=0.5, s=10, c=colors[region], label=region)
ax.set_xlabel('Update Intensity (per 1000 active devices)')
ax.set_ylabel('Average Rating')
ax.set_title('Update Intensity vs Rating by Region')
ax.legend()
ax.grid(True, alpha=0.3)

# Subplot 3: Update frequency trend over time by region
ax = axes[2]
for region in df_cr['region'].unique():
    sub = df_cr[df_cr['region'] == region]
    daily = sub.groupby('date_dt').agg({'update_intensity': 'mean'}).reset_index()
    ax.plot(daily['date_dt'], daily['update_intensity'], label=region, alpha=0.8)
ax.set_xlabel('Date')
ax.set_ylabel('Update Intensity (per 1000 active)')
ax.set_title('Update Intensity Trends by Region')
ax.legend()
ax.grid(True, alpha=0.3)

# Subplot 4: Device-level update intensity vs active
ax = axes[3]
for device in df_dr['device'].unique()[:4]:  # just first 4 for clarity
    sub = df_dr[df_dr['device'] == device]
    daily = sub.groupby('date_dt').agg({'update_intensity': 'mean', 'active_devices_last_30_days': 'sum'}).reset_index()
    ax.scatter(daily['update_intensity'], daily['active_devices_last_30_days']/1e6, alpha=0.3, s=5, label=device)
ax.set_xlabel('Update Intensity (per 1000 active devices)')
ax.set_ylabel('Active Devices (Millions)')
ax.set_title('Update Intensity vs Active Devices by Device Type')
ax.legend(fontsize=7)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig4_update_interaction.png', dpi=100)
plt.close()
print("Saved fig4_update_interaction.png")