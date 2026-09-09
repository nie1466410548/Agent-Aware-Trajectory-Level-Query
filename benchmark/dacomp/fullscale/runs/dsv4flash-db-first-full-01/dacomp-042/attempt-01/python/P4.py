import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, fisher_exact

row_data = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle (45-59)'
       ELSE 'Older (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  o."Treatment response" AS response,
  o."Treatment engagement" AS engagement,
  o."Satisfaction Rating" AS satisfaction,
  e."Missed Appointment" AS missed
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
""")
df = db.frame(row_data)

# === Non-compliance rate by barrier within age group ===
print("=== Non-compliance rate (%) by barrier within age group ===")
nc_summary = df.groupby(['age_group', 'barrier']).apply(
    lambda g: pd.Series({
        'n': len(g),
        'non_compliant': (g['adherence'] == 'Non-compliant').sum(),
        'nc_rate': (g['adherence'] == 'Non-compliant').mean() * 100
    })
).reset_index()
print(nc_summary.to_string(index=False))

# Overall non-compliance per group
overall_nc = df.groupby('age_group')['adherence'].apply(lambda g: (g=='Non-compliant').mean()*100)
print("\nOverall non-compliance rate by age group:")
print(overall_nc)

# Post-hoc: middle-aged, Transportation vs rest of middle-aged
mid = df[df['age_group'] == 'Middle (45-59)']
a = mid[mid['barrier'] == 'Transportation']['adherence'].eq('Non-compliant').sum()
b = (mid[mid['barrier'] == 'Transportation']['adherence'].ne('Non-compliant')).sum()
c = mid[mid['barrier'] != 'Transportation']['adherence'].eq('Non-compliant').sum()
d = (mid[mid['barrier'] != 'Transportation']['adherence'].ne('Non-compliant')).sum()
print(f"\nMiddle-aged: Transportation non-compliant {a}/{a+b} vs others {c}/{c+d}")
table = [[a, b], [c, d]]
odds, p_val = fisher_exact(table)
print(f"Fisher exact: odds ratio={odds:.3f}, p={p_val:.4f}")

# Also test transportation vs specific others within middle
for other_bar in ['Time', 'Financial', 'Multiple']:
    sub = mid[mid['barrier'].isin(['Transportation', other_bar])]
    ct = pd.crosstab(sub['barrier'], sub['adherence'].eq('Non-compliant'))
    if ct.shape == (2,2) and ct.values.min() > 0:
        odds, p_val = fisher_exact(ct.values)
        print(f"Transportation vs {other_bar}: OR={odds:.3f}, p={p_val:.4f}")
    else:
        chi2t, pt, _, _ = chi2_contingency(ct)
        print(f"Transportation vs {other_bar}: Chi2={chi2t:.3f}, p={pt:.4f}")

# === Minimal improvement rate by barrier within age group ===
print("\n=== Minimal improvement rate (%) by barrier within age group ===")
mi_summary = df.groupby(['age_group', 'barrier']).apply(
    lambda g: pd.Series({
        'n': len(g),
        'minimal': (g['improvement'] == 'Minimal').sum(),
        'mi_rate': (g['improvement'] == 'Minimal').mean() * 100,
        'sig_rate': (g['improvement'] == 'Significant').mean() * 100
    })
).reset_index()
print(mi_summary.to_string(index=False))

print("\nOverall minimal improvement rate by age group:")
print(df.groupby('age_group')['improvement'].apply(lambda g: (g=='Minimal').mean()*100))
print("\nOverall significant improvement rate by age group:")
print(df.groupby('age_group')['improvement'].apply(lambda g: (g=='Significant').mean()*100))

# === Average satisfaction rating by barrier within age group ===
print("\n=== Mean satisfaction rating by age group × barrier ===")
sat = df.groupby(['age_group', 'barrier'])['satisfaction'].mean().unstack()
print(sat)

print("\nOverall satisfaction by age group:")
print(df.groupby('age_group')['satisfaction'].mean())

# === Treatment response by barrier and age group ===
print("\n=== Treatment response (Poor %) by barrier within age group ===")
resp = df.groupby(['age_group', 'barrier']).apply(
    lambda g: (g['response'] == 'Poor').mean() * 100
).unstack()
print(resp)

# === FIGURE 5: Non-compliance rate heatmap ===
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

nc_pivot = nc_summary.pivot(index='barrier', columns='age_group', values='nc_rate').fillna(0)
sns.heatmap(nc_pivot, annot=True, fmt='.1f', cmap='Reds', ax=axes[0],
            cbar_kws={'label': 'Non-compliance rate (%)'}, vmin=0, vmax=45,
            linewidths=1, linecolor='white')
axes[0].set_title('Treatment Non-Compliance Rate by Barrier & Age Group', fontweight='bold')

mi_pivot = mi_summary.pivot(index='barrier', columns='age_group', values='mi_rate').fillna(0)
sns.heatmap(mi_pivot, annot=True, fmt='.1f', cmap='YlOrRd', ax=axes[1],
            cbar_kws={'label': 'Minimal improvement rate (%)'}, vmin=35, vmax=60,
            linewidths=1, linecolor='white')
axes[1].set_title('Minimal Symptom Improvement Rate by Barrier & Age Group', fontweight='bold')

plt.tight_layout()
plt.savefig('/work/fig5_adherence_improvement_heatmaps.png', dpi=150, bbox_inches='tight')
plt.close()

# === FIGURE 6: Significant improvement + satisfaction bar chart ===
fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))

# Significant improvement rate
sig = df.groupby(['age_group', 'barrier']).apply(
    lambda g: (g['improvement'] == 'Significant').mean() * 100
).unstack()
sig = sig[['Young (18-44)', 'Middle (45-59)', 'Older (60+)']]
sig.plot(kind='bar', ax=axes[0], color=['#4C72B0', '#DD8452', '#55A868'], edgecolor='white')
axes[0].set_title('Significant Symptom Improvement Rate (%)', fontweight='bold')
axes[0].set_ylabel('Percentage (%)')
axes[0].set_xlabel('Treatment Barrier')
axes[0].legend(title='Age Group')
axes[0].tick_params(axis='x', rotation=0)
for container in axes[0].containers:
    axes[0].bar_label(container, fmt='%.1f', fontsize=8)

sat = df.groupby(['age_group', 'barrier'])['satisfaction'].mean().unstack()
sat = sat[['Young (18-44)', 'Middle (45-59)', 'Older (60+)']]
sat.plot(kind='bar', ax=axes[1], color=['#4C72B0', '#DD8452', '#55A868'], edgecolor='white')
axes[1].set_title('Mean Satisfaction Rating by Barrier & Age Group', fontweight='bold')
axes[1].set_ylabel('Satisfaction Rating (1-10)')
axes[1].set_xlabel('Treatment Barrier')
axes[1].tick_params(axis='x', rotation=0)
for container in axes[1].containers:
    axes[1].bar_label(container, fmt='%.1f', fontsize=8)

plt.tight_layout()
plt.savefig('/work/fig6_significant_satisfaction.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigures saved.")

# Kruskal-Wallis for satisfaction across age groups
from scipy.stats import kruskal
groups = [df[df['age_group'] == g]['satisfaction'] for g in ['Young (18-44)', 'Middle (45-59)', 'Older (60+)']]
h, p_kw = kruskal(*groups)
print(f"\nKruskal-Wallis satisfaction by age group: H={h:.3f}, p={p_kw:.4f}")