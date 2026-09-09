import os
os.makedirs('work', exist_ok=True)
print("Work directory created/verified")

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Get data via db queries
r = db.query("SELECT Category, CAST(strftime('%Y', \"Order Date\") AS INTEGER) AS yr, SUM(Sales) AS total_sales, SUM(Quantity) AS total_qty, SUM(profit) AS total_profit FROM \"order\" GROUP BY Category, yr ORDER BY Category, yr")
cat_df = db.frame(r)

r = db.query("""WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
)
SELECT Category, yr, sales, ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly ORDER BY Category, yr""")
growth_df = db.frame(r)

r = db.query("""SELECT o.Region, sp."Regional Manager", CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr, SUM(o.Sales) AS sales, SUM(o.profit) AS profit, COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", yr ORDER BY o.Region, yr""")
reg_df = db.frame(r)

r = db.query("""SELECT o.Region, sp."Regional Manager", SUM(o.Sales) AS total_sales, SUM(o.profit) AS total_profit, ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS profit_margin_pct, COUNT(DISTINCT o."Order ID") AS n_orders, COUNT(*) AS n_rows
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager" ORDER BY total_sales DESC""")
reg_tot_df = db.frame(r)

r = db.query("""WITH order_returns AS (
  SELECT DISTINCT o."Order ID", o.Region, sp."Regional Manager", CASE WHEN r."Return" = 'Yes' THEN 1 ELSE 0 END AS is_returned
  FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
)
SELECT Region, "Regional Manager", COUNT(DISTINCT "Order ID") AS total_orders, SUM(is_returned) AS returned_orders, ROUND(100.0 * SUM(is_returned) / COUNT(DISTINCT "Order ID"), 2) AS return_rate_pct
FROM order_returns GROUP BY Region, "Regional Manager" ORDER BY return_rate_pct DESC""")
ret_df = db.frame(r)

r = db.query("""SELECT o.Region, sp."Regional Manager", o.Category, SUM(o.Sales) AS total_sales, ROUND(100.0 * SUM(o.Sales) / SUM(SUM(o.Sales)) OVER (PARTITION BY o.Region), 2) AS pct_of_region_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", o.Category ORDER BY o.Region, total_sales DESC""")
reg_cat_df = db.frame(r)

print("Data loaded successfully")

# ========== FIGURE 1: Category Sales Trends ==========
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# 1a: Sales by category over years
ax = axes[0]
for cat in ['Furniture','Office Supplies','Technology']:
    sub = cat_df[cat_df['Category']==cat]
    ax.plot(sub['yr'], sub['total_sales']/1e6, marker='o', linewidth=2.5, label=cat)
ax.set_xlabel('Year')
ax.set_ylabel('Total Sales (Millions)')
ax.set_title('Category Sales Trends (2015-2018)')
ax.legend()
ax.grid(alpha=0.3)

# 1b: YoY Growth rates
ax = axes[1]
growth_plot = growth_df.dropna().copy()
categories = ['Furniture','Office Supplies','Technology']
years = [2016, 2017, 2018]
x = np.arange(len(years))
width = 0.25
for i, cat in enumerate(categories):
    sub = growth_plot[growth_plot['Category']==cat]
    vals = [sub[sub['yr']==y]['yoy_growth_pct'].values[0] for y in years]
    bars = ax.bar(x + i*width, vals, width, label=cat, alpha=0.7)
    for j, v in enumerate(vals):
        ax.text(x[j] + i*width, v + 0.5, f'{v:.1f}%', ha='center', fontsize=8)
ax.set_xticks(x + width)
ax.set_xticklabels(['2016','2017','2018'])
ax.set_ylabel('YoY Growth (%)')
ax.set_title('Year-over-Year Growth by Category')
ax.legend()
ax.grid(alpha=0.3, axis='y')

# 1c: Overall profit margin by category
ax = axes[2]
cat_profit = cat_df.groupby('Category')[['total_sales','total_profit']].sum().reset_index()
cat_profit['margin'] = 100 * cat_profit['total_profit'] / cat_profit['total_sales']
colors = ['#ff9999','#66b3ff','#99ff99']
bars = ax.bar(cat_profit['Category'], cat_profit['margin'], color=colors, alpha=0.8)
for bar, val in zip(bars, cat_profit['margin']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2, f'{val:.2f}%', ha='center', fontsize=10)
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Overall Profit Margin by Category')
ax.grid(alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('work/category_sales_trends.png', dpi=150)
plt.close()
print("Figure 1 saved")

# ========== FIGURE 2: Regional Manager Performance ==========
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 2a: Total sales by region/manager
ax = axes[0,0]
reg_tot_sorted = reg_tot_df.sort_values('total_sales', ascending=True)
colors = plt.cm.Paired(np.linspace(0, 1, len(reg_tot_sorted)))
bars = ax.barh(reg_tot_sorted['Region'] + ' (' + reg_tot_sorted['Regional Manager'] + ')', 
               reg_tot_sorted['total_sales']/1e6, color=colors)
for bar, val in zip(bars, reg_tot_sorted['total_sales']):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, f'{val/1e6:.2f}M', 
            va='center', fontsize=9)
