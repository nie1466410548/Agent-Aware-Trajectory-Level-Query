import pandas as pd
import numpy as np
import json

# Load top customers
with open('/work/top_customers.txt', 'r') as f:
    top_customers = [line.strip() for line in f]
print(f"Top customers: {len(top_customers)}")

# First, get order-level data for Home & Furniture
# We'll use SQL query to get what we need
from db import db

# Get Home & Furniture orders with customer info
result = db.query("""
SELECT "Customer ID", substr("Order Date",1,4) AS yr, 
       "Order ID", "Quantity", "Product", Sales, profit,
       Sales * 1.0 / CAST(CAST("Quantity" AS REAL) AS INTEGER) AS unit_price,
       profit * 1.0 / Sales AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
  AND "Quantity" != 'abc'
  AND "Quantity" IS NOT NULL
""")
rows = db.rows(result)
orders = pd.DataFrame(rows, columns=['Customer ID', 'yr', 'Order ID', 'Quantity', 'Product', 'Sales', 'profit', 'unit_price', 'margin'])
orders['Quantity'] = pd.to_numeric(orders['Quantity'])
orders['yr'] = orders['yr'].astype(int)

# Mark segment
orders['segment'] = orders['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

# Stats by year and segment
stats = orders.groupby(['yr', 'segment']).agg(
    n_orders=('Order ID', 'count'),
    avg_qty=('Quantity', 'mean'),
    avg_margin=('margin', 'mean'),
    total_sales=('Sales', 'sum'),
    total_profit=('profit', 'sum')
).round(4)
print("=== Stats by Year and Segment ===")
print(stats)

# Year-over-year margin change
for seg in ['Top Tier', 'Other']:
    seg_data = orders[orders['segment'] == seg]
    yr_margin = seg_data.groupby('yr')['margin'].mean()
    print(f"\n{seg} margins by year:")
    print(yr_margin)
    yr_margin_pct = yr_margin.pct_change() * 100
    print(f"{seg} margin % change:")
    print(yr_margin_pct)

# Avg quantity by year and segment
print("\n\n=== Avg Quantity by Year and Segment ===")
qty_stats = orders.groupby(['yr', 'segment'])['Quantity'].mean().round(3)
print(qty_stats)

# Distribution of quantity by segment
print("\n\n=== Quantity Distribution ===")
qty_dist = orders.groupby(['segment', 'Quantity']).size().unstack(fill_value=0)
print(qty_dist)

# Test if the difference is significant
from scipy import stats as scipy_stats

for yr in [2022, 2023, 2024]:
    top_qty = orders[(orders['segment'] == 'Top Tier') & (orders['yr'] == yr)]['Quantity']
    other_qty = orders[(orders['segment'] == 'Other') & (orders['yr'] == yr)]['Quantity']
    t_stat, p_val = scipy_stats.ttest_ind(top_qty, other_qty, equal_var=False)
    print(f"\n{yr}: Top Tier mean qty={top_qty.mean():.3f}, Other mean qty={other_qty.mean():.3f}, t={t_stat:.3f}, p={p_val:.6f}")