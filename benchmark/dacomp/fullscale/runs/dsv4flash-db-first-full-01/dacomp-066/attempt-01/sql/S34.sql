
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
