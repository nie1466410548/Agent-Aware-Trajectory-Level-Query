import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Get data for visualization
result = db.query("""
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 'Low-Margin' ELSE 'Normal' END AS order_type
  FROM sheet1
""")
df = db.frame(result)

print(f"Total rows: {len(df)}")
print(f"Low-margin orders: {(df['order_type'] == 'Low-Margin').sum()}")
print(f"Normal orders: {(df['order_type'] == 'Normal').sum()}")

# Set up the style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (14, 10)

# 1. Cost vs Revenue per Unit comparison
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# --- Chart 1: Average cost components per unit ---
cost_data = df.groupby('order_type').agg({
    'Sales Quantity': 'mean',
    'Total Logistics Revenue': 'mean',
    'Freight Cost': 'mean',
    'Warehousing Cost': 'mean',
    'Other Operating Costs': 'mean',
    'Total Logistics Cost': 'mean',
    'Profit': 'mean',
    'Profit Margin': 'mean',
    'Discount Amount': 'mean'
}).reset_index()

# Per-unit metrics
for col in ['Total Logistics Revenue', 'Freight Cost', 'Warehousing Cost', 'Other Operating Costs', 'Total Logistics Cost']:
    cost_data[col + '_per_unit'] = cost_data[col] / cost_data['Sales Quantity']

print("\n--- Per-unit cost comparison ---")
print(cost_data[['order_type', 'Sales Quantity', 'Total Logistics Revenue_per_unit', 'Freight Cost_per_unit', 
                  'Warehousing Cost_per_unit', 'Other Operating Costs_per_unit', 'Total Logistics Cost_per_unit']])

# --- Chart 2: Distribution of Sales Quantity ---
ax1 = axes[0, 0]
df_qty = df[df['Sales Quantity'] <= 30]  # Cap for visibility
for typ, color in [('Low-Margin', 'crimson'), ('Normal', 'steelblue')]:
    subset = df_qty[df_qty['order_type'] == typ]
    ax1.hist(subset['Sales Quantity'], bins=30, alpha=0.6, label=typ, color=color, density=True)
ax1.set_xlabel('Sales Quantity')
ax1.set_ylabel('Density')
ax1.set_title('Sales Quantity Distribution (Qty ≤ 30)')
ax1.legend()

# --- Chart 3: Discount rate distribution ---
ax2 = axes[0, 1]
df['discount_rate'] = df['Discount Amount'] / df['List Price Revenue'].replace(0, np.nan) * 100
df_disc = df[df['discount_rate'] <= 50]
for typ, color in [('Low-Margin', 'crimson'), ('Normal', 'steelblue')]:
    subset = df_disc[df_disc['order_type'] == typ]
    ax2.hist(subset['discount_rate'], bins=30, alpha=0.6, label=typ, color=color, density=True)
ax2.set_xlabel('Discount Rate (% of List Price)')
ax2.set_ylabel('Density')
ax2.set_title('Discount Rate Distribution')
ax2.legend()

# --- Chart 4: Cost structure breakdown ---
ax3 = axes[0, 2]
cost_components = ['Freight Cost', 'Warehousing Cost', 'Other Operating Costs']
x = np.arange(2)
width = 0.25
for i, comp in enumerate(cost_components):
    vals = cost_data.groupby('order_type')[comp].mean().values
    ax3.bar(x + i*width, vals, width, label=comp)
ax3.set_xticks(x + width)
ax3.set_xticklabels(['Normal', 'Low-Margin'])
ax3.set_ylabel('Average Cost ($)')
ax3.set_title('Average Cost Components')
ax3.legend()

# --- Chart 5: Profit Margin vs Discount Rate scatter ---
ax4 = axes[1, 0]
df_sample = df.sample(min(2000, len(df)), random_state=42)
ax4.scatter(df_sample[df_sample['order_type']=='Normal']['discount_rate'], 
            df_sample[df_sample['order_type']=='Normal']['Profit Margin'],
            alpha=0.3, s=10, color='steelblue', label='Normal')
ax4.scatter(df_sample[df_sample['order_type']=='Low-Margin']['discount_rate'], 
            df_sample[df_sample['order_type']=='Low-Margin']['Profit Margin'],
            alpha=0.5, s=10, color='crimson', label='Low-Margin')
ax4.axhline(y=0.3976, color='gray', linestyle='--', alpha=0.5, label='Threshold (39.76%)')
ax4.set_xlabel('Discount Rate (%)')
ax4.set_ylabel('Profit Margin')
ax4.set_title('Profit Margin vs Discount Rate')
ax4.legend()

# --- Chart 6: Revenue per unit vs Quantity ---
ax5 = axes[1, 1]
df_small = df[df['Sales Quantity'] <= 20]
for typ, color in [('Low-Margin', 'crimson'), ('Normal', 'steelblue')]:
    subset = df_small[df_small['order_type'] == typ]
    ax5.scatter(subset['Sales Quantity'], subset['Total Logistics Revenue'] / subset['Sales Quantity'].replace(0, 1),
                alpha=0.3, s=10, color=color, label=typ)
ax5.set_xlabel('Sales Quantity')
ax5.set_ylabel('Revenue per Unit ($)')
ax5.set_title('Revenue per Unit vs Sales Quantity')
ax5.legend()

# --- Chart 7: Cost per unit vs Quantity ---
ax6 = axes[1, 2]
for typ, color in [('Low-Margin', 'crimson'), ('Normal', 'steelblue')]:
    subset = df_small[df_small['order_type'] == typ]
    ax6.scatter(subset['Sales Quantity'], subset['Total Logistics Cost'] / subset['Sales Quantity'].replace(0, 1),
                alpha=0.3, s=10, color=color, label=typ)
ax6.set_xlabel('Sales Quantity')
ax6.set_ylabel('Cost per Unit ($)')
ax6.set_title('Cost per Unit vs Sales Quantity')
ax6.legend()

plt.tight_layout()
plt.savefig('/work/figure1_cost_structure.png', dpi=150)
plt.close()
print("Saved figure1_cost_structure.png")