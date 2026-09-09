import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_json('/work/promo_full.json', orient='records')

# Prepare dataframe for heatmap
bins = [0, 0.2, 0.3, 0.4, 1.0]
labels = ['<20%','20-30%','30-40%','>40%']
df['dd_bin'] = pd.cut(df['discount_depth'], bins=bins, labels=labels, include_lowest=True)

# Units heatmap
pivot_units = df.groupby(['cat_name','dd_bin'], observed=True)['sale_count'].mean().unstack('dd_bin')
# Revenue heatmap
pivot_rev = df.groupby(['cat_name','dd_bin'], observed=True)['revenue'].mean().unstack('dd_bin')
# Count heatmap
pivot_cnt = df.groupby(['cat_name','dd_bin'], observed=True)['sale_count'].count().unstack('dd_bin')

# Filter to categories with at least 30 total promos
cnt = df.groupby('cat_name')['sale_count'].count()
major = cnt[cnt >= 30].index.tolist()
pivot_units = pivot_units.loc[major]
pivot_rev = pivot_rev.loc[major]

fig, axes = plt.subplots(1, 2, figsize=(14, 8))

# Heatmap: avg units
sns.heatmap(pivot_units.round(1), annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[0],
            linewidths=0.5, cbar_kws={'label': 'Avg Units per Promotion'})
axes[0].set_title('Average Units per Promotion\nby Category & Discount Depth')
axes[0].set_ylabel('Level 1 Category')
axes[0].set_xlabel('Discount Depth')

# Heatmap: avg revenue
sns.heatmap(pivot_rev.round(1), annot=True, fmt='.1f', cmap='YlGnBu', ax=axes[1],
            linewidths=0.5, cbar_kws={'label': 'Avg Revenue per Promotion'})
axes[1].set_title('Average Revenue per Promotion\nby Category & Discount Depth')
axes[1].set_ylabel('Level 1 Category')
axes[1].set_xlabel('Discount Depth')

plt.tight_layout()
plt.savefig('/work/heatmap_effectiveness.png', dpi=120)
plt.close()
print("Heatmap saved")

# Create a summary chart of Pearson correlations by category
cat_corr = pd.read_csv('/work/category_results.csv')
cat_corr = cat_corr.dropna(subset=['pearson_r'])
cat_corr = cat_corr.sort_values('pearson_r')
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['steelblue' if r > 0 else 'coral' for r in cat_corr['pearson_r']]
ax.barh(cat_corr['category'], cat_corr['pearson_r'], color=colors, edgecolor='grey')
for i, row in cat_corr.iterrows():
    ax.text(row['pearson_r'] + 0.003 if row['pearson_r'] < 0 else row['pearson_r'] + 0.003, 
            i, f'{row["pearson_r"]:.3f}', va='center', fontsize=8)
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Pearson Correlation (Discount Depth vs Sales)')
ax.set_title('Correlation between Discount Depth and Sales by Category')
plt.tight_layout()
plt.savefig('/work/correlation_by_category.png', dpi=100)
plt.close()
print("Correlation chart saved")