import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Read data from the query results
# S7: yearly sales by category
import json
with open('results/S7.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
cat_df = pd.DataFrame(rows, columns=['Category','yr','total_sales','total_qty','total_profit'])

# S9: yoy growth
with open('results/S9.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
growth_df = pd.DataFrame(rows, columns=['Category','yr','sales','yoy_growth_pct'])

# S10: region-yearly
with open('results/S10.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
reg_df = pd.DataFrame(rows, columns=['Region','Regional Manager','yr','sales','profit','n_orders'])

# S12: overall region stats
with open('results/S12.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
reg_tot_df = pd.DataFrame(rows, columns=['Region','Regional Manager','total_sales','total_profit','profit_margin_pct','n_orders','n_rows'])

# S15: return rates
with open('results/S15.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
ret_df = pd.DataFrame(rows, columns=['Region','Regional Manager','total_orders','returned_orders','return_rate_pct'])

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
for cat in ['Furniture','Office Supplies','Technology']:
    sub = growth_df[growth_df['Category']==cat].dropna()
    ax.bar(sub['yr'].astype(str) + '-' + cat[0], sub['yoy_growth_pct'], label=cat, alpha=0.7)
    # Add value labels
    for i, v in enumerate(sub['yoy_growth_pct']):
        ax.text(i*3 + (0 if cat=='Furniture' else 1 if cat=='Office Supplies' else 2), v + 0.5, f'{v:.1f}%', ha='center', fontsize=8)
ax.set_xlabel('Year')
ax.set_ylabel('YoY Growth (%)')
ax.set_title('Year-over-Year Growth by Category')
ax.legend()
ax.grid(alpha=0.3, axis='y')

# 1c: Profit margin by category
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
# Compute 2015-2018 growth per region
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

# ========== FIGURE 3: Category breakdown by region ==========
fig, ax = plt.subplots(figsize=(12, 6))
# S16: region-category
with open('results/S16.rows.jsonl') as f:
    rows = [json.loads(line) for line in f]
reg_cat_df = pd.DataFrame(rows, columns=['Region','Regional Manager','Category','total_sales','pct_of_region_sales'])

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

print("All figures saved successfully.")