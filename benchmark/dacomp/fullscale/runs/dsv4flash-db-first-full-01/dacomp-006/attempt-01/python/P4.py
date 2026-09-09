import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Load monthly order-level data
result = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, COUNT(*) AS orders, SUM(\"Profit\") AS profit, AVG(\"Profit\") AS avg_profit FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
monthly = db.frame(result)
print(monthly)

# Volume vs per-order decomposition of month-over-month change
# Total change = orders_a*avg_a - orders_b*avg_b
# = (orders_a - orders_b)*avg_b + (avg_a - avg_b)*orders_a  (approximation)
print("\n--- Volume vs margin decomposition of MoM changes ---")
prev = None
for _, row in monthly.iterrows():
    if prev is not None:
        d_orders = row['orders'] - prev['orders']
        d_avg = row['avg_profit'] - prev['avg_profit']
        volume_effect = d_orders * prev['avg_profit']
        margin_effect = d_avg * row['orders']
        total = row['profit'] - prev['profit']
        print(f"{row['month']}: total={total:+.0f}, volume_effect={volume_effect:+.0f} ({volume_effect/total*100:+.0f}%), "
              f"avg-per-order_effect={margin_effect:+.0f} ({margin_effect/total*100:+.0f}%)")
    prev = row

# Check quantity vs unit price decomposition of revenue
result2 = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, SUM(\"Sales Quantity\") AS qty, SUM(\"Total Logistics Revenue\") AS rev, SUM(\"Profit\") AS profit FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
q = db.frame(result2)
q['price'] = q['rev'] / q['qty']
print("\n--- Revenue = Qty x Price; correlation with profit ---")
print("Corr(profit, qty):", q['profit'].corr(q['qty']).round(4))
print("Corr(profit, price):", q['profit'].corr(q['price']).round(4))
print("CV qty:", (q['qty'].std()/q['qty'].mean()*100).round(1), "%")
print("CV price:", (q['price'].std()/q['price'].mean()*100).round(1), "%")

# --- Figure: Age & Gender variance share ---
age_share = pd.Series({'50-59': 37.3, '30-39': 25.0, '40-49': 23.2, '20-29': 15.2, '60-69': -0.7})
gender_share = pd.Series({'Male': 67.8, 'Female': 32.2})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
colors_age = ['#2ecc71' if v >= 0 else '#e74c3c' for v in age_share.values]
bars1 = ax1.barh(age_share.index, age_share.values, color=colors_age, alpha=0.8, edgecolor='gray')
ax1.set_xlabel('Variance Share (%)')
ax1.set_title('Variance Share by Age Range', fontsize=13, fontweight='bold')
for bar, val in zip(bars1, age_share.values):
    ax1.text(val + 0.8 if val >= 0 else val - 0.8, bar.get_y() + bar.get_height()/2, f'{val:.1f}%',
             va='center', fontsize=10, ha='left' if val >= 0 else 'right')

bars2 = ax2.barh(gender_share.index, gender_share.values, color=['#3498db', '#e74c3c'], alpha=0.8, edgecolor='gray')
ax2.set_xlabel('Variance Share (%)')
ax2.set_title('Variance Share by Customer Gender', fontsize=13, fontweight='bold')
for bar, val in zip(bars2, gender_share.values):
    ax2.text(val + 0.8, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10)

plt.tight_layout()
plt.savefig('/work/sc_age_gender_variance.png', dpi=150)
plt.close()
print("Saved sc_age_gender_variance.png")

# Monthly profit by age range and gender - table for report
result3 = db.query("SELECT \"Age Range\" AS age, \"Customer Gender\" AS gender, strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS p FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY age, gender, month ORDER BY age, gender, month")
age_gender_month = db.frame(result3)
print("\n--- Monthly profit by age group (mean, SD, CV) ---")
for age in age_gender_month['age'].unique():
    sub = age_gender_month[age_gender_month['age'] == age]
    grp = sub.groupby('month')['p'].sum()
    print(f"{age}: mean={grp.mean()/1000:.0f}k, sd={grp.std()/1000:.0f}k, CV={grp.std()/grp.mean()*100:.1f}%")

print("\n--- Monthly profit by gender (mean, SD, CV) ---")
for g in age_gender_month['gender'].unique():
    sub = age_gender_month[age_gender_month['gender'] == g]
    grp = sub.groupby('month')['p'].sum()
    print(f"{g}: mean={grp.mean()/1000:.0f}k, sd={grp.std()/1000:.0f}k, CV={grp.std()/grp.mean()*100:.1f}%")

print("\nDone.")