import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

rows = db.query("SELECT * FROM sheet1")
df = db.frame(rows)

col = "Parents' education level"

# ============ Multiple Regression ============
# Prepare dummy variables
df_ml = df.copy()
df_ml['is_male'] = (df_ml['Gender']=='Male').astype(int)
df_ml['is_other_gender'] = (df_ml['Gender']=='Other').astype(int)
df_ml['has_parttime'] = (df_ml['Part-time job']=='Yes').astype(int)
df_ml['has_extracurricular'] = (df_ml['Extracurricular activity participation']=='Yes').astype(int)
df_ml['diet_good'] = (df_ml['Diet quality']=='Good').astype(int)
df_ml['diet_poor'] = (df_ml['Diet quality']=='Poor').astype(int)
df_ml['internet_good'] = (df_ml['Internet quality']=='Good').astype(int)
df_ml['internet_poor'] = (df_ml['Internet quality']=='Poor').astype(int)
df_ml['parent_bachelor'] = (df_ml[col]=='Bachelor').astype(int)
df_ml['parent_master'] = (df_ml[col]=='Master').astype(int)
# Reference: parent_highschool (includes null)

# Features for regression
features = ['Daily study time', 'Social media usage time', 'Attendance rate', 
            'Sleep duration', 'Exercise frequency', 'Mental health score', 'Age',
            'is_male', 'is_other_gender', 'has_parttime', 'has_extracurricular',
            'diet_good', 'diet_poor', 'internet_good', 'internet_poor',
            'parent_bachelor', 'parent_master']

X = df_ml[features].values
y = df_ml['Exam score'].values

# Add constant for intercept
X_with_const = np.column_stack([np.ones(X.shape[0]), X])

# OLS using normal equation
beta = np.linalg.lstsq(X_with_const, y, rcond=None)[0]
y_pred = X_with_const @ beta
residuals = y - y_pred
n = len(y)
k = X_with_const.shape[1] - 1  # number of predictors (excluding intercept)
mse = np.sum(residuals**2) / (n - k - 1)
se = np.sqrt(mse * np.diag(np.linalg.inv(X_with_const.T @ X_with_const)))
t_stats = beta / se
p_values = 2 * (1 - stats.t.cdf(np.abs(t_stats), df=n-k-1))

# R-squared
ss_res = np.sum(residuals**2)
ss_tot = np.sum((y - y.mean())**2)
r2 = 1 - ss_res/ss_tot
adj_r2 = 1 - (1-r2)*(n-1)/(n-k-1)

print("===== Multiple Linear Regression =====")
print(f"R-squared: {r2:.4f}, Adjusted R-squared: {adj_r2:.4f}")
print(f"n={n}, k={k}")
print()

feature_names = ['Intercept'] + features
print(f"{'Feature':<30s} {'Coef':>10s} {'SE':>10s} {'t':>10s} {'p':>10s}")
print("-"*70)
for i, (name, coef, se_val, t_val, p_val) in enumerate(zip(feature_names, beta, se, t_stats, p_values)):
    sig = '***' if p_val < 0.001 else '**' if p_val < 0.01 else '*' if p_val < 0.05 else ''
    print(f"{name:<30s} {coef:>10.4f} {se_val:>10.4f} {t_val:>10.4f} {p_val:>10.6f} {sig}")

# Standardized coefficients (beta weights)
X_std = (X - X.mean(axis=0)) / X.std(axis=0)
y_std = (y - y.mean()) / y.std()
beta_std = np.linalg.lstsq(X_std, y_std, rcond=None)[0]

print("\n===== Standardized Coefficients (Beta Weights) =====")
for name, coef in sorted(zip(features, beta_std), key=lambda x: abs(x[1]), reverse=True):
    print(f"{name:<30s} {coef:>10.4f}")