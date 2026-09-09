SELECT job_parent_departments,
       SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) as female_hires,
       SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END) as hires_with_gender,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END), 0), 1) as female_pct
FROM greenhouse__application_enhanced 
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
HAVING hires_with_gender >= 5
ORDER BY female_pct DESC
LIMIT 15