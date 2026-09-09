import numpy as np, pandas as pd, json
from scipy.optimize import minimize, approx_fprime
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

print("y mean:", y.mean())
print("X stats:", X.describe().to_string())

# Standardize for better convergence
X_mean = X.mean(axis=0)
X_std = X.std(axis=0)
X_std[X_std==0] = 1
Xs = (X - X_mean) / X_std

Xa = np.column_stack([np.ones(len(Xs)), Xs.values])
names = ['Intercept'] + list(X.columns)

def negll(beta):
    z = Xa @ beta
    p = np.clip(1/(1+np.exp(-z)), 1e-15, 1-1e-15)
    return -np.mean(y*np.log(p) + (1-y)*np.log(1-p))

# Try with different starting point
beta0 = np.zeros(Xa.shape[1])
beta0[0] = np.log(y.mean()/(1-y.mean()))  # set intercept to log-odds of baseline
print("Init negll:", negll(beta0))

res = minimize(negll, beta0, method='L-BFGS-B', options={'maxiter':10000, 'gtol':1e-12, 'ftol':1e-15})
print("Success:", res.success, "niter:", res.nit, "nfev:", res.nfev, "negll:", res.fun)
beta = res.x
print("Beta nonzero:", (np.abs(beta)>0.001).sum())

# Hessian
g = approx_fprime(beta, negll, 1e-5)
eps = 1e-4
H = np.zeros((len(beta), len(beta)))
for i in range(len(beta)):
    ei = np.zeros(len(beta)); ei[i]=eps
    H[:,i] = (approx_fprime(beta+ei, negll, 1e-5) - g)/eps

Hinv = np.linalg.inv(H)
se = np.sqrt(np.abs(np.diag(Hinv)))
or_ = np.exp(beta)
ci_lo = np.exp(beta - 1.96*se)
ci_hi = np.exp(beta + 1.96*se)
pvals = 2*(1-norm.cdf(np.abs(beta/se)))

out = pd.DataFrame({'coef_std': beta, 'se': se, 'OR': or_, 'CI_lo': ci_lo, 'CI_hi': ci_hi, 'p': pvals}, index=names)
print("\nLogistic Regression Results (standardized features):")
print(out.round(4).to_string())