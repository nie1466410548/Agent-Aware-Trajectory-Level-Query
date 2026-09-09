import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1].copy()
noncohort = df[df['is_target']==0].copy()

# ---- Manual OLS on ROI ----
feat_cols = ['ips','onboarding','team_size','par','sre','total_sales_amount','acq']
X = df[feat_cols].dropna()
y = df.loc[X.index,'roi']
X1 = np.column_stack([np.ones(len(X))] + [X[c].values for c in feat_cols])
beta, res, rank, sv = np.linalg.lstsq(X1, y.values, rcond=None)
yhat = X1 @ beta
ss_res = np.sum((y.values - yhat)**2)
ss_tot = np.sum((y.values - y.mean())**2)
r2 = 1 - ss_res/ss_tot
print("=== OLS on ROI (raw units) ===")
for c, b in zip(['intercept']+feat_cols, beta):
    print(f"  {c:18s}: {b:+.4f}")
print(f"  R^2 = {r2:.4f}")

# standardized betas
Xz = (X - X.mean()) / X.std()
Xz1 = np.column_stack([np.ones(len(Xz))] + [Xz[c].values for c in feat_cols])
bz = np.linalg.lstsq(Xz1, y.values, rcond=None)[0]
print("\n=== Standardized betas ===")
for c, b in zip(['intercept']+feat_cols, bz):
    print(f"  {c:18s}: {b:+.4f}")

# ---- Decision maker x size cross ----
print("\n=== Decision maker x size tier cohort % ===")
cross = pd.crosstab(df['dm'], df['company_size_tier'], values=df['is_target'], aggfunc='mean')*100
print(cross.reindex(['C-Level','VP','Director','Manager','Individual Contributor']).round(1).to_string())

# ---- Onboarding quartiles ----
print("\n=== Onboarding quartile vs PAR, cohort share, ROI ===")
df['onb_q'] = pd.qcut(df['onboarding'], 4, labels=['Q1_low','Q2','Q3','Q4_high'])
onb_agg = df.groupby('onb_q', observed=True).agg(
    n=('roi','count'), avg_par=('par','mean'), avg_sre=('sre','mean'),
    cohort_pct=('is_target','mean'), avg_roi=('roi','mean')).reset_index()
print(onb_agg.to_string(index=False))

# Fig: onboarding quartiles
fig, ax = plt.subplots(figsize=(8.5, 5))
x = np.arange(4); w = 0.35
ax.bar(x - w/2, onb_agg['avg_par'], w, color='#4c72b0', label='Avg product adoption rate')
ax.bar(x + w/2, 100*onb_agg['cohort_pct'], w, color='#c44e52', label='% in target cohort')
ax.set_xticks(x); ax.set_xticklabels(['Q1 (low)','Q2','Q3','Q4 (high)'])
ax.set_ylabel('Rate / %')
ax2 = ax.twinx()
ax2.plot(x, onb_agg['avg_roi'], 'o-', color='#55a868', label='Avg ROI')
ax2.set_ylabel('Avg ROI ratio')
ax.set_title('Onboarding Score Quartiles: Adoption, Cohort Share, ROI')
ax.legend(loc='upper left'); ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig("/work/fig_onboarding_quartiles.png", dpi=110)
plt.close()
print("Saved fig_onboarding_quartiles.png")

# Fig: IPS vs ROI bar (monotonicity)
ips_agg = df.groupby('ips.round(1)').agg(n=('roi','count'), avg_roi=('roi','mean')).reset_index()
ips_agg.columns = ['ips_bucket','n','avg_roi']
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

# Fig: Cohort ROI distribution by decision maker
fig, ax = plt.subplots(figsize=(9, 5))
order = ['C-Level','VP','Director','Manager','Individual Contributor']
dm_roi = cohort.groupby('dm')['roi'].agg(['count','mean','median']).reindex(order)
ax.boxplot([cohort.loc[cohort['dm']==d,'roi'].values for d in order], labels=order)
ax.set_title('Target Cohort ROI Distribution by Decision Maker Level')
ax.set_ylabel('ROI ratio (CLV / Acquisition Cost)')
plt.tight_layout()
plt.savefig("/work/fig_dm_roi.png", dpi=110)
plt.close()
print("Saved fig_dm_roi.png")

# Fig: acquisition cost comparison
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

# Churn by lifecycle in cohort
print("\n=== Cohort churn by lifecycle ===")
print(cohort.groupby('lifecycle_stage').agg(n=('roi','count'), avg_churn=('churn','mean'),
      avg_roi=('roi','mean'), avg_ttv=('ttv','mean')).reindex(['Activation','Growth','Maturity','Retention','Dormant']).to_string())

# Time to value
print("\n=== Time-to-value by cohort ===")
t, p = stats.ttest_ind(cohort['ttv'].dropna(), noncohort['ttv'].dropna(), equal_var=False)
print(f"cohort avg ttv={cohort['ttv'].mean():.1f}, noncohort={noncohort['ttv'].mean():.1f}, t={t:.2f}, p={p:.2e}")

print("\nAll done.")