ax.set_xlabel('Total Sales (Millions)')
ax.set_title('Total Sales by Region (2015-2018)')

# 2b: Profit margin by region
ax = axes[0,1]
reg_tot_sorted2 = reg_tot_df.sort_values('profit_margin_pct', ascending=True)
colors = plt.cm.Paired(np.linspace(0, 1, len(reg_tot_sorted2)))
bars = ax.barh(reg_tot_sorted2['Region'] + ' (' + reg_tot_sorted2['Regional Manager'] + ')', 
               reg_tot_sorted2['profit_margin_pct'], color=colors)
for bar, val in zip(bars, reg_tot_sorted2['profit_margin_pct']):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{val:.2f}%', 
            va='center', fontsize=9)
ax.set_xlabel('Profit Margin (%)')
ax.set_title('Profit Margin by Region')

# 2c: Return rate by region
ax = axes[1,0]
ret_sorted = ret_df.sort_values('return_rate_pct', ascending=True)
colors = plt.cm.Paired(np.linspace(0, 1, len(ret_sorted)))
bars = ax.barh(ret_sorted['Region'] + ' (' + ret_sorted['Regional Manager'] + ')', 
               ret_sorted['return_rate_pct'], color=colors)
for bar, val in zip(bars, ret_sorted['return_rate_pct']):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, f'{val:.2f}%', 
            va='center', fontsize=9)
ax.set_xlabel('Return Rate (%)')
ax.set_title('Order Return Rate by Region')

# 2d: Sales growth (2015 to 2018) by region
ax = axes[1,1]
reg_2015 = reg_df[reg_df['yr']==2015][['Region','sales']].rename(columns={'sales':'sales_2015'})
reg_2018 = reg_df[reg_df['yr']==2018][['Region','sales']].rename(columns={'sales':'sales_2018'})
reg_growth = reg_2015.merge(reg_2018, on='Region')
reg_growth['growth_pct'] = 100 * (reg_growth['sales_2018'] - reg_growth['sales_2015']) / reg_growth['sales_2015']
reg_growth = reg_growth.merge(reg_tot_df[['Region','Regional Manager']], on='Region')
reg_growth = reg_growth.sort_values('growth_pct', ascending=True)
colors = plt.cm.Paired(np.linspace(0, 1, len(reg_growth)))
bars = ax.barh(reg_growth['Region'] + ' (' + reg_growth['Regional Manager'] + ')', 
               reg_growth['growth_pct'], color=colors)
for bar, val in zip(bars, reg_growth['growth_pct']):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', 
            va='center', fontsize=9)
ax.set_xlabel('Total Sales Growth 2015→2018 (%)')
ax.set_title('Regional Sales Growth (2015 to 2018)')

plt.tight_layout()
plt.savefig('work/regional_manager_performance.png', dpi=150)
plt.close()
print("Figure 2 saved")

# ========== FIGURE 3: Category breakdown by region ==========
fig, ax = plt.subplots(figsize=(12, 6))
regions = reg_cat_df['Region'].unique()
categories = ['Technology','Furniture','Office Supplies']
x = np.arange(len(regions))
width = 0.25
for i, cat in enumerate(categories):
    sub = reg_cat_df[reg_cat_df['Category']==cat]
    sub = sub.set_index('Region').reindex(regions)
    ax.bar(x + i*width, sub['total_sales']/1e6, width, label=cat, alpha=0.8)
ax.set_xticks(x + width)
ax.set_xticklabels([f'{r}\n({m})' for r, m in zip(regions, reg_tot_df.set_index('Region').loc[regions, 'Regional Manager'])])
ax.set_ylabel('Total Sales (Millions)')
ax.set_title('Sales by Category in Each Region')
ax.legend()
ax.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('work/category_by_region.png', dpi=150)
plt.close()
print("Figure 3 saved")

print("All figures saved successfully!")