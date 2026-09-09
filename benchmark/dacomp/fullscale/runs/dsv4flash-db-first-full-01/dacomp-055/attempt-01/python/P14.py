import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1].copy()
noncohort = df[df['is_target']==0].copy()

# Fix: create bucket column properly
df['ips_bucket'] = df['ips'].round(1)
ips_agg = df.groupby('ips_bucket').agg(n=('roi','count'), avg_roi=('roi','mean')).reset_index()

# Fig: IPS vs ROI bar
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.bar(ips_agg['ips_bucket'].astype(str), ips_agg['avg_roi'], color='#4c72b0', alpha=0.85)
ax.set_xlabel('Investment Priority Score (rounded)')
ax.set_ylabel('Avg ROI ratio')
ax.set_title('Average ROI by Investment Priority Score Level — no monotonic lift from higher IPS')
ax.tick_params(axis='x', rotation=90)
plt.tight_layout()
plt.savefig("/work/fig_ips_roi.png", dpi=110)
plt.close()
print("Saved fig_ips_roi.png")

# Fig: cohort ROI by decision maker
fig, ax = plt.subplots(figsize=(9, 5))
order = ['C-Level','VP','Director','Manager','Individual Contributor']
ch_data = [cohort.loc[cohort['dm']==d,'roi'].values for d in order if d in cohort['dm'].values]
bp = ax.boxplot(ch_data, labels=[d for d in order if d in cohort['dm'].values])
ax.set_title('Target Cohort ROI Distribution by Decision Maker Level')
ax.set_ylabel('ROI ratio (CLV / Acquisition Cost)')
plt.tight_layout()
plt.savefig("/work/fig_dm_roi.png", dpi=110)
plt.close()
print("Saved fig_dm_roi.png")

# Fig: acquisition cost and team size
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=df, x='is_target', y='acq', ax=axes[0])
axes[0].set_xticklabels(['Non-cohort','Target cohort'])
axes[0].set_title('Acquisition Cost by Cohort')
sns.boxplot(data=df, x='is_target', y='team_size', ax=axes[1])
axes[1].set_xticklabels(['Non-cohort','Target cohort'])
axes[1].set_title('Team Size by Cohort')
plt.tight_layout()
plt.savefig("/work/fig_acq_team.png", dpi=110)
plt.close()
print("Saved fig_acq_team.png")

# Churn by lifecycle
print("=== Cohort churn by lifecycle ===")
print(cohort.groupby('lifecycle_stage').agg(n=('roi','count'), avg_churn=('churn','mean'),
      avg_roi=('roi','mean'), avg_ttv=('ttv','mean')).reindex(['Activation','Growth','Maturity','Retention','Dormant']).to_string())

# TTV
print("\n=== Time-to-value ===")
t, p = stats.ttest_ind(cohort['ttv'].dropna(), noncohort['ttv'].dropna(), equal_var=False)
print(f"cohort avg ttv={cohort['ttv'].mean():.1f}, noncohort={noncohort['ttv'].mean():.1f}, t={t:.2f}, p={p:.2e}")

# IPS vs composite for the final systematic bias insight
print("\n=== IPS vs Components: Spearman correlations ===")
for col in ['par','sre','total_sales_amount','onboarding','team_size','roi']:
    r, p = stats.spearmanr(df['ips'], df[col])
    print(f"  IPS vs {col:15s}: r={r:.3f}, p={p:.2e}")

# Health score vs IPS: strong correlation
r, p = stats.spearmanr(df['ips'], df['health'])
print(f"  IPS vs {'health':15s}: r={r:.3f}, p={p:.2e}")

# Cohort concentration by company size
print("\n=== Cohort concentration by size tier ===")
sz = df.groupby('company_size_tier').agg(
    total=('is_target','count'),
    cohort=('is_target','sum'),
    pct=('is_target','mean'),
    avg_roi=('roi','mean'),
    avg_acq=('acq','mean')
).reindex(['Startup','Small','Medium','Large','Enterprise'])
print(sz.to_string())

print("\nAll Python analysis complete.")