import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_json('/results/S28.rows.jsonl', lines=True)
df.columns = ['cat_name','sale_count','discount_depth','promotion_price','pdj_price','limit_count']
print(df.shape)
print(df.head())

# Basic stats
print("\nOverall stats:")
print(df[['sale_count','discount_depth']].describe())

# Overall correlations
r_p, p_p = stats.pearsonr(df.discount_depth, df.sale_count)
r_s, p_s = stats.spearmanr(df.discount_depth, df.sale_count)
print(f"\nOverall Pearson: r={r_p:.4f}, p={p_p:.2e}")
print(f"Overall Spearman: r={r_s:.4f}, p={p_s:.2e}")

# Bin discount depth
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
labels = ['<10%','10-20%','20-30%','30-40%','40-50%','>50%']
df['dd_bin'] = pd.cut(df.discount_depth, bins=bins, labels=labels, include_lowest=True)
bin_sum = df.groupby('dd_bin', observed=True).agg(
    n_promos=('sale_count','count'),
    total_sales=('sale_count','sum'),
    avg_sales=('sale_count','mean'),
    median_sales=('sale_count','median'),
    avg_dd=('discount_depth','mean')
).round(2)
print("\nDiscount depth bins (overall):")
print(bin_sum)

# Save for later use
df.to_json('/work/promo_data.json', orient='records')
print("\nsaved")