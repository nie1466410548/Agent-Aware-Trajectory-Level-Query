import pandas as pd
import numpy as np

# Marketing department comparison
sql_mkt = """
SELECT r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY r.application_quarter
"""
print("Marketing quarterly:")
print(db.frame(db.query(sql_mkt)))

# Marketing by role
sql_mkt_role = """
SELECT 
  CASE 
    WHEN j.name LIKE 'Content Marketing%' THEN 'Content Marketing'
    WHEN j.name LIKE 'Digital Marketing%' THEN 'Digital Marketing'
    WHEN j.name LIKE 'Growth Marketing%' THEN 'Growth Marketing'
    WHEN j.name LIKE 'Marketing Analyst%' THEN 'Marketing Analyst'
    ELSE 'Other'
  END AS role,
  r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY role, r.application_quarter
ORDER BY role, r.application_quarter
"""
print("\nMarketing role quarterly:")
print(db.frame(db.query(sql_mkt_role)))

# Marketing by hiring manager
sql_mkt_hm = """
SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter
"""
print("\nMarketing hiring manager quarterly:")
print(db.frame(db.query(sql_mkt_hm)))

# Check if number of distinct job titles correlates with manager rate
# at manager level
sql_mgr = """
SELECT j.hiring_managers, j.departments,
  COUNT(DISTINCT j.name) AS distinct_roles,
  COUNT(DISTINCT j.created_month) AS months_active,
  COUNT(*) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers
ORDER BY avg_rate
"""
print("\nManager-level portfolio:")
print(db.frame(db.query(sql_mgr)))