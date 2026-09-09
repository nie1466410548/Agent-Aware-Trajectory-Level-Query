SELECT MIN(j.created_at) AS min_created, MAX(j.created_at) AS max_created,
       MIN(r.job_created_at) AS min_job_created, MAX(r.job_created_at) AS max_job_created
FROM greenhouse__job_enhanced j
JOIN greenhouse__recruitment_performance r ON r.job_id = j.job_id