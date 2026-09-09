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

print("Monthly columns:", monthly.columns.tolist())
print("Prod_month columns:", prod_month.columns.tolist())

# --- Variance Decomposition ---
# Merge product-month with total
merged = prod_month.merge(monthly[['month', 'profit']], on='month', how='left')
# Compute deviations
merged['p_dev'] = merged['p'] - merged.groupby('dim')['p'].transform('mean')
merged['t_dev'] = merged['profit'] - merged['profit'].mean()
merged['cov_term'] = merged['p_dev'] * merged['t_dev']
var_t = (merged['t_dev'] ** 2).mean()
prod_variance_share = merged.groupby('dim')['cov_term'].mean() / var_t * 100
print("\nProduct variance share:")
print(prod_variance_share.sort_values(ascending=False))

# Province variance decomposition
prov_merged = prov_month.merge(monthly[['month', 'profit']], on='month', how='left')
prov_merged['p_dev'] = prov_merged['p'] - prov_merged.groupby('province')['p'].transform('mean')
prov_merged['t_dev'] = prov_merged['profit'] - prov_merged['profit'].mean()
prov_merged['cov_term'] = prov_merged['p_dev'] * prov_merged['t_dev']
prov_variance_share = prov_merged.groupby('province')['cov_term'].mean() / var_t * 100
print("\nProvince variance share:")
print(prov_variance_share.sort_values(ascending=False))

# --- Correlation analysis ---
print("\n--- Correlation of monthly profit with other metrics ---")
for col in ['rev', 'cost', 'qty', 'orders', 'avg_margin', 'avg_price']:
    corr = monthly['profit'].corr(monthly[col])
    print(f"  Profit vs {col}: {corr:.4f}")

# CV of key metrics
print("\n--- Coefficient of Variation (CV%) ---")
for col in ['profit', 'rev', 'cost', 'qty', 'orders', 'avg_margin', 'avg_price']:
    cv = monthly[col].std() / monthly[col].mean() * 100
    print(f"  {col}: {cv:.1f}%")

# --- Figure: Profit components correlation ---
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
metrics = ['rev', 'cost', 'qty', 'orders', 'avg_margin', 'avg_price']
titles = ['Revenue (k)', 'Cost (k)', 'Quantity', 'Orders', 'Avg Margin', 'Avg Unit Price']
for ax, met, tit in zip(axes.flatten(), metrics, titles):
    vals = monthly[met].values
    if met in ['rev', 'cost']:
        vals = vals / 1000
    ax.scatter(vals, monthly['profit'].values/1000, alpha=0.7, s=80, c='steelblue')
    ax.set_xlabel(tit, fontsize=11)
    ax.set_ylabel('Profit (k)', fontsize=11)
    # Add trend line
    z = np.polyfit(vals, monthly['profit'].values/1000, 1)
    p = np.poly1d(z)
    x_line = np.linspace(vals.min(), vals.max(), 100)
    ax.plot(x_line, p(x_line), 'r--', alpha=0.6)
    corr = monthly['profit'].corr(monthly[met])
    ax.set_title(f'{tit} (r={corr:.2f})', fontsize=12)
plt.suptitle('Monthly Profit Drivers - South China', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('/work/sc_profit_drivers_scatter.png', dpi=150)
plt.close()
print("Saved sc_profit_drivers_scatter.png")

# --- Figure 3: Variance share pie charts ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Product variance share
prod_sorted = prod_variance_share.sort_values(ascending=False)
colors_prod = plt.cm.tab20(np.linspace(0, 1, len(prod_sorted)))
wedges1, texts1, autotexts1 = ax1.pie(prod_sorted.values, labels=prod_sorted.index, autopct='%1.1f%%',
    colors=colors_prod, startangle=90, textprops={'fontsize': 10})
ax1.set_title('Variance Share by Product', fontsize=13, fontweight='bold')

# Province variance share
prov_sorted = prov_variance_share.sort_values(ascending=False)
colors_prov = plt.cm.Set1(np.linspace(0, 1, len(prov_sorted)))
wedges2, texts2, autotexts2 = ax2.pie(prov_sorted.values, labels=prov_sorted.index, autopct='%1.1f%%',
    colors=colors_prov, startangle=90, textprops={'fontsize': 10})
ax2.set_title('Variance Share by Province', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/sc_variance_share_pie.png', dpi=150)
plt.close()
print("Saved sc_variance_share_pie.png")

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

print("\nAll Python analysis complete.")