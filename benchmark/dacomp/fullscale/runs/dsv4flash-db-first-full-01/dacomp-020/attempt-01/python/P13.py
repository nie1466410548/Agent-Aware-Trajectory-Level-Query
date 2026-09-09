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

# HC1 robust covariance
hat = X @ np.linalg.pinv(X.T @ X) @ X.T  # hat matrix
hii = np.diag(hat)
XWX = X.T @ (X * resid**2)  # HC0
XtX_inv = np.linalg.pinv(X.T @ X)
cov_hc0 = XtX_inv @ XWX @ XtX_inv
cov_hc1 = cov_hc0 * (n/(n-k))
cov_hc3 = XtX_inv @ (X.T @ (X * (resid**2/(1-hii)**2))) @ XtX_inv

se_hc1 = np.sqrt(np.diag(cov_hc1))
se_hc3 = np.sqrt(np.diag(cov_hc3))
t_hc1 = beta/se_hc1
p_hc1 = 2*(1-stats.t.cdf(np.abs(t_hc1), n-k))

names = ['Intercept'] + list(base.columns)
idx_mh = names.index('Mental health score')
print(f"Mental health score coefficient = {beta[idx_mh]:.4f}")
print(f"  Classical SE = {np.sqrt(np.diag(XtX_inv*sigma2))[idx_mh]:.4f}, t={beta[idx_mh]/np.sqrt(np.diag(XtX_inv*sigma2))[idx_mh]:.2f}")
print(f"  HC1 robust SE = {se_hc1[idx_mh]:.4f}, t={t_hc1[idx_mh]:.2f}, p={p_hc1[idx_mh]:.2e}")
print(f"  HC3 robust SE = {se_hc3[idx_mh]:.4f}")
print(f"  HC1 95% CI = [{beta[idx_mh]-1.96*se_hc1[idx_mh]:.3f}, {beta[idx_mh]+1.96*se_hc1[idx_mh]:.3f}]")
print(f"  HC3 95% CI = [{beta[idx_mh]-1.96*se_hc3[idx_mh]:.3f}, {beta[idx_mh]+1.96*se_hc3[idx_mh]:.3f}]")

# Exact p-value bound for t=25.24
print(f"\nP-value for t=25.24 with df=985: p < {stats.t.sf(25.24, 985)*2:.3e}")

# Also confirm MH slope difference between attendance levels using the interaction model SE
# Interaction model for attendance
X_att = np.column_stack([np.ones(len(df)), base, df['Mental health score']*df['Attendance rate']])
beta_att = np.linalg.pinv(X_att.T @ X_att) @ X_att.T @ y
resid_att = y - X_att @ beta_att
n2 = len(y); k2 = X_att.shape[1]
sigma2_att = resid_att @ resid_att / (n2-k2)
se_att = np.sqrt(np.diag(np.linalg.pinv(X_att.T @ X_att)*sigma2_att))
print(f"\nMHxAttendance interaction b={beta_att[-1]:.4f}, se={se_att[-1]:.4f}, t={beta_att[-1]/se_att[-1]:.2f}, p={2*stats.t.sf(abs(beta_att[-1]/se_att[-1]), n2-k2):.2e}")

# Interaction model for social media
X_sm = np.column_stack([np.ones(len(df)), base, df['Mental health score']*df['Social media usage time']])
beta_sm = np.linalg.pinv(X_sm.T @ X_sm) @ X_sm.T @ y
resid_sm = y - X_sm @ beta_sm
sigma2_sm = resid_sm @ resid_sm / (n2-k2)
se_sm = np.sqrt(np.diag(np.linalg.pinv(X_sm.T @ X_sm)*sigma2_sm))
print(f"MHxSocialMedia interaction b={beta_sm[-1]:.4f}, se={se_sm[-1]:.4f}, t={beta_sm[-1]/se_sm[-1]:.2f}, p={2*stats.t.sf(abs(beta_sm[-1]/se_sm[-1]), n2-k2):.2e}")
