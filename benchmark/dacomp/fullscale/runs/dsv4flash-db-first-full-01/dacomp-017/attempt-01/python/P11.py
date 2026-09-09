import pandas as pd
import numpy as np
from scipy import stats as scipy_stats

with open('/work/top_customers.txt', 'r') as f:
    top_customers = [line.strip() for line in f]

result = db.query("""
SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows = db.rows(result)
hf = pd.DataFrame(rows, columns=['Customer ID', 'Year', 'Quantity'])
hf['Year'] = hf['Year'].astype(int)
hf['Quantity'] = pd.to_numeric(hf['Quantity'])
hf['Segment'] = hf['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

print("=== Welch t-test: Top Tier vs Other Avg Quantity by Year ===")
for yr in [2022, 2023, 2024]:
    top = hf[(hf['Segment'] == 'Top Tier') & (hf['Year'] == yr)]['Quantity']
    other = hf[(hf['Segment'] == 'Other') & (hf['Year'] == yr)]['Quantity']
    t, p = scipy_stats.ttest_ind(top, other, equal_var=False)
    print(f"{yr}: Top Tier={top.mean():.3f} (n={len(top)}), Other={other.mean():.3f} (n={len(other)}), t={t:.3f}, p={p:.4f}")

# Also compare margin by segment
result2 = db.query("""
SELECT "Customer ID", substr("Order Date",1,4) AS yr, profit, Sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
""")
rows2 = db.rows(result2)
hf2 = pd.DataFrame(rows2, columns=['Customer ID', 'Year', 'profit', 'Sales'])
hf2['Year'] = hf2['Year'].astype(int)
hf2['Margin'] = hf2['profit'] / hf2['Sales']
hf2['Segment'] = hf2['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

print("\n=== Avg Margin by Year and Segment ===")
print(hf2.groupby(['Year', 'Segment'])['Margin'].mean().round(4))

print("\n=== Aggregate Margin by Year and Segment ===")
agg = hf2.groupby(['Year', 'Segment']).agg(
    total_profit=('profit', 'sum'),
    total_sales=('Sales', 'sum')
).reset_index()
agg['Agg_Margin'] = agg['total_profit'] / agg['total_sales']
print(agg.round(4))

# Also check product browsing engagement for top vs other
result3 = db.query("""
SELECT pb."Customer ID", pb."Product Category", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Customer ID"
""")
rows3 = db.rows(result3)
browsing = pd.DataFrame(rows3, columns=['Customer ID', 'Product Category', 'avg_browsing', 'avg_like', 'avg_share', 'avg_add_to_cart'])
browsing['Segment'] = browsing['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

print("\n=== Browsing Engagement by Segment ===")
engage = browsing.groupby('Segment')[['avg_browsing', 'avg_like', 'avg_share', 'avg_add_to_cart']].mean().round(3)
print(engage)

# Test significance
for col in ['avg_browsing', 'avg_like', 'avg_share', 'avg_add_to_cart']:
    top = browsing[browsing['Segment'] == 'Top Tier'][col]
    other = browsing[browsing['Segment'] == 'Other'][col]
    t, p = scipy_stats.ttest_ind(top, other, equal_var=False)
    print(f"{col}: Top={top.mean():.3f}, Other={other.mean():.3f}, t={t:.3f}, p={p:.4f}")