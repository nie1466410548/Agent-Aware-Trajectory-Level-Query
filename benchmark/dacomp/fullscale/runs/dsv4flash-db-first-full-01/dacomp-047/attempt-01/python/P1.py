import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load category daily sales
cats = db.rows(db.query("SELECT strftime('%Y-%m-%d', \"Sales Date\") AS d, pi.\"Category Name\" AS cat, SUM(\"Sales volume (kg)\") AS vol FROM sales_records s JOIN product_information pi ON s.\"Item Code\"=pi.\"Item Code\" GROUP BY d, cat"))
cat_df = pd.DataFrame(cats)
cat_pivot = cat_df.pivot_table(index='d', columns='cat', values='vol', aggfunc='sum').fillna(0)
cat_cols = cat_pivot.columns.tolist()

# Correlation matrix
corr = cat_pivot.corr()
print("=== Category Daily Sales Correlation Matrix ===")
print(corr)

# Plot heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, vmin=-1, vmax=1, fmt='.3f')
plt.title('Category Daily Sales Volume Correlation')
plt.tight_layout()
plt.savefig('/work/category_correlation.png', dpi=150)
plt.close()
print("Saved category_correlation.png")

# Now load item-level monthly data for seasonality
items = db.rows(db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
"""))
item_df = pd.DataFrame(items)
item_df['vol'] = item_df['vol'].astype(float)

# Total volume per item
item_total = item_df.groupby(['code','name','cat'])['vol'].sum().reset_index()
item_total.columns = ['code','name','cat','total_vol']
item_total = item_total.sort_values('total_vol', ascending=False)

# July volume per item
july_items = item_df[item_df['mo'] == '07'].groupby(['code','name','cat'])['vol'].sum().reset_index()
july_items.columns = ['code','name','cat','july_vol']
july_items = july_items.sort_values('july_vol', ascending=False)

print("\n=== Top 15 Items by July Sales Volume ===")
print(july_items.head(15).to_string(index=False))

# Compute July seasonality index (ratio of July avg daily to overall avg daily)
# First get daily avg per item per month
item_daily = db.rows(db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
"""))
item_daily_df = pd.DataFrame(item_daily)
item_daily_df['avg_daily'] = item_daily_df['avg_daily'].astype(float)

# Compute overall avg daily per item
overall_avg = item_daily_df.groupby(['code','name','cat'])['avg_daily'].mean().reset_index()
overall_avg.columns = ['code','name','cat','overall_avg_daily']

# July avg daily
july_avg = item_daily_df[item_daily_df['mo'] == '07'].groupby(['code','name','cat'])['avg_daily'].mean().reset_index()
july_avg.columns = ['code','name','cat','july_avg_daily']

# Merge
seasonality = overall_avg.merge(july_avg, on=['code','name','cat'])
seasonality['july_seasonality'] = seasonality['july_avg_daily'] / seasonality['overall_avg_daily']

# Filter for items with at least some non-zero data
seasonality = seasonality[seasonality['overall_avg_daily'] > 0].copy()
seasonality = seasonality.sort_values('july_avg_daily', ascending=False)

print("\n=== Top 20 Items by July Avg Daily Sales with Seasonality Index ===")
print(seasonality.head(20).to_string(index=False))

# Now let's get items that have a seasonal peak in July
# Items with july_seasonality > 1.0 (above average in July)
peak_july = seasonality[seasonality['july_seasonality'] > 1.0].sort_values('july_avg_daily', ascending=False)
print(f"\nNumber of items with July seasonality > 1.0: {len(peak_july)}")
print("\n=== Top 15 Items Peaking in July (by July avg daily) ===")
print(peak_july.head(15).to_string(index=False))

# Save key data for later use
seasonality.to_csv('/work/seasonality.csv', index=False)

# Monthly pattern for top items
top_items_codes = july_items.head(15)['code'].tolist()
top_items_monthly = item_df[item_df['code'].isin(top_items_codes)].copy()
top_items_monthly = top_items_monthly.pivot_table(index='mo', columns='name', values='vol', aggfunc='sum').fillna(0)
print("\n=== Monthly pattern of top 15 July items ===")
print(top_items_monthly.round(1))