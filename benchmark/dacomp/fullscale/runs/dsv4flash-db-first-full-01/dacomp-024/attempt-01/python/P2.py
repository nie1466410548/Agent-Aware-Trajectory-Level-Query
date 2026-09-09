import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data
res = db.query("""
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
FROM base GROUP BY Region, Segment, year
ORDER BY year, Region, Segment
""")
df = db.frame(res)

# Compute derived metrics
df['margin_pct'] = round(100 * df['profit'] / df['sales'], 2)
df['profit_per_customer'] = round(df['profit'] / df['customers'], 2)
df['sales_per_customer'] = round(df['sales'] / df['customers'], 2)
df['avg_order_value'] = round(df['sales'] / df['orders'], 2)

# Compute year total customers and sales for penetration share
year_totals = df.groupby('year')[['customers', 'sales']].sum().rename(
    columns={'customers': 'total_customers', 'sales': 'total_sales'})
df = df.merge(year_totals, on='year')
df['customer_share_pct'] = round(100 * df['customers'] / df['total_customers'], 1)
df['sales_share_pct'] = round(100 * df['sales'] / df['total_sales'], 1)

# Sort by year for growth computation
df = df.sort_values(['Region', 'Segment', 'year']).reset_index(drop=True)
for col in ['sales', 'profit', 'customers', 'orders']:
    df[col + '_yoy'] = df.groupby(['Region', 'Segment'])[col].pct_change() * 100

# Aggregate to region level
region_year = df.groupby(['Region', 'year']).agg(
    sales=('sales', 'sum'), profit=('profit', 'sum'),
    customers=('customers', 'sum'), orders=('orders', 'sum')).reset_index()
region_year['margin_pct'] = round(100 * region_year['profit'] / region_year['sales'], 2)
region_year['profit_per_customer'] = round(region_year['profit'] / region_year['customers'], 2)

# Segment level
seg_year = df.groupby(['Segment', 'year']).agg(
    sales=('sales', 'sum'), profit=('profit', 'sum'),
    customers=('customers', 'sum')).reset_index()
seg_year['margin_pct'] = round(100 * seg_year['profit'] / seg_year['sales'], 2)

plt.rcParams.update({'font.size': 10, 'figure.figsize': (12, 8)})

# ============== FIGURE 1: Sales by Region (2015-2017) ==============
fig, ax = plt.subplots(figsize=(10,6))
regions = ['Central', 'East', 'South', 'West']
years = ['2015','2016','2017']
colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']
x = np.arange(len(years))
width = 0.2
for i, reg in enumerate(regions):
    vals = region_year[region_year['Region']==reg].set_index('year').loc[years, 'sales'].values
    ax.bar(x + i*width, vals, width, label=reg, color=colors[i])
ax.set_xticks(x + width*1.5)
ax.set_xticklabels(years)
ax.set_ylabel('Total Sales ($)')
ax.set_title('Total Sales by Region (2015-2017)')
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig('/work/fig1_sales_by_region.png', dpi=150)
plt.close()

# ============== FIGURE 2: Profit Margin by Region (2015-2017) ==============
fig, ax = plt.subplots(figsize=(10,6))
for i, reg in enumerate(regions):
    vals = region_year[region_year['Region']==reg].set_index('year').loc[years, 'margin_pct'].values
    ax.plot(years, vals, 'o-', label=reg, color=colors[i], linewidth=2, markersize=8)
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Profit Margin by Region (2015-2017)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig2_margin_by_region.png', dpi=150)
plt.close()

# ============== FIGURE 3: Sales by Region-Segment stacked bar 2017 ==============
fig, ax = plt.subplots(figsize=(12,6))
df_2017 = df[df['year']=='2017'].copy()
segments = ['Consumer', 'Corporate', 'Home Office']
seg_colors = ['#1a55a0', '#e68a2e', '#3a7a3a']
x = np.arange(len(regions))
width = 0.25
for i, seg in enumerate(segments):
    vals = [df_2017[(df_2017['Region']==r) & (df_2017['Segment']==seg)]['sales'].values[0] for r in regions]
    ax.bar(x + i*width, vals, width, label=seg, color=seg_colors[i])
