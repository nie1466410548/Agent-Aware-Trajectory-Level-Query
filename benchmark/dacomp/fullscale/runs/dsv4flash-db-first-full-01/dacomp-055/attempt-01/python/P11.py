import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/work/analysis_final.csv")
cohort = df[df['is_target']==1].copy()
noncohort = df[df['is_target']==0].copy()
n = len(df)

# ---- 1. Component contribution: which component drives the bottom-50% composite? ----
print("=== Composite component analysis ===")
for name, col in [('sales','nsales'),('adoption','nadopt'),('resolution','nres')]:
    print(f"{name:10s} cohort_avg={cohort[col].mean():.4f}  noncohort_avg={noncohort[col].mean():.4f}")

# ---- 2. What correlates with IPS? Is IPS aligned with actual returns? ----
print("\n=== Correlations with investment_priority_score ===")
for m in ['roi','par','sre','total_sales_amount','onboarding','team_size','churn','composite']:
    r, p = stats.spearmanr(df['ips'], df[m])
    print(f"  IPS vs {m:15s}: Spearman r={r:.3f}, p={p:.2e}")

# ---- 3. health score semantics ----
print("\n=== customer_health_score semantics ===")
print("health range:", df['health'].min(), "-", df['health'].max())
r, p = stats.spearmanr(df['health'], df['churn'])
print(f"  health vs churn: r={r:.3f}, p={p:.2e}")
r, p = stats.spearmanr(df['health'], df['roi'])
print(f"  health vs roi: r={r:.3f}, p={p:.2e}")
r, p = stats.spearmanr(df['health'], df['par'])
print(f"  health vs par: r={r:.3f}, p={p:.2e}")
r, p = stats.spearmanr(df['health'], df['ips'])
print(f"  health vs ips: r={r:.3f}, p={p:.2e}")
# cohort avg health vs non
print(f"  cohort avg health={cohort['health'].mean():.3f}, noncohort={noncohort['health'].mean():.3f}")

# ---- 4. IPS overestimation segments ----
print("\n=== IPS vs ROI deciles: is the model monotonic? ===")
df['ips_decile'] = pd.qcut(df['ips'], 5, labels=['Q1_low','Q2','Q3','Q4','Q5_high'])
print(df.groupby('ips_decile', observed=True).agg(
    n=('roi','count'), avg_roi=('roi','mean'), avg_par=('par','mean'), avg_sales=('total_sales_amount','mean')).to_string())

# ---- 5. Acquisition cost analysis ----
print("\n=== Acquisition cost ===")
print(f"cohort avg acq: {cohort['acq'].mean():.2f}, median: {cohort['acq'].median():.2f}")
print(f"noncohort avg acq: {noncohort['acq'].mean():.2f}, median: {noncohort['acq'].median():.2f}")
t, p = stats.ttest_ind(cohort['acq'], noncohort['acq'], equal_var=False)
print(f"t={t:.2f}, p={p:.2e}")

# ---- 6. Decision maker x company size: who gets over-invested ----
print("\n=== Decision maker x size tier: cohort concentration ===")
cross = pd.crosstab(df['dm'], df['company_size_tier'], values=df['is_target'], aggfunc='mean')*100
print(cross.round(1).to_string())

# ---- 7. Multiple regression for ROI (informal, standardized betas) ----
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
feat_df = df[['ips','onboarding','team_size','par','sre','total_sales_amount','acq']].copy()
X = feat_df.dropna()
y = df.loc[X.index,'roi']
scaler = StandardScaler()
Xs = scaler.fit_transform(X)
reg = LinearRegression().fit(Xs, y)
for name, coef in zip(X.columns, reg.coef_):
    print(f"  standardized beta for {name:18s}: {coef:+.4f}")

# ---- 8. Fig: IPS score vs composite performance scatter with segment highlight ----
fig, ax = plt.subplots(figsize=(9, 6))
sns.scatterplot(data=df, x='ips', y='composite', hue='is_target',
                hue_order=[1,0], palette={1:'#c44e52',0:'#bbbbbb'}, alpha=0.6, s=12, ax=ax)
ax.axvline(df['ips'].quantile(0.7), color='green', ls='--', lw=1.2, label=f"IPS 70th pct = {df['ips'].quantile(0.7):.2f}")
ax.axhline(df['composite'].quantile(0.5), color='blue', ls='--', lw=1.2, label=f"Composite 50th pct = {df['composite'].quantile(0.5):.3f}")
ax.set_xlabel('Investment Priority Score')
ax.set_ylabel('Composite Performance Score')
ax.set_title('Investment Priority vs Composite Performance\n(Top-right = over-invested, bottom-right = target cohort)')
ax.legend(loc='lower right')
plt.tight_layout()
plt.savefig("/work/fig_ips_composite.png", dpi=110)
plt.close()
print("Saved fig_ips_composite.png")

# ---- 9. Fig: health score semantics ----
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.boxplot(data=df, x='is_target', y='health', ax=axes[0])
axes[0].set_xticklabels(['Non-cohort','Target cohort'])
axes[0].set_title('customer_health_score by cohort')
sns.boxplot(data=df, x='is_target', y='roi', ax=axes[1])
axes[1].set_xticklabels(['Non-cohort','Target cohort'])
axes[1].set_title('ROI ratio by cohort')
plt.tight_layout()
plt.savefig("/work/fig_health_roi.png", dpi=110)
plt.close()
print("Saved fig_health_roi.png")
print("\nAll done.")