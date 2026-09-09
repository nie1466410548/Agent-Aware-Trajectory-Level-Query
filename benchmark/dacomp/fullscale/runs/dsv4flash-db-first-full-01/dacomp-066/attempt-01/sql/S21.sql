SELECT DISTINCT 
  CASE 
    WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
    WHEN j.name LIKE 'Backend%' THEN 'Backend'
    WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
    WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
    WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
    WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
    WHEN j.name LIKE 'QA%' THEN 'QA'
    WHEN j.name LIKE 'Security%' THEN 'Security'
    WHEN j.name LIKE 'Site Reliability%' THEN 'Site Reliability'
    WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
    WHEN j.name LIKE 'Systems%' THEN 'Systems'
    WHEN j.name LIKE 'Engineering Manager%' THEN 'Engineering Manager'
    ELSE 'Other'
  END AS role_category
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY role_category