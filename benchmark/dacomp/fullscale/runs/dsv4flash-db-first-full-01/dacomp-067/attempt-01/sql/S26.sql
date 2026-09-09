SELECT current_job_stage, COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY current_job_stage
ORDER BY cnt DESC