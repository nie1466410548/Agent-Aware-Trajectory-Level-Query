import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_json('/work/promo_full.json', orient='records')

# Revenue per promotion computed
df['revenue'] = df['sale_count'] * df['promotion_price']

# Focus on categories with n>=30
cnt = df.groupby('cat_name')['sale_count'].count()
major = cnt[cnt >= 30].index.tolist()
sub = df[df['cat_name'].isin(major)].copy()

# Per category x bin stats
bins = [0, 0.2, 0.3, 0.4, 1.0]
labels = ['<20%','20-30%','30-40%','>40%']
sub['dd_bin'] = pd.cut(sub['discount_depth'], bins=bins, labels=labels, include_lowest=True)

pivot_units = sub.groupby(['cat_name','dd_bin'], observed=True)['sale_count'].agg(['mean','count']).unstack('dd_bin')
pivot_rev = sub.groupby(['cat_name','dd_bin'], observed=True)['revenue'].mean().unstack('dd_bin')

print("Average units per promotion by category & discount depth:")
print(pivot_units['mean'].round(1).to_string())
print("\nAverage revenue per promotion by category & discount depth:")
print(pivot_rev.round(1).to_string())
print("\nCounts:")
print(pivot_units['count'].round(0).to_string())

# Identify each category's best discount bin for revenue
best_rev = pivot_rev.idxmax(axis=1)
print("\nBest revenue bin per category:")
print(best_rev.to_string())

# Identify each category's best bin for units
best_units = pivot_units['mean'].idxmax(axis=1)
print("\nBest units bin per category:")
print(best_units.to_string())

pivot_units['mean'].round(1).to_csv('/work/pivot_units.csv')
pivot_rev.round(1).to_csv('/work/pivot_rev.csv')
print("\nSaved pivot tables.")