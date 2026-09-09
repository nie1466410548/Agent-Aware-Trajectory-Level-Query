import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('priority_scores.csv')

# Figure 1: Boxplot of the three sub-scores + priority by origin
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
sub = df[['origin', 'backlog_score', 'supply_interrupt_score', 'quality_risk_score', 'priority_score']]
melted = sub.melt(id_vars='origin', var_name='score_type', value_name='score')
sns.boxplot(data=melted, x='score_type', y='score', hue='origin', ax=axes[0])
axes[0].set_title('Risk sub-scores by origin (Imported / Joint-venture)')
axes[0].tick_params(axis='x', rotation=15)

# Violin of priority by origin
sns.violinplot(data=df, x='origin', y='priority_score', ax=axes[1])
sns.stripplot(data=df, x='origin', y='priority_score', color='black', alpha=0.4, size=3, ax=axes[1])
axes[1].set_title('Overall priority score distribution by origin')
plt.tight_layout()
plt.savefig('figure1_scores_by_origin.png', dpi=110)
plt.close()

# Figure 2: Top 15 drugs by priority score (horizontal bar)
top15 = df.nlargest(15, 'priority_score')
fig, ax = plt.subplots(figsize=(9, 7))
colors = ['#d62728' if o == 'Imported' else '#1f77b4' for o in top15['origin']]
ax.barh(top15['drug_id'][::-1], top15['priority_score'][::-1], color=colors[::-1])
ax.set_xlabel('Priority score (0-100)')
ax.set_title('Top 15 Imported/JV drugs requiring prioritized supervision')
ax.legend(handles=[plt.Rectangle((0,0),1,1,color='#d62728', label='Imported'),
                   plt.Rectangle((0,0),1,1,color='#1f77b4', label='Joint-venture')])
plt.tight_layout()
plt.savefig('figure2_top15.png', dpi=110)
plt.close()

# Figure 3: Bubble scatter - backlog vs quality vs supply (bubble = priority)
fig, ax = plt.subplots(figsize=(10, 7))
for o, c in [('Imported', '#d62728'), ('Joint-venture', '#1f77b4')]:
    d = df[df['origin'] == o]
    sc = ax.scatter(d['backlog_score'], d['quality_risk_score'], s=d['supply_interrupt_score']*1.5,
                    c=c, alpha=0.55, edgecolors='white', label=o)
ax.set_xlabel('Inventory backlog score')
ax.set_ylabel('Quality risk score')
ax.set_title('Backlog vs Quality risk (bubble size = supply interruption risk)')
ax.legend()
plt.tight_layout()
plt.savefig('figure3_scatter.png', dpi=110)
plt.close()

print("Figures saved")
print(df.groupby('origin')[['backlog_score','supply_interrupt_score','quality_risk_score','priority_score']].mean().round(1))

# Priority tiers
df['tier'] = pd.cut(df['priority_score'], bins=[0, 40, 50, 60, 100], labels=['Low','Medium','High','Critical'])
print("\nTier distribution:")
print(df.groupby(['origin','tier']).size().unstack(fill_value=0))
