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

# ---- Raw-scale model (1-5 units) ----
Xa_r = np.column_stack([np.ones(n), X.values])
def nll(b):
    z = Xa_r @ b
    p = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    return -np.mean(y*np.log(p)+(1-y)*np.log(1-p))
def nllg(b):
    z = Xa_r @ b
    p = np.clip(1/(1+np.exp(-z)), 1e-12, 1-1e-12)
    return nll(b), Xa_r.T@(p-y)/n
res = minimize(lambda b: nllg(b)[0], np.zeros(Xa_r.shape[1]), jac=lambda b: nllg(b)[1], method='BFGS', options={'maxiter':20000,'gtol':1e-12})
b = res.x
z = Xa_r @ b
p = np.clip(1/(1+np.exp(-z)),1e-12,1-1e-12)
I = (Xa_r.T * (p*(1-p))) @ Xa_r   # observed information = SUM, not mean
cov = np.linalg.inv(I)
se = np.sqrt(np.diag(cov))
or_ = np.exp(b)
outr = pd.DataFrame({'coef': b, 'se': se, 'OR': or_,
                     'CI_lo': np.exp(b-1.96*se), 'CI_hi': np.exp(b+1.96*se),
                     'p': 2*(1-norm.cdf(np.abs(b/se)))}, index=names)
pd.set_option('display.width', 220)
print("Logistic Regression on raw 1-5 scale (OR per unit; ref: Healthy diet, 7-8h/More-8h sleep):")
print(outr.round(4).to_string())
np.save('/work/beta_raw.npy', b)

def pred(fin, acad, sat, hours, age=22, male=0, fam=0, slt5=0, s56=0, du=0, dm=0):
    f = np.array([fin, acad, sat, hours, age, male, fam, slt5, s56, du, dm], float)
    return 1/(1+np.exp(-(b[0]+b[1:]@f)))
print("\n--- Predicted probability of ever having suicidal thoughts ---")
print("Protective profile (fin=1, acad=1, sat=4, hrs=6, Healthy, 7-8h):", round(pred(1,1,4,6),3))
print("High financial stress only (fin=5):", round(pred(5,1,4,6),3))
print("High academic stress only (acad=5):", round(pred(1,5,4,6),3))
print("High both (fin=5, acad=5, sat=2, hrs=10):", round(pred(5,5,2,10),3))
print("High both + Unhealthy diet + <5h sleep:", round(pred(5,5,2,10,slt5=1,du=1),3))
print("High both + Unhealthy + <5h + family history:", round(pred(5,5,2,10,slt5=1,du=1,fam=1),3))
