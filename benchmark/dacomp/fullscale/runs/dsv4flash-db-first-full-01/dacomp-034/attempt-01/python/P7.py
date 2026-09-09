import pandas as pd
import numpy as np

df = pd.read_json('/work/promo_data.json', orient='records')

# limit_count stats
print("limit_count describe:")
print(df['limit_count'].describe())
print("\nFraction sale_count >= limit_count (sold-out / capped):")
print((df['sale_count'] >= df['limit_count']).mean())
print("N capped:", (df['sale_count'] >= df['limit_count']).sum())

# Fill rate = sale_count/limit_count
df['fill_rate'] = df['sale_count'] / df['limit_count']
print("\nfill_rate describe:")
print(df['fill_rate'].describe())

# Relationship between discount depth and fill rate
r = df['discount_depth'].corr(df['fill_rate'])
print(f"\ncorr(discount_depth, fill_rate) = {r:.4f}")

# Per-category: capped fraction
caps = df.groupby('cat_name').apply(lambda g: (g['sale_count'] >= g['limit_count']).mean()).sort_values(ascending=False)
print("\nCapped fraction by category:")
print(caps.round(3))