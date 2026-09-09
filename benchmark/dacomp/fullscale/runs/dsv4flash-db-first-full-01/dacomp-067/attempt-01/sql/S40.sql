SELECT job_parent_departments, COUNT(*) as cnt, 
       AVG(duration_interview_minutes) as avg_duration,
       ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes','strong yes','yes') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as positive_pct
FROM greenhouse__interview_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
ORDER BY cnt DESC
LIMIT 15