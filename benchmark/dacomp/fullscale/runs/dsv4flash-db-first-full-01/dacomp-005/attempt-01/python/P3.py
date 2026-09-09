import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats

# Get data
result = db.query("""
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
""")
df = db.frame(result)

df['discount_rate'] = df['Discount Amount'] / df['List Price Revenue'].replace(0, np.nan) * 100
df['cost_per_unit'] = df['Total Logistics Cost'] / df['Sales Quantity'].replace(0, 1)
df['rev_per_unit'] = df['Total Logistics Revenue'] / df['Sales Quantity'].replace(0, 1)
df['freight_per_unit'] = df['Freight Cost'] / df['Sales Quantity'].replace(0, 1)

# Separate groups
lm = df[df['is_low'] == 1]
normal = df[df['is_low'] == 0]

print("=" * 70)
print("KEY STATISTICAL COMPARISONS (Low-Margin vs Normal Orders)")
print("=" * 70)

# 1. Sales Quantity
print("\n--- Sales Quantity ---")
print(f"Low-Margin:  mean={lm['Sales Quantity'].mean():.2f}, median={lm['Sales Quantity'].median():.1f}, std={lm['Sales Quantity'].std():.2f}")
print(f"Normal:      mean={normal['Sales Quantity'].mean():.2f}, median={normal['Sales Quantity'].median():.1f}, std={normal['Sales Quantity'].std():.2f}")
t_stat, p_val = stats.mannwhitneyu(lm['Sales Quantity'], normal['Sales Quantity'], alternative='less')
print(f"Mann-Whitney U test: p-value = {p_val:.2e} (significant difference)")

# 2. Discount Rate
print("\n--- Discount Rate (% of List Price) ---")
print(f"Low-Margin:  mean={lm['discount_rate'].mean():.2f}%, median={lm['discount_rate'].median():.2f}%")
print(f"Normal:      mean={normal['discount_rate'].mean():.2f}%, median={normal['discount_rate'].median():.2f}%")
t_stat, p_val = stats.mannwhitneyu(lm['discount_rate'], normal['discount_rate'], alternative='greater')
print(f"Mann-Whitney U test: p-value = {p_val:.2e} (significant difference)")

# 3. Cost per unit
print("\n--- Cost per Unit ($) ---")
print(f"Low-Margin:  mean={lm['cost_per_unit'].mean():.2f}, median={lm['cost_per_unit'].median():.2f}")
print(f"Normal:      mean={normal['cost_per_unit'].mean():.2f}, median={normal['cost_per_unit'].median():.2f}")
t_stat, p_val = stats.mannwhitneyu(lm['cost_per_unit'], normal['cost_per_unit'], alternative='greater')
print(f"Mann-Whitney U test: p-value = {p_val:.2e} (significant difference)")

# 4. Revenue per unit
print("\n--- Revenue per Unit ($) ---")
print(f"Low-Margin:  mean={lm['rev_per_unit'].mean():.2f}, median={lm['rev_per_unit'].median():.2f}")
print(f"Normal:      mean={normal['rev_per_unit'].mean():.2f}, median={normal['rev_per_unit'].median():.2f}")
t_stat, p_val = stats.mannwhitneyu(lm['rev_per_unit'], normal['rev_per_unit'], alternative='less')
print(f"Mann-Whitney U test: p-value = {p_val:.2e} (significant difference)")

# 5. Freight cost per unit
print("\n--- Freight Cost per Unit ($) ---")
print(f"Low-Margin:  mean={lm['freight_per_unit'].mean():.2f}, median={lm['freight_per_unit'].median():.2f}")
print(f"Normal:      mean={normal['freight_per_unit'].mean():.2f}, median={normal['freight_per_unit'].median():.2f}")

# 6. Analyze the fixed vs variable cost structure
print("\n\n--- Cost Structure Analysis: Correlation with Quantity ---")
print(f"Low-Margin: Cost vs Quantity correlation r = {lm['Sales Quantity'].corr(lm['Total Logistics Cost']):.4f}")
print(f"Normal:     Cost vs Quantity correlation r = {normal['Sales Quantity'].corr(normal['Total Logistics Cost']):.4f}")
print(f"Low-Margin: Rev vs Quantity correlation r = {lm['Sales Quantity'].corr(lm['Total Logistics Revenue']):.4f}")
print(f"Normal:     Rev vs Quantity correlation r = {normal['Sales Quantity'].corr(normal['Total Logistics Revenue']):.4f}")

