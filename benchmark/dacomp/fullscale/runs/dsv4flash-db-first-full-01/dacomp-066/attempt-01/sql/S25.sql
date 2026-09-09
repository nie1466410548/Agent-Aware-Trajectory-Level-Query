SELECT j.application_to_interview_rate, j.overall_conversion_rate, j.count_total_applications, j.count_completed_interviews, j.departments
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
LIMIT 10