import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/parsed_data.csv')

# Prepare regression dataset
model_df = df[df['Decoration'].notna() & df['Orientation'].notna()].copy()

# Build features
features = pd.DataFrame(index=model_df.index)
features['watch_count'] = model_df['Watch Count'].values
features['floor_level'] = model_df['floor_num'].values
features['bedrooms'] = model_df['bedrooms'].values
features['living_rooms'] = model_df['living_rooms'].values
features['area'] = model_df['area_num'].values
features['price_sqm'] = model_df['price_sqm_num'].values

# Dummies
dec_dummies = pd.get_dummies(model_df['Decoration'], prefix='dec', drop_first=True)
ori_dummies = pd.get_dummies(model_df['Orientation'], prefix='ori', drop_first=True)

X = pd.concat([features, dec_dummies, ori_dummies], axis=1)
X = X.dropna()
y = model_df.loc[X.index, 'Showings'].values.astype(float)

X = X.astype(float)
X.insert(0, 'intercept', 1.0)

# Convert to numpy
X_mat = X.values
n, k = X_mat.shape

# OLS via normal equations
beta = np.linalg.pinv(X_mat.T @ X_mat) @ X_mat.T @ y
yhat = X_mat @ beta
resid = y - yhat
sigma2 = resid @ resid / (n - k)
se = np.sqrt(np.diag(np.linalg.pinv(X_mat.T @ X_mat)) * sigma2)
tstat = beta / se
pvals = 2 * (1 - stats.t.cdf(np.abs(tstat), df=n - k))

results = pd.DataFrame({'coef': beta, 'std_err': se, 't': tstat, 'p_value': pvals}, index=X.columns)
results['sig_01'] = results['p_value'] < 0.01

r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
print(f"OLS for Showings: n={n}, k={k}, R²={r2:.4f}")
print(results.round(6).to_string())

# Also run ANOVA for each factor separately
print("\n=== ANOVA / F-tests for Showings ===")
for factor in ['Decoration', 'Orientation', 'floor_category']:
    groups = []
    for v in df[factor].unique():
        vals = df.loc[df[factor]==v, 'Showings'].dropna().values
        if len(vals) > 5:
            groups.append(vals)
    if len(groups) > 1:
        f, p = stats.f_oneway(*groups)
        print(f"{factor}: F={f:.2f}, p={p:.2e}")

# Also check bedrooms
groups = []
for v in [1,2,3,4,5]:
    vals = df.loc[df['bedrooms']==v, 'Showings'].dropna().values
    if len(vals) > 5:
        groups.append(vals)
f, p = stats.f_oneway(*groups)
print(f"bedrooms (1-5): F={f:.2f}, p={p:.2e}")

# Floor category + high floor vs others
groups = []
for v in ['low_floor', 'mid_floor', 'high_floor', 'building_total']:
    vals = df.loc[df['floor_category']==v, 'Showings'].dropna().values
    if len(vals) > 5:
        groups.append(vals)
f, p = stats.f_oneway(*groups)
print(f"floor_category: F={f:.2f}, p={p:.2e}")