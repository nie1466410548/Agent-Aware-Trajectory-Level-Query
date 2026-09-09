import numpy as np, pandas as pd, json
from scipy.optimize import minimize

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
Xm = X.mean(axis=0); Xs_ = X.std(axis=0)
Xz = (X - Xm)/Xs_
Xa = np.column_stack([np.ones(n), Xz.values])

def nll_g(b):
    z = Xa @ b
    p = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    return -np.mean(y*np.log(p)+(1-y)*np.log(1-p)), Xa.T@(p-y)/n

res = minimize(lambda b: nll_g(b)[0], np.zeros(Xa.shape[1]), jac=lambda b: nll_g(b)[1], method='BFGS', options={'maxiter':10000,'gtol':1e-10})
b = res.x
z = Xa @ b
p = np.clip(1/(1+np.exp(-z)),1e-12,1-1e-12)
H = (Xa.T * (p*(1-p))) @ Xa / n
print("H shape:", H.shape)
eig = np.linalg.eigvalsh(H)
print("Eigenvalues of H:", np.round(eig, 8))
print("Condition number:", np.linalg.cond(H))
print("diag of H:", np.round(np.diag(H), 6))
print("gradient norm at optimum:", np.linalg.norm(Xa.T@(p-y)/n))
print("corr matrix check:")
print(pd.DataFrame(Xz).corr().abs().unstack().sort_values(ascending=False).head(10))