# 7. Cost components as % of revenue
print("\n\n--- Cost as % of Revenue ---")
for comp in ['Freight Cost', 'Warehousing Cost', 'Other Operating Costs', 'Total Logistics Cost']:
    lm_pct = (lm[comp].sum() / lm['Total Logistics Revenue'].sum()) * 100
    normal_pct = (normal[comp].sum() / normal['Total Logistics Revenue'].sum()) * 100
    print(f"  {comp}:")
    print(f"    Low-Margin: {lm_pct:.2f}% of revenue")
    print(f"    Normal:     {normal_pct:.2f}% of revenue")

# 8. Total financial impact of low-margin orders
print("\n\n--- Financial Impact ---")
print(f"Low-Margin orders: {len(lm)} orders")
print(f"  Total Revenue: ${lm['Total Logistics Revenue'].sum():.2f}")
print(f"  Total Cost:    ${lm['Total Logistics Cost'].sum():.2f}")
print(f"  Total Profit:  ${lm['Profit'].sum():.2f}")
print(f"  Total Discount: ${lm['Discount Amount'].sum():.2f}")
print(f"  Discount as % of Revenue: {lm['Discount Amount'].sum() / lm['Total Logistics Revenue'].sum() * 100:.2f}%")
print(f"\nNormal orders: {len(normal)} orders")
print(f"  Total Revenue: ${normal['Total Logistics Revenue'].sum():.2f}")
print(f"  Total Cost:    ${normal['Total Logistics Cost'].sum():.2f}")
print(f"  Total Profit:  ${normal['Profit'].sum():.2f}")

# 9. Correlation between discount rate and profit margin
print("\n\n--- Correlation: Discount Rate vs Profit Margin ---")
r_lm, p_lm = stats.pearsonr(lm['discount_rate'].dropna(), lm['Profit Margin'].loc[lm['discount_rate'].notna()])
r_all, p_all = stats.pearsonr(df['discount_rate'].dropna(), df['Profit Margin'].loc[df['discount_rate'].notna()])
print(f"  Low-Margin: r = {r_lm:.4f}, p = {p_lm:.2e}")
print(f"  All orders: r = {r_all:.4f}, p = {p_all:.2e}")

# 10. What percentage of low-margin orders have negative profit?
lm_neg = (lm['Profit'] < 0).sum()
print(f"\n\n--- Profitability of Low-Margin Orders ---")
print(f"  Orders with negative profit: {lm_neg} ({lm_neg/len(lm)*100:.2f}%)")
print(f"  Orders with positive profit: {len(lm) - lm_neg} ({(len(lm)-lm_neg)/len(lm)*100:.2f}%)")

# 11. Analyze the "sweet spot" - what quantity would make these viable?
print("\n\n--- Break-even Analysis ---")
lm_avg_cost = lm['Total Logistics Cost'].mean()
lm_avg_rev_per_unit = lm['Total Logistics Revenue'].sum() / lm['Sales Quantity'].sum()
print(f"  Average cost per low-margin order: ${lm_avg_cost:.2f}")
print(f"  Average revenue per unit (low-margin): ${lm_avg_rev_per_unit:.2f}")
print(f"  Break-even quantity: {np.ceil(lm_avg_cost / lm_avg_rev_per_unit):.0f} units")

# Compare with normal orders
normal_avg_cost = normal['Total Logistics Cost'].mean()
normal_avg_rev_per_unit = normal['Total Logistics Revenue'].sum() / normal['Sales Quantity'].sum()
print(f"  Average cost per normal order: ${normal_avg_cost:.2f}")
print(f"  Average revenue per unit (normal): ${normal_avg_rev_per_unit:.2f}")

# 12. Top destinations with highest low-margin rates
print("\n\n--- Top 10 Destinations by Low-Margin Rate (min 30 orders) ---")
dest_stats = df.groupby('Destination').agg(
    total=('Profit Margin', 'count'),
    low=('is_low', 'sum')
).reset_index()
dest_stats['pct'] = dest_stats['low'] / dest_stats['total'] * 100
dest_stats = dest_stats[dest_stats['total'] >= 30].sort_values('pct', ascending=False)
for _, row in dest_stats.head(10).iterrows():
    print(f"  {row['Destination']}: {row['pct']:.2f}% ({row['low']}/{row['total']})")

print("\n\n=== ANALYSIS COMPLETE ===")