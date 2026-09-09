import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1].copy()
noncohort = df[df['is_target']==0].copy()

# ---- IPS buckets by rounded value ----
print("=== IPS level vs avg ROI / PAR (monotonicity check) ===")
df['ips_bucket'] = df['ips'].round(1)
ips_agg = df.groupby('ips_bucket').agg(n=('roi','count'), avg_roi=('roi','mean'),
                                       avg_par=('par','mean'), avg_comp=('composite','mean')).reset_index()
print(ips_agg.to_string(index=False))

# ---- Spearman: IPS vs ROI within top-30 IPS group ----
top = df[df['ips'] >= 1.62]
r, p = stats.spearmanr(top['ips'], top['roi'])
print(f"\nWithin top-30% IPS (n={len(top)}): IPS vs ROI Spearman r={r:.3f}, p={p:.2e}")

# ---- Regression for ROI ----
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
feat_cols = ['ips','onboarding','team_size','par','sre','total_sales_amount','acq']
X = df[feat_cols].dropna()
y = df.loc[X.index,'roi']
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
reg = LinearRegression().fit(Xs, y)
print("\n=== Standardized betas on ROI ===")
for name, coef in zip(X.columns, reg.coef_):
    print(f"  {name:18s}: {coef:+.4f}")
print(f"  R^2 = {reg.score(Xs, y):.4f}")

# ---- Decision maker x size tier cross ----
print("\n=== Decision maker x size tier cohort % ===")
cross = pd.crosstab(df['dm'], df['company_size_tier'], values=df['is_target'], aggfunc='mean')*100
print(cross.reindex(['C-Level','VP','Director','Manager','Individual Contributor']).round(1).to_string())

# ---- Onboarding effect: quartile analysis on PAR ----
print("\n=== Onboarding quartile vs PAR and cohort share ===")
df['onb_q'] = pd.qcut(df['onboarding'], 4, labels=['Q1_low','Q2','Q3','Q4_high'])
onb_agg = df.groupby('onb_q', observed=True).agg(
    n=('roi','count'), avg_par=('par','mean'), avg_sre=('sre','mean'),
    cohort_pct=('is_target','mean'), avg_roi=('roi','mean')).reset_index()
print(onb_agg.to_string(index=False))

# ---- Fig: Onboarding quartiles ----
fig, ax = plt.subplots(figsize=(8, 5))
x = np.arange(4)
w = 0.35
ax.bar(x - w/2, onb_agg['avg_par'], w, color='#4c72b0', label='Avg product adoption rate')
ax.bar(x + w/2, 100*onb_agg['cohort_pct'], w, color='#c44e52', label='% in target cohort (right axis)')
ax2 = ax.twinx()
ax2.plot(x, onb_agg['avg_roi'], 'o-', color='#55a868', label='Avg ROI')
ax2.set_ylabel('Avg ROI ratio')
ax.set_xticks(x); ax.set_xticklabels(['Q1 (low)','Q2','Q3','Q4 (high)'])
ax.set_ylabel('Rate / %')
ax.set_title('Onboarding Score Quartiles: Adoption, Cohort Share, ROI')
ax.legend(loc='upper left'); ax2.legend(loc='upper right')
plt.tight_layout()
plt.savefig("/work/fig_onboarding_quartiles.png", dpi=110)
plt.close()
print("Saved fig_onboarding_quartiles.png")

# ---- Fig: IPS vs ROI decile monotonicity ----
fig, ax = plt.subplots(figsize=(9,5))
ax.bar(ips_agg['ips_bucket'].astype(str), ips_agg['avg_roi'], color='#4c72b0', alpha=0.85)
ax.set_xlabel('Investment Priority Score (rounded)')
ax.set_ylabel('Avg ROI ratio')
ax.set_title('Average ROI by Investment Priority Score Level\n(no monotonic lift from higher IPS)')
plt.tight_layout()
plt.savefig("/work/fig_ips_roi.png", dpi=110)
plt.close()
print("Saved fig_ips_roi.png")

# ---- Additional: acquisition cost efficiency ----
print("\n=== Acquisition cost by size tier (cohort) ===")
sz = cohort.groupby('company_size_tier').agg(
    n=('acq','count'), avg_acq=('acq','mean'), avg_clv=('clv','mean'), avg_roi=('roi','mean'))
print(sz.reindex(['Startup','Small','Medium','Large','Enterprise']).to_string())

# churn in cohort by stage
print("\n=== Cohort churn & risk by lifecycle ===")
print(cohort.groupby('lifecycle_stage').agg(n=('roi','count'), avg_churn=('churn','mean'), avg_roi=('roi','mean')).reindex(['Activation','Growth','Maturity','Retention','Dormant']).to_string())

print("\nDone.")