import numpy as np
import pandas as pd

geo = db.frame(db.query("SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs, revenue_tier, market_tier FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'"))

# Tier comparison
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
print("=== Revenue Tier Comparison ===")
print(tier)

print()
print("=== Market Tier Comparison ===")
mtier = geo.groupby('market_tier').agg(
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
print(mtier)

print()
print("=== Markets with ARPU under $7 ===")
print(geo[geo['average_revenue_per_user'] <= 7][['country','region','average_revenue_per_user','avg_transaction_value','app_quality_score','app_crash_rate_per_1k','revenue_tier','market_tier']])

print()
print("=== Markets with ARPU between $3 and $7 ===")
print(geo[(geo['average_revenue_per_user'] > 3) & (geo['average_revenue_per_user'] <= 7)][['country','region','average_revenue_per_user','revenue_tier','market_tier']])

print()
print("=== All 14 markets sorted by ARPU ===")
print(geo[['country','region','average_revenue_per_user','avg_transaction_value','app_quality_score','app_crash_rate_per_1k','weekly_growth_rate','revenue_tier','market_tier']].to_string(index=False))