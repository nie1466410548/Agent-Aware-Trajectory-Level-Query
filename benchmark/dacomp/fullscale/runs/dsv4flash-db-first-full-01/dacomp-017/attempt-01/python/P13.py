import pandas as pd
import numpy as np
import json

# RFM summary
rfm = pd.read_csv('/work/rfm_segmentation.csv')
print("=== RFM Segment Summary ===")
print(rfm.groupby('Segment')[['recency', 'frequency', 'monetary']].mean().round(2))
print("\nSegment counts:", rfm['Segment'].value_counts().to_dict())
print("RFM score ranges:", rfm.groupby('Segment')['RFM_total'].min().to_dict())

# Top tier profit share
with open('/work/top_customers.txt', 'r') as f:
    top_customers = [line.strip() for line in f]

result = db.query("""
SELECT "Customer ID", SUM(profit) AS profit, SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Customer ID"
""")
rows = db.rows(result)
cust = pd.DataFrame(rows, columns=['Customer ID', 'profit', 'sales'])
cust['Top'] = cust['Customer ID'].isin(top_customers)
print("\n=== Profit share ===")
print("Top Tier customers:", cust['Top'].sum(), "of", len(cust))
print("Top Tier profit share:", round(cust[cust['Top']]['profit'].sum() / cust['profit'].sum(), 4))
print("Top Tier sales share:", round(cust[cust['Top']]['sales'].sum() / cust['sales'].sum(), 4))

# Overall H&F totals
result2 = db.query("""
SELECT COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit
FROM order_information WHERE "Product Category" = 'Home & Furniture'
""")
r2 = db.rows(result2)[0]
print("\n=== H&F overall totals ===")
print("Orders:", r2[0], "Sales:", r2[1], "Profit:", round(r2[2],1))

# Check number of distinct Order IDs / rows per order (1 row per order?)
result3 = db.query("""
SELECT COUNT(DISTINCT "Order ID") AS distinct_orders, COUNT(*) AS rows_count
FROM order_information WHERE "Product Category" = 'Home & Furniture'
""")
r3 = db.rows(result3)[0]
print("Distinct Order IDs:", r3[0], "Rows:", r3[1], "-> rows per order:", round(r3[1]/r3[0],2))