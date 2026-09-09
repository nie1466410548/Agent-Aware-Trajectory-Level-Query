
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
