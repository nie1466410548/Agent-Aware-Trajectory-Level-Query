import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Collect all data for the candidate items
# 1. July sales volume and seasonality
res = db.query("""
    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july_vol,
           ROUND(SUM(s."Sales volume (kg)"),1) AS total_vol,
           ROUND(COUNT(DISTINCT s."Sales Date")*1.0/1096,4) AS freq,
           ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)"*s."Unit price (yuan/kg)" ELSE 0 END),0) AS july_revenue
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
""")
cols = res['executions'][0]['columns']
rows = db.rows(res)
candidates = pd.DataFrame(rows, columns=cols)
candidates['july_vol'] = candidates['july_vol'].astype(float)
candidates['july_pct'] = candidates['july_vol'] / candidates['total_vol'] * 100

# 2. Loss rates
res2 = db.query("""
    SELECT pl."Item Code" AS code, pl."Loss Rate (%)" AS loss_rate
    FROM product_loss pl
    WHERE pl."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
""")
cols2 = res2['executions'][0]['columns']
rows2 = db.rows(res2)
loss = pd.DataFrame(rows2, columns=cols2)

# 3. Profit margin (avg retail - avg wholesale)
res3 = db.query("""
    SELECT s."Item Code" AS code, 
           ROUND(AVG(s."Unit price (yuan/kg)") - AVG(pp."Wholesale price (yuan/kg)"),2) AS margin
    FROM sales_records s
    LEFT JOIN purchase_price pp ON s."Item Code"=pp."Item Code" AND date(s."Sales Date")=date(pp."Date")
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code"
""")
cols3 = res3['executions'][0]['columns']
rows3 = db.rows(res3)
margin = pd.DataFrame(rows3, columns=cols3)

# Merge
df = candidates.merge(loss, on='code', how='left').merge(margin, on='code', how='left')
df['july_pct'] = df['july_pct'].round(1)
df = df.sort_values('july_vol', ascending=False)

print("=== Candidate Items Comprehensive Analysis ===")
print(df.to_string(index=False))

# Now let's get the July seasonality index for each item
res4 = db.query("""
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
cols4 = res4['executions'][0]['columns']
rows4 = db.rows(res4)
seas = pd.DataFrame(rows4, columns=cols4)
seas['avg_daily'] = seas['avg_daily'].astype(float)

overall = seas.groupby(['code','name'])['avg_daily'].mean().reset_index()
overall.columns = ['code','name','overall_avg']
july_s = seas[seas['mo']=='07'].groupby(['code','name'])['avg_daily'].mean().reset_index()
july_s.columns = ['code','name','july_avg']
seas_idx = overall.merge(july_s, on=['code','name'])
seas_idx['seasonality'] = (seas_idx['july_avg'] / seas_idx['overall_avg']).round(3)

df = df.merge(seas_idx[['code','seasonality','july_avg']], on='code')
print("\n=== Final Candidate Table ===")
print(df.to_string(index=False))

# Recommendations - Three combinations
print("\n\n=== RECOMMENDED THREE FRUIT-AND-VEGETABLE COMBINATIONS FOR JULY 2023 REPLENISHMENT ===\n")

# Combination 1: Summer Leafy Greens (all high July seasonality, complementary)
print("Combination 1: Summer Leafy Greens Bundle")
print("Items: Yunnan Leaf Lettuce, Water Spinach, Sweet Potato Vine Tips")
print("Rationale: All three have very high July seasonality (>1.7), strong positive correlations")
print("  (Sweet Potato Vine Tips ~ Water Spinach r=0.65), and are the top-selling summer leafy greens.")
print("  Yunnan Leaf Lettuce (#1 July volume at 2984 kg), Water Spinach (1402 kg), Sweet Potato Vine Tips (1404 kg)")
print("  These summer vegetables naturally peak in July and are often purchased together.")
print()

# Combination 2: Cauliflower-Pepper-Eggplant Mix (different categories, good July performance)
print("Combination 2: Cauliflower-Pepper-Eggplant Variety Mix")
print("Items: Broccoli, Purple Eggplant (2), Spiral chili pepper")
print("Rationale: Broccoli (Cauliflower group) has strong July sales (2909 kg) and seasonality (1.22).")
print("  Purple Eggplant (Eggplant group) has 1337 kg July volume with seasonality 1.09.")
print("  Spiral chili pepper (Pepper Category) has 932 kg July volume with seasonality 1.17.")
print("  These three items come from different categories, providing diversity and reducing replenishment risk.")
print("  They are complementary (low negative correlations), offering balanced meal options.")
print()

# Combination 3: Chinese Greens & Cauliflower (traditional high-demand items)
print("Combination 3: Chinese Greens & Cauliflower Traditional Set")
print("Items: Yunnan Romaine Lettuce, Shanghai Bok Choy, Green-stem Loose Cauliflower")
print("Rationale: Yunnan Romaine Lettuce (1683 kg July, seasonality 1.44) and Shanghai Bok Choy (918 kg, 1.20)")
print("  are highly correlated (r=0.62), indicating they are often sold together.")
print("  Green-stem Loose Cauliflower (1224 kg, seasonality 1.05) complements from the Cauliflower group.")
print("  These are traditional Chinese vegetable staples with reliable July demand.")
print("  Shanghai Bok Choy has good margin (2.84 yuan/kg) and reasonable loss rate.")

# Save a summary figure
plt.figure(figsize=(14, 10))
# Plot July volume vs seasonality index
plt.subplot(2,2,1)
scatter = plt.scatter(df['seasonality'], df['july_vol'], c=df['margin'], 
                      s=df['july_vol']/10, cmap='RdYlGn', alpha=0.7)
for _, row in df.iterrows():
    plt.annotate(row['name'][:15], (row['seasonality'], row['july_vol']), fontsize=8)
plt.colorbar(scatter, label='Margin (yuan/kg)')
plt.xlabel('July Seasonality Index')
plt.ylabel('July Total Volume (kg)')
plt.title('Item July Performance: Volume vs Seasonality')
plt.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/work/july_recommendation_analysis.png', dpi=150)
plt.close()
print("Saved july_recommendation_analysis.png")