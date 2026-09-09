import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Product preference by gender
sql = """
WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT o."Product", c.gender, COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY o."Product", c.gender
"""
pdf = db.frame(db.query(sql))
pvt = pdf.pivot(index='Product', columns='gender', values='orders').fillna(0)
pvt['ratio_f_m'] = pvt['Female'] / pvt['Male']
pvt['total_orders'] = pvt['Female'] + pvt['Male']
pvt = pvt.sort_values('ratio_f_m', ascending=False)
print('Product order ratio (Female/Male):')
print(pvt[['Female','Male','ratio_f_m','total_orders']].round(2))

# Profit share by product
prof_pvt = pdf.pivot(index='Product', columns='gender', values='profit').fillna(0)
prof_pvt['total_profit'] = prof_pvt['Female'] + prof_pvt['Male']
prof_pvt['f_pct'] = prof_pvt['Female'] / prof_pvt['total_profit'] * 100
prof_pvt = prof_pvt.sort_values('total_profit', ascending=False)
print('\nProfit share by product:')
print(prof_pvt[['Female','Male','total_profit','f_pct']].round(1))

# Visualization of product preference
fig, ax = plt.subplots(figsize=(10, 5))
pvt_sorted = pvt.sort_values('ratio_f_m')
y = range(len(pvt_sorted))
ax.barh(y, pvt_sorted['Female'], label='Female', color='#d95f02')
ax.barh(y, pvt_sorted['Male'], left=pvt_sorted['Female'], label='Male', color='#1b9e77')
ax.set_yticks(y); ax.set_yticklabels(pvt_sorted.index)
ax.set_xlabel('Number of orders')
ax.set_title('Fashion orders by product and gender')
ax.legend()
for i, (idx, row) in enumerate(pvt_sorted.iterrows()):
    ax.text(row.Female+row.Male+10, i, f'{row.ratio_f_m:.2f}x', va='center', fontsize=9)
plt.tight_layout(); plt.savefig('/work/fig5_product_gender_preference.png'); plt.close()
print('done')