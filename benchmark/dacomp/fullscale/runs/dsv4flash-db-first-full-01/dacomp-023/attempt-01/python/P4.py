import os
os.makedirs('work', exist_ok=True)
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# Category share over time
r = db.query("""SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
FROM "order" GROUP BY Category, yr ORDER BY Category, yr""")
share_df = db.frame(r)
pivot = share_df.pivot(index='yr', columns='Category', values='sales')
pivot = pivot[['Office Supplies','Technology','Furniture']]
shares = pivot.div(pivot.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(9, 5))
colors = ['#66b3ff', '#99ff99', '#ff9999']
shares.plot(kind='bar', stacked=True, ax=ax, color=colors, alpha=0.85)
for i, yr in enumerate(shares.index):
    cum = 0
    for cat in shares.columns:
        val = shares.loc[yr, cat]
        ax.text(i, cum + val/2, f'{val:.1f}%', ha='center', va='center', fontsize=8)
        cum += val
ax.set_ylabel('Share of Total Sales (%)')
ax.set_xlabel('Year')
ax.set_title('Category Sales Share by Year')
ax.set_xticklabels([str(y) for y in shares.index], rotation=0)
ax.legend(title='Category')
ax.grid(alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('work/category_share.png', dpi=150)
plt.close()
print("Share figure saved")

# ---- ANOVA: does average order sales differ across regions? ----
r = db.query("""SELECT o.Region, sp."Regional Manager", o."Order ID", SUM(o.Sales) AS order_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, o."Order ID" ORDER BY o.Region, o."Order ID\"""")
odf = db.frame(r)
print("Order-level data shape:", odf.shape)

groups = [g['order_sales'].values for _, g in odf.groupby('Region')]
F, p = stats.f_oneway(*groups)
print(f"ANOVA avg order sales across regions: F={F:.3f}, p={p:.4g}")

# Also Kruskal-Wallis (nonparametric)
H, p_kw = stats.kruskal(*groups)
print(f"Kruskal-Wallis: H={H:.3f}, p={p_kw:.4g}")

# Descriptive by region
desc = odf.groupby('Region').agg(mean_order_sales=('order_sales','mean'), std=('order_sales','std'), n=('order_sales','count'))
print(desc.round(2))

# Correlation: return rate vs profit margin across regions (descriptive)
r = db.query("""SELECT o.Region,
       ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS margin,
       COUNT(DISTINCT o."Order ID") AS total_orders
FROM "order" o GROUP BY o.Region""")
marg_df = db.frame(r)
print(marg_df)

print("ANOVA and descriptives done")