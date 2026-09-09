import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('/work/parsed_data.csv')

# Prepare regression dataset: only complete rows
model_df = df[df['Decoration'].notna() & df['Orientation'].notna() & df['floor_num'].notna() & df['Watch Count'].notna()].copy()

# Target: Showings
y = model_df['Showings'].values.astype(float)

# Features
# Bedrooms, living rooms, floor level, price/sqm, area, watch count
features = pd.DataFrame(index=model_df.index)
features['watch_count'] = model_df['Watch Count']
features['floor_level'] = model_df['floor_num']
features['bedrooms'] = model_df['bedrooms']
features['living_rooms'] = model_df['living_rooms']
features['area'] = model_df['area_num']
features['price_sqm'] = model_df['price_sqm_num']

# Dummies for Decoration (baseline: High-quality renovation)
dec_dummies = pd.get_dummies(model_df['Decoration'], prefix='dec', drop_first=True)
# Dummies for Orientation (baseline: South)
ori_dummies = pd.get_dummies(model_df['Orientation'], prefix='ori', drop_first=True)

X = pd.concat([features, dec_dummies, ori_dummies], axis=1).dropna()
y_aligned = model_df.loc[X.index, 'Showings'].values.astype(float)

X = X.astype(float)
X.insert(0, 'intercept', 1.0)

# OLS via normal equations
XtX = X.T @ X
XtX_inv = np.linalg.pinv(XtX)
beta = XtX_inv @ X.T @ y_aligned
yhat = X @ beta
resid = y_aligned - yhat
n, k = X.shape
sigma2 = resid @ resid / (n - k)
se = np.sqrt(np.diag(XtX_inv) * sigma2)
tstat = beta / se
pvals = 2 * (1 - stats.t.cdf(np.abs(tstat), df=n - k))

results = pd.DataFrame({'coef': beta, 'std_err': se, 't': tstat, 'p_value': pvals}, index=X.columns)
results['sig'] = results['p_value'] < 0.01

r2 = 1 - (resid @ resid) / ((y_aligned - y_aligned.mean()) @ (y_aligned - y_aligned.mean()))
print(f"OLS for Showings: n={n}, k={k}, R²={r2:.4f}")
print(results.round(4).to_string())

# Interpretation: Poisson-style would be better for counts, but OLS gives direction/significance.
# Also run ANOVA for each factor separately
print("\n=== ANOVA / F-tests ===")
for factor in ['Decoration', 'Orientation', 'floor_category', 'bedrooms']:
    groups = [df.loc[df[factor]==v, 'Showings'].values for v in df[factor].unique() if df.loc[df[factor]==v, 'Showings'].notna().sum() > 5]
    f, p = stats.f_oneway(*groups)
    print(f"{factor}: F={f:.2f}, p={p:.2e}")