import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Read full dataset
df = db.frame(db.query("SELECT * FROM agricultural_product_price_tren"))
df['Collection Date'] = pd.to_datetime(df['Collection Date'])
df['month'] = df['Collection Date'].dt.to_period('M').astype(str)

# Monthly stats by category, market, price type
monthly = df.groupby(['month', 'Product Category', 'Market Name', 'Price Type']).agg(
    avg_price=('Average Price', 'mean'),
    min_price=('Average Price', 'min'),
    max_price=('Average Price', 'max'),
    std_price=('Average Price', 'std'),
    count=('Average Price', 'count'),
    avg_on_shelf=('On-shelf Quantity (tons)', 'mean'),
    avg_trading_vol=('Trading Volume (tons)', 'mean')
).reset_index()

monthly = monthly.sort_values(['Product Category', 'Market Name', 'Price Type', 'month'])
monthly['prev_avg_price'] = monthly.groupby(['Product Category', 'Market Name', 'Price Type'])['avg_price'].shift(1)
monthly['mom_growth_pct'] = ((monthly['avg_price'] - monthly['prev_avg_price']) / monthly['prev_avg_price']) * 100

# Overall monthly (across all markets)
overall = df.groupby(['month', 'Product Category', 'Price Type']).agg(
    avg_price=('Average Price', 'mean'),
    std_price=('Average Price', 'std'),
    count=('Average Price', 'count'),
    avg_on_shelf=('On-shelf Quantity (tons)', 'mean'),
    avg_trading_vol=('Trading Volume (tons)', 'mean'),
    total_on_shelf=('On-shelf Quantity (tons)', 'sum'),
    total_trading_vol=('Trading Volume (tons)', 'sum')
).reset_index().sort_values(['Product Category', 'Price Type', 'month'])

overall['prev_avg_price'] = overall.groupby(['Product Category', 'Price Type'])['avg_price'].shift(1)
overall['mom_growth_pct'] = ((overall['avg_price'] - overall['prev_avg_price']) / overall['prev_avg_price']) * 100

print("=== Overall (All Markets Combined) MoM Growth ===")
cols = ['month', 'Product Category', 'Price Type', 'avg_price', 'mom_growth_pct', 'count', 'avg_on_shelf', 'avg_trading_vol']
print(overall[cols].to_string(index=False))

# Save
overall.to_csv('/work/overall_mom.csv', index=False)
monthly.to_csv('/work/monthly_mom.csv', index=False)
print("\n\nFiles saved. Shape:", overall.shape)

# Compute price volatility per category (coefficient of variation across all observations)
print("\n\n=== Price Volatility (CV) by Category ===")
for cat in df['Product Category'].unique():
    sub = df[df['Product Category'] == cat]
    cv = sub['Average Price'].std() / sub['Average Price'].mean() * 100
    print(f"{cat}: CV={cv:.2f}%, n={len(sub)}, mean_price={sub['Average Price'].mean():.2f}, std={sub['Average Price'].std():.2f}")

# By category and price type
print("\n=== Price Volatility by Category and Price Type ===")
for (cat, pt), sub in df.groupby(['Product Category', 'Price Type']):
    cv = sub['Average Price'].std() / sub['Average Price'].mean() * 100
    print(f"{cat} | {pt}: CV={cv:.2f}%, n={len(sub)}, mean={sub['Average Price'].mean():.2f}, std={sub['Average Price'].std():.2f}")