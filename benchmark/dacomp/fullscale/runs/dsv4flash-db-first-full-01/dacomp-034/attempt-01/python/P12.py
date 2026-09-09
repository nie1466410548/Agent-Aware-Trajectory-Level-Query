import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

cat_corr = pd.read_csv('/work/category_results.csv')
cat_corr['pearson_r'] = pd.to_numeric(cat_corr['pearson_r'], errors='coerce')
cat_corr = cat_corr.dropna(subset=['pearson_r']).sort_values('pearson_r')

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['steelblue' if r > 0 else 'coral' for r in cat_corr['pearson_r']]
ax.barh(cat_corr['category'], cat_corr['pearson_r'], color=colors, edgecolor='grey')
for i, row in cat_corr.iterrows():
    ax.text(row['pearson_r'] + 0.005 if row['pearson_r'] >= 0 else row['pearson_r'] - 0.005, 
            i, f'{row["pearson_r"]:.3f}', va='center', fontsize=8, 
            ha='left' if row['pearson_r'] >= 0 else 'right')
ax.axvline(0, color='black', linewidth=0.8)
ax.set_xlabel('Pearson Correlation (Discount Depth vs Sales)')
ax.set_title('Correlation between Discount Depth and Sales by Level 1 Category')
plt.tight_layout()
plt.savefig('/work/correlation_by_category.png', dpi=100)
plt.close()
print("Correlation chart saved")

# Also create discount depth distribution by category (to see if avg discount differs)
import seaborn as sns
df = pd.read_json('/work/promo_full.json', orient='records')
cnt = df.groupby('cat_name')['sale_count'].count()
major = cnt[cnt >= 30].index.tolist()
sub = df[df['cat_name'].isin(major)]
fig, ax = plt.subplots(figsize=(12, 5))
sns.boxplot(data=sub, x='discount_depth', y='cat_name', order=sorted(major, key=lambda c: sub[sub['cat_name']==c]['discount_depth'].mean()), 
            palette='coolwarm', showfliers=False)
ax.set_title('Discount Depth Distribution by Level 1 Category')
ax.set_xlabel('Discount Depth')
ax.set_ylabel('')
plt.tight_layout()
plt.savefig('/work/discount_depth_distribution.png', dpi=100)
plt.close()
print("Distribution chart saved")