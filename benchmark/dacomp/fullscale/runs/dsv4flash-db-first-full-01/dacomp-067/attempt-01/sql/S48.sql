SELECT ie.interviewer_name, ie.job_title, ie.job_departments, ie.job_parent_departments,
       ie.overall_recommendation, ie.application_id, ie.candidate_id
FROM greenhouse__interview_enhanced ie
WHERE ie.overall_recommendation IS NOT NULL
LIMIT 20