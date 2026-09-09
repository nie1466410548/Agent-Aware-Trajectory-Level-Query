import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# --- Load data ---
result = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS profit, SUM(\"Total Logistics Revenue\") AS rev, SUM(\"Total Logistics Cost\") AS cost, SUM(\"Sales Quantity\") AS qty, COUNT(*) AS orders, AVG(\"Profit Margin\") AS avg_margin, AVG(\"Logistics Unit Price\") AS avg_price FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
monthly = db.frame(result)

result2 = db.query("SELECT \"Consigned Product\" AS dim, strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS p FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY dim, month ORDER BY dim, month")
prod_month = db.frame(result2)

result3 = db.query("SELECT substr(\"Destination\", 13, instr(substr(\"Destination\", 13), '-') - 1) AS province, strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS p FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY province, month ORDER BY province, month")
prov_month = db.frame(result3)

# Variance share calculations
merged = prod_month.merge(monthly[['month', 'profit']], on='month', how='left')
merged['p_dev'] = merged['p'] - merged.groupby('dim')['p'].transform('mean')
merged['t_dev'] = merged['profit'] - merged['profit'].mean()
merged['cov_term'] = merged['p_dev'] * merged['t_dev']
var_t = (merged['t_dev'] ** 2).mean()
prod_variance_share = merged.groupby('dim')['cov_term'].mean() / var_t * 100
prod_sorted = prod_variance_share.sort_values(ascending=False)

prov_merged = prov_month.merge(monthly[['month', 'profit']], on='month', how='left')
prov_merged['p_dev'] = prov_merged['p'] - prov_merged.groupby('province')['p'].transform('mean')
prov_merged['t_dev'] = prov_merged['profit'] - prov_merged['profit'].mean()
prov_merged['cov_term'] = prov_merged['p_dev'] * prov_merged['t_dev']
prov_variance_share = prov_merged.groupby('province')['cov_term'].mean() / var_t * 100
prov_sorted = prov_variance_share.sort_values(ascending=False)

# --- Figure 3: Variance share bar charts ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Product variance share - bar chart
colors_prod = plt.cm.tab20(np.linspace(0, 1, len(prod_sorted)))
bars1 = ax1.barh(prod_sorted.index, prod_sorted.values, color=colors_prod, alpha=0.8, edgecolor='gray')
ax1.set_xlabel('Variance Share (%)', fontsize=12)
ax1.set_title('Variance Share by Product Category', fontsize=13, fontweight='bold')
for bar, val in zip(bars1, prod_sorted.values):
    ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10)

# Province variance share - bar chart (handle negative)
colors_prov = ['#2ecc71' if v >= 0 else '#e74c3c' for v in prov_sorted.values]
bars2 = ax2.barh(prov_sorted.index, prov_sorted.values, color=colors_prov, alpha=0.8, edgecolor='gray')
ax2.set_xlabel('Variance Share (%)', fontsize=12)
ax2.set_title('Variance Share by Province', fontsize=13, fontweight='bold')
for bar, val in zip(bars2, prov_sorted.values):
    if val >= 0:
        ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10)
    else:
        ax2.text(val - 2.5, bar.get_y() + bar.get_height()/2, f'{val:.1f}%', va='center', fontsize=10, ha='right')

plt.tight_layout()
plt.savefig('/work/sc_variance_share_bar.png', dpi=150)
plt.close()
print("Saved sc_variance_share_bar.png")

# --- Figure 4: Monthly profit by product (stacked area) ---
prod_pivot = prod_month.pivot(index='month', columns='dim', values='p').fillna(0)
fig, ax = plt.subplots(figsize=(14, 7))
months = prod_pivot.index
colors = plt.cm.tab20(np.linspace(0, 1, len(prod_pivot.columns)))
ax.stackplot(months, prod_pivot.values.T, labels=prod_pivot.columns, colors=colors, alpha=0.8)
ax.plot(months, prod_pivot.sum(axis=1).values/1000, 'k-', linewidth=2, label='Total')
ax.set_ylabel('Profit (thousands)', fontsize=13)
ax.set_xlabel('Month', fontsize=13)
ax.set_title('Monthly Profit by Product Category - South China', fontsize=14, fontweight='bold')
ax.legend(fontsize=9, loc='upper left', ncol=2)
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('/work/sc_product_stacked_area.png', dpi=150)
plt.close()
print("Saved sc_product_stacked_area.png")

