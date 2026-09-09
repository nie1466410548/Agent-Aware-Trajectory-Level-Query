import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# Load monthly profit data
result = db.query("SELECT strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS profit, SUM(\"Total Logistics Revenue\") AS rev, SUM(\"Total Logistics Cost\") AS cost, SUM(\"Sales Quantity\") AS qty, COUNT(*) AS orders, AVG(\"Profit Margin\") AS avg_margin, AVG(\"Logistics Unit Price\") AS avg_price FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY month ORDER BY month")
monthly = db.frame(result)
print("Monthly data:")
print(monthly)

# Load product-month data
result2 = db.query("SELECT \"Consigned Product\" AS dim, strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS p FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY dim, month ORDER BY dim, month")
prod_month = db.frame(result2)
print("\nProduct-month sample:")
print(prod_month.head(16))

# Load province-month data
result3 = db.query("SELECT substr(\"Destination\", 13, instr(substr(\"Destination\", 13), '-') - 1) AS province, strftime('%Y-%m', \"Date\") AS month, SUM(\"Profit\") AS p FROM sheet1 WHERE \"Destination\" LIKE 'South China%%' GROUP BY province, month ORDER BY province, month")
prov_month = db.frame(result3)
print("\nProvince-month sample:")
print(prov_month.head(12))

# Set up plotting style
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 12
sns.set_style("whitegrid")

# --- Figure 1: Monthly profit trend ---
fig, ax1 = plt.subplots(figsize=(14, 6))
months = monthly['month'].tolist()
profit = monthly['profit'].values / 1000  # in thousands
mean_profit = np.mean(profit)
colors = ['#2ecc71' if p >= mean_profit else '#e74c3c' for p in profit]
bars = ax1.bar(months, profit, color=colors, alpha=0.7, edgecolor='gray', linewidth=0.5)
ax1.axhline(y=mean_profit, color='blue', linestyle='--', linewidth=1.5, label=f'Mean: {mean_profit:.0f}k')
ax1.set_ylabel('Total Profit (thousands)', fontsize=13)
ax1.set_xlabel('Month', fontsize=13)
ax1.set_title('South China Monthly Total Profit (2023)', fontsize=15, fontweight='bold')
ax1.tick_params(axis='x', rotation=45)
ax1.legend(fontsize=11)

# Add value labels on bars
for bar, val in zip(bars, profit):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f'{val:.0f}k', 
             ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/sc_monthly_profit.png', dpi=150)
plt.close()
print("Saved sc_monthly_profit.png")

# --- Figure 2: Month-over-month change decomposition by product ---
# Compute month-over-month changes for each product
prod_month_pivot = prod_month.pivot(index='month', columns='dim', values='p').fillna(0)
# Get total
total_pivot = monthly[['month', 'profit']].set_index('month')
total_chg = total_pivot.diff().dropna()

# Product changes
prod_chg = prod_month_pivot.diff().dropna()

# For the Feb transition (Jan->Feb), which products contributed most?
print("\n--- Month-over-month change decomposition ---")
for i in range(len(total_chg)):
    month = total_chg.index[i]
    total_chg_val = total_chg.iloc[i, 0]
    print(f"\n{month}: total change = {total_chg_val:+.0f}")
    # Top 3 positive and negative contributors
    contributors = prod_chg.iloc[i].sort_values(key=abs, ascending=False)
    print("  Top contributors:")
    for dim, val in contributors.head(5).items():
        print(f"    {dim}: {val:+.0f}")
    print("  Bottom contributors:")
    for dim, val in contributors.tail(3).items():
        print(f"    {dim}: {val:+.0f}")

# Plot: stacked bar of product contributions to monthly changes
fig, ax = plt.subplots(figsize=(14, 7))
idx = np.arange(len(prod_chg.index))
width = 0.7
bottom = np.zeros(len(prod_chg.index))
colors_list = plt.cm.Set2(np.linspace(0, 1, len(prod_chg.columns)))
for i, col in enumerate(prod_chg.columns):
    vals = prod_chg[col].values / 1000
    ax.bar(idx, vals, width, bottom=bottom, label=col, color=colors_list[i], alpha=0.8)
    bottom += vals

