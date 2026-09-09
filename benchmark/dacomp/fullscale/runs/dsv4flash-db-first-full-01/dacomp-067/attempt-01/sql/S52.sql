SELECT ie.interviewer_name, ie.job_title, ie.job_parent_departments, ie.overall_recommendation
FROM greenhouse__interview_enhanced ie
WHERE ie.interviewer_name IS NOT NULL AND ie.job_parent_departments IS NOT NULL
LIMIT 5