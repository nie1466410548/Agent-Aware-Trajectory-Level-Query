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

# Sample vegetable products in Dec and Jan to check composition
veg = df[df['Product Category']=='Vegetable']
for m in ['2024-10','2024-12','2025-01']:
    sub = veg[veg['month']==m]
    print(f"\n=== {m} Vegetable sample (wholesale) ===")
    w = sub[sub['Price Type']=='Wholesale Price'].sort_values('Average Price')
    print(w[['Product Name','Market Name','Average Price','On-shelf Quantity (tons)']].head(10).to_string(index=False))
    print("...")
    print(w[['Product Name','Market Name','Average Price','On-shelf Quantity (tons)']].tail(5).to_string(index=False))

# Monthly price vs supply correlations (Vegetable, all market-price-type cells)
monthly = df.groupby(['month','Product Category','Price Type','Market Name']).agg(
    price_mean=('Average Price','mean'),
    avg_on_shelf=('On-shelf Quantity (tons)','mean'),
    avg_vol=('Trading Volume (tons)','mean'),
    n=('Average Price','count')
).reset_index()
veg_m = monthly[monthly['Product Category']=='Vegetable']
print(f"\n\nCorrelations across all veg monthly cells (n={len(veg_m)}):")
print(f"  price_mean vs avg_on_shelf: {veg_m['price_mean'].corr(veg_m['avg_on_shelf']):.3f}")
print(f"  price_mean vs avg_vol: {veg_m['price_mean'].corr(veg_m['avg_vol']):.3f}")

# Same but per market (wholesale only)
print("\nPer-market correlation (Vegetable Wholesale):")
for m in df['Market Name'].unique():
    sub = veg_m[(veg_m['Market Name']==m) & (veg_m['Price Type']=='Wholesale Price')]
    if len(sub) > 2:
        print(f"  {m[:25]:<27} n={len(sub):<3} corr(price, on_shelf)={sub['price_mean'].corr(sub['avg_on_shelf']):.3f}")

# Overall correlation across ALL rows: price vs on-shelf
print(f"\nRow-level corr (all rows): price vs on_shelf = {df['Average Price'].corr(df['On-shelf Quantity (tons)']):.3f}")
print(f"Row-level corr (all rows): price vs trading vol = {df['Average Price'].corr(df['Trading Volume (tons)']):.3f}")
print(f"Row-level corr (Vegetable only): {veg['Average Price'].corr(veg['On-shelf Quantity (tons)']):.3f}")

# Also examine trading volume / on-shelf ratio (sell-through)
df['sell_rate'] = df['Trading Volume (tons)'] / df['On-shelf Quantity (tons)']
print(f"\nSell-through rate (trading vol / on-shelf): mean={df['sell_rate'].mean():.3f}, median={df['sell_rate'].median():.3f}")
print(f"Corr(price, sell_rate) all rows: {df['Average Price'].corr(df['sell_rate']):.3f}")