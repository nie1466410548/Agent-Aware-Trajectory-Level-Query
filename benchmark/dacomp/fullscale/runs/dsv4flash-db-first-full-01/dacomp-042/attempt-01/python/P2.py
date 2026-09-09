import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Set style
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12

# Color palette
colors = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']
improvement_colors = {'Minimal': '#C44E52', 'Moderate': '#DD8452', 'Significant': '#55A868'}

# ============ FIGURE 1: Barrier distribution by age group ============
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

barrier_age = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, barrier
""")
df_ba = db.frame(barrier_age)

# Compute totals per age group
totals = df_ba.groupby('age_group')['n'].sum().reset_index()
totals_dict = dict(zip(totals['age_group'], totals['n']))
df_ba['pct'] = df_ba.apply(lambda row: row['n'] / totals_dict[row['age_group']] * 100, axis=1)

print("Percentages of barriers by age group:")
print(df_ba)

# Plot
for i, (age_grp, ax) in enumerate(zip(['Young Adults (18-44)', 'Middle-aged (45-59)', 'Older Adults (60+)'], axes)):
    sub = df_ba[df_ba['age_group'] == age_grp]
    bars = ax.bar(sub['barrier'], sub['pct'], color=colors, edgecolor='white', linewidth=0.5)
    ax.set_title(age_grp, fontweight='bold', fontsize=13)
    ax.set_ylim(0, 50)
    ax.set_ylabel('Percentage (%)')
    ax.set_xlabel('Treatment Barrier')
    for bar, pct in zip(bars, sub['pct']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{pct:.1f}%', 
                ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.suptitle('Distribution of Treatment Barriers by Age Group', fontsize=15, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/work/fig1_barrier_distribution.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ FIGURE 2: Symptom improvement by age group ============
fig, ax = plt.subplots(figsize=(10, 6))

imp_age = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, improvement
ORDER BY age_group, improvement
""")
df_ia = db.frame(imp_age)
totals_i = df_ia.groupby('age_group')['n'].sum().reset_index()
totals_i_dict = dict(zip(totals_i['age_group'], totals_i['n']))
df_ia['pct'] = df_ia.apply(lambda row: row['n'] / totals_i_dict[row['age_group']] * 100, axis=1)

# Grouped bar
bar_width = 0.25
x = np.arange(3)
for i, imp in enumerate(['Minimal', 'Moderate', 'Significant']):
    sub = df_ia[df_ia['improvement'] == imp]
    sub = sub.set_index('age_group').reindex(['Young Adults (18-44)', 'Middle-aged (45-59)', 'Older Adults (60+)'])
    ax.bar(x + i*bar_width, sub['pct'], bar_width, label=imp, color=improvement_colors[imp], edgecolor='white')

