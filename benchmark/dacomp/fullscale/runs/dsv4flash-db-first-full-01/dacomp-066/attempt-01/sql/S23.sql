WITH eng AS (
  SELECT r.*, j.name AS job_name, j.departments,
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
  WHERE j.departments = 'Engineering'
)
SELECT role_category,
  SUM(CASE WHEN application_quarter=3 THEN total_applications END) AS q3_apps,
  SUM(CASE WHEN application_quarter=4 THEN total_applications END) AS q4_apps,
  SUM(CASE WHEN application_quarter=3 THEN total_interviews END) AS q3_interviews,
  SUM(CASE WHEN application_quarter=4 THEN total_interviews END) AS q4_interviews,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=3 THEN total_interviews END) / NULLIF(SUM(CASE WHEN application_quarter=3 THEN total_applications END), 0), 2) AS q3_interview_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=4 THEN total_interviews END) / NULLIF(SUM(CASE WHEN application_quarter=4 THEN total_applications END), 0), 2) AS q4_interview_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=3 THEN hired_count END) / NULLIF(SUM(CASE WHEN application_quarter=3 THEN total_applications END), 0), 2) AS q3_hire_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=4 THEN hired_count END) / NULLIF(SUM(CASE WHEN application_quarter=4 THEN total_applications END), 0), 2) AS q4_hire_rate
FROM eng
GROUP BY role_category
ORDER BY role_category