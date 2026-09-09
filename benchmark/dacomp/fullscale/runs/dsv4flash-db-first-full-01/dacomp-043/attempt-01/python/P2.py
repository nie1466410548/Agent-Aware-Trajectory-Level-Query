import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# 1. Complication Severity Distribution
severity = ['Mild', 'Moderate', 'Severe']
deceased_sev = [7, 13, 7]  # n=27
recovered_sev = [71, 46, 18]  # n=135
deceased_sev_pct = [s/27*100 for s in deceased_sev]
recovered_sev_pct = [s/135*100 for s in recovered_sev]
x = np.arange(len(severity))
width = 0.35
ax1 = axes[0]
bars1 = ax1.bar(x - width/2, deceased_sev_pct, width, label='Deceased (n=27)', color='#d62728')
bars2 = ax1.bar(x + width/2, recovered_sev_pct, width, label='Recovered (n=135)', color='#2ca02c')
ax1.set_ylabel('Percentage (%)')
ax1.set_title('Complication Severity Grading')
ax1.set_xticks(x)
ax1.set_xticklabels(severity)
ax1.legend()
ax1.set_ylim(0, 60)
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 2. Complication Types in Complication Management
comp_types = ['Pneumonia', 'Encephalitis', 'Hepatitis']
deceased_ct = [11, 9, 7]
recovered_ct = [13, 42, 80]
deceased_ct_pct = [c/27*100 for c in deceased_ct]
recovered_ct_pct = [c/135*100 for c in recovered_ct]
ax2 = axes[1]
bars1 = ax2.bar(x - width/2, deceased_ct_pct, width, label='Deceased', color='#d62728')
bars2 = ax2.bar(x + width/2, recovered_ct_pct, width, label='Recovered', color='#2ca02c')
ax2.set_ylabel('Percentage (%)')
ax2.set_title('Complication Types (Complication Mgmt)')
ax2.set_xticks(x)
ax2.set_xticklabels(comp_types)
ax2.legend()
ax2.set_ylim(0, 70)
for bar in bars1:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

# 3. Past Medical History
past_med = ['None', 'J01 (Respiratory)', 'B20 (HIV)']
deceased_pm = [19, 22, 15]
recovered_pm = [75, 25, 55]
deceased_pm_pct = [p/56*100 for p in deceased_pm]
recovered_pm_pct = [p/155*100 for p in recovered_pm]
ax3 = axes[2]
bars1 = ax3.bar(x - width/2, deceased_pm_pct, width, label='Deceased', color='#d62728')
bars2 = ax3.bar(x + width/2, recovered_pm_pct, width, label='Recovered', color='#2ca02c')
ax3.set_ylabel('Percentage of cases (%)')
ax3.set_title('Past Medical History')
ax3.set_xticks(x)
ax3.set_xticklabels(['None', 'J01', 'B20'], fontsize=9)
ax3.legend()
ax3.set_ylim(0, 70)
for bar in bars1:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)
for bar in bars2:
    ax3.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1, f'{bar.get_height():.0f}%', ha='center', fontsize=8)

plt.suptitle('HFMD: Deceased vs Recovered — Complication Management & Medical History', fontsize=16, fontweight='bold')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/work/figure3_complication_history.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 created.")