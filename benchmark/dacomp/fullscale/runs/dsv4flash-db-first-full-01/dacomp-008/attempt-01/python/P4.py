import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/project_data.csv')

# Cross tab: risk x status
print("Risk x Status composition:")
print(pd.crosstab(df['risk'], df['status']))
print()
print("Project Type x Status:")
print(pd.crosstab(df['Project Type'], df['status']))
print()

# ---- OLS regression on all projects ----
# y = deviation; X = [1, team, budget, sat, risk_Medium, risk_High]
X = pd.DataFrame({
    'const': 1.0,
    'team': df['team'],
    'budget': df['budget'],
    'sat': df['sat'],
    'risk_Medium': (df['risk']=='Medium Risk').astype(int),
    'risk_High': (df['risk']=='High Risk').astype(int),
})
y = df['deviation'].values
beta, res, rank, sv = np.linalg.lstsq(X.values, y, rcond=None)
yhat = X.values @ beta
ss_res = np.sum((y - yhat)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r2 = 1 - ss_res/ss_tot
n, k = X.shape
adj_r2 = 1 - (1-r2)*(n-1)/(n-k-1)
print("OLS: deviation ~ team + budget + sat + risk (ALL projects)")
print(f"  R2={r2:.4f}, adjR2={adj_r2:.4f}")
for name, b in zip(X.columns, beta):
    print(f"  {name}: {b:.4f}")

# ---- OLS on completed projects ----
dfc = df[df['status']=='Completed'].copy()
Xc = pd.DataFrame({
    'const': 1.0,
    'team': dfc['team'],
    'budget': dfc['budget'],
    'sat': dfc['sat'],
    'risk_Medium': (dfc['risk']=='Medium Risk').astype(int),
})
# drop risk_High as no completed high risk; add priority
Xc['priority_High'] = (dfc['Priority']=='High').astype(int)
Xc['priority_Medium'] = (dfc['Priority']=='Medium').astype(int)
yc = dfc['deviation'].values
Xcm = Xc[['const','team','budget','sat','risk_Medium','priority_High','priority_Medium']]
beta_c, res, rank, sv = np.linalg.lstsq(Xcm.values, yc, rcond=None)
yhat_c = Xcm.values @ beta_c
ss_res = np.sum((yc - yhat_c)**2)
ss_tot = np.sum((yc - np.mean(yc))**2)
r2_c = 1 - ss_res/ss_tot
nc, kc = Xcm.shape
adj_r2_c = 1 - (1-r2_c)*(nc-1)/(nc-kc-1)
print("\nOLS: deviation ~ team + budget + sat + risk_Medium + priority (COMPLETED only)")
print(f"  R2={r2_c:.4f}, adjR2={adj_r2_c:.4f}, n={nc}")
for name, b in zip(Xcm.columns, beta_c):
    print(f"  {name}: {b:.4f}")

# ---- OLS on dev_pct (all) ----
y2 = df['dev_pct'].values
beta2, res, rank, sv = np.linalg.lstsq(X.values, y2, rcond=None)
yhat2 = X.values @ beta2
ss_res2 = np.sum((y2 - yhat2)**2)
ss_tot2 = np.sum((y2 - np.mean(y2))**2)
r2b = 1 - ss_res2/ss_tot2
print("\nOLS: dev_pct ~ team + budget + sat + risk (ALL)")
print(f"  R2={r2b:.4f}")
for name, b in zip(X.columns, beta2):
    print(f"  {name}: {b:.4f}")

# Completed projects: how many are over/under budget?
print("\nCompleted projects over/under budget:")
over = (dfc['actual'] > dfc['budget']).sum()
under = (dfc['actual'] <= dfc['budget']).sum()
print(f"  Over budget: {over}, Under/At budget: {under}, total: {len(dfc)}")
print(f"  Share over budget: {over/len(dfc)*100:.1f}%")

# By project type among completed
print("\nCompleted over-budget share by type:")
for pt, g in dfc.groupby('Project Type'):
    o = (g['actual'] > g['budget']).sum()
    print(f"  {pt}: {o}/{len(g)} ({o/len(g)*100:.1f}%)")

# Average deviations by team size bucket for completed
dfc['team_bucket'] = pd.cut(dfc['team'], bins=[0,5,10,15,20,30], labels=['<=5','6-10','11-15','16-20','21+'])
print("\nCompleted: mean deviation by team size bucket:")
print(dfc.groupby('team_bucket', observed=True)['deviation'].agg(['count','mean','median']).round(2).to_string())