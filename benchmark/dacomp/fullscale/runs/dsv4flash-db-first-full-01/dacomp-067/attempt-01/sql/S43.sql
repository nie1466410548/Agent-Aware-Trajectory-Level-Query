SELECT sourced_from as channel,
       COUNT(*) as applications,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
       ROUND(100.0 * SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as interview_rate,
       AVG(count_interviews) as avg_interviews_per_app
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
ORDER BY hires DESC