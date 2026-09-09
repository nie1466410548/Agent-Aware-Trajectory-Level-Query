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

# Drop NaN
mask = np.isfinite(X).all(axis=1)
print("Dropped rows with NaN:", (~mask).sum())
X = X[mask]
y = y[mask]

X_mean = X.mean(axis=0); X_std = X.std(axis=0)
Xs = (X - X_mean) / X_std
Xa = np.column_stack([np.ones(len(Xs)), Xs.values])
names = ['Intercept'] + list(X.columns)

def negll(beta):
    z = Xa @ beta
    p = np.clip(1/(1+np.exp(-z)), 1e-15, 1-1e-15)
    return -np.mean(y*np.log(p) + (1-y)*np.log(1-p))

beta0 = np.zeros(Xa.shape[1])
beta0[0] = np.log(y.mean()/(1-y.mean()))
print("Init negll:", round(negll(beta0),4))

res = minimize(negll, beta0, method='L-BFGS-B', options={'maxiter':10000,'gtol':1e-12,'ftol':1e-15})
print("Success:", res.success, "nfev:", res.nfev, "negll:", round(res.fun,4))
beta = res.x

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
pd.set_option('display.width', 200)
print("\nLogistic Regression Results (standardized features; OR per 1 SD):")
print(out.round(4).to_string())

# Save raw-scale model for scenario prediction: fit on raw X with clean data
Xa_raw = np.column_stack([np.ones(len(X)), X.values])
res_raw = minimize(lambda b: (lambda z: -np.mean(y*np.log(np.clip(1/(1+np.exp(-z)),1e-15,1-1e-15)) + (1-y)*np.log(np.clip(1/(1+np.exp(-z)),1e-15,1-1e-15))))(Xa_raw@b), np.zeros(Xa_raw.shape[1]), method='L-BFGS-B', options={'maxiter':10000,'gtol':1e-12,'ftol':1e-15})
braw = res_raw.x
np.save('/work/beta_raw.npy', braw)
print("Raw-scale converged:", res_raw.success)

def predict_scenario(fin, acad, sat, hours, age=22, male=0, fam=0, sleep_lt5=0, sleep_56=0, diet_unhealthy=0, diet_mod=0):
    feats = np.array([fin, acad, sat, hours, age, male, fam, sleep_lt5, sleep_56, diet_unhealthy, diet_mod], dtype=float)
    return 1/(1+np.exp(-(braw[0] + np.dot(braw[1:], feats))))

print("\n--- Predicted probabilities ---")
print("Low stress healthy (fin=1,acad=1,sat=4,hours=6):", round(predict_scenario(1,1,4,6),4))
print("High financial only (fin=5,acad=1,sat=4,hours=6):", round(predict_scenario(5,1,4,6),4))
print("High academic only (fin=1,acad=5,sat=4,hours=6):", round(predict_scenario(1,5,4,6),4))
print("High both (fin=5,acad=5,sat=2,hours=10):", round(predict_scenario(5,5,2,10),4))
print("High both + Unhealthy + <5h:", round(predict_scenario(5,5,2,10, sleep_lt5=1, diet_unhealthy=1),4))
print("High both + Unhealthy + <5h + fam:", round(predict_scenario(5,5,2,10, sleep_lt5=1, diet_unhealthy=1, fam=1),4))
