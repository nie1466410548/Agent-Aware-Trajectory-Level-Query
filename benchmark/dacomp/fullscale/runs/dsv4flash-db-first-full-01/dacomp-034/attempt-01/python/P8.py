import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_json('/work/promo_data.json', orient='records')

# Define categories with > 20 promotions for reliable analysis
major_cats = df['cat_name'].value_counts()[df['cat_name'].value_counts() > 20].index.tolist()
print("Major categories:", major_cats)

# 1. Overall scatter with regression line
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df['discount_depth'], df['sale_count'], alpha=0.3, s=5)
slope, intercept, r_val, p_val, stderr = stats.linregress(df['discount_depth'], df['sale_count'])
x_line = np.linspace(0.1, 1.0, 100)
ax.plot(x_line, slope * x_line + intercept, 'r-', linewidth=2, 
        label=f'OLS: y={slope:.1f}x+{intercept:.1f}, R²={r_val**2:.3f}')
ax.set_xlabel('Discount Depth')
ax.set_ylabel('Sales (units)')
ax.set_title('Overall: Discount Depth vs Sales (Single-Item Direct Price Reduction)')
ax.legend()
ax.set_ylim(0, df['sale_count'].quantile(0.95))
plt.tight_layout()
plt.savefig('/work/overall_scatter.png', dpi=100)
plt.close()
print("1. Overall scatter saved")

# 2. Binned bar chart
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
labels = ['<10%','10-20%','20-30%','30-40%','40-50%','>50%']
df['dd_bin'] = pd.cut(df['discount_depth'], bins=bins, labels=labels, include_lowest=True)
bin_avg = df.groupby('dd_bin', observed=True)['sale_count'].agg(['mean','median','count']).reset_index()
fig, ax = plt.subplots(figsize=(9,5))
colors = ['#4a7fb5','#6ba3d6','#8cc4f0','#f0c040','#e88820','#c04020']
ax.bar(bin_avg['dd_bin'], bin_avg['mean'], color=colors, alpha=0.8, edgecolor='grey')
for i, row in bin_avg.iterrows():
    ax.text(i, row['mean']+1, f'n={int(row["count"])}', ha='center', fontsize=9)
ax.set_xlabel('Discount Depth Interval')
ax.set_ylabel('Average Sales per Promotion')
ax.set_title('Average Sales by Discount Depth Interval')
plt.tight_layout()
plt.savefig('/work/binned_bar.png', dpi=100)
plt.close()
print("2. Binned bar saved")

# 3. Per-category scatter plots (top 8 categories)
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()
top_cats = df.groupby('cat_name')['sale_count'].sum().sort_values(ascending=False).head(8).index
for i, cat in enumerate(top_cats):
    sub = df[df['cat_name'] == cat]
    ax = axes[i]
    ax.scatter(sub['discount_depth'], sub['sale_count'], alpha=0.4, s=8)
    if len(sub) >= 2:
        s, ic, rv, pv, se = stats.linregress(sub['discount_depth'], sub['sale_count'])
        xl = np.linspace(sub['discount_depth'].min(), sub['discount_depth'].max(), 50)
        ax.plot(xl, s*xl+ic, 'r-', linewidth=2)
        ax.text(0.05, 0.95, f'R²={rv**2:.3f}', transform=ax.transAxes, va='top', fontsize=9,
                bbox=dict(facecolor='white', alpha=0.7))
    ax.set_title(f'{cat}\n(n={len(sub)})', fontsize=9)
    ax.set_xlabel('Discount Depth', fontsize=8)
    ax.set_ylabel('Sales', fontsize=8)
    ax.set_ylim(0, sub['sale_count'].quantile(0.95))
plt.tight_layout()
plt.savefig('/work/per_category_scatter.png', dpi=100)
plt.close()
print("3. Per-category scatter saved")

# 4. Category comparison: avg_sales vs avg_dd
cat_sum = df.groupby('cat_name').agg(
    n_promos=('sale_count','count'),
    total_sales=('sale_count','sum'),
    avg_sales=('sale_count','mean'),
    avg_dd=('discount_depth','mean')
).reset_index()
cat_sum = cat_sum[cat_sum['n_promos'] >= 10]
fig, ax = plt.subplots(figsize=(10,6))
sc = ax.scatter(cat_sum['avg_dd'], cat_sum['avg_sales'], s=cat_sum['n_promos']*2, 
                c=cat_sum['total_sales'], cmap='viridis', alpha=0.7, edgecolors='black')
for _, row in cat_sum.iterrows():
    if row['n_promos'] >= 20:
        ax.annotate(row['cat_name'], (row['avg_dd'], row['avg_sales']), fontsize=7, ha='center')
ax.set_xlabel('Average Discount Depth')
ax.set_ylabel('Average Sales per Promotion')
ax.set_title('Category Comparison: Discount Depth vs Sales Effectiveness')
cbar = plt.colorbar(sc, label='Total Sales')
plt.tight_layout()
plt.savefig('/work/category_comparison.png', dpi=100)
plt.close()
print("4. Category comparison saved")

# 5. Meat category detailed analysis
meat = df[df['cat_name'] == 'Meat'].copy()
print("\nMeat category analysis:")
meat['dd_bin'] = pd.cut(meat['discount_depth'], bins=[0,0.15,0.2,0.25,0.3,0.5,1.0], 
                        labels=['<15%','15-20%','20-25%','25-30%','30-50%','>50%'])
print(meat.groupby('dd_bin', observed=True)['sale_count'].agg(['mean','median','count']))
print("Avg discount depth:", meat['discount_depth'].mean())
print("Avg sales:", meat['sale_count'].mean())

# 6. Snack Food (most promos) detailed
snack = df[df['cat_name'] == 'Snack Food'].copy()
print("\nSnack Food binned analysis:")
snack['dd_bin'] = pd.cut(snack['discount_depth'], bins=[0,0.15,0.2,0.25,0.3,0.4,1.0],
                          labels=['<15%','15-20%','20-25%','25-30%','30-40%','>40%'])
print(snack.groupby('dd_bin', observed=True)['sale_count'].agg(['mean','median','count']))

print("\nDone with all analyses.")