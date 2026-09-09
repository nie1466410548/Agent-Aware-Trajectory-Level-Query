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

# Segment flags per market
geo = geo.copy()
geo['segment'] = 'none'
for idx, row in geo.iterrows():
    if row['store_conversion_rate'] > 15 and row['avg_daily_revenue'] < 5:
        geo.at[idx, 'segment'] = 'A'
    elif row['avg_daily_revenue'] > 7 and row['store_conversion_rate'] < 10:
        geo.at[idx, 'segment'] = 'B'

seg_a = geo[geo['segment'] == 'A'].copy()
seg_b = geo[geo['segment'] == 'B'].copy()

# Geo aggregates per app
geo_agg = geo.groupby('package_name').agg(
    n_markets_geo=('country', 'count'),
    total_visitors_30d=('store_visitors_30d', 'sum'),
    total_installs_30d=('store_installs_30d', 'sum'),
    total_revenue_30d_geo=('revenue_last_30_days', 'sum'),
    avg_conv_rate_geo=('store_conversion_rate', 'mean'),
    avg_ros=('revenue_opportunity_score', 'mean'),
    avg_gps=('growth_potential_score', 'mean'),
    avg_uqs=('user_quality_score', 'mean'),
    avg_sps=('store_performance_score', 'mean'),
    avg_oms=('overall_market_score', 'mean')
).reset_index()

merged = portfolio.merge(geo_agg, on='package_name', how='left')
merged['in_seg_a'] = merged['package_name'].isin(set(seg_a['package_name'])).astype(int)
merged['in_seg_b'] = merged['package_name'].isin(set(seg_b['package_name'])).astype(int)

# Number of flagged markets per app
seg_counts = geo.groupby('package_name')['segment'].value_counts().unstack(fill_value=0)
seg_counts = seg_counts.rename(columns={'A': 'segA_markets', 'B': 'segB_markets', 'none': 'segNone_markets'})
merged = merged.merge(seg_counts, on='package_name', how='left')

# ---- Composite opportunity score ----
def minmax(s):
    return (s - s.min()) / (s.max() - s.min())

for f in ['avg_ros', 'avg_gps', 'portfolio_health_score', 'revenue_score', 'engagement_score']:
    merged[f + '_norm'] = minmax(merged[f])

merged['log_visitors'] = np.log1p(merged['total_visitors_30d'])
merged['log_visitors_norm'] = minmax(merged['log_visitors'])
merged['seg_bonus'] = (merged['segA_markets'] + merged['segB_markets']).clip(upper=1) * 0.5

weights = {
    'avg_ros_norm': 0.20, 'avg_gps_norm': 0.20,
    'portfolio_health_score_norm': 0.15, 'revenue_score_norm': 0.15,
    'engagement_score_norm': 0.10, 'log_visitors_norm': 0.10, 'seg_bonus': 0.10
}
merged['composite_score'] = sum(merged[k] * v for k, v in weights.items())

TOTAL = 5_000_000
merged['budget_share'] = merged['composite_score'] / merged['composite_score'].sum()
merged['allocated_budget'] = merged['budget_share'] * TOTAL
merged = merged.sort_values('allocated_budget', ascending=False).reset_index(drop=True)

# ---- Expected ROI model ----
# Expected Q4 return multiple per app based on the platform's own market opportunity scoring:
# ROAS_app = (avg revenue_opportunity_score + avg growth_potential_score) / 100
merged['roas'] = (merged['avg_ros'] + merged['avg_gps']) / 100.0
merged['expected_roi'] = (merged['roas'] - 1.0) * 100.0
merged['expected_inc_rev'] = merged['allocated_budget'] * merged['roas']

port_inc_rev = merged['expected_inc_rev'].sum()
port_roi = (port_inc_rev - TOTAL) / TOTAL * 100
print(f"Portfolio expected incremental revenue: ${port_inc_rev:,.0f}")
print(f"Portfolio expected ROI: {port_roi:.1f}%")

# ---- Output allocation table ----
out_cols = ['package_name', 'allocated_budget', 'budget_share', 'avg_ros', 'avg_gps',
            'roas', 'expected_roi', 'expected_inc_rev',
            'segA_markets', 'segB_markets', 'total_revenue_30d',
            'bcg_matrix_category', 'investment_priority', 'growth_stage']
print("\n=== FINAL BUDGET ALLOCATION ===")
print(merged[out_cols].round(2).to_string(index=False))
print(f"\nTotal budget: ${merged['allocated_budget'].sum():,.0f}")
print(f"Sum of shares: {merged['budget_share'].sum():.6f}")

# Check each app's expected ROI
print("\nPer-app expected ROI (must be >=25% or justified):")
for _, r in merged.iterrows():
    status = "OK" if r['expected_roi'] >= 25 else "BELOW"
    print(f"  {r['package_name']:30s} ROI={r['expected_roi']:.1f}% [{status}]")

merged.to_pickle('/work/final_allocation.pkl')
geo.to_pickle('/work/geo_seg.pkl')
print("\nSaved final_allocation.pkl and geo_seg.pkl")