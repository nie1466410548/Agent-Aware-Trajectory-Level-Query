
SELECT current_job_stage,
       COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
       SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
       SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY cnt DESC
