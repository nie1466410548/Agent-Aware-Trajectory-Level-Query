
SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.count_completed_interviews AS completed_interviews,
  j.avg_interviews_per_application,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate AS app_to_int_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