# --- Figure 5: Monthly profit by province (stacked area) ---
prov_pivot = prov_month.pivot(index='month', columns='province', values='p').fillna(0)
fig, ax = plt.subplots(figsize=(14, 7))
months = prov_pivot.index
colors = plt.cm.Set1(np.linspace(0, 1, len(prov_pivot.columns)))
ax.stackplot(months, prov_pivot.values.T, labels=prov_pivot.columns, colors=colors, alpha=0.8)
ax.plot(months, prov_pivot.sum(axis=1).values/1000, 'k-', linewidth=2, label='Total')
ax.set_ylabel('Profit (thousands)', fontsize=13)
ax.set_xlabel('Month', fontsize=13)
ax.set_title('Monthly Profit by Province - South China', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper left')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('/work/sc_province_stacked_area.png', dpi=150)
plt.close()
print("Saved sc_province_stacked_area.png")

# --- Figure 6: Revenue and Cost components ---
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

# Revenue components
rev_result = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, SUM(\"List Price Revenue\") AS list_price, SUM(\"Logistics Value-Added Service Revenue\") AS vas, SUM(\"Discount Amount\") AS discount FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
rev_comp = db.frame(rev_result)
cost_result = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, SUM(\"Freight Cost\") AS freight, SUM(\"Warehousing Cost\") AS warehousing, SUM(\"Other Operating Costs\") AS other FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
cost_comp = db.frame(cost_result)

# Revenue components
ax1 = axes[0]
months_labels = monthly['month'].tolist()
x = np.arange(len(months_labels))
width = 0.25
ax1.bar(x - width, rev_comp['list_price'].values/1000, width, label='List Price Revenue', alpha=0.8)
ax1.bar(x, rev_comp['vas'].values/1000, width, label='Value-Added Service', alpha=0.8)
ax1.bar(x + width, rev_comp['discount'].values/1000, width, label='Discount Amount', alpha=0.8)
ax1.plot(x, monthly['rev'].values/1000, 'ko-', linewidth=2, label='Total Revenue')
ax1.set_xticks(x)
ax1.set_xticklabels(months_labels, rotation=45)
ax1.set_ylabel('Amount (thousands)', fontsize=12)
ax1.set_title('Monthly Revenue Components', fontsize=13, fontweight='bold')
ax1.legend(fontsize=10)

# Cost components
ax2 = axes[1]
ax2.bar(x - width, cost_comp['freight'].values/1000, width, label='Freight Cost', alpha=0.8)
ax2.bar(x, cost_comp['warehousing'].values/1000, width, label='Warehousing Cost', alpha=0.8)
ax2.bar(x + width, cost_comp['other'].values/1000, width, label='Other Operating Costs', alpha=0.8)
ax2.plot(x, monthly['cost'].values/1000, 'ko-', linewidth=2, label='Total Cost')
ax2.set_xticks(x)
ax2.set_xticklabels(months_labels, rotation=45)
ax2.set_ylabel('Amount (thousands)', fontsize=12)
ax2.set_title('Monthly Cost Components', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('/work/sc_revenue_cost_components.png', dpi=150)
plt.close()
print("Saved sc_revenue_cost_components.png")

# --- Summary statistics for report ---
print("\n=== KEY FINDINGS ===")
print(f"Monthly profit mean: {monthly['profit'].mean()/1000:.1f}k")
print(f"Monthly profit range: {monthly['profit'].min()/1000:.1f}k - {monthly['profit'].max()/1000:.1f}k")
print(f"Overall CV: {monthly['profit'].std()/monthly['profit'].mean()*100:.1f}%")
print(f"Largest drop: Feb 2023 ({monthly.iloc[1]['profit']/1000:.1f}k, {(monthly.iloc[1]['profit']-monthly.iloc[0]['profit'])/monthly.iloc[0]['profit']*100:.1f}%)")
print(f"Largest gain: Mar 2023 ({monthly.iloc[2]['profit']/1000:.1f}k, {(monthly.iloc[2]['profit']-monthly.iloc[1]['profit'])/monthly.iloc[1]['profit']*100:.1f}%)")

# Product-level CV
print("\nProduct CV%:")
for dim in prod_variance_share.sort_values(ascending=False).index:
    sub = prod_month[prod_month['dim']==dim]
    cv = sub['p'].std() / sub['p'].mean() * 100
    share = prod_variance_share[dim]
    print(f"  {dim}: CV={cv:.1f}%, VarianceShare={share:.1f}%")

print("\nProvince CV%:")
for prov in prov_variance_share.sort_values(ascending=False).index:
    sub = prov_month[prov_month['province']==prov]
    cv = sub['p'].std() / sub['p'].mean() * 100
    share = prov_variance_share[prov]
    print(f"  {prov}: CV={cv:.1f}%, VarianceShare={share:.1f}%")

print("\nAll figures saved successfully.")