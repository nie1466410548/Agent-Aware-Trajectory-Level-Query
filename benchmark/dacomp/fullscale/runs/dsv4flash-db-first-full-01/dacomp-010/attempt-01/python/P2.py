import json
from scipy import stats
import pandas as pd
import numpy as np

# Query transaction-level data for Wheat 2024 via logged db interface
result = db.query('''
SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty,
       c."Unit Price (yuan)" AS price,
       c."Total Transaction Amount" AS amount,
       c."Buyer Type" AS buyer,
       c."Promotion" AS promo,
       f."Customer Satisfaction" AS sat,
       f."Repurchase intention" AS repur
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'
''')
rows = db.rows(result)
cols = ['channel','qty','price','amount','buyer','promo','sat','repur']
df = pd.DataFrame(rows, columns=cols)
print("Wheat 2024 completed transactions:", len(df))
print(df.groupby('channel').agg(n=('qty','size'), total_qty=('qty','sum'),
      avg_qty_per_trans=('qty','mean'), med_qty=('qty','median'),
      avg_price=('price','mean'), avg_amount=('amount','mean')).round(2).to_string())

# Statistical tests across channels
channels = df['channel'].unique()
print("\nChannels:", list(channels))

# Kruskal-Wallis on unit price across channels
groups = [df[df['channel']==c]['price'].values for c in channels]
H, p = stats.kruskal(*groups)
print(f"\nKruskal-Wallis unit price across channels: H={H:.3f}, p={p:.4f}")

# Kruskal-Wallis on transaction quantity across channels
groups_q = [df[df['channel']==c]['qty'].values for c in channels]
Hq, pq = stats.kruskal(*groups_q)
print(f"Kruskal-Wallis transaction qty across channels: H={Hq:.3f}, p={pq:.4f}")

# Mann-Whitney pairwise for price: E-commerce vs Wholesale market
ec = df[df['channel']=='E-commerce Platform']['price'].values
wm = df[df['channel']=='Wholesale market']['price'].values
u, pu = stats.mannwhitneyu(ec, wm, alternative='two-sided')
print(f"Mann-Whitney E-comm vs Wholesale price: U={u:.1f}, p={pu:.4f}")

# Compare e-comm vs cooperative quantity per transaction
co = df[df['channel']=='Cooperative']['qty'].values
u2, pu2 = stats.mannwhitneyu(ec, co, alternative='two-sided')
print(f"Mann-Whitney E-comm vs Cooperative qty: U={u2:.1f}, p={pu2:.4f}")

# Promotion analysis for E-commerce wheat
print("\n=== E-commerce promo breakdown ===")
print(df[df['channel']=='E-commerce Platform'].groupby('promo').agg(n=('qty','size'), total_qty=('qty','sum')).to_string())

# Overall seasonal pattern check - correlation season vs quantity per product
result2 = db.query('''
SELECT f."Season label" AS season, b."Agricultural Product Name" AS product,
       SUM(c."Sales Quantity (units)") AS total_qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", b."Agricultural Product Name"
''')
rows2 = db.rows(result2)
df2 = pd.DataFrame(rows2, columns=['season','product','total_qty'])
piv = df2.pivot(index='product', columns='season', values='total_qty').reindex(['Wheat','Maize','Vegetables','Rice','Fruit'])[['Spring','Summer','Autumn','Winter']]
pct = piv.div(piv.sum(axis=1), axis=0).round(3)*100
print("\n=== % of annual quantity per season by product ===")
print(pct.to_string())

print("\n=== Wheat share of season total ===")
season_totals = df2.groupby('season')['total_qty'].sum()
wheat = df2[df2['product']=='Wheat'].set_index('season')['total_qty']
print((wheat/season_totals*100).round(1).to_string())
