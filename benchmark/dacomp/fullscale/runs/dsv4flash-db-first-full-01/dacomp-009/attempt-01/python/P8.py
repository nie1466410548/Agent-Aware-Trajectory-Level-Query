import json, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

with open('/results/S27.rows.jsonl') as f:
    rows = [json.loads(l) for l in f]
df = pd.DataFrame(rows)
df.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
              'total_eff_hours','total_units','avg_units','avg_pass_rate','composite_score','rank']

with open('/results/S29.rows.jsonl') as f:
    rows2 = [json.loads(l) for l in f]
df_sal = pd.DataFrame(rows2)
df_sal.columns = ['Employee ID','Employee','Base Salary','Company Accommodation']
df = df.merge(df_sal, on=['Employee ID','Employee'], how='left')

df['group'] = np.where(df['rank']<=10, 'Top 10', 'Rest')

# Figure: normalized attribute comparison (z-scores style, but on mean-normalized scale)
attrs = ['Age','tenure_months','avg_units','avg_pass_rate','total_eff_hours','Base Salary']
labels = ['Age','Tenure (months)','Avg Units/Day','Pass Rate (%)','Eff. Hours (total)','Base Salary']

top_means = [df.loc[df.group=='Top 10', a].mean() for a in attrs]
rest_means = [df.loc[df.group=='Rest', a].mean() for a in attrs]

# Convert to % of overall mean for comparability
overall = [df[a].mean() for a in attrs]
top_rel = [t/o*100 for t,o in zip(top_means, overall)]
rest_rel = [r/o*100 for r,o in zip(rest_means, overall)]

x = np.arange(len(labels))
w = 0.35
fig, ax = plt.subplots(figsize=(11,6))
b1 = ax.bar(x-w/2, top_rel, w, label='Top 10', color='crimson')
b2 = ax.bar(x+w/2, rest_rel, w, label='Rest (n=58)', color='steelblue')
ax.axhline(100, color='grey', ls='--', lw=1)
ax.set_ylabel('Value relative to workforce average (%)')
ax.set_title('Top-10 performers vs. rest: attribute profile (100% = workforce mean)')
ax.set_xticks(x); ax.set_xticklabels(labels, rotation=20)
for b in list(b1)+list(b2):
    ax.annotate(f'{b.get_height():.0f}%', (b.get_x()+b.get_width()/2, b.get_height()), ha='center', va='bottom', fontsize=8)
ax.legend()
plt.tight_layout()
plt.savefig('/work/top10_vs_rest_profile.png', dpi=150)
print("saved top10_vs_rest_profile.png")

# Figure: gender composition and discipline
fig2, axes = plt.subplots(1, 2, figsize=(11, 4.5))
# Gender shares in top10 vs rest
share = pd.DataFrame({
    'Female': [df[df.group=='Top 10']['Gender'].eq('Female').mean()*100,
               df[df.group=='Rest']['Gender'].eq('Female').mean()*100],
    'Male': [df[df.group=='Top 10']['Gender'].eq('Male').mean()*100,
             df[df.group=='Rest']['Gender'].eq('Male').mean()*100]
}, index=['Top 10','Rest'])
share.plot(kind='bar', ax=axes[0], color=['lightcoral','steelblue'])
axes[0].set_title('Gender composition (%)')
axes[0].set_ylabel('% of group')
axes[0].tick_params(axis='x', rotation=0)

# Discipline share
with open('/results/S21.rows.jsonl') as f:
    rows3 = [json.loads(l) for l in f]
dfd = pd.DataFrame(rows3)
dfd.columns = ['Employee ID','Employee','Team','Gender','Age','Education Level','tenure_months','days',
               'total_eff_hours','avg_eff_hours','total_units','avg_units','avg_pass_rate','discipline_days']
df = df.merge(dfd[['Employee ID','discipline_days']], on='Employee ID', how='left')
df['group'] = np.where(df['rank']<=10, 'Top 10', 'Rest')
disc_share = df.groupby('group')['discipline_days'].apply(lambda s: (s>0).mean()*100)
disc_share.plot(kind='bar', ax=axes[1], color=['crimson','steelblue'])
axes[1].set_title('Employees with ≥1 disciplinary record (%)')
axes[1].set_ylabel('% of group')
axes[1].tick_params(axis='x', rotation=0)
plt.tight_layout()
plt.savefig('/work/gender_discipline_summary.png', dpi=150)
print("saved gender_discipline_summary.png")

# Print the full ranked table for the report reference
print("\n=== FULL RANKING (top 20) ===")
cols = ['rank','Employee','Gender','Age','Education Level','tenure_months','Team','avg_units','avg_pass_rate','composite_score']
print(df.sort_values('rank')[cols].head(20).round(2).to_string(index=False))

print("\n=== Key stats table for report ===")
print("Overall: N=%d, Female=%d, Male=%d" % (len(df), (df.Gender=='Female').sum(), (df.Gender=='Male').sum()))
print("Avg units/day female=%.1f male=%.1f" % (df[df.Gender=='Female']['avg_units'].mean(), df[df.Gender=='Male']['avg_units'].mean()))
print("Avg pass rate female=%.2f male=%.2f" % (df[df.Gender=='Female']['avg_pass_rate'].mean(), df[df.Gender=='Male']['avg_pass_rate'].mean()))
