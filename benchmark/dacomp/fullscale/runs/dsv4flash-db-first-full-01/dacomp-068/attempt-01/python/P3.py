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
    n_markets=('country', 'count'),
    total_visitors_30d=('store_visitors_30d', 'sum'),
    total_installs_30d=('store_installs_30d', 'sum'),
    total_revenue_30d=('revenue_last_30_days', 'sum'),
    avg_daily_revenue=('avg_daily_revenue', 'mean'),
    avg_conv_rate=('store_conversion_rate', 'mean'),
    avg_ros=('revenue_opportunity_score', 'mean'),
    avg_gps=('growth_potential_score', 'mean'),
    avg_uqs=('user_quality_score', 'mean'),
    avg_sps=('store_performance_score', 'mean'),
    avg_oms=('overall_market_score', 'mean')
).reset_index()

# Identify segments per app
seg_a_apps = set()
seg_b_apps = set()
geo = geo.copy()
geo['segment'] = 'none'
for idx, row in geo.iterrows():
    if row['store_conversion_rate'] > 15 and row['avg_daily_revenue'] < 5:
        seg_a_apps.add(row['package_name'])
        geo.at[idx, 'segment'] = 'A'
    if row['avg_daily_revenue'] > 7 and row['store_conversion_rate'] < 10:
        seg_b_apps.add(row['package_name'])
        geo.at[idx, 'segment'] = 'B'

# Merge
merged = portfolio.merge(geo_agg, on='package_name', how='left')
merged['in_seg_a'] = merged['package_name'].isin(seg_a_apps).astype(int)
merged['in_seg_b'] = merged['package_name'].isin(seg_b_apps).astype(int)

# Manual min-max normalization
def minmax(s):
    return (s - s.min()) / (s.max() - s.min())

factors = ['avg_ros', 'avg_gps', 'portfolio_health_score', 'revenue_score', 'engagement_score']
for f in factors:
    merged[f + '_norm'] = minmax(merged[f])

merged['log_visitors'] = np.log1p(merged['total_visitors_30d'])
merged['log_visitors_norm'] = minmax(merged['log_visitors'])

# Segment bonus
merged['seg_bonus'] = (merged['in_seg_a'] * 0.5 + merged['in_seg_b'] * 0.5)

# Composite score
weights = {
    'avg_ros_norm': 0.20,
    'avg_gps_norm': 0.20,
    'portfolio_health_score_norm': 0.15,
    'revenue_score_norm': 0.15,
    'engagement_score_norm': 0.10,
    'log_visitors_norm': 0.10,
    'seg_bonus': 0.10
}
merged['composite_score'] = sum(merged[k] * v for k, v in weights.items())

total_budget = 5_000_000
merged['budget_share'] = merged['composite_score'] / merged['composite_score'].sum()
merged['allocated_budget'] = merged['budget_share'] * total_budget

merged_sorted = merged.sort_values('allocated_budget', ascending=False)

print("=== Budget Allocation ($5M) ===")
cols = ['package_name', 'composite_score', 'budget_share', 'allocated_budget',
        'total_revenue_30d', 'avg_daily_revenue', 'avg_ros', 'avg_gps',
        'portfolio_health_score', 'bcg_matrix_category', 'investment_priority',
        'in_seg_a', 'in_seg_b']
print(merged_sorted[cols].round(4).to_string(index=False))
print(f"\nTotal: ${merged_sorted['allocated_budget'].sum():,.2f}")

# Save for later use
merged_sorted.to_pickle('/work/merged_budget.pkl')
print("Saved merged data to /work/merged_budget.pkl")