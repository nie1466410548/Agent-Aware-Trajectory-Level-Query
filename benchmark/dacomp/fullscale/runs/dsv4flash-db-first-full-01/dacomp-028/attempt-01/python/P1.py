import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Read full dataset
df = db.frame(db.query("SELECT * FROM agricultural_product_price_tren"))

# Convert date
df['Collection Date'] = pd.to_datetime(df['Collection Date'])
df['month'] = df['Collection Date'].dt.to_period('M').astype(str)

print("Dataset shape:", df.shape)
print("Columns:", df.columns.tolist())
print("Categories:", df['Product Category'].unique())
print("Markets:", df['Market Name'].unique())
print("Date range:", df['Collection Date'].min(), "-", df['Collection Date'].max())
print("\nPrice types:", df['Price Type'].unique())
print("\nSample rows per category:")
print(df.groupby('Product Category').agg({'Product Name': 'nunique', 'Market Name': 'nunique', 'Collection Date': 'nunique'}).reset_index())

# Check if wholesale and retail are mixed - we should analyze separately
# Monthly average price by category, market, and price type
monthly_stats = df.groupby(['month', 'Product Category', 'Market Name', 'Price Type']).agg(
    avg_price=('Average Price', 'mean'),
    min_price=('Average Price', 'min'),
    max_price=('Average Price', 'max'),
    std_price=('Average Price', 'std'),
    count=('Average Price', 'count'),
    avg_on_shelf=('On-shelf Quantity (tons)', 'mean'),
    avg_trading_vol=('Trading Volume (tons)', 'mean')
).reset_index()

print("\n\nMonthly stats shape:", monthly_stats.shape)
print(monthly_stats.head(20))

# Save to use later
monthly_stats.to_csv('/work/monthly_stats.csv', index=False)