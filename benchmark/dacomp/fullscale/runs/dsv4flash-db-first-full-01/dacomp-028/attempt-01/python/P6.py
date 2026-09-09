import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

df = db.frame(db.query("SELECT * FROM agricultural_product_price_tren"))
df['Collection Date'] = pd.to_datetime(df['Collection Date'])
df['month'] = df['Collection Date'].dt.to_period('M').astype(str)

# Build per product+market+price type+category monthly series
key = ['Product Name','Product Category','Market Name','Price Type']
g = df.groupby(key + ['month']).agg(avg_price=('Average Price','mean'),
                                    on_shelf=('On-shelf Quantity (tons)','mean'),
                                    vol=('Trading Volume (tons)','mean'),
                                    n=('Average Price','count')).reset_index()

g['month_idx'] = pd.to_datetime(g['month'] + '-01')
g = g.sort_values(key + ['month_idx'])
g['prev_price'] = g.groupby(key)['avg_price'].shift(1)
g['prev_month'] = g.groupby(key)['month'].shift(1)

# Determine month gap
g['gap'] = (g['month_idx'].dt.to_period('M').astype(int) - 
            pd.to_datetime(g['prev_month']+'-01').dt.to_period('M').astype(int)).where(g['prev_month'].notna())
g['mo_change_pct'] = (g['avg_price'] - g['prev_price'])/g['prev_price']*100

# Consecutive months
consec = g[g['gap']==1].copy()
print("=== Product-level consecutive-month price transitions ===")
print("Total transitions:", len(consec))

print("\nBy category:")
print(consec.groupby('Product Category').agg(
    n=('avg_price','count'),
    mean_chg=('mo_change_pct','mean'),
    median_chg=('mo_change_pct','median'),
    pct_up=('mo_change_pct', lambda x: (x>0).mean()*100)
).to_string())

print("\nSample transitions:")
print(consec[['Product Name','Product Category','Market Name','Price Type','month','prev_month','avg_price','prev_price','mo_change_pct']].head(15).to_string(index=False))

# Now compute price volatility at product level
# For each product+market+price type, compute CV
vol = df.groupby(key).agg(
    price_std=('Average Price','std'),
    price_mean=('Average Price','mean'),
    n_obs=('Average Price','count'),
    mean_on_shelf=('On-shelf Quantity (tons)','mean'),
    mean_vol=('Trading Volume (tons)','mean'),
    std_on_shelf=('On-shelf Quantity (tons)','std'),
    std_vol=('Trading Volume (tons)','std')
).reset_index()
vol['price_cv'] = vol['price_std'] / vol['price_mean'] * 100

multi = vol[vol['n_obs']>1].dropna(subset=['price_cv'])
print(f"\n\n=== Product-level price volatility (n_obs>1) ===")
print(f"Number of products with multiple observations: {len(multi)}")

if len(multi) > 3:
    print("\nTop 25 by CV:")
    print(multi.sort_values('price_cv', ascending=False)[['Product Name','Product Category','Market Name','Price Type','n_obs','price_cv','mean_on_shelf','mean_vol']].head(25).to_string(index=False))
    
    # Correlation between price CV and mean supply
    c1 = multi['price_cv'].corr(multi['mean_on_shelf'])
    c2 = multi['price_cv'].corr(multi['mean_vol'])
    print(f"\nCorrelation: price-CV vs mean on-shelf qty: {c1:.3f}")
    print(f"Correlation: price-CV vs mean trading vol: {c2:.3f}")
    
    # Also check on-shelf CV
    multi['on_shelf_cv'] = multi['std_on_shelf'] / multi['mean_on_shelf'] * 100
    multi['vol_cv'] = multi['std_vol'] / multi['mean_vol'] * 100
    c3 = multi['price_cv'].corr(multi['on_shelf_cv'])
    c4 = multi['price_cv'].corr(multi['vol_cv'])
    print(f"Correlation: price-CV vs on-shelf-CV: {c3:.3f}")
    print(f"Correlation: price-CV vs trading-vol-CV: {c4:.3f}")

# Save
consec.to_csv('/work/consecutive_transitions.csv', index=False)
multi.to_csv('/work/product_volatility.csv', index=False)
print("\nFiles saved.")