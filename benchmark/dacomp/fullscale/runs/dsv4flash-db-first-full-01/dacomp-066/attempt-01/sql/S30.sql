SELECT j.hiring_managers, 
  j.recruiters,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_recruiters,
  j.count_total_applications,
  j.count_completed_interviews,
  ROUND(100.0*j.count_completed_interviews/j.count_total_applications,2) AS interview_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering' AND j.recruiters IS NOT NULL
LIMIT 20