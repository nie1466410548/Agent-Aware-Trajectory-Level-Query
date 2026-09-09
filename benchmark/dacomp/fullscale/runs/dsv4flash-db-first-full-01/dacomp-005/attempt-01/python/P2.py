import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Get data
result = db.query("""
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 'Low-Margin' ELSE 'Normal' END AS order_type
  FROM sheet1
""")
df = db.frame(result)

df['discount_rate'] = df['Discount Amount'] / df['List Price Revenue'].replace(0, np.nan) * 100
df['Date'] = pd.to_datetime(df['Date'])
df['month'] = df['Date'].dt.month
df['region'] = df['Destination'].str.split('-').str[0]

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# --- Chart 1: Monthly low-margin rate ---
ax1 = axes[0, 0]
monthly = df.groupby('month').agg(
    total=('Profit Margin', 'count'),
    low=('order_type', lambda x: (x == 'Low-Margin').sum())
).reset_index()
monthly['pct'] = monthly['low'] / monthly['total'] * 100
ax1.plot(monthly['month'], monthly['pct'], 'o-', color='crimson', linewidth=2)
ax1.set_xlabel('Month (2023)')
ax1.set_ylabel('Low-Margin Rate (%)')
ax1.set_title('Monthly Low-Margin Order Rate')
ax1.set_xticks(range(1, 13))
ax1.axhline(y=monthly['pct'].mean(), color='gray', linestyle='--', alpha=0.7, label=f'Avg: {monthly["pct"].mean():.2f}%')
ax1.legend()

# --- Chart 2: Low-margin rate by region ---
ax2 = axes[0, 1]
region_stats = df.groupby('region').agg(
    total=('Profit Margin', 'count'),
    low=('order_type', lambda x: (x == 'Low-Margin').sum())
).reset_index()
region_stats['pct'] = region_stats['low'] / region_stats['total'] * 100
region_stats = region_stats.sort_values('pct', ascending=True)
colors = ['crimson' if v > region_stats['pct'].mean() else 'steelblue' for v in region_stats['pct']]
ax2.barh(region_stats['region'], region_stats['pct'], color=colors)
ax2.set_xlabel('Low-Margin Rate (%)')
ax2.set_title('Low-Margin Rate by Region')
ax2.axvline(x=region_stats['pct'].mean(), color='gray', linestyle='--', alpha=0.7)

# --- Chart 3: Low-margin rate by Age Range ---
ax3 = axes[0, 2]
age_stats = df.groupby('Age Range').agg(
    total=('Profit Margin', 'count'),
    low=('order_type', lambda x: (x == 'Low-Margin').sum())
).reset_index()
age_stats['pct'] = age_stats['low'] / age_stats['total'] * 100
ax3.bar(age_stats['Age Range'], age_stats['pct'], color=['crimson' if v > 6.81 else 'steelblue' for v in age_stats['pct']])
ax3.set_xlabel('Age Range')
ax3.set_ylabel('Low-Margin Rate (%)')
ax3.set_title('Low-Margin Rate by Age Range')
ax3.axhline(y=6.81, color='gray', linestyle='--', alpha=0.7, label='Overall: 6.81%')
ax3.legend()

# --- Chart 4: Low-margin rate by Consigned Product ---
ax4 = axes[1, 0]
prod_stats = df.groupby('Consigned Product').agg(
    total=('Profit Margin', 'count'),
    low=('order_type', lambda x: (x == 'Low-Margin').sum())
).reset_index()
prod_stats['pct'] = prod_stats['low'] / prod_stats['total'] * 100
prod_stats = prod_stats.sort_values('pct', ascending=True)
ax4.barh(prod_stats['Consigned Product'], prod_stats['pct'], color='steelblue')
ax4.set_xlabel('Low-Margin Rate (%)')
ax4.set_title('Low-Margin Rate by Product')
ax4.axvline(x=6.81, color='gray', linestyle='--', alpha=0.7, label='Overall: 6.81%')
ax4.legend()

# --- Chart 5: Discount Rate vs. Profit Margin by product ---
ax5 = axes[1, 1]
for prod in df['Consigned Product'].unique():
    subset = df[df['Consigned Product'] == prod]
    lm_subset = subset[subset['order_type'] == 'Low-Margin']
    ax5.scatter([prod]*len(lm_subset), lm_subset['discount_rate'], alpha=0.3, s=5, color='crimson')
ax5.set_xticklabels(df['Consigned Product'].unique(), rotation=45, ha='right')
ax5.set_ylabel('Discount Rate (%)')
ax5.set_title('Discount Rates of Low-Margin Orders by Product')

# --- Chart 6: Quantity distribution for low-margin orders ---
ax6 = axes[1, 2]
lm_df = df[df['order_type'] == 'Low-Margin']
qty_bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 40]
qty_labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-15', '16-20', '21-30', '31-40']
lm_df['qty_group'] = pd.cut(lm_df['Sales Quantity'], bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30, 100], 
                            labels=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11-15', '16-20', '21-30', '31+'])
qty_dist = lm_df['qty_group'].value_counts().sort_index()
ax6.bar(range(len(qty_dist)), qty_dist.values, color='crimson')
ax6.set_xticks(range(len(qty_dist)))
ax6.set_xticklabels(qty_dist.index, rotation=45)
ax6.set_xlabel('Sales Quantity')
ax6.set_ylabel('Number of Low-Margin Orders')
ax6.set_title('Low-Margin Orders by Sales Quantity')

plt.tight_layout()
plt.savefig('/work/figure2_demographics_trends.png', dpi=150)
plt.close()
print("Saved figure2_demographics_trends.png")