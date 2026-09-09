import numpy as np, pandas as pd
from scipy import stats

df = pd.read_csv('work/sheet1_full.csv')

def ols_simple(y, X):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n, k = X.shape
    XtX = X.T @ X
    XtX_inv = np.linalg.pinv(XtX)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    resid = y - yhat
    rss = resid @ resid
    tss = np.sum((y - y.mean())**2)
    r2 = 1 - rss/tss
    adj_r2 = 1 - (1-r2)*(n-1)/(n-k)
    sigma2 = rss/(n-k)
    cov_b = sigma2 * XtX_inv
    se = np.sqrt(np.diag(cov_b))
    t = beta/se
    p = 2*(1 - stats.t.cdf(np.abs(t), n-k))
    ci_lo = beta - stats.t.ppf(0.975, n-k)*se
    ci_hi = beta + stats.t.ppf(0.975, n-k)*se
    return dict(beta=beta, se=se, t=t, p=p, ci_lo=ci_lo, ci_hi=ci_hi, r2=r2, adj_r2=adj_r2,
                rss=rss, n=n, k=k, resid=resid)

def make_base_design(df):
    d = pd.DataFrame(index=df.index)
    d['Mental health score'] = df['Mental health score']
    d['Daily study time'] = df['Daily study time']
    d['Social media usage time'] = df['Social media usage time']
    d['Attendance rate'] = df['Attendance rate']
    d['Sleep duration'] = df['Sleep duration']
    d['Exercise frequency'] = df['Exercise frequency']
    d['Diet_Good'] = (df['Diet quality']=='Good').astype(int)
    d['Diet_Poor'] = (df['Diet quality']=='Poor').astype(int)
    d['Part_time_Yes'] = (df['Part-time job']=='Yes').astype(int)
    d['Internet_Good'] = (df['Internet quality']=='Good').astype(int)
    d['Internet_Poor'] = (df['Internet quality']=='Poor').astype(int)
    d['Parent_Bachelor'] = (df["Parents' education level"]=='Bachelor').astype(int)
    d['Parent_Master'] = (df["Parents' education level"]=='Master').astype(int)
    d['Parent_Missing'] = (df["Parents' education level"].isnull()).astype(int)
    return d

y = df['Exam score'].values

# Continuous variables to test for interaction
continuous_vars = ['Daily study time', 'Social media usage time', 'Attendance rate', 
                   'Sleep duration', 'Exercise frequency']
# Binary/categorical variables (as dummies)
categorical_dummies = ['Diet_Good', 'Diet_Poor', 'Part_time_Yes', 'Internet_Good', 'Internet_Poor',
                       'Parent_Bachelor', 'Parent_Master', 'Parent_Missing']

base = make_base_design(df)

results_interactions = []
for var in continuous_vars:
    X = base.copy()
    X[f'MHx{var}'] = df['Mental health score'] * df[var]
    Xmat = np.column_stack([np.ones(len(df)), X])
    m = ols_simple(y, Xmat)
    names = ['Intercept'] + list(X.columns)
    # Find interaction term index
    int_idx = names.index(f'MHx{var}')
    results_interactions.append({
        'variable': var,
        'type': 'continuous',
        'beta_int': m['beta'][int_idx],
        'se_int': m['se'][int_idx],
        't_int': m['t'][int_idx],
        'p_int': m['p'][int_idx],
        'ci_lo': m['ci_lo'][int_idx],
        'ci_hi': m['ci_hi'][int_idx],
        'r2': m['r2'],
        'r2_no_int': None  # will fill later
    })

# Also check extra demographics
extra_vars = ['Age', 'Gender_Male', 'Gender_Other', 'Extra_Yes']
for var in extra_vars:
    if var == 'Age':
        # continuous
        d = df['Age']
    elif var == 'Gender_Male':
        d = (df['Gender']=='Male').astype(int)
    elif var == 'Gender_Other':
        d = (df['Gender']=='Other').astype(int)
    elif var == 'Extra_Yes':
        d = (df['Extracurricular activity participation']=='Yes').astype(int)
    
    X = base.copy()
    X[f'MHx{var}'] = df['Mental health score'] * d
    Xmat = np.column_stack([np.ones(len(df)), X])
    m = ols_simple(y, Xmat)
    names = ['Intercept'] + list(X.columns)
    int_idx = names.index(f'MHx{var}')
    results_interactions.append({
        'variable': var,
        'type': 'continuous' if var=='Age' else 'binary',
        'beta_int': m['beta'][int_idx],
        'se_int': m['se'][int_idx],
        't_int': m['t'][int_idx],
        'p_int': m['p'][int_idx],
        'ci_lo': m['ci_lo'][int_idx],
        'ci_hi': m['ci_hi'][int_idx],
        'r2': m['r2'],
        'r2_no_int': None
    })

