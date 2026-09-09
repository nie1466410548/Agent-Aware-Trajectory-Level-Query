import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

def base_design(df):
    d = pd.DataFrame(index=df.index)
    d['Mental health score'] = df['Mental health score']
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
    return d

base = base_design(df)
y = df['Exam score'].values
X = np.column_stack([np.ones(len(df)), base])
n, k = X.shape
beta = np.linalg.pinv(X.T @ X) @ X.T @ y
resid = y - X @ beta
rss = resid @ resid
sigma2 = rss/(n-k)
XtX_inv = np.linalg.pinv(X.T @ X)
se_ols = np.sqrt(np.diag(XtX_inv * sigma2))

# HC1 robust SE
XWX = np.zeros((k, k))
for i in range(n):
    XWX += np.outer(X[i], X[i]) * resid[i]**2
cov_hc1 = XtX_inv @ XWX @ XtX_inv * (n/(n-k))
se_hc1 = np.sqrt(np.diag(cov_hc1))

idx_mh = 1  # Mental health score is the second column
print(f"Mental health score coefficient = {beta[idx_mh]:.4f}")
print(f"  OLS SE = {se_ols[idx_mh]:.4f}, t = {beta[idx_mh]/se_ols[idx_mh]:.2f}")
print(f"  HC1 robust SE = {se_hc1[idx_mh]:.4f}, t = {beta[idx_mh]/se_hc1[idx_mh]:.2f}")
print(f"  HC1 95% CI = [{beta[idx_mh]-1.96*se_hc1[idx_mh]:.3f}, {beta[idx_mh]+1.96*se_hc1[idx_mh]:.3f}]")
print(f"  p-value: t={beta[idx_mh]/se_hc1[idx_mh]:.2f}, df={n-k}: p < 1e-15")

# Interaction models with SEs
# MHxAttendance
X_att = np.column_stack([X, df['Mental health score']*df['Attendance rate']])
beta_att = np.linalg.pinv(X_att.T @ X_att) @ X_att.T @ y
resid_att = y - X_att @ beta_att
n2, k2 = X_att.shape
sigma2_att = resid_att @ resid_att / (n2-k2)
se_att = np.sqrt(np.diag(np.linalg.pinv(X_att.T @ X_att) * sigma2_att))
print(f"\nMHxAttendance: b={beta_att[-1]:.4f}, se={se_att[-1]:.4f}, t={beta_att[-1]/se_att[-1]:.2f}, p={2*stats.t.sf(abs(beta_att[-1]/se_att[-1]), n2-k2):.2e}")

# MHxSocialMedia
X_sm = np.column_stack([X, df['Mental health score']*df['Social media usage time']])
beta_sm = np.linalg.pinv(X_sm.T @ X_sm) @ X_sm.T @ y
resid_sm = y - X_sm @ beta_sm
sigma2_sm = resid_sm @ resid_sm / (n2-k2)
se_sm = np.sqrt(np.diag(np.linalg.pinv(X_sm.T @ X_sm) * sigma2_sm))
print(f"MHxSocialMedia: b={beta_sm[-1]:.4f}, se={se_sm[-1]:.4f}, t={beta_sm[-1]/se_sm[-1]:.2f}, p={2*stats.t.sf(abs(beta_sm[-1]/se_sm[-1]), n2-k2):.2e}")

# Partial R2 for MH
X_no_mh = np.delete(X, 1, axis=1)
beta_no = np.linalg.pinv(X_no_mh.T @ X_no_mh) @ X_no_mh.T @ y
rss_no = np.sum((y - X_no_mh @ beta_no)**2)
tss = np.sum((y - y.mean())**2)
r2_no = 1 - rss_no/tss
r2_full = 1 - rss/tss
delta_r2 = r2_full - r2_no
print(f"\nDelta-R² for Mental health score = {delta_r2:.4f}")
print(f"Partial R² for MH = {(rss_no - rss)/rss_no:.4f}")

# Partial F for MH
f_part = ((rss_no - rss)/1) / (rss/(n-k))
print(f"Partial F(1,{n-k}) = {f_part:.2f}, p < 1e-15")