import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data again
res = db.query("""
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit
FROM base GROUP BY Region, Segment, year
""")
df = db.frame(res)
df['margin_pct'] = 100*df['profit']/df['sales']

# Heatmap of margin by Region x Segment (mean over years)
pivot = df.pivot_table(index='Segment', columns='Region', values='margin_pct', aggfunc='mean')
fig, ax = plt.subplots(figsize=(9,5))
im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=-10, vmax=30)
ax.set_xticks(range(len(pivot.columns))); ax.set_xticklabels(pivot.columns)
ax.set_yticks(range(len(pivot.index))); ax.set_yticklabels(pivot.index)
for i in range(pivot.shape[0]):
    for j in range(pivot.shape[1]):
        ax.text(j, i, f'{pivot.values[i,j]:.1f}%', ha='center', va='center',
                color='black' if abs(pivot.values[i,j])<20 else 'white', fontsize=11)
ax.set_title('Average Profit Margin (%) by Region and Segment (2015-2017)')
plt.colorbar(im, ax=ax, label='Profit Margin %')
plt.tight_layout()
plt.savefig('/work/fig8_margin_heatmap.png', dpi=150)
plt.close()

# Category profit by region
res2 = db.query("""
WITH base AS (
  SELECT s1.Region, s2.Category, s2.Quantity*s2."Sales per Unit" AS sales,
         s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Category, SUM(sales) AS sales, SUM(profit) AS profit FROM base GROUP BY Region, Category
""")
cat = db.frame(res2)
cat['margin'] = 100*cat['profit']/cat['sales']

fig, axes = plt.subplots(1, 4, figsize=(18,5), sharey=True)
regions = ['Central','East','South','West']
cats = ['Technology','Office Supplies','Furniture']
for ax, reg in zip(axes, regions):
    sub = cat[cat['Region']==reg].set_index('Category').reindex(cats)
    ax.bar(sub.index, sub['profit'], color=['#2ca02c','#ff7f0e','#1f77b4'])
    for i, (idx, row) in enumerate(sub.iterrows()):
        ax.text(i, row['profit'], f"{row['margin']:.1f}%", ha='center', va='bottom')
    ax.set_title(reg)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.tick_params(axis='x', rotation=15)
axes[0].set_ylabel('Profit ($)')
fig.suptitle('Profit by Category and Region (2015-2017)', fontsize=13)
plt.tight_layout()
plt.savefig('/work/fig9_category_profit_region.png', dpi=150)
plt.close()

# Compute key summary table for the report
res3 = db.query("""
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers
FROM base GROUP BY Region, Segment, year
""")
df3 = db.frame(res3)
df3['margin_pct'] = round(100*df3['profit']/df3['sales'],2)
df3['profit_per_customer'] = round(df3['profit']/df3['customers'],2)

# YoY growth of profit per region-segment from 2015->2017 (CAGR-like)
pivot_sales = df3.pivot_table(index=['Region','Segment'], columns='year', values='sales')
pivot_profit = df3.pivot_table(index=['Region','Segment'], columns='year', values='profit')
pivot_profit['total_profit'] = pivot_profit[['2015','2016','2017']].sum(axis=1)
pivot_sales['total_sales'] = pivot_sales[['2015','2016','2017']].sum(axis=1)
summary = pd.DataFrame({
    'Total Sales': pivot_sales['total_sales'],
    'Total Profit': pivot_profit['total_profit'],
    '2015 Sales': pivot_sales['2015'],
    '2016 Sales': pivot_sales['2016'],
    '2017 Sales': pivot_sales['2017'],
    '2015 Profit': pivot_profit['2015'],
    '2016 Profit': pivot_profit['2016'],
    '2017 Profit': pivot_profit['2017'],
})
summary['Margin 15-17 %'] = round(100*summary['Total Profit']/summary['Total Sales'],2)
summary['Sales Growth 15-17 %'] = round(100*(summary['2017 Sales']/summary['2015 Sales']-1),1)
summary['Profit Growth 15-17 %'] = round(100*(summary['2017 Profit']/summary['2015 Profit']-1),1)
print(summary.round(0).to_string())
print("\nSouth Home Office 2017 loss:", pivot_profit.loc[('South','Home Office'),'2017'])
print("\nCentral Consumer margin 2017:", round(100*pivot_profit.loc[('Central','Consumer'),'2017']/pivot_sales.loc[('Central','Consumer'),'2017'],2))
print("Figures created: fig8, fig9")
