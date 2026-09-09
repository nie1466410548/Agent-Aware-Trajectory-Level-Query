import numpy as np
import pandas as pd
from scipy import stats

geo = db.frame(db.query("SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'"))

# Correlations of ARPU and ATV with quality metrics
print("=== Correlation of monthly ARPU with market health metrics (n=14 markets) ===")
for col in ['app_quality_score', 'app_crash_rate_per_1k', 'day_30_retention_rate', 'daily_churn_rate', 'weekly_growth_rate', 'overall_market_score']:
    r_p, p_p = stats.pearsonr(geo['average_revenue_per_user'], geo[col])
    r_s, p_s = stats.spearmanr(geo['average_revenue_per_user'], geo[col])
    print(f"ARPU vs {col:28s}: Pearson r={r_p:+.3f} (p={p_p:.3f}) | Spearman rho={r_s:+.3f} (p={p_s:.3f})")

print()
print("=== Regional summary (weighted by active devices) ===")
geo['daily_rev_per_device'] = geo['avg_daily_revenue'] / geo['avg_active_devices']
geo['rev_per_install'] = geo['avg_daily_revenue'] / geo['avg_daily_installs']
region = geo.groupby('region').agg(
    countries=('country', 'count'),
    total_daily_rev=('avg_daily_revenue', 'sum'),
    avg_arpu=('average_revenue_per_user', 'mean'),
    avg_quality=('app_quality_score', 'mean'),
    avg_crash=('app_crash_rate_per_1k', 'mean'),
    avg_d30ret=('day_30_retention_rate', 'mean'),
    avg_churn=('daily_churn_rate', 'mean'),
    avg_growth=('weekly_growth_rate', 'mean'),
    avg_ms=('overall_market_score', 'mean'),
    avg_rev_per_install=('rev_per_install', 'mean')
).sort_values('total_daily_rev', ascending=False)
print(region.round(3))

print()
print("=== Group comparison (High ARPU > $7 vs low) ===")
geo['grp'] = np.where(geo['average_revenue_per_user'] > 7, 'High', 'Low')
summary = geo.groupby('grp').agg(
    n=('country', 'count'),
    avg_arpu=('average_revenue_per_user', 'mean'),
    avg_atv=('avg_transaction_value', 'mean'),
    avg_quality=('app_quality_score', 'mean'),
    avg_crash=('app_crash_rate_per_1k', 'mean'),
    avg_d30=('day_30_retention_rate', 'mean'),
    avg_churn=('daily_churn_rate', 'mean'),
    avg_growth=('weekly_growth_rate', 'mean'),
    avg_ms=('overall_market_score', 'mean'),
    total_rev=('avg_daily_revenue', 'sum'),
    total_devices=('avg_active_devices', 'sum')
).round(3)
print(summary)

print()
print("=== Tier 1 vs Tier 3 (revenue tier) comparison ===")
tier = geo.groupby('revenue_tier').agg(
    n=('country', 'count'),
    avg_arpu=('average_revenue_per_user', 'mean'),
    avg_atv=('avg_transaction_value', 'mean'),
    avg_quality=('app_quality_score', 'mean'),
    avg_crash=('app_crash_rate_per_1k', 'mean'),
    avg_d30=('day_30_retention_rate', 'mean'),
    avg_churn=('daily_churn_rate', 'mean'),
    avg_growth=('weekly_growth_rate', 'mean'),
    avg_ms=('overall_market_score', 'mean'),
    total_rev=('avg_daily_revenue', 'sum'),
    total_devices=('avg_active_devices', 'sum')
).round(3)
print(tier)

# Key metric check
print()
print("=== Markets with ARPU under $7 ===")
print(geo[geo['average_revenue_per_user'] <= 7][['country','region','average_revenue_per_user','avg_transaction_value','app_quality_score','app_crash_rate_per_1k']])
print("=== Markets with ARPU between 3 and 7 ===")
print(geo[(geo['average_revenue_per_user'] > 3) & (geo['average_revenue_per_user'] <= 7)][['country','region','average_revenue_per_user']])