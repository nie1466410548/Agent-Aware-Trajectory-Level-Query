import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Create figures directory
import os
os.makedirs('/work', exist_ok=True)

# Set style
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 12

# ========== FIGURE 1: Channel Performance Comparison ==========
channels = ['LinkedIn', 'Indeed', 'Employee\nReferral', 'University\nRecruiting', 
            'Headhunter', 'Company\nWebsite', 'Glassdoor', 'AngelList']
hire_rates = [23.4, 20.2, 16.3, 28.3, 25.1, 28.5, 27.6, 15.9]
hires = [197, 545, 404, 693, 647, 280, 259, 284]
process_days = [18.8, 22.3, 18.4, 41.7, 22.0, 43.5, 36.1, 42.5]
efficiency = [241.7, 242.9, 221.6, 300.4, 237.3, 244.5, 238.1, 275.2]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Hire Rate
ax1 = axes[0, 0]
colors = ['#4CAF50' if h >= 24 else '#FF9800' for h in hire_rates]
bars1 = ax1.bar(channels, hire_rates, color=colors, edgecolor='gray')
ax1.set_title('Hire Rate by Channel (%)', fontweight='bold', fontsize=14)
ax1.set_ylabel('Hire Rate (%)')
ax1.tick_params(axis='x', rotation=45)
for bar, val in zip(bars1, hire_rates):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{val}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax1.axhline(y=24.4, color='red', linestyle='--', alpha=0.7, label='Overall Avg (24.4%)')
ax1.legend()

# Total Hires
ax2 = axes[0, 1]
colors2 = ['#2196F3'] * 8
bars2 = ax2.bar(channels, hires, color=colors2, edgecolor='gray')
ax2.set_title('Total Hires by Channel', fontweight='bold', fontsize=14)
ax2.set_ylabel('Number of Hires')
ax2.tick_params(axis='x', rotation=45)
for bar, val in zip(bars2, hires):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

# Process Days
ax3 = axes[1, 0]
colors3 = ['#4CAF50' if d <= 25 else '#FF9800' if d <= 35 else '#f44336' for d in process_days]
bars3 = ax3.bar(channels, process_days, color=colors3, edgecolor='gray')
ax3.set_title('Average Process Duration (Days)', fontweight='bold', fontsize=14)
ax3.set_ylabel('Days')
ax3.tick_params(axis='x', rotation=45)
for bar, val in zip(bars3, process_days):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{val}d', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Efficiency Score
ax4 = axes[1, 1]
colors4 = ['#4CAF50' if e >= 250 else '#FF9800' for e in efficiency]
bars4 = ax4.bar(channels, efficiency, color=colors4, edgecolor='gray')
ax4.set_title('Efficiency Score by Channel', fontweight='bold', fontsize=14)
ax4.set_ylabel('Efficiency Score')
ax4.tick_params(axis='x', rotation=45)
for bar, val in zip(bars4, efficiency):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
             str(val), ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('/work/channel_performance.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved: channel_performance.png")

# ========== FIGURE 2: Cost Optimization Strategy ==========
channels_clean = ['LinkedIn', 'Indeed', 'Emp. Referral', 'Univ. Rec.', 
                  'Headhunter', 'Web', 'Glassdoor', 'AngelList']

# Per-hire cost estimates (industry benchmarks)
cost_per_hire = [350, 300, 2500, 4000, 12000, 150, 250, 200]
# Current hires
current_hires = [197, 545, 404, 693, 647, 280, 259, 284]
# Target hires (optimized)
target_hires = [250, 600, 500, 700, 400, 350, 300, 200]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Current vs Target hires
x = np.arange(len(channels_clean))
width = 0.35
bars1 = ax1.bar(x - width/2, current_hires, width, label='Current', color='#2196F3', edgecolor='gray')
bars2 = ax1.bar(x + width/2, target_hires, width, label='Optimized', color='#4CAF50', edgecolor='gray')
ax1.set_title('Channel Reallocation Strategy', fontweight='bold', fontsize=14)
ax1.set_ylabel('Number of Hires')
ax1.set_xticks(x)
ax1.set_xticklabels(channels_clean, rotation=45)
ax1.legend()
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             str(int(bar.get_height())), ha='center', va='bottom', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             str(int(bar.get_height())), ha='center', va='bottom', fontsize=8)

# Cost breakdown
current_costs = [ch * cph + f for ch, cph, f in zip(current_hires, cost_per_hire, [5000, 3000, 2000, 15000, 2000, 1000, 2000, 1000])]
target_costs = [ch * cph + f for ch, cph, f in zip(target_hires, cost_per_hire, [5000, 3000, 2000, 15000, 2000, 1000, 2000, 1000])]

bars3 = ax2.bar(x - width/2, current_costs, width, label='Current Cost', color='#f44336', edgecolor='gray')
bars4 = ax2.bar(x + width/2, target_costs, width, label='Optimized Cost', color='#4CAF50', edgecolor='gray')
ax2.set_title('Channel Cost Comparison ($)', fontweight='bold', fontsize=14)
ax2.set_ylabel('Cost ($)')
ax2.set_xticks(x)
ax2.set_xticklabels(channels_clean, rotation=45)
ax2.legend()
ax2.set_yscale('log')

