import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load geo market analysis
result = db.query("SELECT * FROM google_play__geo_market_analysis ORDER BY package_name, country")
geo = db.frame(result)
print("Geo market analysis columns:", list(geo.columns))
print("Rows:", len(geo))
print(geo[['package_name', 'country', 'country_name', 'avg_daily_revenue', 'store_conversion_rate']])

# Identify segments
seg_a = geo[(geo['store_conversion_rate'] > 15) & (geo['avg_daily_revenue'] < 5)]
seg_b = geo[(geo['avg_daily_revenue'] > 7) & (geo['store_conversion_rate'] < 10)]

print("\n=== Segment A: High conversion (>15%) but low revenue (<$5) ===")
print(seg_a[['package_name', 'country', 'country_name', 'avg_daily_revenue', 'store_conversion_rate', 'store_visitors_30d', 'store_installs_30d', 'revenue_last_30_days']])

print("\n=== Segment B: High revenue (>$7) but low conversion (<10%) ===")
print(seg_b[['package_name', 'country', 'country_name', 'avg_daily_revenue', 'store_conversion_rate', 'store_visitors_30d', 'store_installs_30d', 'revenue_last_30_days']])

# Count by app
seg_a_by_app = seg_a.groupby('package_name').agg(
    n_markets=('country', 'count'),
    total_visitors=('store_visitors_30d', 'sum'),
    total_installs=('store_installs_30d', 'sum'),
    total_revenue=('revenue_last_30_days', 'sum'),
    avg_conv=('store_conversion_rate', 'mean'),
    avg_rev=('avg_daily_revenue', 'mean')
).reset_index()

seg_b_by_app = seg_b.groupby('package_name').agg(
    n_markets=('country', 'count'),
    total_visitors=('store_visitors_30d', 'sum'),
    total_installs=('store_installs_30d', 'sum'),
    total_revenue=('revenue_last_30_days', 'sum'),
    avg_conv=('store_conversion_rate', 'mean'),
    avg_rev=('avg_daily_revenue', 'mean')
).reset_index()

print("\n=== Segment A by app ===")
print(seg_a_by_app)
print("\n=== Segment B by app ===")
print(seg_b_by_app)

# Load product portfolio
result = db.query("SELECT * FROM google_play__product_portfolio_analysis ORDER BY package_name")
portfolio = db.frame(result)
print("\n=== Product Portfolio ===")
print(portfolio[['package_name', 'total_revenue_30d', 'avg_daily_revenue', 'portfolio_health_score', 'bcg_matrix_category', 'investment_priority', 'growth_stage', 'revenue_score', 'engagement_score', 'total_markets']])

# Load dashboard aggregate for 2024
result = db.query("""
SELECT package_name,
       SUM(daily_net_revenue) AS rev2024,
       SUM(store_visitors) AS vis2024,
       SUM(store_acquisitions) AS acq2024,
       SUM(daily_net_revenue)/NULLIF(SUM(store_acquisitions),0) AS rev_per_acq,
       SUM(store_acquisitions)*1.0/NULLIF(SUM(store_visitors),0) AS conv_rate
FROM google_play__comprehensive_performance_dashboard
WHERE date_day >= '2024-01-01' AND date_day < '2025-01-01'
GROUP BY package_name
ORDER BY package_name
""")
dash = db.frame(result)
print("\n=== Dashboard 2024 Aggregates ===")
print(dash)