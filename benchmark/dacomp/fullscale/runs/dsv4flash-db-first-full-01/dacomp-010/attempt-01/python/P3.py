import json
import pandas as pd
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
print(f"E-comm min: {ec.min()}, max: {ec.max()}")
print(f"Cooperative min: {co.min()}, max: {co.max()}")
print(f"All E-comm > all Cooperative? {all(e > co.max() for e in ec)}")
print(f"All Coop > all E-comm? {all(c > ec.max() for c in co)}")