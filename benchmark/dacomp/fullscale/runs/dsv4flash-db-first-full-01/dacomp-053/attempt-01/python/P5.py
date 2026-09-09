import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Reload classified data
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

# Final summary figure: dual-panel showing the two inversion profiles vs controls
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

metrics = ['completion_percentage','efficiency_score','time_management_score','collaboration_score','complexity_factor']
groups = ['HHLV','HH_HV','LHHV','LH_LV']
colors = {'HHLV':'#e74c3c','HH_HV':'#2ecc71','LHHV':'#3498db','LH_LV':'#95a5a6'}

data = df[df['inv_group'].isin(groups)].groupby('inv_group')[metrics].mean()

# Normalize to 0-100 scale for comparability (complexity_factor ~1-2.5)
norm = data.copy()
norm['complexity_factor'] = norm['complexity_factor']/2.5*100

x = np.arange(len(metrics))
w = 0.18
for i, g in enumerate(groups):
    offset = (i - 1.5)*w
    axes[0].bar(x + offset, norm.loc[g].values, w, label=g, color=colors[g], alpha=0.85)
axes[0].set_xticks(x)
axes[0].set_xticklabels(['Completion','Efficiency','Time Mgmt','Collaboration','Complexity'], fontsize=9, rotation=15)
axes[0].set_title('Normalized Score Profile (0-100 scale)\nComplexity rescaled (max 2.5 = 100)', fontsize=11, fontweight='bold')
axes[0].legend(fontsize=8)
axes[0].grid(axis='y', alpha=0.3)

# Panel 2: elapsed/planned ratio
df['elapsed_ratio'] = df['elapsed_days']/df['planned_duration_days']
ratio_means = df[df['inv_group'].isin(groups)].groupby('inv_group')['elapsed_ratio'].mean().sort_values()
colors2 = [colors[g] for g in ratio_means.index]
axes[1].barh(ratio_means.index, ratio_means.values, color=colors2, alpha=0.85)
axes[1].axvline(1.0, color='gray', linestyle='--', alpha=0.7)
axes[1].set_title('Average Elapsed/Planned Duration Ratio\n(>1 = behind plan, <1 = ahead of plan)', fontsize=11, fontweight='bold')
axes[1].set_xlabel('Elapsed days / Planned days')
axes[1].grid(axis='x', alpha=0.3)

# Panel 3: key categorical shares
cats = pd.DataFrame(index=groups)
cats['behind_sched_%'] = df[df['inv_group'].isin(groups)].groupby('inv_group')['schedule_forecast'].apply(lambda s: (s=='behind_schedule').mean()*100)
cats['ahead_sched_%'] = df[df['inv_group'].isin(groups)].groupby('inv_group')['schedule_forecast'].apply(lambda s: (s=='ahead_of_schedule').mean()*100)
cats['low_priority_%'] = df[df['inv_group'].isin(groups)].groupby('inv_group')['management_priority'].apply(lambda s: (s=='low').mean()*100)
cats['minimal_risk_%'] = df[df['inv_group'].isin(groups)].groupby('inv_group')['risk_level'].apply(lambda s: (s=='minimal_risk').mean()*100)

x = np.arange(len(groups))
w2 = 0.2
axes[2].bar(x-1.5*w2, cats['behind_sched_%'], w2, label='Behind schedule %', color='#e74c3c')
axes[2].bar(x-0.5*w2, cats['ahead_sched_%'], w2, label='Ahead of schedule %', color='#2ecc71')
axes[2].bar(x+0.5*w2, cats['low_priority_%'], w2, label='Low mgmt priority %', color='#f39c12')
axes[2].bar(x+1.5*w2, cats['minimal_risk_%'], w2, label='Minimal risk %', color='#3498db')
axes[2].set_xticks(x)
axes[2].set_xticklabels(groups, fontsize=9)
axes[2].set_title('Categorical Attribute Shares by Group', fontsize=11, fontweight='bold')
axes[2].legend(fontsize=7, loc='upper left')
axes[2].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('inversion_summary.png', dpi=150)
plt.close()
print("Saved inversion_summary.png")

# Print the detailed table for report
print("\nGroup profiles (raw):")
print(data.round(2).to_string())
print("\nElapsed ratio by group:")
print(ratio_means.round(2).to_string())
print("\nCategorical shares:")
print(cats.round(1).to_string())

# Statistical test: HHLV vs HH_HV time_management
from scipy.stats import mannwhitneyu, ttest_ind
hhlv_tm = df[df['inv_group']=='HHLV']['time_management_score']
hh_hv_tm = df[df['inv_group']=='HH_HV']['time_management_score']
lhhv_tm = df[df['inv_group']=='LHHV']['time_management_score']
lh_lv_tm = df[df['inv_group']=='LH_LV']['time_management_score']
print("\nMann-Whitney HHLV vs HH_HV time_mgmt: p =", mannwhitneyu(hhlv_tm, hh_hv_tm).pvalue)
print("Mann-Whitney LHHV vs LH_LV time_mgmt: p =", mannwhitneyu(lhhv_tm, lh_lv_tm).pvalue)
print("Mann-Whitney HHLV vs HH_HV collab: p =", mannwhitneyu(df[df['inv_group']=='HHLV']['collaboration_score'], df[df['inv_group']=='HH_HV']['collaboration_score']).pvalue)

# Also test ROI differences
print("Mann-Whitney HHLV vs LH_LV roi: p =", mannwhitneyu(df[df['inv_group']=='HHLV']['roi_efficiency_ratio'], df[df['inv_group']=='LH_LV']['roi_efficiency_ratio']).pvalue)
print("Mann-Whitney LHHV vs HH_HV roi: p =", mannwhitneyu(df[df['inv_group']=='LHHV']['roi_efficiency_ratio'], df[df['inv_group']=='HH_HV']['roi_efficiency_ratio']).pvalue)
