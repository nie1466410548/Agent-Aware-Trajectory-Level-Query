import numpy as np, pandas as pd, json
from scipy.optimize import minimize
from scipy.stats import norm

cols = ['suicidal','Gender','Age','Academic stress','Financial stress','Satisfaction with studies','Work/study hours','Sleep duration','Dietary habits','Family history of mental illness']
rows = []
with open('/results/S28.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows, columns=cols)
df['y'] = (df['suicidal']=='Yes').astype(int)
df['male'] = (df['Gender']=='Male').astype(int)
df['fam'] = (df['Family history of mental illness']=='Yes').astype(int)
sleep = pd.get_dummies(df['Sleep duration'], prefix='sleep')
diet = pd.get_dummies(df['Dietary habits'], prefix='diet')
X = pd.concat([
    df[['Academic stress','Financial stress','Satisfaction with studies','Work/study hours','Age','male','fam']],
    sleep[['sleep_Less than 5 hours','sleep_5-6 hours']],
    diet[['diet_Unhealthy','diet_Moderate']]
], axis=1).astype(float)
y = df['y'].values
mask = np.isfinite(X).all(axis=1)
X, y = X[mask], y[mask]
n = len(y)
names = ['Intercept'] + list(X.columns)

Xm = X.mean(axis=0); Xs_ = X.std(axis=0)
Xz = (X - Xm)/Xs_
Xa = np.column_stack([np.ones(n), Xz.values])

def negll_grad(beta):
    z = Xa @ beta
    p = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    ll = -np.mean(y*np.log(p) + (1-y)*np.log(1-p))
    grad = Xa.T @ (p - y) / n
    return ll, grad

res = minimize(lambda b: negll_grad(b)[0], np.zeros(Xa.shape[1]), jac=lambda b: negll_grad(b)[1], method='BFGS', options={'maxiter':10000,'gtol':1e-10})
beta = res.x
print("Success:", res.success, "nfev:", res.nfev, "nit:", res.nit)

# Analytic Hessian at optimum
z = Xa @ beta
p = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
H = (Xa.T * (p*(1-p))) @ Xa / n
Hinv = np.linalg.inv(H)
se = np.sqrt(np.diag(Hinv))
or_ = np.exp(beta)
ci_lo = np.exp(beta - 1.96*se)
ci_hi = np.exp(beta + 1.96*se)
pvals = 2*(1-norm.cdf(np.abs(beta/se)))
out = pd.DataFrame({'coef_std': beta, 'se': se, 'OR_per_SD': or_, 'CI_lo': ci_lo, 'CI_hi': ci_hi, 'p': pvals}, index=names)
pd.set_option('display.width', 220)
print("\nLogistic Regression (standardized predictors; OR per 1 SD):")
print(out.round(4).to_string())
print("Baseline (mean features) predicted prob:", round(1/(1+np.exp(-beta[0])),4))

# Fit raw-scale model using analytic gradient too
Xa_r = np.column_stack([np.ones(n), X.values])
def nllr(b):
    z = Xa_r @ b
    pp = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    return -np.mean(y*np.log(pp)+(1-y)*np.log(1-pp))
def nllr_grad(b):
    z = Xa_r @ b
    pp = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    return nllr(b), Xa_r.T @ (pp - y)/n
resr = minimize(lambda b: nllr_grad(b)[0], np.zeros(Xa_r.shape[1]), jac=lambda b: nllr_grad(b)[1], method='BFGS', options={'maxiter':10000,'gtol':1e-10})
braw = resr.beta if hasattr(resr,'beta') else resr.x
np.save('/work/beta_raw.npy', braw)
zr = Xa_r @ braw
pr = np.clip(1/(1+np.exp(-zr)),1e-12,1-1e-12)
Hr = (Xa_r.T * (pr*(1-pr))) @ Xa_r / n
se_r = np.sqrt(np.diag(np.linalg.inv(Hr)))
outr = pd.DataFrame({'coef': braw, 'se': se_r, 'OR': np.exp(braw),
                     'CI_lo': np.exp(braw-1.96*se_r), 'CI_hi': np.exp(braw+1.96*se_r),
                     'p': 2*(1-norm.cdf(np.abs(braw/se_r)))}, index=names)
print("\nLogistic Regression (raw 1-5 scale predictors; OR per unit):")
print(outr.round(4).to_string())

def pred(fin, acad, sat, hours, age=22, male=0, fam=0, slt5=0, s56=0, du=0, dm=0):
    f = np.array([fin, acad, sat, hours, age, male, fam, slt5, s56, du, dm], float)
    return 1/(1+np.exp(-(braw[0]+braw[1:]@f)))

print("\n--- Predicted probabilities ---")
print("Low stress healthy (fin=1,acad=1,sat=4,hours=6):", round(pred(1,1,4,6),3))
print("High financial only (fin=5,acad=1,sat=4,hours=6):", round(pred(5,1,4,6),3))
print("High academic only (fin=1,acad=5,sat=4,hours=6):", round(pred(1,5,4,6),3))
print("High both (fin=5,acad=5,sat=2,hours=10):", round(pred(5,5,2,10),3))
print("High both + Unhealthy + <5h:", round(pred(5,5,2,10,slt5=1,du=1),3))
print("High both + Unhealthy + <5h + fam:", round(pred(5,5,2,10,slt5=1,du=1,fam=1),3))
