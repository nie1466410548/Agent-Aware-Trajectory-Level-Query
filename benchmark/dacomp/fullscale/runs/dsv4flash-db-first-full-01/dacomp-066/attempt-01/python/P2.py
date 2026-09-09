import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm

# reload data
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
cols = ['n_interviewers','created_month','avg_job_rating','rating_completion_rate','apps']
for c in cols:
    r, p = stats.pearsonr(df[c], df['app_to_int_rate'])
    print(f"corr(app_to_int_rate, {c}) = {r:.3f} (p={p:.4f})")

print()
# Spearman
for c in ['n_interviewers','created_month']:
    r, p = stats.spearmanr(df[c], df['app_to_int_rate'])
    print(f"spearman(app_to_int_rate, {c}) = {r:.3f} (p={p:.4f})")

print()
# Mean conversion by n_interviewers
print(df.groupby('n_interviewers')['app_to_int_rate'].agg(['mean','count']))
t = stats.ttest_ind(df[df.n_interviewers==1]['app_to_int_rate'], df[df.n_interviewers==2]['app_to_int_rate'])
print("t-test 1 vs 2 interviewers:", t)

# OLS regression
X = df[['n_interviewers','created_month','avg_job_rating','apps']].copy()
X = sm.add_constant(X)
X = pd.get_dummies(df[['hiring_managers']], prefix='hm', drop_first=True).join(X)
y = df['app_to_int_rate']
model = sm.OLS(y, X).fit()
print()
print(model.summary())
