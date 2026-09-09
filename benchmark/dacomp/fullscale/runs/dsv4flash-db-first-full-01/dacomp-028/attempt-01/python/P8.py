import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

df = db.frame(db.query("SELECT * FROM agricultural_product_price_tren"))
df['Collection Date'] = pd.to_datetime(df['Collection Date'])
df['month'] = df['Collection Date'].dt.to_period('M').astype(str)

# Build product-level monthly series
key = ['Product Name','Product Category','Market Name','Price Type']
g = df.groupby(key + ['month']).agg(
    avg_price=('Average Price','mean'),
    on_shelf=('On-shelf Quantity (tons)','mean'),
    vol=('Trading Volume (tons)','mean')
).reset_index()

g['month_idx'] = pd.to_datetime(g['month'] + '-01')
g = g.sort_values(key + ['month_idx'])
g['prev_price'] = g.groupby(key)['avg_price'].shift(1)
g['prev_month'] = g.groupby(key)['month'].shift(1)
g['prev_on_shelf'] = g.groupby(key)['on_shelf'].shift(1)
g['prev_vol'] = g.groupby(key)['vol'].shift(1)

# Month gap
g['month_int'] = g['month_idx'].dt.to_period('M').astype(int)
prev_month_int = pd.to_datetime(g['prev_month']+'-01').dt.to_period('M').astype(int).where(g['prev_month'].notna())
g['gap'] = (g['month_int'] - prev_month_int).where(g['prev_month'].notna())

# Consecutive (gap==1)
consec = g[g['gap']==1].copy()
consec['price_chg_pct'] = (consec['avg_price'] - consec['prev_price'])/consec['prev_price']*100
consec['on_shelf_chg_pct'] = (consec['on_shelf'] - consec['prev_on_shelf'])/consec['prev_on_shelf']*100
consec['vol_chg_pct'] = (consec['vol'] - consec['prev_vol'])/consec['prev_vol']*100

print("Consecutive transitions:", len(consec))
print("\nPrice change vs supply change correlations:")
c1 = consec['price_chg_pct'].corr(consec['on_shelf_chg_pct'])
c2 = consec['price_chg_pct'].corr(consec['vol_chg_pct'])
print(f"Corr(price_chg%, on_shelf_chg%): {c1:.3f}")
print(f"Corr(price_chg%, vol_chg%): {c2:.3f}")

consec['abs_price_chg'] = np.abs(consec['price_chg_pct'])
print(f"Corr(|price_chg%|, on_shelf_chg%): {consec['abs_price_chg'].corr(consec['on_shelf_chg_pct']):.3f}")
print(f"Corr(|price_chg%|, vol_chg%): {consec['abs_price_chg'].corr(consec['vol_chg_pct']):.3f}")

# Monthly volatility vs supply
monthly_vol = df.groupby(['month','Product Category','Price Type','Market Name']).agg(
    price_std=('Average Price','std'),
    price_mean=('Average Price','mean'),
    avg_on_shelf=('On-shelf Quantity (tons)','mean'),
    avg_vol=('Trading Volume (tons)','mean'),
    n=('Average Price','count')
).reset_index()
monthly_vol['price_cv'] = monthly_vol['price_std'] / monthly_vol['price_mean'] * 100
multi_month = monthly_vol[monthly_vol['n']>1].dropna(subset=['price_cv'])
print(f"\nMonthly cells with >1 obs: {len(multi_month)}")
if len(multi_month) > 5:
    c3 = multi_month['price_cv'].corr(multi_month['avg_on_shelf'])
    c4 = multi_month['price_cv'].corr(multi_month['avg_vol'])
    print(f"Corr(monthly price-CV, avg_on_shelf): {c3:.3f}")
    print(f"Corr(monthly price-CV, avg_vol): {c4:.3f}")

# ========== VISUALIZATIONS ==========

# Fig 1: Price trends by market (Vegetable)
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
markets = df['Market Name'].unique()
colors = {'Wholesale Price': 'steelblue', 'Retail Price (Type)': 'firebrick'}

