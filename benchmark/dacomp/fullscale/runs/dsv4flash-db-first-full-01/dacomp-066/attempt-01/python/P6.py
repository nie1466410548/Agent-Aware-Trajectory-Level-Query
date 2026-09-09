import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sql_jobs = """
SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.avg_job_rating,
  j.application_to_interview_rate AS app_to_int_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
"""
df = db.frame(db.query(sql_jobs))

# Boxplot by hiring manager
fig, ax = plt.subplots(figsize=(10, 6))
managers = df.groupby('hiring_managers')['app_to_int_rate'].mean().sort_values().index
data = [df[df.hiring_managers==m]['app_to_int_rate'].values for m in managers]
bp = ax.boxplot(data, labels=managers, patch_artist=True)
for patch, color in zip(bp['boxes'], plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(managers)))):
    patch.set_facecolor(color)
ax.set_ylabel('Application-to-Interview Rate (%)')
ax.set_title('Distribution of Conversion Rates by Hiring Manager (Engineering)')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('/work/manager_boxplot.png', dpi=150)

# Scatter: conversion rate vs created_month, colored by n_interviewers
fig, ax = plt.subplots(figsize=(9, 6))
for n_int in [1, 2]:
    subset = df[df.n_interviewers == n_int]
    ax.scatter(subset['created_month'], subset['app_to_int_rate'], 
               alpha=0.6, s=20, label=f'{n_int} interviewer(s)', 
               color='steelblue' if n_int==1 else 'coral')
ax.set_xlabel('Job Creation Month (2024)')
ax.set_ylabel('Application-to-Interview Rate (%)')
ax.set_title('Engineering Conversion Rate vs. Creation Month\n(Colored by Number of Interviewers)')
ax.set_xticks(range(7, 13))
ax.set_xticklabels(['Jul','Aug','Sep','Oct','Nov','Dec'])
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/scatter_month_interviewers.png', dpi=150)

print("Saved boxplot and scatter plots")