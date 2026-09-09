import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Figure 1: Resource intensity comparison Level 5 vs Non-Level 5
categories = ['Affected\nper Staff', 'Affected\nper $1k Budget', 'Affected\nper Food Ton', 'Affected\nper Transp. Ton', 'Displaced\nper Shelter Unit', 'Injured\nper Medic']
l5_vals = [3253, 0.273, 2307, 341.2, 27.5, 54.5]
nonl5_vals = [2635, 0.215, 2490, 374.1, 26.4, 65.1]

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Left: resource intensity ratios
x = np.arange(len(categories))
w = 0.35
ax = axes[0]
bars1 = ax.bar(x - w/2, l5_vals, w, label='Level 5', color='crimson', alpha=0.8)
bars2 = ax.bar(x + w/2, nonl5_vals, w, label='Non-Level 5', color='steelblue', alpha=0.8)
ax.set_ylabel('Ratio Value')
ax.set_title('Resource Intensity Ratios by Severity Level')
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=9)
ax.legend()
ax.set_yscale('log')
for bar in bars1:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05, str(bar.get_height()),
            ha='center', va='bottom', fontsize=7, rotation=45)
for bar in bars2:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05, str(bar.get_height()),
            ha='center', va='bottom', fontsize=7, rotation=45)

# Right: Key performance indicators comparison
metrics = ['Medical%\nof Staff', 'Volunteer\nRatio', 'Delivery\nSuccess %', 'Delivery\nDelay %', 'PPE\nCritical %', 'Training\nComplete %']
l5_pct = [34.0, 3.2, 85.8, 36.1, 37.6, 29.7]
nonl5_pct = [27.6, 2.7, 84.7, 30.7, 31.4, 33.4]

x2 = np.arange(len(metrics))
ax2 = axes[1]
bars3 = ax2.bar(x2 - w/2, l5_pct, w, label='Level 5', color='crimson', alpha=0.8)
bars4 = ax2.bar(x2 + w/2, nonl5_pct, w, label='Non-Level 5', color='steelblue', alpha=0.8)
ax2.set_ylabel('Percentage (%)')
ax2.set_title('Human Resource & Delivery Metrics')
ax2.set_xticks(x2)
ax2.set_xticklabels(metrics, fontsize=9)
ax2.legend()
for bar in bars3:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{bar.get_height():.1f}%',
            ha='center', va='bottom', fontsize=7)
for bar in bars4:
    ax2.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f'{bar.get_height():.1f}%',
            ha='center', va='bottom', fontsize=7)

plt.tight_layout()
plt.savefig('/work/fig1_resource_intensity.png', dpi=150)
plt.close()

# Figure 2: Level 5 operational status distributions
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Resource Allocation Status
labels_ras = ['Sufficient (74)', 'Critical (65)', 'Limited (63)']
vals_ras = [74, 65, 63]
colors_ras = ['#2ecc71', '#e74c3c', '#f39c12']
axes[0].pie(vals_ras, labels=labels_ras, colors=colors_ras, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Resource Allocation Status')

# Supply Flow Status
labels_sfs = ['Stable (78)', 'Disrupted (69)', 'Strained (55)']
vals_sfs = [78, 69, 55]
colors_sfs = ['#2ecc71', '#e74c3c', '#f39c12']
axes[1].pie(vals_sfs, labels=labels_sfs, colors=colors_sfs, autopct='%1.1f%%', startangle=90)
axes[1].set_title('Supply Flow Status')

# Last-Mile Delivery Status
labels_lm = ['On Track (64)', 'Delayed (73)', 'Other (65)']
vals_lm = [64, 73, 65]
colors_lm = ['#2ecc71', '#e74c3c', '#3498db']
axes[2].pie(vals_lm, labels=labels_lm, colors=colors_lm, autopct='%1.1f%%', startangle=90)
axes[2].set_title('Last-Mile Delivery Status')

plt.tight_layout()
plt.savefig('/work/fig2_operational_status.png', dpi=150)
plt.close()

# Figure 3: Cost breakdown and financial metrics for Level 5
fig, ax = plt.subplots(figsize=(10, 6))
costs = ['Operational\nCosts', 'Transport\nCosts', 'Storage\nCosts', 'Personnel\nCosts']
avg_costs = [488103, 524621, 255483, 547049]
bars = ax.bar(costs, avg_costs, color=['#1abc9c','#3498db','#9b59b6','#e67e22'], alpha=0.8)
ax.set_ylabel('Average USD')
ax.set_title('Average Cost Breakdown for Level 5 Events')
for bar in bars:
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5000, f'${bar.get_height():,.0f}',
            ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('/work/fig3_cost_breakdown.png', dpi=150)
plt.close()

# Figure 4: Emergency Level vs Duration for Level 5
fig, ax = plt.subplots(figsize=(8, 5))
levels = ['Black', 'Orange', 'Red', 'Yellow']
durations = [217, 197, 183, 161]
counts = [51, 63, 45, 43]
bars = ax.bar(levels, durations, color=['#2c3e50','#e67e22','#e74c3c','#f1c40f'], alpha=0.8)
ax.set_ylabel('Average Estimated Duration (days)')
ax.set_title('Average Operation Duration by Emergency Level\n(Level 5 Disasters)')
for i, (bar, c) in enumerate(zip(bars, counts)):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+3, f'{durations[i]} days\n(n={c})',
            ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('/work/fig4_emergency_duration.png', dpi=150)
plt.close()

print("All figures created successfully")