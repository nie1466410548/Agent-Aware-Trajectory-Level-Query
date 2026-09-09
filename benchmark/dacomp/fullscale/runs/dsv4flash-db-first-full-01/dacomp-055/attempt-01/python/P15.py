import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1].copy()
noncohort = df[df['is_target']==0].copy()

# Fig: cohort ROI by decision maker
fig, ax = plt.subplots(figsize=(9, 5))
order = ['C-Level','VP','Director','Manager','Individual Contributor']
ch_data = [cohort.loc[cohort['dm']==d,'roi'].values for d in order if d in cohort['dm'].values]
labels = [d for d in order if d in cohort['dm'].values]
bp = ax.boxplot(ch_data)
ax.set_xticklabels(labels)
ax.set_title('Target Cohort ROI Distribution by Decision Maker Level')
ax.set_ylabel('ROI ratio (CLV / Acquisition Cost)')
plt.tight_layout()
plt.savefig("/work/fig_dm_roi.png", dpi=110)
plt.close()
print("Saved fig_dm_roi.png")

# Fig: acquisition cost and team size
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
bp1 = axes[0].boxplot([noncohort['acq'].values, cohort['acq'].values])
axes[0].set_xticklabels(['Non-cohort','Target cohort'])
axes[0].set_title('Acquisition Cost by Cohort')
bp2 = axes[1].boxplot([noncohort['team_size'].values, cohort['team_size'].values])
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

# Final systemic bias summary
print("\n=== SYSTEMIC BIAS SUMMARY ===")
print(f"IPS correlation with ROI: Spearman r={stats.spearmanr(df['ips'], df['roi'])[0]:.3f}")
print(f"IPS correlation with PAR: Spearman r={stats.spearmanr(df['ips'], df['par'])[0]:.3f}")
print(f"IPS correlation with SRE: Spearman r={stats.spearmanr(df['ips'], df['sre'])[0]:.3f}")
print(f"IPS correlation with sales: Spearman r={stats.spearmanr(df['ips'], df['total_sales_amount'])[0]:.3f}")
print(f"IPS correlation with health: Spearman r={stats.spearmanr(df['ips'], df['health'])[0]:.3f}")
print(f"Health correlation with churn: Spearman r={stats.spearmanr(df['health'], df['churn'])[0]:.3f}")

# Size tier: ROI vs IPS
print("\n=== Size tier: avg IPS vs avg ROI ===")
sz = df.groupby('company_size_tier').agg(
    avg_ips=('ips','mean'), avg_roi=('roi','mean'), n=('roi','count')).reindex(['Startup','Small','Medium','Large','Enterprise'])
print(sz.to_string())

# Cohort share by industry (for final report)
print("\n=== Industry cohort share ordered ===")
ind_shares = df.groupby('industry_vertical').agg(
    total=('is_target','count'), cohort=('is_target','sum')).reset_index()
ind_shares['pct'] = 100*ind_shares['cohort']/ind_shares['total']
print(ind_shares.sort_values('pct', ascending=False).to_string())

print("\nAll figures and analysis complete.")