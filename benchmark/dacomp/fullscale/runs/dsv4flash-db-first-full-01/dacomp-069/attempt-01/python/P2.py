import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load data
dashboard = db.frame(db.query("SELECT date_day, overall_performance_score, quality_score, daily_net_revenue, daily_installs, daily_uninstalls, active_devices, daily_crashes, crash_rate_per_1k_devices, day_7_retention_rate, day_30_retention_rate, daily_churn_rate FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day"))
dashboard['date'] = pd.to_datetime(dashboard['date_day'])

geo = db.frame(db.query("SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, market_tier, revenue_tier FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY average_revenue_per_user DESC"))

fin = db.frame(db.query("SELECT country_short, date_day, sku_id, net_amount, transactions FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' ORDER BY country_short, date_day, sku_id"))
fin['date'] = pd.to_datetime(fin['date_day'])
fin['month'] = fin['date'].dt.strftime('%Y-%m')

ts = db.frame(db.query("SELECT date_day, daily_revenue, quality_score, crash_rate_per_1k, anr_rate_per_1k, daily_churn_rate FROM google_play__time_series_trends WHERE package_name='com.dev.photoeditor' ORDER BY date_day"))
ts['date'] = pd.to_datetime(ts['date_day'])

# Figure 1: Dashboard decline
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(dashboard['date'], dashboard['overall_performance_score'], 'o-', color='#1a5276', linewidth=2.5, markersize=8, label='Overall Performance Score')
ax1.plot(dashboard['date'], dashboard['quality_score'], 's--', color='#e74c3c', linewidth=2, markersize=7, label='Quality Score')
ax1.set_ylabel('Score', fontsize=12, fontweight='bold')
ax1.set_xlabel('Month (2024)', fontsize=12, fontweight='bold')
ax1.set_title('Overall Performance Score & Quality Score Decline\ncom.dev.photoeditor (Jan-Dec 2024)', fontsize=14, fontweight='bold')
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(60, 90)
for i, row in dashboard.iterrows():
    if i in (0, 7, 11):
        ax1.annotate(f'{row["overall_performance_score"]}', (row['date'], row['overall_performance_score']), textcoords="offset points", xytext=(0, 12), ha='center', fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/fig1_dashboard_decline.png', dpi=150)
plt.close()

# Figure 2: Revenue and Installs
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.bar(dashboard['date'], dashboard['daily_net_revenue']/1000, width=20, color='#2ecc71', alpha=0.7, label='Daily Net Revenue ($K)')
ax1.set_ylabel('Daily Net Revenue ($K)', fontsize=12, fontweight='bold', color='#2ecc71')
ax1.tick_params(axis='y', labelcolor='#2ecc71')
ax2 = ax1.twinx()
ax2.plot(dashboard['date'], dashboard['daily_installs']/1000, 'o-', color='#3498db', linewidth=2.5, markersize=7, label='Daily Installs (K)')
ax2.plot(dashboard['date'], dashboard['daily_uninstalls']/1000, 's--', color='#e74c3c', linewidth=2, markersize=7, label='Daily Uninstalls (K)')
ax2.set_ylabel('Installs / Uninstalls (Thousands)', fontsize=12, fontweight='bold', color='#3498db')
ax2.tick_params(axis='y', labelcolor='#3498db')
ax1.set_xlabel('Month (2024)', fontsize=12, fontweight='bold')
ax1.set_title('Revenue Decline & Install/Uninstall Divergence', fontsize=14, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig2_revenue_installs.png', dpi=150)
plt.close()

# Figure 3: Geo ARPU vs Quality scatter
fig, ax = plt.subplots(figsize=(10, 6))
sizes = {'Tier 1': 200, 'Tier 2': 120, 'Tier 3': 80}
for tier in ['Tier 1', 'Tier 2', 'Tier 3']:
    mask = geo['revenue_tier'] == tier
    n = int(mask.sum())
    ax.scatter(geo.loc[mask, 'average_revenue_per_user'], geo.loc[mask, 'app_quality_score'],
               s=[sizes[tier]]*n, alpha=0.7, label=tier, edgecolors='black', linewidth=0.5)
for i, row in geo.iterrows():
    ax.annotate(row['country'], (row['average_revenue_per_user'], row['app_quality_score']), textcoords="offset points", xytext=(5, 5), ha='left', fontsize=8)
ax.axvline(x=7, color='gray', linestyle='--', alpha=0.5, label='ARPU=$7 threshold')
ax.axvline(x=3, color='gray', linestyle=':', alpha=0.3, label='ARPU=$3 threshold')
ax.set_xlabel('Average Revenue Per User (Monthly ARPU, $)', fontsize=12, fontweight='bold')
ax.set_ylabel('App Quality Score', fontsize=12, fontweight='bold')
ax.set_title('Geo Markets: ARPU vs App Quality Score\ncom.dev.photoeditor', fontsize=14, fontweight='bold')
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig3_geo_arpu_quality.png', dpi=150)
plt.close()

# Figure 4: Finance revenue divergence
fin_summary = fin.groupby(['country_short', 'month']).agg({'net_amount': 'sum', 'transactions': 'sum'}).reset_index()
premium_countries = ['US', 'JP', 'DE']
basic_countries = ['IN', 'BR', 'MX']
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
for c in premium_countries:
    data = fin_summary[fin_summary['country_short'] == c]
    if len(data) > 0:
        ax1.plot(data['month'], data['net_amount']/1000, 'o-', linewidth=2, markersize=6, label=c)
ax1.set_title('Premium SKU Markets: Monthly Revenue ($K)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Net Amount ($K)', fontsize=11, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)
for c in basic_countries:
    data = fin_summary[fin_summary['country_short'] == c]
    if len(data) > 0:
        ax2.plot(data['month'], data['net_amount']/1000, 'o-', linewidth=2, markersize=6, label=c)
ax2.set_title('Basic SKU Markets: Monthly Revenue ($K)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Net Amount ($K)', fontsize=11, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.tick_params(axis='x', rotation=45)
plt.suptitle('Revenue Divergence: Premium Markets Declining, Emerging Markets Growing', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/fig4_revenue_divergence.png', dpi=150)
plt.close()

# Figure 5: High vs Low ARPU comparison
geo['group'] = np.where(geo['average_revenue_per_user'] > 7, 'High ARPU (>$7)', 'Low ARPU (<$7)')
metrics = ['app_quality_score', 'app_crash_rate_per_1k', 'day_30_retention_rate', 'daily_churn_rate', 'weekly_growth_rate', 'overall_market_score']
labels = ['App Quality Score', 'Crash Rate/1k', 'Day-30 Retention', 'Daily Churn Rate', 'Weekly Growth Rate', 'Overall Market Score']
fig, axes = plt.subplots(2, 3, figsize=(14, 9))
axes = axes.flatten()
colors = {'High ARPU (>$7)': '#3498db', 'Low ARPU (<$7)': '#e74c3c'}
for i, (m, l) in enumerate(zip(metrics, labels)):
    means = geo.groupby('group')[m].mean()
    for g in ['High ARPU (>$7)', 'Low ARPU (<$7)']:
        if g in means.index:
            axes[i].bar(g, means[g], alpha=0.7, color=colors[g])
    axes[i].set_title(l, fontsize=11, fontweight='bold')
    axes[i].grid(True, alpha=0.3)
    axes[i].tick_params(axis='x', rotation=15)
plt.suptitle('Comparison: High ARPU (>$7) vs Low ARPU (<$7) Markets', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/fig5_arpu_group_comparison.png', dpi=150)
plt.close()

# Figure 6: Quality degradation
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(ts['date'], ts['crash_rate_per_1k'], 'o-', color='#e74c3c', linewidth=2, markersize=6, label='Crash Rate per 1k Devices')
ax1.set_ylabel('Crash Rate per 1k', fontsize=12, fontweight='bold', color='#e74c3c')
ax1.tick_params(axis='y', labelcolor='#e74c3c')
ax2 = ax1.twinx()
ax2.plot(ts['date'], ts['daily_churn_rate'], 's--', color='#8e44ad', linewidth=2, markersize=6, label='Daily Churn Rate')
ax2.set_ylabel('Daily Churn Rate', fontsize=12, fontweight='bold', color='#8e44ad')
ax2.tick_params(axis='y', labelcolor='#8e44ad')
ax1.set_xlabel('Date (2024)', fontsize=12, fontweight='bold')
ax1.set_title('Quality Degradation: Crash Rate & Churn Rate Rising', fontsize=14, fontweight='bold')
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig6_quality_degradation.png', dpi=150)
plt.close()

print("All figures saved successfully.")
print(geo.groupby('group')[['average_revenue_per_user','app_quality_score','app_crash_rate_per_1k','day_30_retention_rate','daily_churn_rate','weekly_growth_rate','overall_market_score']].mean())