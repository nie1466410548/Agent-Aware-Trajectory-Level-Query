import numpy as np
import pandas as pd

geo = db.frame(db.query("SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs, revenue_tier, market_tier, opportunity_type, investment_recommendation FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'"))

dash = db.frame(db.query("SELECT date_day, overall_performance_score, quality_score, daily_installs, daily_uninstalls, active_devices, daily_crashes, daily_anrs, crash_rate_per_1k_devices, anr_rate_per_1k_devices, daily_churn_rate, day_1_retention_rate, day_7_retention_rate, day_30_retention_rate, daily_net_revenue, daily_transactions, avg_transaction_value, average_revenue_per_user, revenue_health_score, research_budget_usd FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day"))

print("=== App-level changes Jan vs Dec 2024 ===")
first = dash.iloc[0]
last = dash.iloc[-1]
for col in ['overall_performance_score','quality_score','daily_installs','daily_uninstalls','active_devices','daily_crashes','daily_anrs','crash_rate_per_1k_devices','anr_rate_per_1k_devices','daily_churn_rate','day_7_retention_rate','day_30_retention_rate','daily_net_revenue','daily_transactions','avg_transaction_value','average_revenue_per_user','revenue_health_score']:
    f, l = first[col], last[col]
    if isinstance(f, (int, float)) and isinstance(l, (int, float)) and f != 0:
        print(f"{col:32s}: {f:.3f} -> {l:.3f}  ({(l-f)/abs(f)*100:+.1f}%)")

print()
print("=== Revenue share by revenue tier ===")
tier_rev = geo.groupby('revenue_tier')['avg_daily_revenue'].sum()
print(tier_rev)
print("Total:", tier_rev.sum())
print("Share Tier1:", (tier_rev['Tier 1']/tier_rev.sum()*100).round(1), "%")
print("Share Tier3:", (tier_rev['Tier 3']/tier_rev.sum()*100).round(1), "%")

print()
print("=== Revenue share by market tier ===")
mt = geo.groupby('market_tier')['avg_daily_revenue'].sum()
print(mt)
print("Total:", mt.sum())

print()
print("=== Quality and crash by revenue tier ===")
qc = geo.groupby('revenue_tier')[['app_quality_score','app_crash_rate_per_1k','day_7_retention_rate','day_30_retention_rate','daily_churn_rate','weekly_growth_rate']].mean().round(3)
print(qc)

print()
print("=== Top markets (ARPU > $7) growth: negative? ===")
top = geo[geo['average_revenue_per_user'] > 7]
low = geo[geo['average_revenue_per_user'] <= 7]
print(f"High ARPU markets: {len(top)}, avg growth = {top['weekly_growth_rate'].mean():.3f}")
print(f"Low ARPU markets: {len(low)}, avg growth = {low['weekly_growth_rate'].mean():.3f}")
print("High ARPU markets with negative growth:", (top['weekly_growth_rate'] < 0).sum(), "of", len(top))
print("Low ARPU markets with positive growth:", (low['weekly_growth_rate'] > 0).sum(), "of", len(low))

print()
print("=== Store conversion comparison ===")
geo2 = db.frame(db.query("SELECT country, revenue_tier, store_conversion_rate, store_visitors_30d, store_installs_30d FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'"))
print(geo2.groupby('revenue_tier')[['store_conversion_rate','store_visitors_30d','store_installs_30d']].mean().round(3))

print()
print("=== Opportunity types in top markets ===")
print(top[['country','average_revenue_per_user','opportunity_type','investment_recommendation']].to_string(index=False))

# Save a summary CSV for reference
geo.to_csv('/work/geo_market_summary.csv', index=False)
dash.to_csv('/work/dashboard_summary.csv', index=False)
print("\nSummaries saved.")