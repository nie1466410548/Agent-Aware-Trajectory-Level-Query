import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/final_classification.csv')

colors = {'Excellent': '#1a9850', 'Good': '#3288bd', 'Needs Improvement': '#d73027'}
cls_order = ['Excellent', 'Good', 'Needs Improvement']

sns.set_style('whitegrid')
plt.rcParams.update({'font.size': 11})

fig = plt.figure(figsize=(15, 11))

# 1. Composite distribution by class
ax = plt.subplot(2, 2, 1)
for cls in cls_order:
    subset = df[df['classification']==cls]
    ax.hist(subset['composite'], bins=35, alpha=0.65, color=colors[cls], label=f"{cls} (n={len(subset)})", density=True)
ax.set_xlabel('Composite Score (weighted, within-type percentile)')
ax.set_ylabel('Density')
ax.set_title('(a) Composite Score Distribution by Performance Class')
ax.legend(fontsize=9)

# 2. Composite by task type
ax = plt.subplot(2, 2, 2)
sns.boxplot(data=df, x='task_type', y='composite', hue='task_type', palette='Set2', legend=False, ax=ax)
ax.set_xlabel('Task Type')
ax.set_ylabel('Composite Score')
ax.set_title('(b) Composite Score by Task Type')

# 3. Classification proportions by type
ax = plt.subplot(2, 2, 3)
ct = pd.crosstab(df['task_type'], df['classification'])
ct = ct[cls_order]
ct_pct = ct.div(ct.sum(axis=1), axis=0)
ct_pct.plot(kind='bar', stacked=True, color=[colors[c] for c in cls_order], ax=ax)
ax.set_xlabel('Task Type')
ax.set_ylabel('Proportion of Owners')
ax.set_title('(c) Classification Mix by Task Type')
ax.legend(title='Classification', fontsize=9)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# 4. Radar chart of sub-metrics by class
ax = plt.subplot(2, 2, 4, polar=True)
metrics_keys = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
labels = ['Completion Rate','On-Time Rate','Quality (0-1)','Priority-Weighted Completion','Hours Efficiency','Rework Avoidance']
means = df.groupby('classification')[metrics_keys].mean()
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]
for cls in cls_order:
    vals = means.loc[cls].tolist()
    vals += vals[:1]
    ax.plot(angles, vals, 'o-', color=colors[cls], label=cls, linewidth=2)
    ax.fill(angles, vals, alpha=0.1, color=colors[cls])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=9)
ax.set_ylim(0, 1.1)
ax.set_title('(d) Average Sub-Metric Scores by Class', pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.1), fontsize=9)

plt.tight_layout()
plt.savefig('/work/final_evaluation_plan.png', dpi=150)
print("Saved final_evaluation_plan.png")