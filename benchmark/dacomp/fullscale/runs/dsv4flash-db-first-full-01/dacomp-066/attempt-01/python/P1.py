import pandas as pd
import numpy as np
from scipy import stats

# Per-job Engineering data
sql_jobs = """
SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.count_completed_interviews AS completed_interviews,
  j.avg_interviews_per_application,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate AS app_to_int_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
"""
df = db.frame(db.query(sql_jobs))
print("Engineering jobs:", df.shape)
print(df.dtypes)
print(df[['n_interviewers','created_month','app_to_int_rate','overall_conversion_rate','avg_job_rating']].describe())
