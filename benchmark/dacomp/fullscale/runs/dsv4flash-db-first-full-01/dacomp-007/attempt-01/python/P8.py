import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

result = db.query("SELECT * FROM sheet1")
df = db.frame(result)
df['is_attrition'] = (df['Attrition']=='Yes').astype(int)

# Deduplicate (keep first occurrence)
df = df.drop_duplicates(subset='EmpID', keep='first')
print(f"After dedup: {len(df)} rows")

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# 1. Overall attrition by department
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1a. Attrition rate by department
dept_att = df.groupby('Department')['is_attrition'].agg(['count','mean'])
dept_att['rate'] = dept_att['mean']*100
colors = ['#e74c3c' if r > 15 else '#2ecc71' if r < 15 else '#f39c12' for r in dept_att['rate']]
axes[0,0].bar(dept_att.index, dept_att['rate'], color=colors, edgecolor='black')
axes[0,0].set_ylabel('Attrition Rate (%)')
axes[0,0].set_title('Overall Attrition Rate by Department', fontsize=13, fontweight='bold')
for i, (idx, row) in enumerate(dept_att.iterrows()):
    axes[0,0].text(i, row['rate']+0.5, f"{row['rate']:.1f}%", ha='center', fontweight='bold')
axes[0,0].set_ylim(0, 28)

# 1b. Attrition by job level and department
lvl_att = df.groupby(['Department','JobLevel'])['is_attrition'].mean().unstack()*100
lvl_att.plot(kind='bar', ax=axes[0,1], colormap='RdYlGn_r', edgecolor='black')
axes[0,1].set_ylabel('Attrition Rate (%)')
axes[0,1].set_title('Attrition Rate by Job Level & Department', fontsize=13, fontweight='bold')
axes[0,1].legend(title='Job Level')
axes[0,1].set_xlabel('')

# 1c. Composition by job level
dept_comp = df.groupby(['Department','JobLevel']).size().unstack(fill_value=0)
dept_comp_pct = dept_comp.div(dept_comp.sum(axis=1), axis=0)*100
dept_comp_pct.plot(kind='bar', stacked=True, ax=axes[0,2], colormap='viridis', edgecolor='black')
axes[0,2].set_ylabel('% of Department')
axes[0,2].set_title('Job Level Composition by Department', fontsize=13, fontweight='bold')
axes[0,2].legend(title='Job Level')
axes[0,2].set_xlabel('')

# 1d. Attrition by overtime and department
ot_att = df.groupby(['Department','OverTime'])['is_attrition'].mean().unstack()*100
ot_att.plot(kind='bar', ax=axes[1,0], color=['#3498db','#e74c3c'], edgecolor='black')
axes[1,0].set_ylabel('Attrition Rate (%)')
axes[1,0].set_title('Attrition by Overtime & Department', fontsize=13, fontweight='bold')
axes[1,0].legend(title='Overtime')
axes[1,0].set_xlabel('')

# 1e. Attrition by stock option level and department
so_att = df.groupby(['Department','StockOptionLevel'])['is_attrition'].mean().unstack()*100
so_att.plot(kind='bar', ax=axes[1,1], colormap='Blues', edgecolor='black')
axes[1,1].set_ylabel('Attrition Rate (%)')
axes[1,1].set_title('Attrition by Stock Option Level & Department', fontsize=13, fontweight='bold')
axes[1,1].legend(title='Stock Level')
axes[1,1].set_xlabel('')

# 1f. Attrition by marital status and department
ms_att = df.groupby(['Department','MaritalStatus'])['is_attrition'].mean().unstack()*100
ms_att.plot(kind='bar', ax=axes[1,2], colormap='Set2', edgecolor='black')
axes[1,2].set_ylabel('Attrition Rate (%)')
axes[1,2].set_title('Attrition by Marital Status & Department', fontsize=13, fontweight='bold')
axes[1,2].legend(title='Marital Status')
axes[1,2].set_xlabel('')

plt.tight_layout()
plt.savefig('/work/attrition_overview.png', dpi=150, bbox_inches='tight')
print("Saved attrition_overview.png")