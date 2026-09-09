
import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Pull customer-level aggregated data via logged SQL interface
sql = """
WITH cust AS (
  SELECT "Customer ID", "Customer Segment" AS segment, gender, age
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts,
         SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c.segment, o.orders, o.profit, o.sales, b.likes, b.shares, b.carts, b.browse_time
FROM cust c JOIN cust_orders o ON c."Customer ID"=o."Customer ID"
JOIN cust_browse b ON c."Customer ID"=b."Customer ID"
"""
df = db.frame(db.query(sql))
print(df.shape)
print(df.head())
print(df.groupby('gender').agg(customers=('profit','size'), profit_per_cust=('profit','mean'), orders_per_cust=('orders','mean'),
      carts_per_cust=('carts','mean'), browse_time_per_cust=('browse_time','mean')).round(1))

# Correlations between engagement and profit
for col in ['likes','shares','carts','browse_time','orders']:
    r, p = stats.pearsonr(df[col], df['profit'])
    print(f'Pearson profit vs {col}: r={r:.3f}, p={p:.2e}')

# Mann-Whitney U test: female vs male profit per customer
f = df[df.gender=='Female']['profit']; m = df[df.gender=='Male']['profit']
u, p = stats.mannwhitneyu(f, m)
print(f'MWU female vs male profit: U={u}, p={p:.3e}, female_mean={f.mean():.1f}, male_mean={m.mean():.1f}')

# Engagement rates per order
df['cart_rate'] = df['carts']/df['orders']
df['like_rate'] = df['likes']/df['orders']
df['share_rate'] = df['shares']/df['orders']
for g in ['Female','Male']:
    sub = df[df.gender==g]
    print(g, 'avg cart_rate=%.3f like_rate=%.3f share_rate=%.3f browse_min/order=%.2f' % (
        sub.cart_rate.mean(), sub.like_rate.mean(), sub.share_rate.mean(), (sub.browse_time/sub.orders).mean()))

df.to_csv('/work/customer_profit_data.csv', index=False)
print('saved')