ax.set_xticks(x + width)
ax.set_xticklabels(regions)
ax.set_ylabel('Sales ($)')
ax.set_title('Sales by Region and Segment (2017)')
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig('/work/fig3_sales_region_segment_2017.png', dpi=150)
plt.close()

# ============== FIGURE 4: Profit Margin by Region-Segment (2017) ==============
fig, ax = plt.subplots(figsize=(12,6))
for i, seg in enumerate(segments):
    vals = [df_2017[(df_2017['Region']==r) & (df_2017['Segment']==seg)]['margin_pct'].values[0] for r in regions]
    ax.bar(x + i*width, vals, width, label=seg, color=seg_colors[i])
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xticks(x + width)
ax.set_xticklabels(regions)
ax.set_ylabel('Profit Margin (%)')
ax.set_title('Profit Margin by Region and Segment (2017)')
ax.legend()
plt.tight_layout()
plt.savefig('/work/fig4_margin_region_segment_2017.png', dpi=150)
plt.close()

# ============== FIGURE 5: Total Profit by Region-Segment (2015-2017) ==============
fig, ax = plt.subplots(figsize=(12,6))
df_total = df.groupby(['Region','Segment']).agg(sales=('sales','sum'), profit=('profit','sum')).reset_index()
for i, seg in enumerate(segments):
    vals = [df_total[(df_total['Region']==r) & (df_total['Segment']==seg)]['profit'].values[0] for r in regions]
    ax.bar(x + i*width, vals, width, label=seg, color=seg_colors[i])
ax.axhline(y=0, color='black', linewidth=0.5)
ax.set_xticks(x + width)
ax.set_xticklabels(regions)
ax.set_ylabel('Total Profit ($)')
ax.set_title('Total Profit by Region and Segment (2015-2017 Combined)')
ax.legend()
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig('/work/fig5_total_profit_region_segment.png', dpi=150)
plt.close()

# ============== FIGURE 6: Customer Penetration Share by Region ==============
fig, ax = plt.subplots(figsize=(10,6))
region_year['customer_share_pct'] = region_year.groupby('year')['customers'].transform(lambda x: 100*x/x.sum())
for i, reg in enumerate(regions):
    vals = region_year[region_year['Region']==reg].set_index('year').loc[years, 'customer_share_pct'].values
    ax.plot(years, vals, 'o-', label=reg, color=colors[i], linewidth=2, markersize=8)
ax.set_ylabel('Share of Total Customers (%)')
ax.set_title('Customer Penetration Share by Region (2015-2017)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig6_customer_penetration.png', dpi=150)
plt.close()

# ============== FIGURE 7: Sales YoY Growth by Region ==============
fig, ax = plt.subplots(figsize=(10,6))
ry = region_year.copy()
ry = ry.sort_values(['Region','year'])
ry['sales_growth'] = ry.groupby('Region')['sales'].pct_change() * 100
for i, reg in enumerate(regions):
    vals = [ry[(ry['Region']==reg) & (ry['year']==y)]['sales_growth'].values[0] for y in ['2016','2017']]
    ax.bar([f'{reg}-2016', f'{reg}-2017'], vals, color=colors[i], alpha=0.7, width=0.6)
ax.set_ylabel('Sales Growth (%)')
ax.set_title('Year-over-Year Sales Growth by Region')
ax.axhline(y=0, color='black', linewidth=0.5)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/work/fig7_sales_growth_region.png', dpi=150)
plt.close()

print("All figures created successfully.")
print("\nBest performing region-segment combos (total profit 2015-2017):")
print(df_total.sort_values('profit', ascending=False).head(10))
print("\nBest margin combos (2017):")
print(df_2017[['Region','Segment','margin_pct']].sort_values('margin_pct', ascending=False))
print("\nProfit per customer (2017):")
print(df_2017[['Region','Segment','profit_per_customer']].sort_values('profit_per_customer', ascending=False))