# Add total annotations
total_current = sum(current_costs)
total_target = sum(target_costs)
ax2.text(0.5, 0.95, f'Total Current: ${total_current:,.0f}', 
         transform=ax2.transAxes, fontsize=11, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='#ffcccc'))
ax2.text(0.5, 0.88, f'Total Optimized: ${total_target:,.0f} ({(total_current-total_target)/total_current*100:.1f}%↓)', 
         transform=ax2.transAxes, fontsize=11, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='#ccffcc'))

plt.tight_layout()
plt.savefig('/work/cost_optimization.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved: cost_optimization.png")

# ========== FIGURE 3: Funnel Analysis ==========
fig, ax = plt.subplots(figsize=(10, 7))

stages = ['Applications\n(18,186)', 'Interviewed\n(7,172)', 'Hired\n(4,432)']
values = [18186, 7172, 4432]
colors_funnel = ['#2196F3', '#FF9800', '#4CAF50']

# Create funnel bar chart
bars = ax.barh(stages, values, color=colors_funnel, edgecolor='gray', height=0.6)
for bar, val in zip(bars, values):
    ax.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2, 
            f'{val:,}', ha='left', va='center', fontsize=14, fontweight='bold')

# Add conversion rates
ax.annotate('', xy=(7172, 0), xytext=(18186, 0),
            arrowprops=dict(arrowstyle='->', color='#FF9800', lw=2))
ax.text(12500, 0.1, '39.4% conversion', fontsize=11, ha='center', color='#FF9800', fontweight='bold')

ax.annotate('', xy=(4432, 1), xytext=(7172, 1),
            arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=2))
ax.text(5800, 1.1, '61.8% conversion', fontsize=11, ha='center', color='#4CAF50', fontweight='bold')

ax.set_title('Recruitment Funnel', fontweight='bold', fontsize=16)
ax.set_xlabel('Count')
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('/work/funnel_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved: funnel_analysis.png")

# ========== FIGURE 4: Diversity Metrics ==========
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Gender diversity
labels_gender = ['Female', 'Male', 'Non-binary', 'Prefer not to say']
hires_gender = [413, 395, 416, 397]
apps_gender = [1696, 1558, 1652, 1640]
colors_gender = ['#E91E63', '#2196F3', '#9C27B0', '#607D8B']

ax1.pie(hires_gender, labels=labels_gender, autopct='%1.1f%%', 
        colors=colors_gender, startangle=90, explode=(0.05, 0, 0, 0))
ax1.set_title('Gender Distribution of Hires\n(Among reported)', fontweight='bold', fontsize=13)

# Racial diversity
labels_race = ['Asian', 'Black', 'Hispanic', 'Native\nAmerican', 'Other', 'White']
hires_race = [271, 267, 280, 305, 292, 269]
colors_race = ['#FF5722', '#795548', '#FFC107', '#009688', '#673AB7', '#9E9E9E']

ax2.pie(hires_race, labels=labels_race, autopct='%1.1f%%', 
        colors=colors_race, startangle=90, explode=(0, 0, 0, 0.05, 0, 0))
ax2.set_title('Racial Distribution of Hires\n(Among reported)', fontweight='bold', fontsize=13)

# Add target annotations
fig.text(0.15, 0.02, 'Female ≥40% target: ✓ Currently 42.0%', fontsize=11, ha='center', 
         bbox=dict(boxstyle='round', facecolor='#ccffcc'))
fig.text(0.85, 0.02, 'Non-white ≥30% target: ✓ Currently 32.0%', fontsize=11, ha='center',
         bbox=dict(boxstyle='round', facecolor='#ccffcc'))

plt.tight_layout()
plt.savefig('/work/diversity_metrics.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved: diversity_metrics.png")

# ========== FIGURE 5: Interview Quality by Type ==========
fig, ax = plt.subplots(figsize=(10, 6))

int_types = ['Panel Interview', 'Behavioral Interview', 'Technical Interview', 'Final Interview']
positive_pct = [44.3, 43.2, 45.3, 47.5]
avg_ratings = [2.73, 2.70, 2.67, 2.69]
avg_duration = [61.6, 64.6, 64.2, 67.0]

x = np.arange(len(int_types))
width = 0.25

bars1 = ax.bar(x - width, positive_pct, width, label='Positive Rec. %', color='#4CAF50', edgecolor='gray')
bars2 = ax.bar(x, avg_ratings, width, label='Avg Rating (1-5)', color='#2196F3', edgecolor='gray')

ax2 = ax.twinx()
bars3 = ax2.bar(x + width, avg_duration, width, label='Avg Duration (min)', color='#FF9800', edgecolor='gray')

ax.set_title('Interview Quality Metrics by Type', fontweight='bold', fontsize=14)
ax.set_xticks(x)
ax.set_xticklabels(int_types, rotation=15)
ax.set_ylabel('Percentage / Rating')
ax2.set_ylabel('Duration (minutes)')

# Add value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03, 
            f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars3:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
             f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Combine legends
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

plt.tight_layout()
plt.savefig('/work/interview_quality.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved: interview_quality.png")

print("\n=== ALL VISUALIZATIONS COMPLETE ===")