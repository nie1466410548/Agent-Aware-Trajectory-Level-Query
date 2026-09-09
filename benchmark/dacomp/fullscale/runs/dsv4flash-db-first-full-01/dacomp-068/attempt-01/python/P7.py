import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load saved data
merged = pd.read_pickle('/work/final_allocation.pkl')
geo = pd.read_pickle('/work/geo_seg.pkl')

plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})

# --- Figure 1: Scatter plot ---
fig, ax = plt.subplots(figsize=(10, 7))

colors = {'A': '#e74c3c', 'B': '#3498db', 'none': '#95a5a6'}
labels = {'A': 'Seg A: High Conv (>15%), Low Rev (<$5)',
          'B': 'Seg B: High Rev (>$7), Low Conv (<10%)',
          'none': 'Other Markets'}

for seg in ['A', 'B', 'none']:
    subset = geo[geo['segment'] == seg]
    c = colors[seg]
    ax.scatter(subset['avg_daily_revenue'], subset['store_conversion_rate'], 
               c=[c]*len(subset), s=subset['store_visitors_30d']/50000, alpha=0.7,
               label=labels[seg], edgecolors='black', linewidth=0.5)

for _, row in geo.iterrows():
    label = f"{row['package_name'].split('.')[-1]}-{row['country']}"
    ax.annotate(label, (row['avg_daily_revenue'], row['store_conversion_rate']),
                fontsize=8, ha='center', va='bottom', xytext=(0, 5), 
                textcoords='offset points', rotation=45)

ax.axhline(y=15, color='red', linestyle='--', alpha=0.5, label='Conv = 15%')
ax.axvline(x=5, color='red', linestyle='--', alpha=0.5, label='Rev = $5')
ax.axvline(x=7, color='blue', linestyle='--', alpha=0.5, label='Rev = $7')
ax.axhline(y=10, color='blue', linestyle='--', alpha=0.5, label='Conv = 10%')

ax.set_xlabel('Average Daily Revenue (USD)')
ax.set_ylabel('Store Conversion Rate (%)')
ax.set_title('Market Segmentation: Conversion Rate vs. Daily Revenue\n(Bubble size = Store Visitors)')
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('/work/fig1_market_segmentation.png', dpi=150)
plt.close()
print("Saved fig1_market_segmentation.png")

# --- Figure 2: Budget allocation bar chart ---
fig, ax = plt.subplots(figsize=(12, 6))

apps = [n.split('.')[-1] for n in merged['package_name']]
budgets = merged['allocated_budget'] / 1_000_000

has_flag = (merged['segA_markets'] + merged['segB_markets']).clip(upper=1)
bar_colors = ['#2ecc71' if s else '#3498db' for s in has_flag]

bars = ax.barh(apps, budgets, color=bar_colors, edgecolor='black', linewidth=0.5)

for bar, val in zip(bars, budgets):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
            f'${val:.2f}M', ha='left', va='center', fontsize=10)

from matplotlib.patches import Patch
ax.legend(handles=[
    Patch(facecolor='#2ecc71', label='Has Flagged Markets (Seg A or B)'),
    Patch(facecolor='#3498db', label='No Flagged Markets')
], loc='lower right')

ax.set_xlabel('Budget Allocation (USD Millions)')
ax.set_title('Q4 2025 Marketing Budget Allocation per App ($5M Total)')
ax.set_xlim(0, max(budgets) * 1.35)
ax.invert_yaxis()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('/work/fig2_budget_allocation.png', dpi=150)
plt.close()
print("Saved fig2_budget_allocation.png")

# --- Figure 3: Expected ROI per app ---
fig, ax = plt.subplots(figsize=(12, 6))

rois = merged['expected_roi']
colors_roi = ['#27ae60' if r >= 25 else '#e67e22' for r in rois]

bars = ax.barh(apps, rois, color=colors_roi, edgecolor='black', linewidth=0.5)

ax.axvline(x=25, color='red', linestyle='--', linewidth=2, label='Required ROI = 25%')

for bar, val in zip(bars, rois):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
            f'{val:.1f}%', ha='left', va='center', fontsize=10)

port_roi = (merged['expected_inc_rev'].sum() - 5_000_000) / 5_000_000 * 100
ax.set_xlabel('Expected ROI (%)')
ax.set_title(f'Expected ROI per App (Portfolio Average: {port_roi:.1f}%)')
ax.legend()
ax.set_xlim(0, max(rois) * 1.25)
ax.invert_yaxis()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('/work/fig3_expected_roi.png', dpi=150)
plt.close()
print("Saved fig3_expected_roi.png")

print("\nAll figures saved successfully.")