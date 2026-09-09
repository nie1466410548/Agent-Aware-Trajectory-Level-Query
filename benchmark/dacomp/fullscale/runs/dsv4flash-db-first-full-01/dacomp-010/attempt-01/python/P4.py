import json
import pandas as pd
import numpy as np
from scipy import stats

# Re-query Wheat transaction-level data
result = db.query('''
SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'
ORDER BY c."Sales Channel", qty
''')
rows = db.rows(result)
cols = ['channel','qty']
df = pd.DataFrame(rows, columns=cols)

print("=== Transaction qty values per channel ===")
for ch in df['channel'].unique():
    vals = sorted(df[df['channel']==ch]['qty'].values)
    print(f"{ch:25s}: {vals}")
    print(f"  Mean={np.mean(vals):.0f}, Median={np.median(vals):.0f}, N={len(vals)}")
    print()

# Mann-Whitney test
ec = df[df['channel']=='E-commerce Platform']['qty'].values
co = df[df['channel']=='Cooperative']['qty'].values
u, p = stats.mannwhitneyu(ec, co, alternative='two-sided')
print(f"Mann-Whitney E-comm vs Cooperative: U={u:.1f}, p={p:.6f}")

# Check if all E-comm values are greater than all Cooperative values
print(f"E-comm: min={ec.min()}, max={ec.max()}")
print(f"Cooperative: min={co.min()}, max={co.max()}")
print(f"All E-comm > all Cooperative? {all(e > co.max() for e in ec)}")
print(f"All Coop > all E-comm? {all(c > ec.max() for c in co)}")

# Direct sales and Wholesale
ds = df[df['channel']=='Direct sales']['qty'].values
wm = df[df['channel']=='Wholesale market']['qty'].values
u2, p2 = stats.mannwhitneyu(ec, ds, alternative='two-sided')
u3, p3 = stats.mannwhitneyu(ec, wm, alternative='two-sided')
print(f"\nMann-Whitney E-comm vs Direct sales: U={u2:.1f}, p={p2:.6f}")
print(f"Mann-Whitney E-comm vs Wholesale: U={u3:.1f}, p={p3:.6f}")

# Kruskal-Wallis
groups = [df[df['channel']==c]['qty'].values for c in df['channel'].unique()]
H, p = stats.kruskal(*groups)
print(f"\nKruskal-Wallis qty across all channels: H={H:.3f}, p={p:.4f}")