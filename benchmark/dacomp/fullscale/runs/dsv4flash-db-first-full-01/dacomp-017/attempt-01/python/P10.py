import pandas as pd
import numpy as np
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# ========== FIGURE 1: Profit margin by category and year ==========
result = db.query("""
SELECT "Product Category", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
""")
rows = db.rows(result)
margins = pd.DataFrame(rows, columns=['Category', 'Year', 'Margin'])
margins['Year'] = margins['Year'].astype(int)

fig, ax = plt.subplots(figsize=(10, 6))
for cat in margins['Category'].unique():
    d = margins[margins['Category'] == cat]
    ax.plot(d['Year'], d['Margin'], marker='o', label=cat, linewidth=2)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Profit Margin (profit / Sales)', fontsize=12)
ax.set_title('Annual Profit Margin by Product Category (2022–2024)', fontsize=14)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig1_category_margins.png', dpi=150)
plt.close()
print("Figure 1 saved")

# ========== FIGURE 2: Home & Furniture product-level margins ==========
result2 = db.query("""
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY "Product", yr
""")
rows2 = db.rows(result2)
prod_margins = pd.DataFrame(rows2, columns=['Product', 'Year', 'Margin'])
prod_margins['Year'] = prod_margins['Year'].astype(int)

fig, ax = plt.subplots(figsize=(14, 6))
for prod in prod_margins['Product'].unique():
    d = prod_margins[prod_margins['Product'] == prod]
    ax.plot(d['Year'], d['Margin'], marker='o', label=prod, linewidth=2)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Profit Margin', fontsize=12)
ax.set_title('Home & Furniture: Product-Level Profit Margins (2022–2024)', fontsize=14)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig2_product_margins.png', dpi=150)
plt.close()
print("Figure 2 saved")

# ========== FIGURE 3: Avg quantity per order by segment and year ==========
with open('/work/top_customers.txt', 'r') as f:
    top_customers = [line.strip() for line in f]

result3 = db.query("""
SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
""")
rows3 = db.rows(result3)
hf_qty = pd.DataFrame(rows3, columns=['Customer ID', 'Year', 'Quantity'])
hf_qty['Year'] = hf_qty['Year'].astype(int)
hf_qty['Quantity'] = pd.to_numeric(hf_qty['Quantity'])
hf_qty['Segment'] = hf_qty['Customer ID'].apply(lambda x: 'Top Tier' if x in top_customers else 'Other')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Avg quantity
avg_qty = hf_qty.groupby(['Year', 'Segment'])['Quantity'].mean().reset_index()
sns.barplot(data=avg_qty, x='Year', y='Quantity', hue='Segment', ax=ax1)
ax1.set_title('Avg Quantity per Order by Segment', fontsize=12)
ax1.set_ylabel('Avg Quantity')

# Share of large orders (qty>=4)
hf_qty['Large'] = (hf_qty['Quantity'] >= 4).astype(int)
large_share = hf_qty.groupby(['Year', 'Segment'])['Large'].mean().reset_index()
sns.barplot(data=large_share, x='Year', y='Large', hue='Segment', ax=ax2)
ax2.set_title('Share of Orders with Quantity ≥ 4', fontsize=12)
ax2.set_ylabel('Share')

plt.tight_layout()
plt.savefig('/work/fig3_qty_by_segment.png', dpi=150)
plt.close()
print("Figure 3 saved")

# ========== FIGURE 4: RFM segment distribution pie ==========
rfm = pd.read_csv('/work/rfm_segmentation.csv')
seg_counts = rfm['Segment'].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
ax.pie(seg_counts.values, labels=seg_counts.index, autopct='%1.1f%%', 
       colors=colors, startangle=90, explode=(0.05, 0.05, 0.05, 0.05))
ax.set_title('RFM Customer Segment Distribution\n(Home & Furniture)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig4_rfm_segments.png', dpi=150)
plt.close()
print("Figure 4 saved")

# ========== FIGURE 5: Margin vs Quantity scatter ==========
result5 = db.query("""
SELECT profit, Sales, "Quantity", "Discount"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
LIMIT 5000
""")
rows5 = db.rows(result5)
scatter = pd.DataFrame(rows5, columns=['profit', 'Sales', 'Quantity', 'Discount'])
scatter['Quantity'] = pd.to_numeric(scatter['Quantity'])
scatter['Discount'] = pd.to_numeric(scatter['Discount'])
scatter['Margin'] = scatter['profit'] / scatter['Sales']

fig, ax = plt.subplots(figsize=(10, 6))
scatter_sampled = scatter.sample(min(5000, len(scatter)), random_state=42)
scatter_plot = ax.scatter(scatter_sampled['Quantity'], scatter_sampled['Margin'], 
                          c=scatter_sampled['Discount'], cmap='viridis', alpha=0.5, s=20)
ax.set_xlabel('Quantity per Order', fontsize=12)
ax.set_ylabel('Per-Order Profit Margin', fontsize=12)
ax.set_title('Home & Furniture: Margin vs Quantity (colored by Discount)', fontsize=14)
cbar = plt.colorbar(scatter_plot, ax=ax)
cbar.set_label('Discount Rate')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig5_margin_vs_qty.png', dpi=150)
plt.close()
print("Figure 5 saved")

# ========== FIGURE 6: Product sales share shift ==========
result6 = db.query("""
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales DESC
""")
rows6 = db.rows(result6)
share = pd.DataFrame(rows6, columns=['Product', 'Year', 'Sales'])
share['Year'] = share['Year'].astype(int)
share['Share'] = share.groupby('Year')['Sales'].transform(lambda x: x / x.sum())

fig, ax = plt.subplots(figsize=(12, 6))
for prod in share['Product'].unique():
    d = share[share['Product'] == prod]
    ax.plot(d['Year'], d['Share'], marker='o', label=prod, linewidth=2)
ax.set_xlabel('Year', fontsize=12)
ax.set_ylabel('Sales Share', fontsize=12)
ax.set_title('Home & Furniture: Product Sales Share by Year', fontsize=14)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig6_product_share.png', dpi=150)
plt.close()
print("Figure 6 saved")

print("All figures generated successfully")