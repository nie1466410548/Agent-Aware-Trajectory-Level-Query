WITH funnel AS (
  SELECT 
    COUNT(*) as total_applications,
    SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) as interviewed,
    SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
  FROM greenhouse__application_enhanced
)
SELECT total_applications, interviewed, hired,
       ROUND(100.0 * interviewed / total_applications, 1) as app_to_interview_pct,
       ROUND(100.0 * hired / interviewed, 1) as interview_to_hire_pct,
       ROUND(100.0 * hired / total_applications, 1) as overall_hire_rate
FROM funnel