import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = db.frame(db.query("SELECT * FROM agricultural_product_price_tren"))
df['Collection Date'] = pd.to_datetime(df['Collection Date'])
df['month'] = df['Collection Date'].dt.to_period('M').astype(str)

# Final summary: MoM growth by category, market, price type
# Only Vegetable has enough data for meaningful MoM (Fruit has 2 months, Grain has 1 month)

monthly = df.groupby(['month','Product Category','Market Name','Price Type']).agg(
    avg_price=('Average Price','mean'),
    n=('Average Price','count')
).reset_index()
monthly = monthly.sort_values(['Product Category','Market Name','Price Type','month'])
monthly['prev_price'] = monthly.groupby(['Product Category','Market Name','Price Type'])['avg_price'].shift(1)
monthly['mom_growth'] = ((monthly['avg_price'] - monthly['prev_price']) / monthly['prev_price'] * 100).round(2)

# Show Vegetable wholesale MoM by market
print("=== Vegetable Wholesale Price: MoM Growth by Market ===")
vw = monthly[(monthly['Product Category']=='Vegetable') & (monthly['Price Type']=='Wholesale Price')]
print(vw[['month','Market Name','avg_price','mom_growth']].to_string(index=False))

print("\n=== Vegetable Retail Price: MoM Growth by Market ===")
vr = monthly[(monthly['Product Category']=='Vegetable') & (monthly['Price Type']=='Retail Price (Type)')]
print(vr[['month','Market Name','avg_price','mom_growth']].to_string(index=False))

# Overall category MoM
overall = df.groupby(['month','Product Category','Price Type']).agg(
    avg_price=('Average Price','mean'),
    n=('Average Price','count')
).reset_index().sort_values(['Product Category','Price Type','month'])
overall['prev_price'] = overall.groupby(['Product Category','Price Type'])['avg_price'].shift(1)
overall['mom_growth'] = ((overall['avg_price'] - overall['prev_price']) / overall['prev_price'] * 100).round(2)

print("\n=== Overall (All Markets) MoM Growth by Category ===")
print(overall[['month','Product Category','Price Type','avg_price','mom_growth']].to_string(index=False))

# Key stats for report
print("\n\n=== KEY STATISTICS ===")
# Product-level consecutive transitions
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
g['month_int'] = g['month_idx'].dt.to_period('M').astype(int)
prev_mi = pd.to_datetime(g['prev_month']+'-01').dt.to_period('M').astype(int).where(g['prev_month'].notna())
g['gap'] = (g['month_int'] - prev_mi).where(g['prev_month'].notna())
consec = g[g['gap']==1].copy()
consec['price_chg'] = (consec['avg_price'] - consec['prev_price'])/consec['prev_price']*100
consec['on_shelf_chg'] = (consec['on_shelf'] - consec['prev_on_shelf'])/consec['prev_on_shelf']*100

print(f"Product-level consecutive MoM transitions: {len(consec)}")
print(f"Mean MoM price change: {consec['price_chg'].mean():.2f}%")
print(f"Median MoM price change: {consec['price_chg'].median():.2f}%")
print(f"Pct of MoM increases: {(consec['price_chg']>0).mean()*100:.1f}%")
print(f"Corr(price_chg%, on_shelf_chg%): {consec['price_chg'].corr(consec['on_shelf_chg']):.3f}")
print(f"Corr(price, on_shelf) all rows: {df['Average Price'].corr(df['On-shelf Quantity (tons)']):.3f}")
print(f"Corr(price, on_shelf) Vegetable only: {df[df['Product Category']=='Vegetable']['Average Price'].corr(df[df['Product Category']=='Vegetable']['On-shelf Quantity (tons)']):.3f}")

# Monthly aggregate correlation
veg_m = df[df['Product Category']=='Vegetable'].groupby(['month','Price Type','Market Name']).agg(
    price_mean=('Average Price','mean'),
    avg_on_shelf=('On-shelf Quantity (tons)','mean')
).reset_index()
print(f"Monthly veg cells: {len(veg_m)}, corr(price, on_shelf): {veg_m['price_mean'].corr(veg_m['avg_on_shelf']):.3f}")