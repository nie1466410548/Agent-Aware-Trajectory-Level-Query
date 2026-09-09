import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- 1. Role-level conversion rates ---
sql_role = """
WITH eng AS (
  SELECT r.*,
    CASE
      WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
      WHEN j.name LIKE 'Backend%' THEN 'Backend'
      WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
      WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
      WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
      WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
      WHEN j.name LIKE 'QA%' THEN 'QA'
      WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
      ELSE 'Other'
    END AS role_category
  FROM greenhouse__recruitment_performance r
  JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
  WHERE j.departments='Engineering'
)
SELECT role_category, application_quarter,
  SUM(total_applications) AS apps,
  SUM(total_interviews) AS interviews,
  100.0*SUM(total_interviews)/SUM(total_applications) AS interview_rate
FROM eng
GROUP BY role_category, application_quarter
ORDER BY role_category, application_quarter
"""
df_role = db.frame(db.query(sql_role))
print("Role data:")
print(df_role)

# Pivot for plotting
pivot = df_role.pivot(index='role_category', columns='application_quarter', values='interview_rate')
pivot.columns = ['Q3_2024','Q4_2024']
pivot['change'] = pivot['Q4_2024'] - pivot['Q3_2024']
pivot = pivot.sort_values('change')
print(pivot)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(pivot))
ax.bar(x - 0.2, pivot['Q3_2024'], 0.35, label='Q3 2024', color='steelblue')
ax.bar(x + 0.2, pivot['Q4_2024'], 0.35, label='Q4 2024', color='coral')
ax.set_xticks(x)
ax.set_xticklabels(pivot.index, rotation=45, ha='right')
ax.set_ylabel('Application-to-Interview Rate (%)')
ax.set_title('Engineering Role Conversion Rates by Quarter')
ax.legend()
for i, (idx, row) in enumerate(pivot.iterrows()):
    chg = row['change']
    ax.annotate(f'{chg:+.1f}pp', (i, max(row['Q3_2024'], row['Q4_2024']) + 1), ha='center', fontsize=8, color='darkred')
plt.tight_layout()
plt.savefig('/work/role_conversion.png', dpi=150)
print("Saved role_conversion.png")

# --- 2. Hiring manager conversion rates ---
sql_hm = """
SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate,
  SUM(r.hired_count) AS hired,
  100.0*SUM(r.hired_count)/SUM(r.total_applications) AS hire_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter
"""
df_hm = db.frame(db.query(sql_hm))
print("\nHiring Manager data:")
print(df_hm)

pivot_hm = df_hm.pivot(index='hiring_managers', columns='application_quarter', values='interview_rate')
pivot_hm.columns = ['Q3_2024','Q4_2024']
pivot_hm['change'] = pivot_hm['Q4_2024'] - pivot_hm['Q3_2024']
pivot_hm = pivot_hm.sort_values('Q4_2024')
print(pivot_hm)

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(pivot_hm))
ax.bar(x - 0.2, pivot_hm['Q3_2024'], 0.35, label='Q3 2024', color='steelblue')
ax.bar(x + 0.2, pivot_hm['Q4_2024'], 0.35, label='Q4 2024', color='coral')
ax.set_xticks(x)
ax.set_xticklabels(pivot_hm.index, rotation=45, ha='right')
ax.set_ylabel('Application-to-Interview Rate (%)')
ax.set_title('Engineering Hiring Manager Conversion Rates by Quarter')
ax.legend()
for i, (idx, row) in enumerate(pivot_hm.iterrows()):
    chg = row['change']
    ax.annotate(f'{chg:+.1f}pp', (i, max(row['Q3_2024'], row['Q4_2024']) + 1), ha='center', fontsize=8, color='darkred')
plt.tight_layout()
plt.savefig('/work/manager_conversion.png', dpi=150)
print("Saved manager_conversion.png")

# --- 3. Monthly trend line ---
sql_monthly = """
SELECT j.created_month,
  COUNT(DISTINCT j.job_id) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  SUM(j.count_completed_interviews) AS interviews,
  100.0*SUM(j.count_completed_interviews)/SUM(j.count_total_applications) AS interview_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.created_month
ORDER BY j.created_month
"""
df_monthly = db.frame(db.query(sql_monthly))
print("\nMonthly data:")
print(df_monthly)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(df_monthly['created_month'], df_monthly['interview_rate'], 'o-', color='crimson', linewidth=2, markersize=8)
ax.set_xlabel('Job Creation Month (2024)')
ax.set_ylabel('Application-to-Interview Rate (%)')
ax.set_title('Engineering Conversion Rate by Job Creation Month')
ax.set_xticks(df_monthly['created_month'])
ax.set_xticklabels(['Jul','Aug','Sep','Oct','Nov','Dec'])
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/monthly_trend.png', dpi=150)
print("Saved monthly_trend.png")