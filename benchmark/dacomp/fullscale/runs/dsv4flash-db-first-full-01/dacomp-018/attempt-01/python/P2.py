
import pandas as pd, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/customer_profit_data.csv')
sns.set_style('whitegrid')
plt.rcParams['figure.dpi'] = 110

# Fig 1: Total profit and profit per customer by gender x segment
g = df.groupby(['gender','segment']).agg(customers=('profit','size'), profit=('profit','sum'), profit_per=('profit','mean')).reset_index()
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
order = g.sort_values('profit', ascending=False)['segment'].unique()
sns.barplot(data=g, x='segment', y='profit', hue='gender', ax=axes[0], palette=['#d95f02','#1b9e77'])
axes[0].set_title('Total Fashion profit by gender & segment'); axes[0].set_ylabel('Total profit ($)')
sns.barplot(data=g, x='segment', y='profit_per', hue='gender', ax=axes[1], palette=['#d95f02','#1b9e77'])
axes[1].set_title('Profit per customer by gender & segment'); axes[1].set_ylabel('Profit per customer ($)')
for a in axes: a.legend(title='Gender')
plt.tight_layout(); plt.savefig('/work/fig1_gender_segment_profit.png'); plt.close()

# Fig 2: Engagement rates per order by gender
rates = df.groupby('gender').apply(lambda s: pd.Series({
    'Add-to-Cart rate': (s['carts']/s['orders']).mean(),
    'Like rate': (s['likes']/s['orders']).mean(),
    'Share rate': (s['shares']/s['orders']).mean(),
    'Browse min/order': (s['browse_time']/s['orders']).mean()})).reset_index()
rates_m = rates.melt(id_vars='gender', var_name='Metric', value_name='Value')
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=rates_m, x='Metric', y='Value', hue='gender', ax=ax, palette=['#d95f02','#1b9e77'])
ax.set_title('Average engagement per Fashion order by gender')
for i, c in enumerate(ax.containers):
    ax.bar_label(c, fmt='%.2f', fontsize=8)
plt.tight_layout(); plt.savefig('/work/fig2_engagement_by_gender.png'); plt.close()

# Fig 3: Profit concentration by customer quintile
df['quintile'] = pd.qcut(df['profit'].rank(method='first'), 5, labels=[5,4,3,2,1])
conc = df.groupby('quintile', as_index=False).agg(customers=('profit','size'), profit=('profit','sum'))
conc['pct_profit'] = conc['profit']/df['profit'].sum()*100
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=conc, x='quintile', y='pct_profit', palette='Blues_d')
ax.set_title('Share of total Fashion profit by customer profit quintile (Q1 = top 20%)')
ax.set_xlabel('Profit quintile (Q1 highest)'); ax.set_ylabel('% of total profit')
for i, c in enumerate(ax.containers):
    ax.bar_label(c, fmt='%.1f%%', fontsize=9)
plt.tight_layout(); plt.savefig('/work/fig3_profit_concentration.png'); plt.close()

# Fig 4: Monthly profit trend female vs male
sql = """
WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT c.gender, strftime('%Y-%m', o."Order Date") AS ym, SUM(o.profit) AS profit, COUNT(*) AS orders
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, ym
"""
mdf = db.frame(db.query(sql))
mdf['ym'] = pd.to_datetime(mdf['ym'])
mdf = mdf.sort_values('ym')
fig, ax = plt.subplots(figsize=(12, 4.5))
for g, color in [('Female','#d95f02'), ('Male','#1b9e77')]:
    sub = mdf[mdf.gender==g]
    ax.plot(sub.ym, sub.profit, marker='o', ms=3, label=g, color=color)
ax.set_title('Monthly Fashion profit by gender (2022-2025)'); ax.set_ylabel('Monthly profit ($)')
ax.legend(); plt.tight_layout(); plt.savefig('/work/fig4_monthly_profit.png'); plt.close()

print('figures done')
