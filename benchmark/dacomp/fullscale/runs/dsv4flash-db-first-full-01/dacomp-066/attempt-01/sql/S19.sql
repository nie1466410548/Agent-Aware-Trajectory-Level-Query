-- Get Engineering job titles and derive role categories, with quarterly conversion rates
SELECT 
  CASE 
    WHEN r.job_title LIKE 'Frontend%' THEN 'Frontend Engineer'
    WHEN r.job_title LIKE 'Backend%' THEN 'Backend Engineer'
    WHEN r.job_title LIKE 'Full Stack%' THEN 'Full Stack Engineer'
    WHEN r.job_title LIKE 'Data Engineer%' THEN 'Data Engineer'
    ELSE r.job_title
  END AS role_category,
  r.application_year,
  r.application_quarter,
  SUM(r.total_applications) AS total_apps,
  SUM(r.total_interviews) AS total_interviews,
  SUM(r.hired_count) AS total_hired,
  ROUND(100.0 * SUM(r.total_interviews) / SUM(r.total_applications), 2) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments = 'Engineering'
GROUP BY role_category, r.application_year, r.application_quarter
ORDER BY role_category, r.application_year, r.application_quarter