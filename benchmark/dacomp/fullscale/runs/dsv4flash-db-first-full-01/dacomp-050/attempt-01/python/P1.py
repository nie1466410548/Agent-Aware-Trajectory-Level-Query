import numpy as np, pandas as pd, json, os
from scipy.optimize import minimize

rows = []
with open('results/S28.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows)
print(df.shape)
print(df.head(2))

# Build design matrix
df['y'] = (df['suicidal']=='Yes').astype(int)
df['male'] = (df['Gender']=='Male').astype(int)
df['fam'] = (df['Family history of mental illness']=='Yes').astype(int)
sleep = pd.get_dummies(df['Sleep duration'], prefix='sleep')
diet = pd.get_dummies(df['Dietary habits'], prefix='diet')
X = pd.concat([
    df[['Academic stress','Financial stress','Satisfaction with studies','Work/study hours','Age','male','fam']],
    sleep[['sleep_Less than 5 hours','sleep_5-6 hours']],   # ref: 7-8 hours and More than 8 hours
    diet[['diet_Unhealthy','diet_Moderate']]                 # ref: Healthy
], axis=1).astype(float)
y = df['y'].values
Xa = np.column_stack([np.ones(len(X)), X.values])
names = ['Intercept'] + list(X.columns)

def negll(beta):
    z = Xa @ beta
    p = 1/(1+np.exp(-z))
    p = np.clip(p, 1e-9, 1-1e-9)
    return -np.mean(y*np.log(p) + (1-y)*np.log(1-p))

beta0 = np.zeros(Xa.shape[1])
res = minimize(negll, beta0, method='BFGS')
beta = res.x
# Hessian for SEs via finite diff
from scipy.optimize import approx_fprime
g = approx_fprime(beta, negll, 1e-5)
eps = 1e-4
H = np.zeros((len(beta), len(beta)))
for i in range(len(beta)):
    ei = np.zeros(len(beta)); ei[i]=eps
    H[:,i] = (approx_fprime(beta+ei, negll, 1e-5) - g)/eps
se = np.sqrt(np.abs(np.diag(np.linalg.inv(H))))

out = pd.DataFrame({'coef': beta, 'se': se, 'OR': np.exp(beta)})
out['ci_lo'] = np.exp(beta - 1.96*se)
out['ci_hi'] = np.exp(beta + 1.96*se)
out['p'] = 2*(1-__import__('scipy').stats.norm.cdf(np.abs(beta/se)))
print(out.round(4).to_string())
print("baseline pred prob:", round(1/(1+np.exp(-beta[0])),4))
