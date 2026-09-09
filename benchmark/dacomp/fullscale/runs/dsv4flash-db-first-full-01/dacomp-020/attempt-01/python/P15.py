import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')
mh = df['Mental health score'].values.astype(float)
exam = df['Exam score'].values

# Piecewise linear regression with knot at MH=5.5
knot = 5.5
d1 = np.clip(mh - knot, 0, None)  # linear spline basis
X = np.column_stack([np.ones(len(df)), mh, d1])
beta = np.linalg.pinv(X.T @ X) @ X.T @ exam
resid = exam - X @ beta
rss = resid @ resid
tss = np.sum((exam - exam.mean())**2)
r2_pw = 1 - rss/tss
n, k = X.shape
sigma2 = rss/(n-k)
se = np.sqrt(np.diag(np.linalg.pinv(X.T @ X) * sigma2))
t_slope2 = beta[2]/se[2]
p_slope2 = 2*stats.t.sf(abs(t_slope2), n-k)
print(f"Piecewise linear (knot at {knot}): R2={r2_pw:.4f}")
print(f"  Slope below {knot}: {beta[1]:.3f}")
print(f"  Slope above {knot}: {beta[1]+beta[2]:.3f}")
print(f"  Slope change: {beta[2]:.3f}, se={se[2]:.3f}, t={t_slope2:.2f}, p={p_slope2:.4f}")

# Compare to simple linear R2
X_lin = np.column_stack([np.ones(len(df)), mh])
beta_lin = np.linalg.pinv(X_lin.T @ X_lin) @ X_lin.T @ exam
rss_lin = np.sum((exam - X_lin @ beta_lin)**2)
r2_lin = 1 - rss_lin/tss
f_pw = ((rss_lin - rss)/1)/(rss/(n-k))
p_pw = 1 - stats.f.cdf(f_pw, 1, n-k)
print(f"  F-test vs linear: F={f_pw:.3f}, p={p_pw:.4f}, delta_R2={r2_pw-r2_lin:.4f}")

# Alternative knots
for knot in [4.5, 5.0, 6.0, 6.5]:
    d1 = np.clip(mh - knot, 0, None)
    Xt = np.column_stack([np.ones(len(df)), mh, d1])
    bt = np.linalg.pinv(Xt.T @ Xt) @ Xt.T @ exam
    rt = exam - Xt @ bt
    rss_t = rt @ rt
    n_t, k_t = Xt.shape
    sig2_t = rss_t/(n_t-k_t)
    se_t = np.sqrt(np.diag(np.linalg.pinv(Xt.T @ Xt) * sig2_t))
    tt = bt[2]/se_t[2]
    pt = 2*stats.t.sf(abs(tt), n_t-k_t)
    ft = ((rss_lin - rss_t)/1)/(rss_t/(n_t-k_t))
    pft = 1 - stats.f.cdf(ft, 1, n_t-k_t)
    print(f"Knot {knot}: slope_chg={bt[2]:.3f}, t={tt:.2f}, p={pt:.4f}, F={ft:.2f}, pF={pft:.4f}, R2={1-rss_t/tss:.4f}")

# Trend monotonicity: test group means non-decreasing
gm = df.groupby('Mental health score')['Exam score'].mean().values
print(f"\nGroup means: {np.round(gm,2)}")
print(f"Number of non-monotonic adjacent drops: {sum(np.diff(gm)<0)} out of {len(gm)-1}")
