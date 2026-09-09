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

# Check Previous Period Average Price - is it populated and consistent with prior month?
print("Non-null Previous Period Average Price:", df['Previous Period Average Price'].notna().sum(), "/", len(df))
print(df[['Product Name','Product Category','Market Name','Collection Date','Average Price','Previous Period Average Price']].dropna(subset=['Previous Period Average Price']).head(15).to_string())

# Check implied MoM from Previous Period Average Price vs computed
sub = df[df['Previous Period Average Price'].notna()].copy()
sub['implied_mom'] = (sub['Average Price'] - sub['Previous Period Average Price'])/sub['Previous Period Average Price']*100
print("\nImplied MoM from previous-period column:")
print(sub.groupby('Product Category')['implied_mom'].agg(['mean','median','count']).to_string())

# Composition: products observed per month for vegetables
print("\n=== Number of distinct products per month (Vegetable) ===")
veg = df[df['Product Category']=='Vegetable']
print(veg.groupby('month')['Product Name'].nunique().to_string())

# Check Feb 2025 vegetable products (prices ~90)
print("\n=== Feb 2025 Vegetable records ===")
print(veg[veg['month']=='2025-02'][['Product Name','Market Name','Average Price','On-shelf Quantity (tons)','Trading Volume (tons)','Price Type']].sort_values('Average Price').to_string(index=False))

# Check Jun 2024 vegetable wholesale products
print("\n=== Jun 2024 Vegetable wholesale sample ===")
print(veg[(veg['month']=='2024-06') & (veg['Price Type']=='Wholesale Price')][['Product Name','Market Name','Average Price','On-shelf Quantity (tons)','Trading Volume (tons)']].head(15).to_string(index=False))