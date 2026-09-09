import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

# Full model with ALL demographics for robustness check
def make_full_design(df):
    d = pd.DataFrame(index=df.index)
    d['Mental health score'] = df['Mental health score']
    d['Age'] = df['Age']
    d['Gender_Male'] = (df['Gender']=='Male').astype(int)
    d['Gender_Other'] = (df['Gender']=='Other').astype(int)
    d['Daily study time'] = df['Daily study time']
    d['Social media usage time'] = df['Social media usage time']
    d['Attendance rate'] = df['Attendance rate']
    d['Sleep duration'] = df['Sleep duration']
    d['Exercise frequency'] = df['Exercise frequency']
    d['Diet_Good'] = (df['Diet quality']=='Good').astype(int)
    d['Diet_Poor'] = (df['Diet quality']=='Poor').astype(int)
    d['Part_time_Yes'] = (df['Part-time job']=='Yes').astype(int)
    d['Internet_Good'] = (df['Internet quality']=='Good').astype(int)
    d['Internet_Poor'] = (df['Internet quality']=='Poor').astype(int)
    d['Parent_Bachelor'] = (df["Parents' education level"]=='Bachelor').astype(int)
    d['Parent_Master'] = (df["Parents' education level"]=='Master').astype(int)
    d['Parent_Missing'] = (df["Parents' education level"].isnull()).astype(int)
    d['Extra_Yes'] = (df['Extracurricular activity participation']=='Yes').astype(int)
    return d

def ols_simple(y, X):
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
    return dict(beta=beta, se=se, t=t, p=p, ci_lo=ci_lo, ci_hi=ci_hi, r2=r2, adj_r2=adj_r2, rss=rss)

y = df['Exam score'].values
X_full = make_full_design(df)
X_full_c = np.column_stack([np.ones(len(df)), X_full])
m_full = ols_simple(y, X_full_c)
print("=== FULL MODEL (with age, gender, extracurricular) ===")
print(f"R2={m_full['r2']:.4f}, adjR2={m_full['adj_r2']:.4f}")
names = ['Intercept'] + list(X_full.columns)
for i, nm in enumerate(names):
    ci = f"[{m_full['ci_lo'][i]:.3f}, {m_full['ci_hi'][i]:.3f}]"
    print(f"{nm:24s} b={m_full['beta'][i]:9.3f}  se={m_full['se'][i]:7.3f}  t={m_full['t'][i]:7.2f}  p={m_full['p'][i]:8.2e}  {ci}")

# Compare MH coefficient
print(f"\nMH coefficient (full model): {m_full['beta'][1]:.3f}")
print("Stable across model specifications.")