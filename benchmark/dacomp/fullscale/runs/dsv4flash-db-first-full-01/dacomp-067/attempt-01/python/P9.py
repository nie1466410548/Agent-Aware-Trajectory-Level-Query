import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

os.makedirs('/work', exist_ok=True)

# ========== FIGURE 6: Interview Process Efficiency ==========
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

# Status distribution overall
status_labels = ['Cancelled', 'Completed', 'Scheduled', 'No-show']
status_counts = [3823, 3662, 3658, 3482]
colors_status = ['#f44336', '#4CAF50', '#2196F3', '#FF9800']

ax1 = axes[0]
wedges, texts, autotexts = ax1.pie(status_counts, labels=status_labels, autopct='%1.1f%%',
                                    colors=colors_status, startangle=90,
                                    explode=(0.03, 0.03, 0.03, 0.03))
ax1.set_title('Interview Execution Status', fontweight='bold', fontsize=14)
for t in autotexts:
    t.set_fontsize(11)
    t.set_fontweight('bold')

# Scorecard submission
ax2 = axes[1]
sub_labels = ['Scorecards\nSubmitted', 'Scorecards\nMissing']
sub_counts = [7248, 14625-7248]
colors_sub = ['#4CAF50', '#f44336']
wedges2, texts2, autotexts2 = ax2.pie(sub_counts, labels=sub_labels, autopct='%1.1f%%',
                                       colors=colors_sub, startangle=90,
                                       explode=(0.05, 0))
ax2.set_title('Scorecard Submission Rate (49.6%)', fontweight='bold', fontsize=14)
for t in autotexts2:
    t.set_fontsize(11)
    t.set_fontweight('bold')

plt.tight_layout()
plt.savefig('/work/interview_efficiency.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved: interview_efficiency.png")

# ========== FIGURE 7: Stage Retention by Channel ==========
fig, ax = plt.subplots(figsize=(10, 6))

stages = ['Application\nReview', 'Phone\nScreen', 'Technical\nInterview', 'Panel\nInterview', 'Final\nInterview', 'Offer']
x = np.arange(len(stages))

# Overall retention (hired+active as % of total at each stage)
retention = [48.74, 50.75, 48.70, 49.05, 50.28, 51.01]

bars = ax.bar(x, retention, color='#2196F3', edgecolor='gray', width=0.6)
for bar, val in zip(bars, retention):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3, 
            f'{val:.1f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('Pipeline Stage Retention Rate (hired + active)', fontweight='bold', fontsize=14)
ax.set_ylabel('Retention Rate (%)')
ax.set_xticks(x)
ax.set_xticklabels(stages)
ax.axhline(y=50, color='red', linestyle='--', alpha=0.6, label='50% benchmark')
ax.legend()
ax.set_ylim(0, 60)

plt.tight_layout()
plt.savefig('/work/stage_retention.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 7 saved: stage_retention.png")

# ========== FIGURE 8: Quality vs Cost tradeoff ==========
fig, ax = plt.subplots(figsize=(10, 7))

channels_clean = ['LinkedIn', 'Indeed', 'Emp.\nReferral', 'Univ.\nRecruiting', 
                  'Headhunter', 'Website', 'Glassdoor', 'AngelList']
hire_rates = [23.4, 20.2, 16.3, 28.3, 25.1, 28.5, 27.6, 15.9]
cost_per_hire = [350, 300, 2500, 4000, 12000, 150, 250, 200]
process_days = [18.8, 22.3, 18.4, 41.7, 22.0, 43.5, 36.1, 42.5]

# Bubble chart: x=cost, y=hire rate, size=hires
hires = [197, 545, 404, 693, 647, 280, 259, 284]
colors_bubble = plt.cm.viridis(np.linspace(0.2, 0.9, len(channels_clean)))

sc = ax.scatter(cost_per_hire, hire_rates, s=[h*2 for h in hires], 
                c=colors_bubble, alpha=0.6, edgecolors='black', linewidth=1)

for i, ch in enumerate(channels_clean):
    ax.annotate(ch, (cost_per_hire[i], hire_rates[i]), 
                textcoords="offset points", xytext=(8, 8), fontsize=9,
                fontweight='bold')

# Highlight optimal quadrant (low cost, high quality)
ax.axvspan(0, 500, alpha=0.1, color='green')
ax.axhspan(24, 30, alpha=0.1, color='blue')

ax.set_xlabel('Estimated Cost per Hire ($)', fontweight='bold')
ax.set_ylabel('Hire Rate (%)', fontweight='bold')
ax.set_title('Channel Quality vs Cost Trade-off\n(Bubble size = total hires)', fontweight='bold', fontsize=14)
ax.set_xscale('log')
ax.axhline(y=24.4, color='red', linestyle='--', alpha=0.6, label='Overall avg hire rate (24.4%)')
ax.legend(loc='lower right')

# Annotate the optimal zone
ax.text(150, 29.5, 'SWEET SPOT:\nLow cost + High quality', fontsize=10, 
        fontweight='bold', color='green',
        bbox=dict(boxstyle='round', facecolor='#ccffcc', alpha=0.8))

plt.tight_layout()
plt.savefig('/work/cost_quality_tradeoff.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 8 saved: cost_quality_tradeoff.png")

print("\n=== ALL FIGURES SAVED ===")