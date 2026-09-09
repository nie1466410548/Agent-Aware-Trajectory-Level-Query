import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/work/owner_classification_v3.csv')

# Set style
sns.set_style('whitegrid')
plt.rcParams.update({'font.size': 11})

# 1. Histogram of composite scores with classification color overlay
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# a) Composite distribution
ax = axes[0,0]
colors = {'Excellent': '#2ecc71', 'Good': '#3498db', 'Needs Improvement': '#e74c3c'}
for cls in ['Needs Improvement', 'Good', 'Excellent']:
    subset = df[df['classification']==cls]
    ax.hist(subset['composite'], bins=30, alpha=0.7, color=colors[cls], label=cls, density=True)
ax.set_xlabel('Composite Score')
ax.set_ylabel('Density')
ax.set_title('Composite Score Distribution by Classification')
ax.legend()

# b) Composite by task type
ax = axes[0,1]
sns.boxplot(data=df, x='task_type', y='composite', palette='Set2', ax=ax)
ax.set_xlabel('Task Type')
ax.set_ylabel('Composite Score')
ax.set_title('Composite Score by Task Type')

# c) Classification proportion by type
ax = axes[1,0]
ct = pd.crosstab(df['task_type'], df['classification'], normalize='index')
ct.plot(kind='bar', stacked=True, color=[colors['Needs Improvement'], colors['Good'], colors['Excellent']], ax=ax)
ax.set_xlabel('Task Type')
ax.set_ylabel('Proportion')
ax.set_title('Classification Proportion by Task Type')
ax.legend(loc='upper right')
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# d) Radar chart of sub-metrics by class
ax = axes[1,1]
metrics_labels = ['Completion\nRate', 'On-Time\nRate', 'Quality\n(0-1)', 'Priority\nWeighted', 'Hours\nEfficiency', 'Rework\nAvoidance']
metrics_keys = ['completion_rate','on_time_rate','quality_norm','priority_weighted_completion','hours_efficiency','rework_avoidance']
class_means = df.groupby('classification')[metrics_keys].mean()

angles = np.linspace(0, 2*np.pi, len(metrics_labels), endpoint=False).tolist()
angles += angles[:1]
for cls, color in [('Needs Improvement','#e74c3c'), ('Good','#3498db'), ('Excellent','#2ecc71')]:
    values = class_means.loc[cls].tolist()
    values += values[:1]
    ax.plot(angles, values, 'o-', color=color, label=cls, linewidth=2)
    ax.fill(angles, values, alpha=0.1, color=color)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(metrics_labels, fontsize=9)
ax.set_ylim(0, 1.1)
ax.set_title('Performance Sub-Metrics by Class')
ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('/work/evaluation_plan.png', dpi=150)
print("Saved figure: evaluation_plan.png")