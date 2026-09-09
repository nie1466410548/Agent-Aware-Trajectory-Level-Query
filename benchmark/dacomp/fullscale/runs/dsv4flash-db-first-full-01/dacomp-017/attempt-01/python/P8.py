import pandas as pd
import numpy as np
import json

result2 = db.query("""
SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows2 = db.rows(result2)
hf = pd.DataFrame(rows2, columns=['yr', 'Product', 'Quantity', 'Sales', 'profit'])
hf['Quantity'] = pd.to_numeric(hf['Quantity'])
hf['yr'] = hf['yr'].astype(int)

for yr in [2022, 2023, 2024]:
    d = hf[hf['yr'] == yr]
    print(f"{yr}: agg margin = {d['profit'].sum()/d['Sales'].sum():.6f}, avg qty = {d['Quantity'].mean():.3f}, n={len(d)}")

# Verify profit = Sales/Quantity pattern for Home & Furniture
hf['pred'] = hf['Sales'] / hf['Quantity']
hf['resid'] = (hf['profit'] - hf['pred']).abs()
print("\nRows where profit == Sales/Qty exactly (H&F):", (hf['resid'] < 0.001).mean().round(4))
print("Rows where margin == 1/qty (H&F):", ((hf['profit']/hf['Sales'] - 1/hf['Quantity']).abs() < 0.001).mean().round(4))

# Per-product avg qty by year
prod_qty = hf.groupby(['Product', 'yr'])['Quantity'].mean().unstack().round(3)
print("\nAvg quantity per order by product-year:")
print(prod_qty)

# Per-product margin by year
prod_margin = hf.groupby(['Product', 'yr']).apply(lambda g: g['profit'].sum()/g['Sales'].sum()).unstack().round(4)
print("\nProfit margin by product-year:")
print(prod_margin)

# Decomposition: margin change 2023->2024
hf23 = hf[hf['yr'] == 2023]
hf24 = hf[hf['yr'] == 2024]
m23 = hf23['profit'].sum()/hf23['Sales'].sum()
m24 = hf24['profit'].sum()/hf24['Sales'].sum()
print(f"\nMargin 2023: {m23:.6f}, 2024: {m24:.6f}, change: {m24-m23:.6f}")

# Counterfactual 1: 2024 product sales mix with 2023 per-product avg qty (margin=1/qty implied)
# Aggregate margin = sum(sales_p * (1/qty_p_23)) / sum(sales_p)  [since profit=sales/qty]
sales24 = hf24.groupby('Product')['Sales'].sum()
qty23 = hf23.groupby('Product')['Quantity'].mean()
cf_margin_q23 = sum(sales24[p] * (1/qty23[p]) for p in sales24.index) / sales24.sum()
print(f"CF 2024 margin with 2023 qty levels (same product mix): {cf_margin_q23:.6f}")

# Counterfactual 2: 2023 product sales mix with 2024 per-product avg qty
sales23 = hf23.groupby('Product')['Sales'].sum()
qty24 = hf24.groupby('Product')['Quantity'].mean()
cf_margin_q24 = sum(sales23[p] * (1/qty24[p]) for p in sales23.index) / sales23.sum()
print(f"CF 2023 margin with 2024 qty levels (same product mix): {cf_margin_q24:.6f}")

print(f"\nQuantity-level contribution (mix-of-qty effect): {m23 - cf_margin_q24:.6f}")
print(f"Product-mix contribution (mix-of-product effect): {cf_margin_q24 - m24:.6f}")

# Compare qty growth per segment
hf2 = hf.copy()
# load top customers
with open('/work/top_customers.txt', 'r') as f:
    top = [line.strip() for line in f]
seg_map = pd.Series(['Top Tier' if c in top else 'Other' for c in []])
# Actually need Customer ID; requery with customer id
print("\n-- Requerying with Customer ID --")