total_chg_vals = total_chg['profit'].values / 1000
ax.plot(idx, total_chg_vals, 'ko-', linewidth=2, markersize=6, label='Total Change')
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax.set_xticks(idx)
ax.set_xticklabels(prod_chg.index, rotation=45)
ax.set_ylabel('Change in Profit (thousands)', fontsize=13)
ax.set_xlabel('Month Transition', fontsize=13)
ax.set_title('Product Contribution to Month-over-Month Profit Changes', fontsize=14, fontweight='bold')
ax.legend(fontsize=9, loc='upper left', ncol=2)
plt.tight_layout()
plt.savefig('/work/sc_product_change_contrib.png', dpi=150)
plt.close()
print("Saved sc_product_change_contrib.png")

# --- Figure 3: Province-level decomposition ---
prov_month_pivot = prov_month.pivot(index='month', columns='province', values='p').fillna(0)
prov_chg = prov_month_pivot.diff().dropna()

fig, ax = plt.subplots(figsize=(14, 7))
idx = np.arange(len(prov_chg.index))
bottom = np.zeros(len(prov_chg.index))
colors_list = plt.cm.Set1(np.linspace(0, 1, len(prov_chg.columns)))
for i, col in enumerate(prov_chg.columns):
    vals = prov_chg[col].values / 1000
    ax.bar(idx, vals, width, bottom=bottom, label=col, color=colors_list[i], alpha=0.8)
    bottom += vals

ax.plot(idx, total_chg_vals, 'ko-', linewidth=2, markersize=6, label='Total Change')
ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax.set_xticks(idx)
ax.set_xticklabels(prov_chg.index, rotation=45)
ax.set_ylabel('Change in Profit (thousands)', fontsize=13)
ax.set_xlabel('Month Transition', fontsize=13)
ax.set_title('Province Contribution to Month-over-Month Profit Changes', fontsize=14, fontweight='bold')
ax.legend(fontsize=11, loc='upper left')
plt.tight_layout()
plt.savefig('/work/sc_province_change_contrib.png', dpi=150)
plt.close()
print("Saved sc_province_change_contrib.png")

# --- Figure 4: Variance decomposition pie charts ---
# Product variance share
prod_month['p_mean'] = prod_month.groupby('dim')['p'].transform('mean')
total_mean = monthly['profit'].mean()
prod_month['total_mean'] = total_mean
prod_month['dev_p'] = prod_month['p'] - prod_month['p_mean']
prod_month['dev_t'] = prod_month['profit'] - prod_month['total_mean']  # This will broadcast
# Actually, let me compute properly
merged = prod_month.merge(monthly[['month', 'profit']], on='month')
merged['p_dev'] = merged['p'] - merged.groupby('dim')['p'].transform('mean')
merged['t_dev'] = merged['profit'] - merged['profit'].mean()
merged['cov_term'] = merged['p_dev'] * merged['t_dev']
var_t = (merged['t_dev'] ** 2).mean()

prod_variance_share = merged.groupby('dim')['cov_term'].mean() / var_t * 100
print("\nProduct variance share:")
print(prod_variance_share.sort_values(ascending=False))

# Province variance share
prov_merged = prov_month.merge(monthly[['month', 'profit']], on='month')
prov_merged['p_dev'] = prov_merged['p'] - prov_merged.groupby('province')['p'].transform('mean')
prov_merged['t_dev'] = prov_merged['profit'] - prov_merged['profit'].mean()
prov_merged['cov_term'] = prov_merged['p_dev'] * prov_merged['t_dev']
prov_variance_share = prov_merged.groupby('province')['cov_term'].mean() / var_t * 100
print("\nProvince variance share:")
print(prov_variance_share.sort_values(ascending=False))

# Correlation analysis
print("\n--- Correlation of monthly profit with other metrics ---")
for col in ['rev', 'cost', 'qty', 'orders', 'avg_margin', 'avg_price']:
    corr = monthly['profit'].corr(monthly[col])
    print(f"  Profit vs {col}: {corr:.4f}")

# CV of key metrics
print("\n--- Coefficient of Variation (CV%) ---")
for col in ['profit', 'rev', 'cost', 'qty', 'orders', 'avg_margin', 'avg_price']:
    cv = monthly[col].std() / monthly[col].mean() * 100
    print(f"  {col}: {cv:.1f}%")

print("\nDone with Python analysis.")