ax.set_xticks(x + bar_width)
ax.set_xticklabels(['Young Adults\n(18-44)', 'Middle-aged\n(45-59)', 'Older Adults\n(60+)'], fontweight='bold')
ax.set_ylabel('Percentage (%)', fontweight='bold')
ax.set_title('Symptom Improvement by Age Group', fontweight='bold', fontsize=14)
ax.legend(title='Improvement', fontsize=11)
for i, imp in enumerate(['Minimal', 'Moderate', 'Significant']):
    sub = df_ia[df_ia['improvement'] == imp]
    sub = sub.set_index('age_group').reindex(['Young Adults (18-44)', 'Middle-aged (45-59)', 'Older Adults (60+)'])
    for j, (idx, row) in enumerate(sub.iterrows()):
        ax.text(j + i*bar_width, row['pct'] + 0.5, f'{row["pct"]:.1f}%', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('/work/fig2_improvement_by_age.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ FIGURE 3: Heatmap of barrier × improvement by age group ============
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

full = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier, improvement
ORDER BY age_group, barrier, improvement
""")
df_full = db.frame(full)

for idx, (age_grp, ax) in enumerate(zip(['Young Adults (18-44)', 'Middle-aged (45-59)', 'Older Adults (60+)'], axes)):
    sub = df_full[df_full['age_group'] == age_grp].copy()
    # Compute percentages within each barrier
    total_by_barrier = sub.groupby('barrier')['n'].transform('sum')
    sub['pct'] = sub['n'] / total_by_barrier * 100
    pivot = sub.pivot(index='barrier', columns='improvement', values='pct').fillna(0)
    pivot = pivot[['Minimal', 'Moderate', 'Significant']]
    
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax, 
                cbar_kws={'label': '% within barrier'}, vmin=0, vmax=70,
                linewidths=1, linecolor='white')
    ax.set_title(age_grp, fontweight='bold', fontsize=13)
    ax.set_xlabel('Symptom Improvement', fontweight='bold')
    ax.set_ylabel('Treatment Barrier', fontweight='bold')

plt.suptitle('Impact of Treatment Barriers on Symptom Improvement by Age Group\n(% within each barrier type)', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/work/fig3_impact_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()

# ============ FIGURE 4: Patient characteristics by age group ============
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Financial stress
fs = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Financial stress" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_fs = db.frame(fs)
tot_fs = df_fs.groupby('age_group')['n'].sum().reset_index()
tot_fs_dict = dict(zip(tot_fs['age_group'], tot_fs['n']))
df_fs['pct'] = df_fs.apply(lambda r: r['n']/tot_fs_dict[r['age_group']]*100, axis=1)
pivot_fs = df_fs.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_fs = pivot_fs[['Mild', 'Moderate', 'Severe']]
pivot_fs.plot(kind='bar', ax=axes[0,0], color=['#55A868', '#DD8452', '#C44E52'], edgecolor='white')
axes[0,0].set_title('Financial Stress', fontweight='bold')
axes[0,0].set_ylabel('Percentage (%)')
axes[0,0].legend(title='Level')
for container in axes[0,0].containers:
    axes[0,0].bar_label(container, fmt='%.1f', fontsize=8)

# Stigma effect
se = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Stigma effect" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_se = db.frame(se)
tot_se = df_se.groupby('age_group')['n'].sum().reset_index()
tot_se_dict = dict(zip(tot_se['age_group'], tot_se['n']))
df_se['pct'] = df_se.apply(lambda r: r['n']/tot_se_dict[r['age_group']]*100, axis=1)
pivot_se = df_se.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_se = pivot_se[['Mild', 'Moderate', 'Severe']]
pivot_se.plot(kind='bar', ax=axes[0,1], color=['#55A868', '#DD8452', '#C44E52'], edgecolor='white')
axes[0,1].set_title('Stigma Effect', fontweight='bold')
for container in axes[0,1].containers:
    axes[0,1].bar_label(container, fmt='%.1f', fontsize=8)

# Housing stability
hs = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Housing stability" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_hs = db.frame(hs)
tot_hs = df_hs.groupby('age_group')['n'].sum().reset_index()
tot_hs_dict = dict(zip(tot_hs['age_group'], tot_hs['n']))
df_hs['pct'] = df_hs.apply(lambda r: r['n']/tot_hs_dict[r['age_group']]*100, axis=1)
pivot_hs = df_hs.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_hs = pivot_hs[['Stable', 'At risk', 'Unstable', 'Homeless']]
pivot_hs.plot(kind='bar', ax=axes[0,2], color=['#55A868', '#DD8452', '#C44E52', '#8B0000'], edgecolor='white')
axes[0,2].set_title('Housing Stability', fontweight='bold')
for container in axes[0,2].containers:
    axes[0,2].bar_label(container, fmt='%.1f', fontsize=8)

# Employment status
em = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Employment status" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_em = db.frame(em)
tot_em = df_em.groupby('age_group')['n'].sum().reset_index()
tot_em_dict = dict(zip(tot_em['age_group'], tot_em['n']))
df_em['pct'] = df_em.apply(lambda r: r['n']/tot_em_dict[r['age_group']]*100, axis=1)
pivot_em = df_em.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_em.plot(kind='bar', ax=axes[1,0], color=sns.color_palette('Set2', n_colors=len(pivot_em.columns)), edgecolor='white')
axes[1,0].set_title('Employment Status', fontweight='bold')
axes[1,0].set_ylabel('Percentage (%)')
for container in axes[1,0].containers:
    axes[1,0].bar_label(container, fmt='%.1f', fontsize=7)

# Insurance status
ins = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Insurance status" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_ins = db.frame(ins)
tot_ins = df_ins.groupby('age_group')['n'].sum().reset_index()
tot_ins_dict = dict(zip(tot_ins['age_group'], tot_ins['n']))
df_ins['pct'] = df_ins.apply(lambda r: r['n']/tot_ins_dict[r['age_group']]*100, axis=1)
pivot_ins = df_ins.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_ins = pivot_ins[['Approved', 'Pending', 'Refused']]
pivot_ins.plot(kind='bar', ax=axes[1,1], color=['#55A868', '#DD8452', '#C44E52'], edgecolor='white')
axes[1,1].set_title('Insurance Status', fontweight='bold')
for container in axes[1,1].containers:
    axes[1,1].bar_label(container, fmt='%.1f', fontsize=8)

# Treatment adherence
ad = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  o."Treatment adherence" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
""")
df_ad = db.frame(ad)
tot_ad = df_ad.groupby('age_group')['n'].sum().reset_index()
tot_ad_dict = dict(zip(tot_ad['age_group'], tot_ad['n']))
df_ad['pct'] = df_ad.apply(lambda r: r['n']/tot_ad_dict[r['age_group']]*100, axis=1)
pivot_ad = df_ad.pivot(index='age_group', columns='val', values='pct').fillna(0)
pivot_ad = pivot_ad[['High', 'Moderate', 'Low', 'Non-compliant']]
pivot_ad.plot(kind='bar', ax=axes[1,2], color=['#55A868', '#DD8452', '#C44E52', '#8B0000'], edgecolor='white')
axes[1,2].set_title('Treatment Adherence', fontweight='bold')
for container in axes[1,2].containers:
    axes[1,2].bar_label(container, fmt='%.1f', fontsize=8)

plt.suptitle('Patient Characteristics and Treatment Adherence by Age Group', fontsize=15, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('/work/fig4_patient_characteristics.png', dpi=150, bbox_inches='tight')
plt.close()

print("All figures saved successfully!")

# Additional stats: Chi-square tests for characteristics
print("\n=== Chi-square: Financial stress × Age group ===")
ct_fs = pd.crosstab(
    df_fs['age_group'], df_fs['val'], values=df_fs['n'], aggfunc='sum'
).fillna(0)
print(ct_fs)
chi2, p, _, _ = chi2_contingency(ct_fs)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

print("\n=== Chi-square: Stigma effect × Age group ===")
ct_se = pd.crosstab(
    df_se['age_group'], df_se['val'], values=df_se['n'], aggfunc='sum'
).fillna(0)
print(ct_se)
chi2, p, _, _ = chi2_contingency(ct_se)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

print("\n=== Chi-square: Housing stability × Age group ===")
ct_hs = pd.crosstab(
    df_hs['age_group'], df_hs['val'], values=df_hs['n'], aggfunc='sum'
).fillna(0)
print(ct_hs)
chi2, p, _, _ = chi2_contingency(ct_hs)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

print("\n=== Chi-square: Employment status × Age group ===")
ct_em = pd.crosstab(
    df_em['age_group'], df_em['val'], values=df_em['n'], aggfunc='sum'
).fillna(0)
print(ct_em)
chi2, p, _, _ = chi2_contingency(ct_em)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

print("\n=== Chi-square: Insurance status × Age group ===")
ct_ins = pd.crosstab(
    df_ins['age_group'], df_ins['val'], values=df_ins['n'], aggfunc='sum'
).fillna(0)
print(ct_ins)
chi2, p, _, _ = chi2_contingency(ct_ins)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

print("\n=== Chi-square: Treatment adherence × Age group ===")
ct_ad = pd.crosstab(
    df_ad['age_group'], df_ad['val'], values=df_ad['n'], aggfunc='sum'
).fillna(0)
print(ct_ad)
chi2, p, _, _ = chi2_contingency(ct_ad)
print(f"Chi2={chi2:.4f}, p={p:.6f}")