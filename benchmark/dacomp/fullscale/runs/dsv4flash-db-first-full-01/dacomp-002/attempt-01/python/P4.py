import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Pull promotional summary by major category via logged interface
res = db.query("""
SELECT "Major Category Name", "Is Promotional", ROUND(SUM("Sales Amount"),2) AS total_amount, COUNT(*) AS n
FROM sheet1
GROUP BY "Major Category Name", "Is Promotional"
""")
df_promo = db.frame(res)
print(df_promo.head())
print("shape:", df_promo.shape)

# Pivot for heatmap
promo_pivot = df_promo.pivot_table(index='Major Category Name', columns='Is Promotional', values='total_amount', aggfunc='sum').fillna(0)
promo_pct = promo_pivot.div(promo_pivot.sum(axis=1), axis=0) * 100

top_cats = promo_pct.sum(axis=1).sort_values(ascending=False).head(10).index.tolist()
promo_pct_top = promo_pct.loc[top_cats]

plt.figure(figsize=(13, 8))
sns.heatmap(promo_pct_top, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=1)
plt.title('Promotional Share of Sales Amount by Major Category (%)', fontsize=16, fontweight='bold')
plt.ylabel('Major Category', fontsize=13)
plt.xlabel('Promotion Type', fontsize=13)
plt.tight_layout()
plt.savefig('/work/figure5_promotional_mix.png', dpi=150)
plt.close()
print("Figure 5 saved")
print(promo_pct_top.to_string())