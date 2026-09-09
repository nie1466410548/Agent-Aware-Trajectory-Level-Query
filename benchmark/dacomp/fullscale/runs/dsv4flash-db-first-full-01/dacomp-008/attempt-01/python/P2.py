import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df = pd.read_csv('/work/project_data.csv')

# Set style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 8)

# 1. Box plot of deviation by Project Type
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Box plot
sns.boxplot(data=df, x='Project Type', y='deviation', ax=axes[0,0], palette='Set2')
axes[0,0].set_title('Cost Deviation by Project Type', fontsize=14)
axes[0,0].set_ylabel('Budget - Actual Cost')

# Violin plot
sns.violinplot(data=df, x='Project Type', y='deviation', ax=axes[0,1], palette='Set2', inner='quartile')
axes[0,1].set_title('Cost Deviation Distribution by Project Type', fontsize=14)
axes[0,1].set_ylabel('Budget - Actual Cost')

# Completed projects only - box plot
df_comp = df[df['status'] == 'Completed']
sns.boxplot(data=df_comp, x='Project Type', y='deviation', ax=axes[1,0], palette='Set2')
axes[1,0].set_title('Cost Deviation by Project Type (Completed Only)', fontsize=14)
axes[1,0].set_ylabel('Budget - Actual Cost')

# Deviation percentage by Project Type
sns.boxplot(data=df, x='Project Type', y='dev_pct', ax=axes[1,1], palette='Set2')
axes[1,1].set_title('Cost Deviation % by Project Type', fontsize=14)
axes[1,1].set_ylabel('Deviation % of Budget')

plt.tight_layout()
plt.savefig('/work/fig1_deviation_by_project_type.png', dpi=100)
plt.close()
print("fig1 saved")

# 2. Scatter plots
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Deviation vs Team Size
for i, ptype in enumerate(['Software Development', 'Infrastructure', 'Marketing Promotion']):
    ax = axes[0, i]
    subset = df[df['Project Type'] == ptype]
    sns.scatterplot(data=subset, x='team', y='deviation', hue='risk', style='status', 
                    alpha=0.7, ax=ax)
    ax.set_title(f'{ptype}', fontsize=12)
    ax.set_xlabel('Team Size')
    ax.set_ylabel('Cost Deviation')
    ax.legend(loc='best', fontsize=8)

# Deviation vs Customer Satisfaction
for i, ptype in enumerate(['Software Development', 'Infrastructure', 'Marketing Promotion']):
    ax = axes[1, i]
    subset = df[df['Project Type'] == ptype]
    sns.scatterplot(data=subset, x='sat', y='deviation', hue='risk', style='status',
                    alpha=0.7, ax=ax)
    ax.set_title(f'{ptype}', fontsize=12)
    ax.set_xlabel('Customer Satisfaction')
    ax.set_ylabel('Cost Deviation')
    ax.legend(loc='best', fontsize=8)

plt.tight_layout()
plt.savefig('/work/fig2_scatter_factors.png', dpi=100)
plt.close()
print("fig2 saved")

# 3. Completed projects scatter
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.scatterplot(data=df_comp, x='team', y='deviation', hue='Project Type', style='risk', alpha=0.8, ax=axes[0])
axes[0].set_title('Completed Projects: Deviation vs Team Size', fontsize=13)
axes[0].set_xlabel('Team Size')
axes[0].set_ylabel('Cost Deviation')

sns.scatterplot(data=df_comp, x='sat', y='deviation', hue='Project Type', style='risk', alpha=0.8, ax=axes[1])
axes[1].set_title('Completed Projects: Deviation vs Customer Satisfaction', fontsize=13)
axes[1].set_xlabel('Customer Satisfaction')
axes[1].set_ylabel('Cost Deviation')

plt.tight_layout()
plt.savefig('/work/fig3_completed_scatter.png', dpi=100)
plt.close()
print("fig3 saved")