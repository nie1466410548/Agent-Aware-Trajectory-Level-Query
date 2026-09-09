SELECT job_parent_departments,
       COUNT(*) as total_apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced 
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
ORDER BY hires DESC
LIMIT 15