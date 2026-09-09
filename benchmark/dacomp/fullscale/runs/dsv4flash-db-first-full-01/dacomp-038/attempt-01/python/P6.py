import pandas as pd
import numpy as np

s1 = db.frame(db.query("SELECT * FROM sheet1"))
s1['dt'] = pd.to_datetime(s1['Promotion Date'])

caixi_new_cats = ['Beer', 'Cherry', 'Chocolate', 'Daifuku', 'Fish skin', 'Jianbing (Chinese pancake)', 'Mooncake', 'Pig Trotter', 'Plum wine', 'apple', 'red wine']

# Caixi v4.9 rows on Jul4-7 (gray) for these cats
g = s1[(s1['Strategy']=='Caixi Strategy v4.9') & (s1['dt'] >= pd.Timestamp('2025-07-04')) & (s1['Promotion Tertiary Category'].isin(caixi_new_cats))]
print("Caixi v4.9 gray rows:", len(g))
print("Total clicks:", g['Clicks'].sum(), "Total impressions:", g['Impressions'].sum())
print("Weighted CTR:", g['Clicks'].sum()/g['Impressions'].sum())

# Per-cat CTRs
per_cat = g.groupby('Promotion Tertiary Category').apply(lambda x: x['Clicks'].sum()/x['Impressions'].sum())
print("\nPer-cat CTR under v4.9:")
print(per_cat.round(4).to_string())
print("\nMean of per-cat CTRs:", per_cat.mean().round(4))
print("Weighted CTR across cats:", (g['Clicks'].sum()/g['Impressions'].sum()).round(4))

# Pre period: same cats under Caixi v4.8 on Jul1-3
p = s1[(s1['Strategy']=='Caixi Strategy v4.8') & (s1['dt'] <= pd.Timestamp('2025-07-03')) & (s1['Promotion Tertiary Category'].isin(caixi_new_cats))]
print("\nCaixi v4.8 pre rows:", len(p))
print("Weighted CTR pre:", (p['Clicks'].sum()/p['Impressions'].sum()).round(4))
per_cat_p = p.groupby('Promotion Tertiary Category').apply(lambda x: x['Clicks'].sum()/x['Impressions'].sum())
print("Mean per-cat CTR pre:", per_cat_p.mean().round(4))
print("\nPer-cat pre CTR:")
print(per_cat_p.round(4).to_string())
