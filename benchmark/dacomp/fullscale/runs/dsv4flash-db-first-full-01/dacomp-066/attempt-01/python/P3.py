import pandas as pd
import numpy as np
from scipy import stats

sql_jobs = """
SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate AS app_to_int_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
"""
df = db.frame(db.query(sql_jobs))

# correlations
for c in ['n_interviewers','created_month','avg_job_rating','rating_completion_rate','apps']:
    r, p = stats.pearsonr(df[c], df['app_to_int_rate'])
    print(f"corr(app_to_int_rate, {c}) = {r:.3f} (p={p:.4f})")

print()
print(df.groupby('n_interviewers')['app_to_int_rate'].agg(['mean','count','std']))
t = stats.ttest_ind(df[df.n_interviewers==1]['app_to_int_rate'], df[df.n_interviewers==2]['app_to_int_rate'])
print("t-test 1 vs 2 interviewers: t=%.3f p=%.4f" % (t.statistic, t.pvalue))

def ols(y, X, names):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    X1 = np.column_stack([np.ones(len(y)), X])
    beta, res, rank, sv = np.linalg.lstsq(X1, y, rcond=None)
    n, k = X1.shape
    resid = y - X1 @ beta
    sigma2 = resid @ resid / (n - k)
    cov = sigma2 * np.linalg.inv(X1.T @ X1)
    se = np.sqrt(np.diag(cov))
    tvals = beta / se
    pvals = 2*(1 - stats.t.cdf(np.abs(tvals), df=n-k))
    print("\nOLS results (n=%d):" % n)
    for nm, b, s, tv, pv in zip(['const']+names, beta, se, tvals, pvals):
        print(f"  {nm:22s} coef={b:8.3f}  se={s:7.3f}  t={tv:7.2f}  p={pv:.4f}")
    r2 = 1 - resid @ resid / ((y - y.mean()) @ (y - y.mean()))
    print("  R^2 = %.3f" % r2)
    return beta

print("\n--- Model 1: numeric factors only ---")
ols(df['app_to_int_rate'], df[['n_interviewers','created_month','avg_job_rating','apps']].values,
    ['n_interviewers','created_month','avg_job_rating','apps'])

print("\n--- Model 2: + hiring manager dummies ---")
X = df[['n_interviewers','created_month','avg_job_rating','apps']].copy()
dums = pd.get_dummies(df['hiring_managers'], prefix='hm', drop_first=True)
Xm = pd.concat([X, dums], axis=1)
ols(df['app_to_int_rate'], Xm.values, list(Xm.columns))
