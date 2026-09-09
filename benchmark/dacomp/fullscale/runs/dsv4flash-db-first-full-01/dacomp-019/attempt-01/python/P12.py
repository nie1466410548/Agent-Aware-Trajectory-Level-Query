import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('priority_scores.csv')

# Figure 4: Heatmap of risk dimensions for top 15 drugs
top15 = df.nlargest(15, 'priority_score')
risk_cols = ['backlog_score', 'supply_interrupt_score', 'quality_risk_score', 'priority_score']
fig, ax = plt.subplots(figsize=(10, 7))
# Normalize for heatmap
hm_data = top15[['drug_id'] + risk_cols].set_index('drug_id')
sns.heatmap(hm_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Score (0-100)'})
ax.set_title('Risk profile of top 15 priority drugs (Imported/JV)', fontsize=12)
plt.tight_layout()
plt.savefig('figure4_heatmap.png', dpi=110)
plt.close()

# Figure 5: Distribution of priority scores
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
for idx, o in enumerate(['Imported', 'Joint-venture']):
    d = df[df['origin'] == o]['priority_score']
    axes[idx].hist(d, bins=15, alpha=0.7, edgecolor='black', color=['#d62728','#1f77b4'][idx])
    axes[idx].axvline(d.median(), color='red', ls='--', label=f'Median={d.median():.1f}')
    axes[idx].set_title(f'{o} drugs (n={len(d)})')
    axes[idx].set_xlabel('Priority score')
    axes[idx].set_ylabel('Count')
    axes[idx].legend()
plt.suptitle('Distribution of priority supervision scores', fontsize=13)
plt.tight_layout()
plt.savefig('figure5_distribution.png', dpi=110)
plt.close()

# Figure 6: Key risk indicators comparison
fig, ax = plt.subplots(figsize=(10, 5))
indicators = ['% Frozen/Scrapped', '% Zero Qualified', '% GSP Not Certified', 
              '% Refrigerated', '% Cold-Chain', '% Abnormal Price']
imported_vals = [64.0, 3.2, 48.0, 34.4, 49.6, 54.0]
jv_vals = [67.6, 7.9, 42.4, 32.4, 48.2, 48.2]

x = np.arange(len(indicators))
w = 0.35
ax.bar(x - w/2, imported_vals, w, label='Imported', color='#d62728', alpha=0.8)
ax.bar(x + w/2, jv_vals, w, label='Joint-venture', color='#1f77b4', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(indicators, rotation=20, ha='right')
ax.set_ylabel('Percentage (%)')
ax.set_title('Key risk indicator comparison: Imported vs Joint-venture drugs')
ax.legend()
for i, v in enumerate(imported_vals):
    ax.text(i - w/2, v + 1, f'{v:.0f}%', ha='center', fontsize=8)
for i, v in enumerate(jv_vals):
    ax.text(i + w/2, v + 1, f'{v:.0f}%', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig('figure6_indicators.png', dpi=110)
plt.close()

print("All figures saved.")