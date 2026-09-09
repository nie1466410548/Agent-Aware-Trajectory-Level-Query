import pandas as pd
import numpy as np
import json
from scipy import stats as scipy_stats

with open('/work/top_customers.txt', 'r') as f:
    top_customers = [line.strip() for line in f]
print(f"Top customers: {len(top_customers)}")

result = db.query("""
SELECT "Customer ID", substr("Order Date",1,4) AS yr, 
       "Order ID", "Quantity", "Product", Sales, profit,
       profit * 1.0 / Sales AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
  AND "Quantity" != 'abc'
  AND "Quantity" IS NOT NULL
""")
rows = db.rows(result)
orders = pd.DataFrame(rows, columns=['Customer ID', 'yr', 'Order ID', 'Quantity', 'Product', 'Sales', 'profit', 'margin'])
orders['Quantity'] = pd.to_numeric(orders['Quantity'])
orders['yr'] = orders['yr'].astype(int)
orders['segment'] = orders['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

stats = orders.groupby(['yr', 'segment']).agg(
    n_orders=('Order ID', 'count'),
    avg_qty=('Quantity', 'mean'),
    avg_margin=('margin', 'mean'),
    total_sales=('Sales', 'sum'),
    total_profit=('profit', 'sum')
).round(4)
print("=== Stats by Year and Segment ===")
print(stats)

print("\n=== Avg Quantity by Year and Segment ===")
qty_stats = orders.groupby(['yr', 'segment'])['Quantity'].mean().round(3)
print(qty_stats)

print("\n=== Quantity Distribution (order counts) ===")
qty_dist = orders.groupby(['segment', 'Quantity']).size().unstack(fill_value=0)
print(qty_dist)

print("\n=== Welch t-test: Top Tier vs Other Quantity per year ===")
for yr in [2022, 2023, 2024]:
    top_qty = orders[(orders['segment'] == 'Top Tier') & (orders['yr'] == yr)]['Quantity']
    other_qty = orders[(orders['segment'] == 'Other') & (orders['yr'] == yr)]['Quantity']
    t_stat, p_val = scipy_stats.ttest_ind(top_qty, other_qty, equal_var=False)
    print(f"{yr}: Top Tier qty={top_qty.mean():.3f} (n={len(top_qty)}), Other qty={other_qty.mean():.3f} (n={len(other_qty)}), t={t_stat:.3f}, p={p_val:.6f}")

# Also compute share of orders with qty>=4 by year/segment
orders['large_order'] = (orders['Quantity'] >= 4).astype(int)
share = orders.groupby(['yr', 'segment'])['large_order'].mean().round(4)
print("\n=== Share of large orders (qty>=4) by year/segment ===")
print(share)

# Correlation between margin and quantity
print("\nOverall corr(margin, qty):", orders['margin'].corr(orders['Quantity']).round(4))