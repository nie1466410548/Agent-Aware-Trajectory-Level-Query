import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import json
import os

# Read the full result files
def read_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            rows.append(json.loads(line))
    return rows

# ---- S14: 2024 seasonal product totals ----
rows14 = read_rows('/results/S14.rows.jsonl')
cols14 = ['season','product','total_qty','n_trans','total_amount','rnk']
df14 = pd.DataFrame(rows14, columns=cols14)
print("=== Seasonal product totals 2024 ===")
print(df14.to_string(index=False))

# ---- S16: Channel x Season x Product ----
rows16 = read_rows('/results/S16.rows.jsonl')
cols16 = ['season','channel','product','total_qty','n_trans']
df16 = pd.DataFrame(rows16, columns=cols16)

# ---- S23: Product x Channel overall ----
rows23 = read_rows('/results/S23.rows.jsonl')
cols23 = ['product','channel','n_trans','total_qty','avg_price','rev_per_unit']
df23 = pd.DataFrame(rows23, columns=cols23)

# ---- S24: Product x Channel satisfaction ----
rows24 = read_rows('/results/S24.rows.jsonl')
cols24 = ['product','channel','very_sat_rate','sat_rate','repurchase_high']
df24 = pd.DataFrame(rows24, columns=cols24)

# ---- S25: Wheat channel by season ----
rows25 = read_rows('/results/S25.rows.jsonl')
cols25 = ['season','channel','n_trans','total_qty','avg_price','avg_amount']
df25 = pd.DataFrame(rows25, columns=cols25)

# ============================================================
# FIGURE 1: Seasonal Sales Quantity by Product (grouped bar)
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
products = ['Wheat','Maize','Vegetables','Rice','Fruit']
seasons = ['Spring','Summer','Autumn','Winter']
# Color map
colors = ['#2E86AB','#A23B72','#F18F01','#C73E1D','#6A994E']

# Pivot data
df_pivot = df14.pivot_table(index='product', columns='season', values='total_qty', aggfunc='sum')
# Reorder
df_pivot = df_pivot.reindex(products)
df_pivot = df_pivot[seasons]

x = np.arange(len(products))
w = 0.2
for i, s in enumerate(seasons):
    ax.bar(x + i*w - 1.5*w, df_pivot[s]/1000, w, label=s, color=colors[i], edgecolor='white', linewidth=0.5)

ax.set_xlabel('Agricultural Product', fontsize=12)
ax.set_ylabel('Total Sales Quantity (thousands of units)', fontsize=12)
ax.set_title('2024 Seasonal Sales Quantity by Agricultural Product', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(products, fontsize=11)
ax.legend(title='Season', fontsize=10)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig1_seasonal_qty_by_product.png', dpi=150)
plt.close()
print("Figure 1 saved.")

# ============================================================
# FIGURE 2: Wheat's channel performance (quantity, price, satisfaction)
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Wheat data from S23
wheat_df = df23[df23['product']=='Wheat'].copy()
wheat_df = wheat_df.sort_values('total_qty', ascending=False)

# 2a: Total quantity by channel
ax = axes[0]
bars = ax.bar(wheat_df['channel'], wheat_df['total_qty']/1000, color=['#2E86AB','#A23B72','#F18F01','#C73E1D'], edgecolor='white')
ax.set_xlabel('Sales Channel', fontsize=11)
ax.set_ylabel('Total Quantity (thousands of units)', fontsize=11)
ax.set_title('Wheat: Total Sales Quantity by Channel', fontsize=12, fontweight='bold')
for bar, val in zip(bars, wheat_df['total_qty']/1000):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+10, f'{val:.0f}k', ha='center', fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 2b: Average price by channel
ax = axes[1]
bars = ax.bar(wheat_df['channel'], wheat_df['avg_price'], color=['#2E86AB','#A23B72','#F18F01','#C73E1D'], edgecolor='white')
ax.set_xlabel('Sales Channel', fontsize=11)
ax.set_ylabel('Average Unit Price (yuan)', fontsize=11)
ax.set_title('Wheat: Average Unit Price by Channel', fontsize=12, fontweight='bold')
for bar, val in zip(bars, wheat_df['avg_price']):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, f'{val:.2f}', ha='center', fontsize=9)
ax.grid(axis='y', alpha=0.3)

