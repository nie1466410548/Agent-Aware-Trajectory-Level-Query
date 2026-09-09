import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Load full data with classification
res = db.query("""
SELECT *, 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other' END AS inv_group
FROM asana__project_analytics
""")
df = db.frame(res)

# Color map for groups
group_colors = {
    'HHLV': '#e74c3c',
    'HH_HV': '#2ecc71',
    'LHHV': '#3498db',
    'LH_LV': '#95a5a6',
    'Other': '#bdc3a7'
}

# 1. Scatter: Health vs ROI colored by inversion group
fig, ax = plt.subplots(figsize=(10, 7))
for grp, grp_df in df.groupby('inv_group'):
    ax.scatter(grp_df['overall_health_score'], grp_df['roi_efficiency_ratio'],
               c=group_colors.get(grp, '#999'), label=grp, alpha=0.7, s=40, edgecolors='w', linewidth=0.5)
ax.axvline(x=75, color='gray', linestyle='--', alpha=0.5, label='Health=75 (A/B boundary)')
ax.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5, label='ROI=0.5')
ax.set_xlabel('Overall Health Score', fontsize=12)
ax.set_ylabel('ROI Efficiency Ratio', fontsize=12)
ax.set_title('Health-Value Inversion: Health Score vs ROI Efficiency', fontsize=14, fontweight='bold')
ax.legend(fontsize=9, loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('work/health_roi_scatter.png', dpi=150)
plt.close()
print("Saved scatter plot")

# 2. Group comparison bar chart
group_profile = df[df['inv_group'].isin(['HHLV','HH_HV','LHHV','LH_LV'])].groupby('inv_group').agg({
    'overall_health_score': 'mean',
    'roi_efficiency_ratio': 'mean',
    'completion_percentage': 'mean',
    'efficiency_score': 'mean',
    'time_management_score': 'mean',
    'collaboration_score': 'mean',
    'complexity_factor': 'mean',
    'elapsed_days': 'mean',
    'planned_duration_days': 'mean'
}).round(2)
group_profile['elapsed_ratio'] = (group_profile['elapsed_days'] / group_profile['planned_duration_days']).round(2)
print("Group profile:")
print(group_profile[['overall_health_score','roi_efficiency_ratio','completion_percentage','efficiency_score','time_management_score','elapsed_ratio']])

# 3. Factor comparison radar chart
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# HHLV vs HH_HV
hhlv = df[df['inv_group']=='HHLV'][['completion_percentage','efficiency_score','time_management_score','collaboration_score']].mean()
hh_hv = df[df['inv_group']=='HH_HV'][['completion_percentage','efficiency_score','time_management_score','collaboration_score']].mean()
lh_lv = df[df['inv_group']=='LH_LV'][['completion_percentage','efficiency_score','time_management_score','collaboration_score']].mean()
lhhv = df[df['inv_group']=='LHHV'][['completion_percentage','efficiency_score','time_management_score','collaboration_score']].mean()

x = np.arange(len(hhlv.index))
w = 0.2
axes[0].bar(x - 1.5*w, hhlv.values, w, label='HHLV (n=11)', color='#e74c3c')
axes[0].bar(x - 0.5*w, hh_hv.values, w, label='HH_HV (n=80)', color='#2ecc71')
axes[0].bar(x + 0.5*w, lh_lv.values, w, label='LH_LV (n=206)', color='#95a5a6')
axes[0].bar(x + 1.5*w, lhhv.values, w, label='LHHV (n=5)', color='#3498db')
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Completion %', 'Efficiency', 'Time Mgmt', 'Collab'], fontsize=10)
axes[0].set_title('Score Component Comparison Across Groups', fontsize=12, fontweight='bold')
axes[0].legend(fontsize=8)
axes[0].set_ylabel('Average Score')
axes[0].grid(axis='y', alpha=0.3)

# Schedule comparison
schedule_data = df[df['inv_group'].isin(['HHLV','HH_HV','LHHV','LH_LV'])]
schedule_pct = schedule_data.groupby('inv_group')['schedule_forecast'].value_counts(normalize=True).unstack(fill_value=0)*100
schedule_pct.plot(kind='bar', ax=axes[1], color=['#2ecc71','#f39c12','#e74c3c'], width=0.7)
axes[1].set_title('Schedule Forecast Distribution by Group', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Percentage (%)')
axes[1].set_xlabel('')
axes[1].legend(fontsize=8)
axes[1].grid(axis='y', alpha=0.3)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('work/group_comparison.png', dpi=150)
plt.close()
print("Saved group comparison")

# 4. Correlation heatmap
corr_cols = ['overall_health_score','roi_efficiency_ratio','completion_percentage','quality_percentage',
             'risk_percentage','efficiency_score','time_management_score','collaboration_score',
             'complexity_factor','elapsed_ratio']
df['elapsed_ratio'] = df['elapsed_days'] / df['planned_duration_days']
corr = df[corr_cols].corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            square=True, linewidths=0.5, ax=ax, vmin=-1, vmax=1)
ax.set_title('Correlation Matrix: Key Project Metrics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('work/correlation_heatmap.png', dpi=150)
plt.close()
print("Saved correlation heatmap")