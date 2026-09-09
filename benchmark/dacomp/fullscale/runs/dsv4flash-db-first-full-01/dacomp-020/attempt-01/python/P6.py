import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

# Prepare design matrix with controls
def make_design(df, add_mh=True, add_extras=False, add_interactions_with=None):
    d = pd.DataFrame(index=df.index)
    if add_mh:
        d['Mental health score'] = df['Mental health score']
    d['Daily study time'] = df['Daily study time']
    d['Social media usage time'] = df['Social media usage time']
    d['Attendance rate'] = df['Attendance rate']
    d['Sleep duration'] = df['Sleep duration']
    d['Exercise frequency'] = df['Exercise frequency']
    # dummies with reference categories
    d['Diet_Good'] = (df['Diet quality']=='Good').astype(int)
    d['Diet_Poor'] = (df['Diet quality']=='Poor').astype(int)
    d['Part_time_Yes'] = (df['Part-time job']=='Yes').astype(int)
    d['Internet_Good'] = (df['Internet quality']=='Good').astype(int)
    d['Internet_Poor'] = (df['Internet quality']=='Poor').astype(int)
    d['Parent_Bachelor'] = (df["Parents' education level"]=='Bachelor').astype(int)
    d['Parent_Master'] = (df["Parents' education level"]=='Master').astype(int)
    d['Parent_Missing'] = (df["Parents' education level"].isnull()).astype(int)
    if add_extras:
        d['Age'] = df['Age']
        d['Gender_Male'] = (df['Gender']=='Male').astype(int)
        d['Gender_Other'] = (df['Gender']=='Other').astype(int)
        d['Extra_Yes'] = (df['Extracurricular activity participation']=='Yes').astype(int)
    if add_interactions_with is not None:
        for var in add_interactions_with:
            d[f'MHx{var}'] = df['Mental health score'] * d[var]
    return d

def ols(y, X):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    XtX = X.T @ X
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    resid = y - yhat
    rss = resid @ resid
    tss = np.sum((y - y.mean())**2)
    r2 = 1 - rss/tss
    adj_r2 = 1 - (1-r2)*(n-1)/(n-k)
    sigma2 = rss/(n-k)
    cov_b = sigma2 * XtX_inv
    se = np.sqrt(np.diag(cov_b))
    t = beta/se
    p = 2*(1 - stats.t.cdf(np.abs(t), n-k))
    ci_lo = beta - stats.t.ppf(0.975, n-k)*se
    ci_hi = beta + stats.t.ppf(0.975, n-k)*se
    return dict(beta=beta, se=se, t=t, p=p, ci_lo=ci_lo, ci_hi=ci_hi, r2=r2, adj_r2=adj_r2,
                rss=rss, n=n, k=k, yhat=yhat, resid=resid)

y = df['Exam score'].values

# Model 1: MH + controls (question 2 specification)
X1 = make_design(df, add_mh=True)
X1_const = np.column_stack([np.ones(len(df)), X1])
m1 = ols(y, X1_const)
print("=== MODEL 1: MH + full controls ===")
print(f"n={m1['n']}, k={m1['k']}, R2={m1['r2']:.4f}, adjR2={m1['adj_r2']:.4f}")
names = ['Intercept'] + list(X1.columns)
for i, nm in enumerate(names):
    print(f"{nm:24s} b={m1['beta'][i]:9.3f}  se={m1['se'][i]:7.3f}  t={m1['t'][i]:7.2f}  p={m1['p'][i]:8.2e}  CI=[{m1['ci_lo'][i]:.3f}, {m1['ci_hi'][i]:.3f}]")

# Model 0: controls only (no MH)
X0 = make_design(df, add_mh=False)
X0_const = np.column_stack([np.ones(len(df)), X0])
m0 = ols(y, X0_const)
print(f"\nModel 0 (controls only): R2={m0['r2']:.4f}")

# delta-R2 for MH
delta_r2 = m1['r2'] - m0['r2']
print(f"Delta-R2 for Mental health score = {delta_r2:.4f}")

# Partial F-test for MH term
df_extra = m1['k'] - m0['k']  # 1
f_part = ((m0['rss'] - m1['rss'])/df_extra) / (m1['rss']/(m1['n']-m1['k']))
p_part = 1 - stats.f.cdf(f_part, df_extra, m1['n']-m1['k'])
print(f"Partial F for MH = {f_part:.3f}, p = {p_part:.3e}")

# Standardized beta for MH (effect size)
sd_mh = df['Mental health score'].std(ddof=1)
sd_exam = df['Exam score'].std(ddof=1)
std_beta = m1['beta'][1] * sd_mh / sd_exam
print(f"Standardized beta (MH) = {std_beta:.4f}")
print(f"Per-1-MH-point effect = {m1['beta'][1]:.3f} exam points")

# Also crude model for comparison
X_crude = np.column_stack([np.ones(len(df)), df['Mental health score'].values.astype(float)])
m_crude = ols(y, X_crude)
print(f"\nCrude MH-only: b={m_crude['beta'][1]:.3f}, R2={m_crude['r2']:.4f}, p={m_crude['p'][1]:.2e}")
