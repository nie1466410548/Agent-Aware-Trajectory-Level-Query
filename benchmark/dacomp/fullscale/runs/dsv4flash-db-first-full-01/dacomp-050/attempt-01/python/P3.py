import numpy as np, pandas as pd, json
from scipy.optimize import minimize
from scipy.stats import norm
from scipy.optimize import approx_fprime

rows = []
with open('/results/S28.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows)
print(df.shape)

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
Xa = np.column_stack([np.ones(len(X)), X.values])
names = ['Intercept'] + list(X.columns)

def negll(beta):
    z = Xa @ beta
    p = np.clip(1/(1+np.exp(-z)), 1e-9, 1-1e-9)
    return -np.mean(y*np.log(p) + (1-y)*np.log(1-p))

res = minimize(negll, np.zeros(Xa.shape[1]), method='BFGS')
beta = res.x
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
out['p'] = 2*(1-norm.cdf(np.abs(beta/se)))
out.index = names
print(out.round(4).to_string())
print("Intercept prob (all refs):", round(1/(1+np.exp(-beta[0])),4))

# Predicted probabilities for illustrative scenarios
def predict(fin, acad, sat, hours, age=22, male=0, fam=0, sleep_lt5=0, sleep_56=0, diet_unhealthy=0, diet_mod=0):
    feats = np.array([fin, acad, sat, hours, age, male, fam, sleep_lt5, sleep_56, diet_unhealthy, diet_mod], dtype=float)
    return 1/(1+np.exp(-(beta[0] + np.dot(beta[1:], feats))))

print("\nScenario predicted probabilities (baseline: fin=1,acad=1,sat=4,hours=6,age22,Healthy,7-8h):")
print("Low stress, healthy lifestyle:", round(predict(1,1,4,6),3))
print("High fin + high acad:", round(predict(5,5,2,10),3))
print("High fin + high acad + Unhealthy + <5h sleep:", round(predict(5,5,2,10, sleep_lt5=1, diet_unhealthy=1),3))