# Also test categorical dummies with interaction
for var in categorical_dummies:
    d = base[var]  # already in base
    X = base.copy()
    X[f'MHx{var}'] = df['Mental health score'] * d
    Xmat = np.column_stack([np.ones(len(df)), X])
    m = ols_simple(y, Xmat)
    names = ['Intercept'] + list(X.columns)
    int_idx = names.index(f'MHx{var}')
    results_interactions.append({
        'variable': var,
        'type': 'dummy',
        'beta_int': m['beta'][int_idx],
        'se_int': m['se'][int_idx],
        't_int': m['t'][int_idx],
        'p_int': m['p'][int_idx],
        'ci_lo': m['ci_lo'][int_idx],
        'ci_hi': m['ci_hi'][int_idx],
        'r2': m['r2'],
        'r2_no_int': None
    })

# Get R2 without interaction (base model)
X_base = np.column_stack([np.ones(len(df)), base])
m_base = ols_simple(y, X_base)
base_r2 = m_base['r2']

# Fill R2 without interaction
for r in results_interactions:
    r['r2_no_int'] = base_r2
    r['delta_r2'] = r['r2'] - base_r2
    # Partial F for interaction (1 df)
    n = len(df)
    k_full = len(base.columns) + 2  # +1 for interaction, +1 for intercept (already counted)
    # Actually: base has k-1 columns (excluding intercept), plus 1 interaction = total k = len(base.columns)+1+1
    # Let me recalculate
    rss_no_int = m_base['rss']
    rss_with_int = (1 - r['r2']) * n * np.var(y, ddof=0)  # need proper rss
    # Better: recompute
    pass

# Recompute properly
print("R2 base (no interactions):", base_r2)
print(f"\n{'Variable':30s} {'beta_int':>8s} {'se':>7s} {'p':>8s} {'CI_lo':>8s} {'CI_hi':>8s} {'delta_R2':>8s}")
print("="*85)

for r in results_interactions:
    # Recompute the actual model to get proper RSS
    X = base.copy()
    X[f'MHx{r["variable"]}'] = df['Mental health score'] * (df[r['variable']] if r['variable'] in continuous_vars+['Age'] else 
        ((df['Gender']=='Male').astype(int) if r['variable']=='Gender_Male' else
         (df['Gender']=='Other').astype(int) if r['variable']=='Gender_Other' else
         (df['Extracurricular activity participation']=='Yes').astype(int) if r['variable']=='Extra_Yes' else
         base[r['variable']]))
    Xmat = np.column_stack([np.ones(len(df)), X])
    m = ols_simple(y, Xmat)
    rss_int = m['rss']
    rss_no_int = m_base['rss']
    n = len(df)
    k_full = m['k']
    k_reduced = m_base['k']
    f_part = ((rss_no_int - rss_int)/1) / (rss_int/(n - k_full))
    p_part = 1 - stats.f.cdf(f_part, 1, n - k_full)
    r['partial_F'] = f_part
    r['partial_p'] = p_part
    r['delta_r2'] = m['r2'] - base_r2
    
    print(f"{r['variable']:30s} {r['beta_int']:8.3f} {r['se_int']:7.3f} {r['p_int']:8.2e} {r['ci_lo']:8.3f} {r['ci_hi']:8.3f} {r['delta_r2']:8.4f}  F={f_part:.2f} p={p_part:.3e}")

# Summary of significant interactions
print("\n\n=== SIGNIFICANT INTERACTIONS (p < 0.05) ===")
sig = [r for r in results_interactions if r['p_int'] < 0.05]
if sig:
    for r in sig:
        print(f"{r['variable']:30s} beta={r['beta_int']:.3f}, p={r['p_int']:.2e}, delta_R2={r['delta_r2']:.4f}")
        if r['beta_int'] > 0:
            print(f"  -> Amplifies MH effect: as {r['variable']} increases, MH effect is stronger")
        else:
            print(f"  -> Dampens MH effect: as {r['variable']} increases, MH effect is weaker")
else:
    print("No significant interactions at p<0.05")
    
# Check for borderline (p<0.10)
border = [r for r in results_interactions if 0.05 <= r['p_int'] < 0.10]
if border:
    print(f"\n=== BORDERLINE INTERACTIONS (0.05 < p < 0.10) ===")
    for r in border:
        print(f"{r['variable']:30s} beta={r['beta_int']:.3f}, p={r['p_int']:.2e}")