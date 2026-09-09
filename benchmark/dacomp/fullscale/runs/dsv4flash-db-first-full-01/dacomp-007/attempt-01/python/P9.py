import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)
df = df.drop_duplicates(subset='EmpID', keep='first')

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 10)

# 2. Job role composition and attrition - horizontal bar chart
fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Role composition within each department
role_counts = df.groupby(['Department','JobRole']).size().unstack(fill_value=0)
role_pct = role_counts.div(role_counts.sum(axis=1), axis=0)*100
role_pct_sorted = role_pct.T.sort_values('Research & Development', ascending=True)
role_pct.T.plot(kind='barh', stacked=True, ax=axes[0], colormap='Set2', edgecolor='black')
axes[0].set_xlabel('Number of Employees')
axes[0].set_title('Job Role Distribution by Department', fontsize=13, fontweight='bold')
axes[0].legend(title='Department', bbox_to_anchor=(1.0, 1.0))

# Attrition rate by job role with color by department
role_att = df.groupby('JobRole').agg(
    n=('EmpID','count'),
    att_rate=('is_attrition','mean')
).sort_values('att_rate')
role_att['att_rate'] *= 100

# Get department for each role
role_dept = df.groupby('JobRole')['Department'].agg(lambda x: x.mode().iloc[0] if len(x.mode())>0 else x.iloc[0])
dept_colors = {'Human Resources': '#e74c3c', 'Research & Development': '#2ecc71', 'Sales': '#3498db'}
bar_colors = [dept_colors.get(role_dept[r], '#95a5a6') for r in role_att.index]

bars = axes[1].barh(role_att.index, role_att['att_rate'], color=bar_colors, edgecolor='black')
for i, (idx, row) in enumerate(role_att.iterrows()):
    axes[1].text(row['att_rate']+0.5, i, f"{row['att_rate']:.1f}%", va='center', fontsize=9)
axes[1].set_xlabel('Attrition Rate (%)')
axes[1].set_title('Attrition Rate by Job Role', fontsize=13, fontweight='bold')

# Add legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor=dept_colors[d], label=d) for d in dept_colors]
axes[1].legend(handles=legend_elements, title='Department')

plt.tight_layout()
plt.savefig('/work/role_analysis.png', dpi=150, bbox_inches='tight')
print("Saved role_analysis.png")

# 3. Income comparison
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Monthly income by job level and department
income_plot = df.groupby(['Department','JobLevel'])['MonthlyIncome'].mean().unstack()
income_plot.T.plot(kind='bar', ax=axes[0], colormap='Set2', edgecolor='black')
axes[0].set_ylabel('Average Monthly Income ($)')
axes[0].set_title('Average Monthly Income by Job Level', fontsize=13, fontweight='bold')
axes[0].legend(title='Department')
axes[0].set_xlabel('Job Level')

# Monthly income by department and role
income_role = df.groupby(['Department','JobRole'])['MonthlyIncome'].mean().unstack()
income_role.T.plot(kind='bar', ax=axes[1], colormap='Set2', edgecolor='black')
axes[1].set_ylabel('Average Monthly Income ($)')
axes[1].set_title('Average Monthly Income by Job Role', fontsize=13, fontweight='bold')
axes[1].legend(title='Department')
axes[1].set_xlabel('')

plt.tight_layout()
plt.savefig('/work/income_analysis.png', dpi=150, bbox_inches='tight')
print("Saved income_analysis.png")