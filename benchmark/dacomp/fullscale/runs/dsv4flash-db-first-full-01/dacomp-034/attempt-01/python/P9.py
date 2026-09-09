import pandas as pd
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

df = pd.read_json('/results/S31.rows.jsonl', lines=True)
df.columns = ['cat_name','sale_count','discount_depth','promotion_price','pdj_price','cost_price','allowance','limit_count']

# Check cost_price == promotion_price
print("Fraction cost_price == promotion_price:", (df['cost_price'] == df['promotion_price']).mean())
print("Fraction cost_price <= 0:", (df['cost_price'] <= 0).mean())
print("allowance>0 fraction:", (df['allowance'] > 0).mean())

# Revenue and margin metrics
df['revenue'] = df['sale_count'] * df['promotion_price']
# Cost basis: if cost_price>0 use it, else use promotion_price (unknown)
df['gross_margin_per_unit'] = df['promotion_price'] - df['cost_price']
df['gross_profit'] = df['sale_count'] * df['gross_margin_per_unit']

# Binned revenue/margin analysis
bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
labels = ['<10%','10-20%','20-30%','30-40%','40-50%','>50%']
df['dd_bin'] = pd.cut(df['discount_depth'], bins=bins, labels=labels, include_lowest=True)
binned = df.groupby('dd_bin', observed=True).agg(
    n=('sale_count','count'),
    avg_units=('sale_count','mean'),
    avg_revenue=('revenue','mean'),
    avg_price=('promotion_price','mean'),
    avg_dd=('discount_depth','mean'),
    median_units=('sale_count','median')
).round(1)
print("\nBinned revenue analysis:")
print(binned)

# Total revenue by bin
tot = df.groupby('dd_bin', observed=True).agg(
    total_units=('sale_count','sum'),
    total_revenue=('revenue','sum')
).round(0)
print("\nTotals by bin:")
print(tot)

# Statistical test of differences across categories (Kruskal-Wallis on avg sales)
cats = [g['sale_count'].values for _, g in df.groupby('cat_name') if len(g) >= 5]
h, p = stats.kruskal(*cats)
print(f"\nKruskal-Wallis across categories: H={h:.2f}, p={p:.2e}")

# Test differences in discount-sales correlation (regression slope heterogeneity) - use ANOVA on log sales?
df['log_sales'] = np.log1p(df['sale_count'])
import scipy.stats as st
# F-test for interaction between category and discount depth
from scipy.stats import f_oneway
# Compare sales across categories with one-way ANOVA on log sales
f, pval = f_oneway(*[df.loc[df['cat_name']==c,'log_sales'].values for c in df['cat_name'].unique() if (df['cat_name']==c).sum()>=5])
print(f"One-way ANOVA on log sales across categories: F={f:.2f}, p={pval:.2e}")

# Save enriched data
df.to_json('/work/promo_full.json', orient='records')
print("\nSaved promo_full.json")

# Revenue-per-unit (avg) trend by bin chart
fig, ax = plt.subplots(1,2, figsize=(12,4))
ax[0].bar(binned.index.astype(str), binned['avg_revenue'], color='#4a7fb5', alpha=0.85)
ax[0].set_title('Average Promotion Revenue by Discount Depth')
ax[0].set_xlabel('Discount Depth')
ax[0].set_ylabel('Avg Revenue (units × promo price)')
ax[1].bar(binned.index.astype(str), binned['avg_units'], color='#e88820', alpha=0.85)
ax[1].set_title('Average Units by Discount Depth')
ax[1].set_xlabel('Discount Depth')
ax[1].set_ylabel('Avg Units')
plt.tight_layout()
plt.savefig('/work/revenue_by_bin.png', dpi=100)
plt.close()
print("Revenue chart saved")