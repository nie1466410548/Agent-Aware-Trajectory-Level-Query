import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

df = pd.read_csv('/work/full_joined.csv')
cat_df = pd.read_csv('/work/cat_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
cat_df['sec_group'] = pd.cut(cat_df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])

# Figure 1: Disease Risk proportion by secondary incident group
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# 1a: Disease Risk
risk_ct = pd.crosstab(df['sec_group'], df['Disease Risk'], normalize='index')
risk_ct.plot(kind='bar', ax=axes[0], color=['#e74c3c','#2ecc71','#f39c12'], edgecolor='black')
axes[0].set_title('Disease Risk by Secondary Incidents', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Secondary Incident Count Group')
axes[0].set_ylabel('Proportion')
axes[0].legend(title='Disease Risk')
axes[0].set_ylim(0, 0.5)
for p in axes[0].patches:
    axes[0].annotate(f'{p.get_height():.2f}', (p.get_x()+p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=8)

# 1b: Monitoring frequency
mon_ct = pd.crosstab(cat_df['sec_group'], cat_df['monitoringfreq'], normalize='index')
mon_ct.plot(kind='bar', ax=axes[1], color=['#3498db','#9b59b6','#1abc9c'], edgecolor='black')
axes[1].set_title('Monitoring Frequency by Secondary Incidents', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Secondary Incident Count Group')
axes[1].set_ylabel('Proportion')
axes[1].legend(title='Monitoring')
for p in axes[1].patches:
    axes[1].annotate(f'{p.get_height():.2f}', (p.get_x()+p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=8)

# 1c: Audit status
aud_ct = pd.crosstab(cat_df['sec_group'], cat_df['auditstate'], normalize='index')
aud_ct.plot(kind='bar', ax=axes[2], color=['#2ecc71','#f39c12','#e74c3c'], edgecolor='black')
axes[2].set_title('Audit Status by Secondary Incidents', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Secondary Incident Count Group')
axes[2].set_ylabel('Proportion')
axes[2].legend(title='Audit Status')
for p in axes[2].patches:
    axes[2].annotate(f'{p.get_height():.2f}', (p.get_x()+p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('/work/fig1_disease_monitoring_audit.png', dpi=150)
plt.close()

# Figure 2: Vaccination rates among High Disease Risk events
fig, ax = plt.subplots(figsize=(8, 5))
sub_high_risk = df[df['Disease Risk']=='High']
sns.boxplot(x='sec_group', y='vaccination', data=sub_high_risk, ax=ax,
            palette=['#3498db','#f39c12','#e74c3c'], order=['Low (0-32)','Medium (33-65)','High (66-100)'])
ax.set_title('Vaccination Coverage Among High Disease-Risk Events\nby Secondary Incident Level', fontsize=13, fontweight='bold')
ax.set_xlabel('Secondary Incident Count Group')
ax.set_ylabel('Vaccination Coverage Rate (%)')
# Add means
means = sub_high_risk.groupby('sec_group')['vaccination'].mean()
for i, (label, mean) in enumerate(means.items()):
    ax.annotate(f'Mean: {mean:.1f}%', xy=(i, mean), ha='center', va='bottom',
                fontsize=10, fontweight='bold', color='black')
plt.tight_layout()
plt.savefig('/work/fig2_vaccination_high_risk.png', dpi=150)
plt.close()

# Figure 3: Lessons Learned Stage by sec group
fig, ax = plt.subplots(figsize=(8, 5))
ll_ct = pd.crosstab(cat_df['sec_group'], cat_df['lessonslearnedstage'], normalize='index')
ll_ct.plot(kind='bar', ax=ax, color=['#2ecc71','#3498db','#f39c12'], edgecolor='black')
ax.set_title('Lessons Learned Stage by Secondary Incidents', fontsize=13, fontweight='bold')
ax.set_xlabel('Secondary Incident Count Group')
ax.set_ylabel('Proportion')
ax.legend(title='Lessons Learned')
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', (p.get_x()+p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('/work/fig3_lessons_learned.png', dpi=150)
plt.close()

# Figure 4: Operation Status by Disaster Level
fig, ax = plt.subplots(figsize=(10, 5))
op_ct = pd.crosstab(df['Disaster Level'], df['Operation Status'], normalize='index')
op_ct.plot(kind='bar', ax=ax, color=['#3498db','#2ecc71','#f39c12','#e74c3c'], edgecolor='black')
ax.set_title('Operation Status by Disaster Level', fontsize=13, fontweight='bold')
ax.set_xlabel('Disaster Level')
ax.set_ylabel('Proportion')
ax.legend(title='Operation Status')
for p in ax.patches:
    if p.get_height() > 0.05:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x()+p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.savefig('/work/fig4_ops_by_level.png', dpi=150)
plt.close()

# Also check nextreviewdate - parse and compute days until review
cat_df['nextreviewdate'] = pd.to_datetime(cat_df['nextreviewdate'], errors='coerce')
res = db.query("SELECT c.\"Secincident Count\", c.\"nextreviewdate\" FROM coordination_and_evaluation c")
review_df = db.frame(res)
review_df['nextreviewdate'] = pd.to_datetime(review_df['nextreviewdate'], errors='coerce')
review_df['days_till_review'] = (pd.Timestamp('2025-09-08') - review_df['nextreviewdate']).dt.days
review_df['sec_group'] = pd.cut(review_df['Secincident Count'], bins=[-1, 32, 65, 100], labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
print("=== Days till next review (negative = overdue) ===")
print(review_df.groupby('sec_group')['days_till_review'].agg(['mean','median','min','max']).round(1))

# Proportion of overdue reviews
review_df['overdue'] = review_df['days_till_review'] < 0
print("\n=== Overdue reviews proportion ===")
print(review_df.groupby('sec_group')['overdue'].mean().round(3))

print("\nFiles saved: fig1, fig2, fig3, fig4")