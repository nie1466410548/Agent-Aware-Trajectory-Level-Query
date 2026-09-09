import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Scenario data
scenarios = ['Current\n(Loss)', 'Remove\nDiscounts', 'Moderate\nDiscounts', 'Reduce\nCosts', 'Combined\nStrategy']
profits = [-7374.06, 5234.11, 4517.22, 107547.30, 119438.58]
colors = ['crimson', 'mediumseagreen', 'steelblue', 'darkorange', 'goldenrod']

fig, ax = plt.subplots(figsize=(12, 7))

bars = ax.bar(scenarios, profits, color=colors, edgecolor='black', linewidth=1.2, width=0.6)

# Add value labels
for bar, val in zip(bars, profits):
    y_pos = bar.get_height() + (3000 if val > 0 else -15000)
    ax.text(bar.get_x() + bar.get_width()/2., y_pos, 
            f'${val:,.0f}', ha='center', va='bottom' if val > 0 else 'top',
            fontsize=12, fontweight='bold')

ax.axhline(y=0, color='black', linewidth=1)
ax.set_ylabel('Total Profit from Low-Margin Orders ($)', fontsize=13)
ax.set_title('Scenario Analysis: Potential Profit Improvement from Remedies', fontsize=15, fontweight='bold')

# Add annotations
ax.annotate('Breakeven', xy=(0, 0), xytext=(-0.5, -20000),
            fontsize=10, color='gray', fontstyle='italic')
ax.annotate('$11,891 recovered\nfrom discounts', xy=(2, 4517), xytext=(1.5, 30000),
            arrowprops=dict(arrowstyle='->', color='steelblue'), fontsize=10, color='steelblue')
ax.annotate('$114,921 saved\nfrom cost reduction', xy=(3, 107547), xytext=(3.5, 80000),
            arrowprops=dict(arrowstyle='->', color='darkorange'), fontsize=10, color='darkorange')

plt.tight_layout()
plt.savefig('/work/figure3_scenario_analysis.png', dpi=150)
plt.close()
print("Saved figure3_scenario_analysis.png")

# Also create a cost breakdown comparison chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Pie chart for low-margin cost breakdown
costs_lm = [63.29, 29.71, 11.22]
labels = ['Freight Cost', 'Warehousing Cost', 'Other Operating Costs']
colors_pie = ['#e74c3c', '#3498db', '#2ecc71']

axes[0].pie(costs_lm, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90, 
            explode=(0.05, 0.05, 0.05))
axes[0].set_title('Low-Margin Orders:\nCost Component Breakdown', fontsize=13, fontweight='bold')

# Pie chart for normal cost breakdown
costs_norm = [54.39, 27.55, 11.03]
axes[1].pie(costs_norm, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90,
            explode=(0.05, 0.05, 0.05))
axes[1].set_title('Normal Orders:\nCost Component Breakdown', fontsize=13, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/figure4_cost_breakdown.png', dpi=150)
plt.close()
print("Saved figure4_cost_breakdown.png")