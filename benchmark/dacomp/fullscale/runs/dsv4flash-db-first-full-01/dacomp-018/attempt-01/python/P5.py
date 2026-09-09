import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Monthly seasonality
sql = """
WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT c.gender, strftime('%m', o."Order Date") AS mm, SUM(o.profit) AS profit, COUNT(*) AS orders
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, mm
"""
mdf = db.frame(db.query(sql))
mdf['mm'] = mdf['mm'].astype(int)
month_names = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}
mdf['month'] = mdf['mm'].map(month_names)

# Total by month
tot = mdf.groupby('mm').agg(profit=('profit','sum'), orders=('orders','sum')).reset_index()
tot['month'] = tot['mm'].map(month_names)
print('Monthly total profit:')
print(tot.sort_values('mm'))

fig, ax = plt.subplots(figsize=(10, 4.5))
sns.barplot(data=tot, x='month', y='profit', order=[month_names[i] for i in range(1,13)], palette='viridis')
ax.set_title('Total Fashion profit by month (all years combined)')
ax.set_ylabel('Total profit ($)')
for i, c in enumerate(ax.containers):
    ax.bar_label(c, fmt='$%.0f', fontsize=8)
plt.tight_layout(); plt.savefig('/work/fig6_monthly_seasonality.png'); plt.close()

# Age distribution by gender
sql2 = """
WITH cust AS (SELECT "Customer ID", gender, age FROM customer_information GROUP BY "Customer ID"),
cust_orders AS (SELECT "Customer ID", SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID")
SELECT c.gender, c.age, co.profit FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
"""
adf = db.frame(db.query(sql2))
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
for g, color, ax in [('Female','#d95f02',axes[0]), ('Male','#1b9e77',axes[1])]:
    sub = adf[adf.gender==g]
    ax.hist(sub.age, bins=20, color=color, alpha=0.7, edgecolor='white')
    ax.set_title(f'{g} customers (n={len(sub)}, mean age={sub.age.mean():.1f})')
    ax.set_xlabel('Age'); ax.set_ylabel('Count')
plt.tight_layout(); plt.savefig('/work/fig7_age_distribution.png'); plt.close()
print('done')