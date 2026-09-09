
SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept_group,
  COUNT(*) as applications,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
  AVG(count_interviews) as avg_interviews
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept_group
ORDER BY hires DESC
