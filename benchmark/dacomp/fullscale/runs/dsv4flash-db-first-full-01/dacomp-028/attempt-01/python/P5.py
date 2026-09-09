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

# Check for duplicate rows in same product+market+month (different price types?)
dups = df.groupby(['Product Name','Market Name','month']).size().reset_index(name='n')
print("Product-market-month cells with >1 obs:", (dups['n']>1).sum(), "of", len(dups))
print("Max obs in a cell:", dups['n'].max())

# Build per product+market+price type monthly series
key = ['Product Name','Market Name','Price Type']
g = df.groupby(key + ['month']).agg(avg_price=('Average Price','mean'),
                                    on_shelf=('On-shelf Quantity (tons)','mean'),
                                    vol=('Trading Volume (tons)','mean'),
                                    n=('Average Price','count')).reset_index()
g = g.sort_values(key + ['month'])

# Create month index (consecutive) to detect adjacent months
g['month_idx'] = pd.to_datetime(g['month'] + '-01')
g = g.sort_values(key + ['month_idx'])
g['prev_price'] = g.groupby(key)['avg_price'].shift(1)
g['prev_month'] = g.groupby(key)['month'].shift(1)

# Determine month gap in months
g['gap'] = (g['month_idx'].dt.to_period('M').astype(int) - pd.to_datetime(g['prev_month']+'-01').dt.to_period('M').astype(int)).where(g['prev_month'].notna())
g['mo_change_pct'] = (g['avg_price'] - g['prev_price'])/g['prev_price']*100

# Only consider consecutive months (gap==1)
consec = g[g['gap']==1].copy()
print("\nProduct-market-price type transitions with consecutive months:", len(consec))

# By category
print("\nTransitions by category:")
print(consec.groupby('Product Category').agg(n=('avg_price','count'),
                                             mean_chg=('mo_change_pct','mean'),
                                             median_chg=('mo_change_pct','median'),
                                             pct_up=('mo_change_pct', lambda x: (x>0).mean()*100)).to_string())

# Volatility of price vs supply relationship at product level
# Compute CV per product-market-price type
vol = df.groupby(key).agg(
    price_cv=('Average Price', lambda x: x.std()/x.mean()*100 if len(x)>1 else np.nan),
    price_std=('Average Price','std'),
    n_obs=('Average Price','count'),
    mean_on_shelf=('On-shelf Quantity (tons)','mean'),
    mean_vol=('Trading Volume (tons)','mean'),
    mean_price=('Average Price','mean')
).reset_index()

multi = vol[vol['n_obs']>1].dropna(subset=['price_cv'])
print("\n\nProduct-market series with >1 obs:", len(multi))
print(multi[['Product Name','Market Name','Price Type','n_obs','price_cv','mean_on_shelf','mean_vol','mean_price']].sort_values('n_obs', ascending=False).head(25).to_string(index=False))

# Correlation between price volatility (CV) and supply for multi-obs products
if len(multi) > 5:
    c1 = multi['price_cv'].corr(multi['mean_on_shelf'])
    c2 = multi['price_cv'].corr(multi['mean_vol'])
    print(f"\nCorrelation of product price-CV vs mean on-shelf qty: {c1:.3f}")
    print(f"Correlation of product price-CV vs mean trading volume: {c2:.3f}")
    # Also correlate price CV with on-shelf std
    vol['on_shelf_cv'] = df.groupby(key)['On-shelf Quantity (tons)'].apply(lambda x: x.std()/x.mean()*100 if len(x)>1 else np.nan).reset_index(drop=True)
    multi2 = vol[vol['n_obs']>1].dropna(subset=['price_cv','on_shelf_cv'])
    if len(multi2)>5:
        print(f"Correlation of price-CV vs on-shelf-CV: {multi2['price_cv'].corr(multi2['on_shelf_cv']):.3f}")

multi.to_csv('/work/product_volatility.csv', index=False)
consec.to_csv('/work/consecutive_transitions.csv', index=False)
print("\nSaved files.")