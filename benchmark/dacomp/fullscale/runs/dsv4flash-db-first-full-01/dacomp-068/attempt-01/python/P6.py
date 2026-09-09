import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load saved data
merged = pd.read_pickle('/work/final_allocation.pkl')
geo = pd.read_pickle('/work/geo_seg.pkl')

# Set up a nice style
plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})

# --- Figure 1: Scatter plot of markets by conversion rate vs avg_daily_revenue ---
fig, ax = plt.subplots(figsize=(10, 7))

colors = {'A': '#e74c3c', 'B': '#3498db', 'none': '#95a5a6'}
labels = {'A': 'Segment A: High Conv ($>15%), Low Rev (<$5)',
          'B': 'Segment B: High Rev ($>7$), Low Conv (<10%)',
          'none': 'Other Markets'}

for seg in ['A', 'B', 'none']:
    subset = geo[geo['segment'] == seg]
    ax.scatter(subset['avg_daily_revenue'], subset['store_conversion_rate'], 
               c=colors[seg], s=subset['store_visitors_30d']/50000, alpha=0.7,
               label=labels[seg], edgecolors='black', linewidth=0.5)

# Annotate points
for _, row in geo.iterrows():
    label = f"{row['package_name'].split('.')[-1]}-{row['country']}"
    ax.annotate(label, (row['avg_daily_revenue'], row['store_conversion_rate']),
                fontsize=8, ha='center', va='bottom', xytext=(0, 5), 
                textcoords='offset points', rotation=45)

# Threshold lines
ax.axhline(y=15, color='red', linestyle='--', alpha=0.5, label='Conversion = 15%')
ax.axvline(x=5, color='red', linestyle='--', alpha=0.5, label='Revenue = $5')
ax.axvline(x=7, color='blue', linestyle='--', alpha=0.5, label='Revenue = $7')
ax.axhline(y=10, color='blue', linestyle='--', alpha=0.5, label='Conversion = 10%')

ax.set_xlabel('Average Daily Revenue ($)')
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

apps = merged['package_name'].str.replace('com.', '').str.replace('.', '.')
budgets = merged['allocated_budget'] / 1_000_000  # in millions

bars = ax.barh(apps, budgets, color=['#2ecc71' if s > 0 else '#e74c3c' for s in merged['segA_markets'] + merged['segB_markets']], 
               edgecolor='black', linewidth=0.5)

# Add value labels
for bar, val in zip(bars, budgets):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
            f'${val:.2f}M', ha='left', va='center', fontsize=10)

# Color segments
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#2ecc71', label='Flagged Markets (Seg A or B)'),
                   Patch(facecolor='#3498db', label='No Flagged Markets')]
actual_colors = ['#2ecc71' if s > 0 else '#3498db' for s in merged['segA_markets'] + merged['segB_markets']]
for i, (bar, c) in enumerate(zip(bars, actual_colors)):
    bar.set_color(c)

ax.legend(handles=[
    Patch(facecolor='#2ecc71', label='Has Flagged Markets (Seg A or B)'),
    Patch(facecolor='#3498db', label='No Flagged Markets')
], loc='lower right')

ax.set_xlabel('Budget Allocation ($ Millions)')
ax.set_title('Q4 2025 Marketing Budget Allocation per App ($5M Total)')
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

# 25% line
ax.axvline(x=25, color='red', linestyle='--', linewidth=2, label='Required ROI = 25%')

for bar, val in zip(bars, rois):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2, 
            f'{val:.1f}%', ha='left', va='center', fontsize=10)

ax.set_xlabel('Expected ROI (%)')
ax.set_title('Expected ROI per App\n(Portfolio Weighted Average: {:.1f}%)'.format(
    (merged['expected_inc_rev'].sum() - 5_000_000)/5_000_000*100))
ax.legend()
ax.invert_yaxis()
ax.grid(True, alpha=0.3, axis='x')
plt.tight_layout()
plt.savefig('/work/fig3_expected_roi.png', dpi=150)
plt.close()
print("Saved fig3_expected_roi.png")

# --- Figure 4: Detailed market breakdown per app ---
fig, axes = plt.subplots(2, 4, figsize=(16, 10))
axes = axes.flatten()

for i, app in enumerate(merged['package_name']):
    ax = axes[i]
    app_geo = geo[geo['package_name'] == app]
    
    conv = app_geo['store_conversion_rate'].values
    rev = app_geo['avg_daily_revenue'].values
    countries = app_geo['country'].values
    seg = app_geo['segment'].values
    
    bar_colors = ['#e74c3c' if s == 'A' else '#3498db' if s == 'B' else '#95a5a6' for s in seg]
    
    x = np.arange(len(countries))
    bar_width = 0.35
    
    ax.bar(x - bar_width/2, conv, bar_width, color=bar_colors, alpha=0.8, label='Conv Rate (%)')
    ax_twin = ax.twinx()
    ax_twin.bar(x + bar_width/2, rev, bar_width, color='#f39c12', alpha=0.8, label='Avg Daily Rev ($)')
    
    ax.set_xticks(x)
    ax.set_xticklabels(countries)
    ax.set_title(f"{app.split('.')[-1]}", fontsize=11)
    ax.set_ylabel('Conv Rate (%)', color='steelblue')
    ax_twin.set_ylabel('Daily Rev ($)', color='#f39c12')
    
    # Threshold lines
    if any(s == 'A' for s in seg):
        ax.axhline(y=15, color='red', linestyle=':', alpha=0.5)
    if any(s == 'B' for s in seg):
        ax_twin.axhline(y=7, color='blue', linestyle=':', alpha=0.5)

plt.suptitle('Per-App Market Breakdown: Conversion Rate and Daily Revenue', fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('/work/fig4_per_app_markets.png', dpi=150)
plt.close()
print("Saved fig4_per_app_markets.png")

print("\nAll figures saved.")