for idx, market in enumerate(markets):
    ax = axes[idx//2, idx%2]
    for pt in ['Wholesale Price', 'Retail Price (Type)']:
        sub = monthly_vol[(monthly_vol['Market Name']==market) & 
                          (monthly_vol['Product Category']=='Vegetable') &
                          (monthly_vol['Price Type']==pt)].sort_values('month')
        if len(sub) > 0:
            ax.plot(sub['month'], sub['price_mean'], marker='o', label=pt, color=colors[pt])
    ax.set_title(market[:30]+'...')
    ax.set_ylabel('Avg Price (Yuan/kg)')
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    ax.grid(True, alpha=0.3)

fig.suptitle('Vegetable Average Price Trends by Market (All Products)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig1_price_trends_by_market.png', dpi=100)
plt.close()

# Fig 2: Price vs On-shelf (Monthly, Vegetable)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
veg_monthly = monthly_vol[monthly_vol['Product Category']=='Vegetable']

for pt, ax in zip(['Wholesale Price', 'Retail Price (Type)'], axes):
    sub = veg_monthly[veg_monthly['Price Type']==pt].sort_values('month')
    sc = ax.scatter(sub['price_mean'], sub['avg_on_shelf'], c=range(len(sub)), cmap='viridis', s=50, alpha=0.7)
    ax.set_xlabel('Average Price (Yuan/kg)')
    ax.set_ylabel('Avg On-shelf Qty (tons)')
    ax.set_title(f'{pt}')
    ax.grid(True, alpha=0.3)
    for i, row in sub.iterrows():
        ax.annotate(row['month'][-2:], (row['price_mean'], row['avg_on_shelf']), fontsize=8)
    plt.colorbar(sc, ax=ax, label='Time Order')

fig.suptitle('Vegetable: Price vs On-shelf Quantity (Monthly, All Markets)', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig2_price_vs_supply.png', dpi=100)
plt.close()

# Fig 3: Product-level price volatility vs supply
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
vol = df.groupby(key).agg(
    price_std=('Average Price','std'),
    price_mean=('Average Price','mean'),
    n_obs=('Average Price','count'),
    mean_on_shelf=('On-shelf Quantity (tons)','mean'),
    mean_vol=('Trading Volume (tons)','mean')
).reset_index()
vol['price_cv'] = vol['price_std'] / vol['price_mean'] * 100
multi = vol[vol['n_obs']>1].dropna(subset=['price_cv'])

if len(multi) > 5:
    axes[0].scatter(multi['price_cv'], multi['mean_on_shelf'], alpha=0.6)
    axes[0].set_xlabel('Price CV (%)')
    axes[0].set_ylabel('Mean On-shelf Qty (tons)')
    axes[0].set_title(f'Corr: {multi["price_cv"].corr(multi["mean_on_shelf"]):.3f}')
    axes[0].grid(True, alpha=0.3)
    axes[1].scatter(multi['price_cv'], multi['mean_vol'], alpha=0.6)
    axes[1].set_xlabel('Price CV (%)')
    axes[1].set_ylabel('Mean Trading Vol (tons)')
    axes[1].set_title(f'Corr: {multi["price_cv"].corr(multi["mean_vol"]):.3f}')
    axes[1].grid(True, alpha=0.3)

fig.suptitle('Product-Level Price Volatility vs Supply Metrics', fontsize=14)
plt.tight_layout()
plt.savefig('/work/fig3_volatility_vs_supply.png', dpi=100)
plt.close()

# Fig 4: MoM Growth by Market (Vegetable Wholesale)
fig, ax = plt.subplots(figsize=(12, 6))
for market in markets:
    sub = monthly_vol[(monthly_vol['Market Name']==market) & 
                      (monthly_vol['Product Category']=='Vegetable') &
                      (monthly_vol['Price Type']=='Wholesale Price')].sort_values('month')
    if len(sub) > 1:
        sub = sub.copy()
        sub['mom_pct'] = sub['price_mean'].pct_change() * 100
        ax.plot(sub['month'][1:], sub['mom_pct'][1:], marker='o', label=market[:25], linewidth=2)

ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Month')
ax.set_ylabel('MoM Growth (%)')
ax.set_title('Vegetable Wholesale Price: Month-over-Month Growth Rate by Market')
ax.legend()
ax.tick_params(axis='x', rotation=45)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig4_mom_growth.png', dpi=100)
plt.close()

# Also product-level MoM distribution histogram
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(consec['price_chg_pct'], bins=20, alpha=0.7, edgecolor='black')
ax.axvline(x=0, color='red', linestyle='--', alpha=0.5)
ax.set_xlabel('MoM Price Change (%)')
ax.set_ylabel('Number of Product-Market Transitions')
ax.set_title('Distribution of Product-Level Month-over-Month Price Changes (Vegetable)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig5_mom_distribution.png', dpi=100)
plt.close()

print("\nAll figures saved in /work/")
for f in sorted(Path('/work').glob('fig*.png')):
    print(f"  {f.name}")