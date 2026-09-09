import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Pull row-level data (only needed columns)
row_data = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle'
       ELSE 'older' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  e."Missed Appointment" AS missed
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
""")
df = db.frame(row_data)
print(f"Total rows: {len(df)}")
print(df['age_group'].value_counts())

# 1. Overall barrier × improvement (pooled)
ct_all = pd.crosstab(df['barrier'], df['improvement'])
print("\nOverall barrier × improvement:")
print(ct_all)
chi2, p, _, _ = chi2_contingency(ct_all)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

# 2. Overall adherence × improvement
ct_ai = pd.crosstab(df['adherence'], df['improvement'])
print("\nOverall adherence × improvement:")
print(ct_ai)
chi2, p, _, _ = chi2_contingency(ct_ai)
print(f"Chi2={chi2:.4f}, p={p:.6f}")

# 3. Adherence by barrier within each age group
print("\n=== Adherence by barrier within each age group ===")
for age_grp in ['young', 'middle', 'older']:
    sub = df[df['age_group'] == age_grp]
    ct = pd.crosstab(sub['barrier'], sub['adherence'])
    print(f"\n{age_grp}:")
    print(ct)
    chi2a, pa, _, _ = chi2_contingency(ct)
    print(f"Chi2={chi2a:.4f}, p={pa:.6f}")

# 4. Logistic regression: minimal improvement (0/1) ~ age_group + barrier + interaction
df2 = df.copy()
df2['minimal'] = (df2['improvement'] == 'Minimal').astype(int)
df2['age_young'] = (df2['age_group'] == 'young').astype(int)
df2['age_older'] = (df2['age_group'] == 'older').astype(int)
df2['bar_fin'] = (df2['barrier'] == 'Financial').astype(int)
df2['bar_mul'] = (df2['barrier'] == 'Multiple').astype(int)
df2['bar_tra'] = (df2['barrier'] == 'Transportation').astype(int)
# reference: middle age, Time barrier

def logit_fit(X, y):
    X = np.column_stack([np.ones(len(X)), X])
    beta = np.zeros(X.shape[1])
    for _ in range(50):
        p = 1 / (1 + np.exp(-X @ beta))
        W = p * (1 - p)
        grad = X.T @ (p - y)
        H = X.T @ (W[:, None] * X)
        try:
            beta = beta - np.linalg.solve(H + np.eye(len(beta))*1e-8, grad)
        except np.linalg.LinAlgError:
            break
    return beta, X, p

# Main effects model
X_main = df2[['age_young', 'age_older', 'bar_fin', 'bar_mul', 'bar_tra']].values
y = df2['minimal'].values
beta_main, Xm, pm = logit_fit(X_main, y)
print("\n=== Logistic regression: Main effects (minimal improvement) ===")
print("Intercept:", beta_main[0])
print("age_young:", beta_main[1])
print("age_older:", beta_main[2])
print("bar_fin:", beta_main[3])
print("bar_mul:", beta_main[4])
print("bar_tra:", beta_main[5])

# Full model with interactions (age x barrier)
inter_cols = []
for a_col in ['age_young', 'age_older']:
    for b_col in ['bar_fin', 'bar_mul', 'bar_tra']:
        col = f'{a_col}x{b_col}'
        df2[col] = df2[a_col] * df2[b_col]
        inter_cols.append(col)
X_full = df2[['age_young', 'age_older', 'bar_fin', 'bar_mul', 'bar_tra'] + inter_cols].values
beta_full, Xf, pf = logit_fit(X_full, y)
print("\n=== Logistic regression: Full model with interactions ===")
print("Intercept:", beta_full[0])
names = ['Intercept', 'age_young', 'age_older', 'bar_fin', 'bar_mul', 'bar_tra'] + inter_cols
for n, b in zip(names, beta_full):
    print(f"{n}: {b:.4f}")

# Likelihood ratio test: does adding interactions improve fit?
def neg_loglik(beta, X, y):
    p = 1 / (1 + np.exp(-X @ beta))
    p = np.clip(p, 1e-10, 1-1e-10)
    return -np.sum(y * np.log(p) + (1-y) * np.log(1-p))

nll_main = neg_loglik(beta_main, np.column_stack([np.ones(len(X_main)), X_main]), y)
nll_full = neg_loglik(beta_full, np.column_stack([np.ones(len(X_full)), X_full]), y)
lr_stat = 2 * (nll_main - nll_full)
df_diff = X_full.shape[1] - X_main.shape[1]
from scipy.stats import chi2 as chi2_dist
p_lr = 1 - chi2_dist.cdf(lr_stat, df_diff)
print(f"\nLikelihood ratio test for barrier×age interaction: LR={lr_stat:.4f}, df={df_diff}, p={p_lr:.6f}")
print(f"NLL main={nll_main:.4f}, NLL full={nll_full:.4f}")

# Also test age group main effect: model with barrier only vs age+barrier
X_barr = df2[['bar_fin', 'bar_mul', 'bar_tra']].values
beta_barr, Xb, pb = logit_fit(X_barr, y)
nll_barr = neg_loglik(beta_barr, np.column_stack([np.ones(len(X_barr)), X_barr]), y)
lr_age = 2 * (nll_barr - nll_main)
p_age = 1 - chi2_dist.cdf(lr_age, 2)
print(f"\nLikelihood ratio test for age effect (controlling barrier): LR={lr_age:.4f}, p={p_age:.6f}")

# Model with barrier only
X_null = np.zeros((len(y), 0))
beta_null = np.array([np.log(y.mean()/(1-y.mean()))])
nll_null = neg_loglik(beta_null, np.ones((len(y),1)), y)
lr_barr = 2 * (nll_null - nll_main)
p_barr = 1 - chi2_dist.cdf(lr_barr, 5)
print(f"\nLikelihood ratio test for full main-effects vs null: LR={lr_barr:.4f}, p={p_barr:.6f}")

# 5. Missed appointments by age group
print("\n=== Missed appointments by age group ===")
print(df.groupby('age_group')['missed'].mean())
print(df.groupby('age_group')['missed'].median())

# 6. Barrier-specific missed appointments
print("\n=== Missed appointments by barrier ===")
print(df.groupby('barrier')['missed'].mean())

# 7. Age × barrier missed appointment means (matrix)
print("\n=== Missed appointments by age_group × barrier ===")
print(df.groupby(['age_group', 'barrier'])['missed'].mean().unstack())

# Correlation between missed and minimal improvement
print("\n=== Mean missed appointments by improvement ===")
print(df.groupby('improvement')['missed'].mean())