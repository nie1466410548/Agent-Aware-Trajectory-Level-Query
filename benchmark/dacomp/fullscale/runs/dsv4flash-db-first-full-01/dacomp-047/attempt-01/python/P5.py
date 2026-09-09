import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load daily sales for top items
res = db.query("""
    SELECT strftime('%Y-%m-%d', s."Sales Date") AS d, s."Item Code", pi."Item Name", SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY d, s."Item Code", pi."Item Name"
    ORDER BY d, pi."Item Name"
""")
cols = res['executions'][0]['columns']
rows = db.rows(res)
daily_df = pd.DataFrame(rows, columns=cols)
daily_df['vol'] = daily_df['vol'].astype(float)

# Pivot
pivot = daily_df.pivot_table(index='d', columns='Item Name', values='vol', aggfunc='sum').fillna(0)

# Compute correlation matrix
corr = pivot.corr()

plt.figure(figsize=(14, 12))
sns.heatmap(corr, annot=True, cmap='RdBu_r', center=0, vmin=-1, vmax=1, fmt='.2f', 
            xticklabels=True, yticklabels=True)
plt.title('Daily Sales Correlation Between Top July Items', fontsize=14)
plt.tight_layout()
plt.savefig('/work/item_correlation.png', dpi=150)
plt.close()
print("Saved item_correlation.png")

# Print top correlations
print("=== Top Positive Correlations ===")
corr_unstack = corr.unstack().reset_index()
corr_unstack.columns = ['item1', 'item2', 'corr']
corr_unstack = corr_unstack[corr_unstack['item1'] < corr_unstack['item2']]
corr_unstack = corr_unstack.sort_values('corr', ascending=False)
print(corr_unstack.head(20).to_string(index=False))

# Compute monthly seasonality index for each item
res2 = db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") * 1.0 / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", mo
""")
cols2 = res2['executions'][0]['columns']
rows2 = db.rows(res2)
monthly_df = pd.DataFrame(rows2, columns=cols2)
monthly_df['avg_daily'] = monthly_df['avg_daily'].astype(float)

# Overall avg per item
overall = monthly_df.groupby(['code','name'])['avg_daily'].mean().reset_index()
overall.columns = ['code','name','overall_avg']

# July avg
july_m = monthly_df[monthly_df['mo']=='07'].groupby(['code','name'])['avg_daily'].mean().reset_index()
july_m.columns = ['code','name','july_avg']

season = overall.merge(july_m, on=['code','name'])
season['seasonality'] = season['july_avg'] / season['overall_avg']
season = season.sort_values('july_avg', ascending=False)

print("\n=== Seasonality Analysis for Top July Items ===")
print(season.to_string(index=False))

# Monthly pattern for each item
pivot_monthly = monthly_df.pivot_table(index='mo', columns='name', values='avg_daily', aggfunc='mean').fillna(0)
print("\n=== Monthly Avg Daily Sales (kg) for Top Items ===")
print(pivot_monthly.round(1))

# Plot monthly patterns for top 8 items
top8 = ['Yunnan Leaf Lettuce','Broccoli','Yunnan Romaine Lettuce','Wuhu green pepper (1)',
        'Peeled Lotus Root (1)','Sweet Potato Vine Tips','Water Spinach','Purple Eggplant (2)']
plt.figure(figsize=(12, 8))
for item in top8:
    if item in pivot_monthly.columns:
        plt.plot(pivot_monthly.index.astype(int), pivot_monthly[item], marker='o', label=item)
plt.xlabel('Month')
plt.ylabel('Avg Daily Sales (kg)')
plt.title('Monthly Seasonality of Top July Items')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/monthly_seasonality.png', dpi=150)
plt.close()
print("Saved monthly_seasonality.png")