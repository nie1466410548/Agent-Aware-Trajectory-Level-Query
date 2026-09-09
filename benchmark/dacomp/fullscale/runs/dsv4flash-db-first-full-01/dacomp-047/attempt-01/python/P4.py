import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# --- Category daily sales correlation ---
res = db.query("SELECT strftime('%Y-%m-%d', \"Sales Date\") AS d, pi.\"Category Name\" AS cat, SUM(\"Sales volume (kg)\") AS vol FROM sales_records s JOIN product_information pi ON s.\"Item Code\"=pi.\"Item Code\" GROUP BY d, cat")
cols = res['executions'][0]['columns']
rows = db.rows(res)
cat_df = pd.DataFrame(rows, columns=cols)
cat_pivot = cat_df.pivot_table(index='d', columns='cat', values='vol', aggfunc='sum').fillna(0)
cat_cols = cat_pivot.columns.tolist()

corr = cat_pivot.corr()
print("=== Category Daily Sales Correlation Matrix ===")
print(corr)

plt.figure(figsize=(10, 8))
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, vmin=-1, vmax=1, fmt='.3f')
plt.title('Category Daily Sales Volume Correlation')
plt.tight_layout()
plt.savefig('/work/category_correlation.png', dpi=150)
plt.close()
print("Saved category_correlation.png")

# --- Item-level monthly seasonality ---
res2 = db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
""")
cols2 = res2['executions'][0]['columns']
rows2 = db.rows(res2)
item_df = pd.DataFrame(rows2, columns=cols2)
item_df['vol'] = item_df['vol'].astype(float)

# July volume per item
july_items = item_df[item_df['mo'] == '07'].groupby(['code','name','cat'])['vol'].sum().reset_index()
july_items.columns = ['code','name','cat','july_vol']
july_items = july_items.sort_values('july_vol', ascending=False)

print("\n=== Top 15 Items by July Total Sales Volume ===")
print(july_items.head(15).to_string(index=False))

# Compute avg daily per item per month (using days per month)
res3 = db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") * 1.0 / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
""")
cols3 = res3['executions'][0]['columns']
rows3 = db.rows(res3)
item_daily_df = pd.DataFrame(rows3, columns=cols3)
item_daily_df['avg_daily'] = item_daily_df['avg_daily'].astype(float)

# Overall avg daily per item
overall_avg = item_daily_df.groupby(['code','name','cat'])['avg_daily'].mean().reset_index()
overall_avg.columns = ['code','name','cat','overall_avg_daily']

# July avg daily
july_avg_monthly = item_daily_df[item_daily_df['mo'] == '07'].groupby(['code','name','cat'])['avg_daily'].mean().reset_index()
july_avg_monthly.columns = ['code','name','cat','july_avg_daily']

# Merge
seasonality = overall_avg.merge(july_avg_monthly, on=['code','name','cat'])
seasonality['july_seasonality'] = seasonality['july_avg_daily'] / seasonality['overall_avg_daily']
seasonality = seasonality[seasonality['overall_avg_daily'] > 0].copy()
seasonality = seasonality.sort_values('july_avg_daily', ascending=False)

print("\n=== Top 20 Items by July Avg Daily Sales with Seasonality ===")
print(seasonality.head(20).to_string(index=False))

# Items with July peak
peak_july = seasonality[seasonality['july_seasonality'] > 1.0].sort_values('july_avg_daily', ascending=False)
print(f"\nItems with July seasonality > 1.0: {len(peak_july)}")
print("\n=== Top 15 Items Peaking in July ===")
print(peak_july.head(15).to_string(index=False))

# Monthly pattern of top July items
top_codes = july_items.head(20)['code'].tolist()
top_monthly = item_df[item_df['code'].isin(top_codes)]
top_pivot = top_monthly.pivot_table(index='mo', columns='name', values='vol', aggfunc='sum').fillna(0)
print("\n=== Monthly pattern of top 20 July items (total kg) ===")
print(top_pivot.round(1))

# Save
seasonality.to_csv('/work/seasonality.csv', index=False)
july_items.to_csv('/work/july_items.csv', index=False)