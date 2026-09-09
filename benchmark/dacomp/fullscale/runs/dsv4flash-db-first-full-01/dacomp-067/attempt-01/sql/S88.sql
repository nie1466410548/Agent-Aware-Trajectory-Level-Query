SELECT count_interviews, 
       COUNT(*) as apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
WHERE count_interviews > 0
GROUP BY count_interviews
ORDER BY count_interviews