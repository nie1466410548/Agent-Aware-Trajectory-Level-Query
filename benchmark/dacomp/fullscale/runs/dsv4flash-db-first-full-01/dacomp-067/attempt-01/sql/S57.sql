SELECT candidate_gender, COUNT(*) as cnt,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
WHERE candidate_gender IS NOT NULL
GROUP BY candidate_gender