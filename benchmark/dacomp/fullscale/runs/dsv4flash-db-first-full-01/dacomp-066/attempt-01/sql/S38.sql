-- Does number of interviewers vary systematically by hiring manager?
SELECT j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  COUNT(*) AS n_jobs,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, n_interviewers
ORDER BY j.hiring_managers, n_interviewers