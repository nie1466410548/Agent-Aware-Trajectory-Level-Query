import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load all data
result = db.query("SELECT * FROM google_play__geo_market_analysis")
geo = db.frame(result)

result = db.query("SELECT * FROM google_play__product_portfolio_analysis")
portfolio = db.frame(result)

# Geo market aggregates per app
geo_agg = geo.groupby('package_name').agg(
    n_markets_geo=('country', 'count'),
    total_visitors_30d=('store_visitors_30d', 'sum'),
    total_installs_30d=('store_installs_30d', 'sum'),
    total_revenue_30d_geo=('revenue_last_30_days', 'sum'),
    avg_daily_revenue_geo=('avg_daily_revenue', 'mean'),
    avg_conv_rate_geo=('store_conversion_rate', 'mean'),
    avg_ros=('revenue_opportunity_score', 'mean'),
    avg_gps=('growth_potential_score', 'mean'),
    avg_uqs=('user_quality_score', 'mean'),
    avg_sps=('store_performance_score', 'mean'),
    avg_oms=('overall_market_score', 'mean')
).reset_index()

# Identify segments per app
seg_a_apps = set()
seg_b_apps = set()
for idx, row in geo.iterrows():
    if row['store_conversion_rate'] > 15 and row['avg_daily_revenue'] < 5:
        seg_a_apps.add(row['package_name'])
    if row['avg_daily_revenue'] > 7 and row['store_conversion_rate'] < 10:
        seg_b_apps.add(row['package_name'])

print("Segment A apps:", seg_a_apps)
print("Segment B apps:", seg_b_apps)

# Merge
merged = portfolio.merge(geo_agg, on='package_name', how='left')
merged['in_seg_a'] = merged['package_name'].isin(seg_a_apps).astype(int)
merged['in_seg_b'] = merged['package_name'].isin(seg_b_apps).astype(int)

print("\nMerged columns:", list(merged.columns))
print("\nPortfolio preview:")
print(merged[['package_name', 'total_revenue_30d', 'avg_daily_revenue', 'total_markets', 
              'portfolio_health_score', 'revenue_score', 'engagement_score',
              'bcg_matrix_category', 'investment_priority']].to_string(index=False))