import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

# Check for multicollinearity in the full model
base = df[['Mental health score', 'Daily study time', 'Social media usage time', 
           'Attendance rate', 'Sleep duration', 'Exercise frequency']]
# Add dummies
for col, cat in [('Diet_Good', 'Fair'), ('Diet_Poor', 'Poor'), 
                 ('Part_time_Yes', 'Yes'), 
                 ('Internet_Good', 'Good'), ('Internet_Poor', 'Poor'),
                 ('Parent_Bachelor', 'Bachelor'), ('Parent_Master', 'Master'), ('Parent_Missing', np.nan)]:
    base[col] = (df['Diet quality']==cat if 'Diet' in col else
                 (df['Part-time job']==cat) if 'Part' in col else
                 (df['Internet quality']==cat) if 'Internet' in col else
                 (df["Parents' education level"]==cat) if pd.notna(cat) else
                 df["Parents' education level"].isnull()).astype(int)

# Compute VIF for each variable
def vif(X):
    X = np.asarray(X, dtype=float)
    n, k = X.shape
    vifs = []
    for j in range(k):
        y_j = X[:, j]
        X_j = np.column_stack([np.ones(n), np.delete(X, j, axis=1)])
        beta = np.linalg.pinv(X_j.T @ X_j) @ X_j.T @ y_j
        rss = np.sum((y_j - X_j @ beta)**2)
        tss = np.sum((y_j - y_j.mean())**2)
        r2 = 1 - rss/tss
        vifs.append(1/(1-r2))
    return vifs

Xmat = base.values
vifs = vif(Xmat)
print("VIF values (VIF > 10 indicates multicollinearity):")
for nm, v in zip(base.columns, vifs):
    print(f"  {nm:30s} VIF = {v:.2f}")

# Check descriptive stats for key variables
print("\nDescriptive stats for key continuous variables:")
for c in ['Mental health score', 'Exam score', 'Daily study time', 'Social media usage time', 
          'Attendance rate', 'Sleep duration', 'Exercise frequency']:
    q = df[c].quantile([0.01, 0.25, 0.5, 0.75, 0.99])
    print(f"  {c}: min={df[c].min():.1f}, max={df[c].max():.1f}, mean={df[c].mean():.1f}, sd={df[c].std():.1f}")
    print(f"    P1={q.iloc[0]:.1f}, P25={q.iloc[1]:.1f}, P50={q.iloc[2]:.1f}, P75={q.iloc[3]:.1f}, P99={q.iloc[4]:.1f}")

# Check normality of residuals from full model
def ols(y, X):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    beta = np.linalg.pinv(X.T @ X) @ X.T @ y
    yhat = X @ beta
    resid = y - yhat
    return resid, yhat, beta

# Full model
XX = np.column_stack([np.ones(len(df)), base])
resid, yhat, _ = ols(df['Exam score'].values, XX)
sw_stat, sw_p = stats.shapiro(resid[:100])  # limit to 100 for speed
print(f"\nShapiro-Wilk normality test (first 100 residuals): stat={sw_stat:.4f}, p={sw_p:.2e}")
print("Residuals: mean={:.4f}, sd={:.4f}".format(np.mean(resid), np.std(resid, ddof=1)))