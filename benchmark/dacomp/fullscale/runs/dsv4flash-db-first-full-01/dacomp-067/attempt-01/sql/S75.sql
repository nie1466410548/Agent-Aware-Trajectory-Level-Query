
SELECT current_job_stage,
  COUNT(*) as total,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
  SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
  SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
  SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY 
  CASE current_job_stage
    WHEN 'Application Review' THEN 1
    WHEN 'Phone Screen' THEN 2
    WHEN 'Technical Interview' THEN 3
    WHEN 'Panel Interview' THEN 4
    WHEN 'Final Interview' THEN 5
    WHEN 'Offer' THEN 6
    ELSE 7
  END
