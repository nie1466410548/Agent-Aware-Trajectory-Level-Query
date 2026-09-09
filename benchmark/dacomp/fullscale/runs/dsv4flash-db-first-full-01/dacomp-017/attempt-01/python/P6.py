import pandas as pd
import numpy as np
import json

# Load all order data for checking profit = Sales/Quantity relationship
result = db.query("""
SELECT "Product Category", "Product", Sales, profit, "Quantity"
FROM order_information
WHERE "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows = db.rows(result)
all_orders = pd.DataFrame(rows, columns=['Product Category', 'Product', 'Sales', 'profit', 'Quantity'])
all_orders['Quantity'] = pd.to_numeric(all_orders['Quantity'])

# Check if profit == Sales/Quantity
all_orders['pred_profit'] = all_orders['Sales'] / all_orders['Quantity']
all_orders['resid'] = (all_orders['profit'] - all_orders['pred_profit']).abs()
print("Max abs residual (profit vs Sales/Qty):", all_orders['resid'].max())
print("Share of rows where profit exactly = Sales/Qty:", (all_orders['resid'] < 0.001).mean().round(4))

# Check if margin = 1/Quantity for all categories
all_orders['margin'] = all_orders['profit'] / all_orders['Sales']
all_orders['one_over_qty'] = 1 / all_orders['Quantity']
diff = (all_orders['margin'] - all_orders['one_over_qty']).abs()
print("Max abs |margin - 1/qty|:", diff.max())
print("Share within 0.001 of 1/qty:", (diff < 0.001).mean().round(4))

# So the key driver: quantity per order (higher qty => lower margin)
# Decomposition of Home & Furniture aggregate margin change 2023->2024
result2 = db.query("""
SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows2 = db.rows(result2)
hf = pd.DataFrame(rows2, columns=['yr', 'Product', 'Quantity', 'Sales', 'profit'])
hf['Quantity'] = pd.to_numeric(hf['Quantity'])

# Aggregate margin by year
for yr in [2022, 2023, 2024]:
    d = hf[hf['yr'] == yr]
    print(f"{yr}: agg margin = {d['profit'].sum()/d['Sales'].sum():.6f}, avg qty = {d['Quantity'].mean():.3f}")

# Contribution of qty mix change to margin: fix product mix
def decompose(d0, d1):
    # margin change = change due to qty mix within product + product mix
    pass

# Simpler: counterfactual - what would 2024 margin be if avg qty per product stayed at 2023 level?
prod_qty_2023 = hf[hf['yr'] == '2023'].groupby('Product')['Quantity'].mean()
prod_qty_2024 = hf[hf['yr'] == '2024'].groupby('Product')['Quantity'].mean()
print("\nAvg qty by product 2023 vs 2024:")
comp = pd.DataFrame({'qty_2023': prod_qty_2023, 'qty_2024': prod_qty_2024})
print(comp.round(3))

# Margin per product-year if profit = sales/qty, aggregate margin = sum(sales_i/qty_i)/sum(sales_i)
# Compute counterfactual: keep 2024 product sales mix but apply 2023 avg qty per product
hf24 = hf[hf['yr'] == '2024']
sales_by_prod_24 = hf24.groupby('Product')['Sales'].sum()
qty_by_prod_23 = hf[hf['yr'] == '2023'].groupby('Product')['Quantity'].mean()

cf_profit = sum(sales_by_prod_24[p] / qty_by_prod_23[p] for p in sales_by_prod_24.index)
cf_margin = cf_profit / sales_by_prod_24.sum()
print(f"\nActual 2024 margin: {hf24['profit'].sum()/hf24['Sales'].sum():.6f}")
print(f"Counterfactual 2024 margin (2023 qty, 2024 mix): {cf_margin:.6f}")
print(f"Margin decline due to within-product qty increase: {hf24['profit'].sum()/hf24['Sales'].sum() - cf_margin:.6f}")

# Counterfactual: keep 2023 product mix but 2024 qty levels
hf23 = hf[hf['yr'] == '2023']
sales_by_prod_23 = hf23.groupby('Product')['Sales'].sum()
qty_by_prod_24 = hf24.groupby('Product')['Quantity'].mean()
cf2_profit = sum(sales_by_prod_23[p] / qty_by_prod_24[p] for p in sales_by_prod_23.index)
cf2_margin = cf2_profit / sales_by_prod_23.sum()
print(f"\nCounterfactual 2023 margin (2024 qty, 2023 mix): {cf2_margin:.6f}")
print(f"Margin decline due to product mix change (holding qty at 2024): {hf23['profit'].sum()/hf23['Sales'].sum() - cf2_margin:.6f}")