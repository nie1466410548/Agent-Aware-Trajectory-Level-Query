import numpy as np, pandas as pd, json

df = pd.read_json('/work/diamonds_analysis.json')

# Regression: log(price) ~ log(carat) + cut + color + clarity + depth + table
df['log_price'] = np.log(df['price'])
df['log_carat'] = np.log(df['carat'])

cut_order = ['Fair','Good','Very Good','Premium','Ideal']
color_order = ['J','I','H','G','F','E','D']
clarity_order = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

df['cut'] = pd.Categorical(df['cut'], categories=cut_order, ordered=True)
df['color'] = pd.Categorical(df['color'], categories=color_order, ordered=True)
df['clarity'] = pd.Categorical(df['clarity'], categories=clarity_order, ordered=True)

# design matrix: continuous + one-hot (drop first)
X = pd.get_dummies(df[['cut','color','clarity']], drop_first=True, dtype=float)
X = pd.concat([df[['log_carat','depth','tbl']], X], axis=1)
X.insert(0, 'const', 1.0)
y = df['log_price'].values
Xm = X.values

# OLS via normal equations with pinv
beta, res, rank, sv = np.linalg.lstsq(Xm, y, rcond=None)
yhat = Xm @ beta
n, p = Xm.shape
dof = n - p
ss_res = np.sum((y - yhat)**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
sigma2 = ss_res/dof
covb = sigma2 * np.linalg.inv(Xm.T @ Xm)
se = np.sqrt(np.diag(covb))
tvals = beta / se
pvals = 2*(1 - __import__('scipy').stats.t.cdf(np.abs(tvals), dof))

res_df = pd.DataFrame({'coef': beta, 'se': se, 't': tvals, 'p': pvals}, index=X.columns)
res_df['exp_coef'] = np.exp(beta)
print(f"R^2 = {r2:.4f}, n={n}, p={p}")
print(res_df.round(4).to_string())

# Also simple model log price ~ log carat only
X2 = np.column_stack([np.ones(n), df['log_carat'].values])
b2 = np.linalg.lstsq(X2, y, rcond=None)[0]
yhat2 = X2 @ b2
r2_simple = 1 - np.sum((y-yhat2)**2)/ss_tot
print(f"\nSimple log-log R^2 = {r2_simple:.4f}, slope = {b2[1]:.4f}")

res_df.to_json('/work/regression_coefs.json')