# 2c: Satisfaction and repurchase rates by channel
wheat_sat = df24[df24['product']=='Wheat'].copy()
wheat_sat = wheat_sat.sort_values('repurchase_high', ascending=False)
ax = axes[2]
x = np.arange(len(wheat_sat))
w = 0.3
ax.bar(x-w/2, wheat_sat['sat_rate']+wheat_sat['very_sat_rate'], w, label='Satisfied+Very Satisfied', color='#2E86AB', edgecolor='white')
ax.bar(x+w/2, wheat_sat['repurchase_high'], w, label='High Repurchase Intention', color='#A23B72', edgecolor='white')
ax.set_xticks(x)
ax.set_xticklabels(wheat_sat['channel'], fontsize=10)
ax.set_ylabel('Rate', fontsize=11)
ax.set_title('Wheat: Satisfaction & Repurchase by Channel', fontsize=12, fontweight='bold')
ax.legend(fontsize=9)
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/fig2_wheat_channel_performance.png', dpi=150)
plt.close()
print("Figure 2 saved.")

# ============================================================
# FIGURE 3: Channel performance across all products - heatmap
# ============================================================
# Create a pivot table of channel share per product
df23_pivot = df23.pivot_table(index='product', columns='channel', values='total_qty', aggfunc='sum')
df23_pivot = df23_pivot[['Cooperative','Direct sales','E-commerce Platform','Wholesale market']]
# Convert to percentage of each product's total
df23_pct = df23_pivot.div(df23_pivot.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(10, 5))
im = ax.imshow(df23_pct.values, cmap='YlGnBu', aspect='auto', vmin=0, vmax=60)
ax.set_xticks(range(len(df23_pct.columns)))
ax.set_xticklabels(df23_pct.columns, fontsize=10)
ax.set_yticks(range(len(df23_pct.index)))
ax.set_yticklabels(df23_pct.index, fontsize=10)
ax.set_title('Product Sales Channel Distribution (% of Total Quantity) - 2024', fontsize=13, fontweight='bold')
for i in range(len(df23_pct.index)):
    for j in range(len(df23_pct.columns)):
        val = df23_pct.values[i, j]
        ax.text(j, i, f'{val:.0f}%', ha='center', va='center', fontsize=10, fontweight='bold',
                color='white' if val > 30 else 'black')
plt.tight_layout()
plt.savefig('/work/fig3_channel_distribution_heatmap.png', dpi=150)
plt.close()
print("Figure 3 saved.")

# ============================================================
# FIGURE 4: Wheat seasonal channel breakdown
# ============================================================
fig, ax = plt.subplots(figsize=(10, 6))
wheat_season_channel = df25.pivot_table(index='season', columns='channel', values='total_qty', aggfunc='sum')
wheat_season_channel = wheat_season_channel.reindex(['Spring','Summer','Autumn','Winter'])
wheat_season_channel = wheat_season_channel[['Cooperative','Direct sales','E-commerce Platform','Wholesale market']]
wheat_season_channel.plot(kind='bar', stacked=True, ax=ax, color=['#2E86AB','#A23B72','#F18F01','#C73E1D'],
                          edgecolor='white', linewidth=0.5)
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Total Sales Quantity (units)', fontsize=12)
ax.set_title('Wheat: Sales Quantity by Channel and Season (2024)', fontsize=13, fontweight='bold')
ax.legend(title='Channel', fontsize=10)
ax.grid(axis='y', alpha=0.3)
# Add total labels
for i, season in enumerate(['Spring','Summer','Autumn','Winter']):
    total = wheat_season_channel.loc[season].sum()
    ax.text(i, total + 20000, f'{total:,.0f}', ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/fig4_wheat_seasonal_channel.png', dpi=150)
plt.close()
print("Figure 4 saved.")

print("\n=== All figures generated ===")