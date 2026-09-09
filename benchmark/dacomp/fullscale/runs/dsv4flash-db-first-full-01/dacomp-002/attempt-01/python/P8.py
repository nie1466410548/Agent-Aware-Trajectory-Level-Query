import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Get daily sales data
res = db.query("""
SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"
""")
df_daily = db.frame(res)
df_daily['Sales_Date_Str'] = df_daily['Sales Date'].astype(str)
df_daily['Date'] = pd.to_datetime(df_daily['Sales_Date_Str'], format='%Y%m%d', errors='coerce')

print("Data shape:", df_daily.shape)
print("Date range:", df_daily['Date'].min(), "to", df_daily['Date'].max())
print("Null dates:", df_daily['Date'].isna().sum())

print("\nTop 5 days by sales amount:")
print(df_daily.nlargest(5, 'total')[['Date','total','n']].to_string())
print("\nBottom 5 days:")
print(df_daily.nsmallest(5, 'total')[['Date','total','n']].to_string())

# Visualize daily sales
plt.figure(figsize=(16, 6))
plt.plot(df_daily['Date'], df_daily['total'], marker='.', linewidth=1, color='steelblue')
plt.title('Daily Sales Amount (Jan-Apr 2015)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=13)
plt.ylabel('Sales Amount (RMB)', fontsize=13)
plt.axvline(x=pd.Timestamp('2015-02-19'), color='red', linestyle='--', alpha=0.7, label='Chinese New Year (Feb 19)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/figure6_daily_sales.png', dpi=150)
plt.close()
print("Figure 6 saved")

# Unit price analysis
res2 = db.query("""
SELECT "Major Category Name", "Sales Month", 
       ROUND(SUM("Sales Amount"), 2) AS total_amount,
       SUM("Sales Quantity") AS total_qty,
       ROUND(SUM("Sales Amount") * 1.0 / NULLIF(SUM("Sales Quantity"), 0), 2) AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" > 0
GROUP BY "Major Category Name", "Sales Month"
ORDER BY "Major Category Name", "Sales Month"
""")
df_price = db.frame(res2)
df_price['Month'] = df_price['Sales Month'].astype(str).str[4:6].astype(int)
df_price['Month_Label'] = df_price['Month'].map({1:'Jan',2:'Feb',3:'Mar',4:'Apr'})

top_cats = ['Daily fresh products', 'Vegetables and fruits', 'Leisure', 'Grain and oil', 
            'Alcoholic beverages', 'Household & Personal Care', 'Meat and poultry', 'Instant mixes']
df_price_top = df_price[df_price['Major Category Name'].isin(top_cats)]

print("\n=== Average Unit Price by Major Category ===")
print(df_price_top[['Major Category Name', 'Month_Label', 'avg_unit_price']].to_string(index=False))

price_pivot = df_price_top.pivot_table(index='Major Category Name', columns='Month_Label', values='avg_unit_price', aggfunc='mean')
plt.figure(figsize=(10, 8))
sns.heatmap(price_pivot, annot=True, fmt='.2f', cmap='viridis', linewidths=1)
plt.title('Average Unit Price by Major Category and Month', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/work/figure7_unit_price.png', dpi=150)
plt.close()
print("Figure 7 saved")

# Customer count
res3 = db.query("""
SELECT "Sales Month", COUNT(DISTINCT "Customer ID") AS customer_count, COUNT(*) AS trans_count
FROM sheet1
GROUP BY "Sales Month" ORDER BY "Sales Month"
""")
df_cust = db.frame(res3)
print("\n=== Customer Count per Month ===")
print(df_cust.to_string(index=False))