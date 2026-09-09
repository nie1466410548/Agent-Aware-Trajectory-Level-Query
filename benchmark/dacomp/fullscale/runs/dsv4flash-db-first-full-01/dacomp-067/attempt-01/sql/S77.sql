
SELECT ie.interview_name,
  COUNT(DISTINCT ie.application_id) as candidates,
  SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) as hired,
  ROUND(100.0 * SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) / COUNT(DISTINCT ie.application_id), 1) as hire_rate
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
GROUP BY ie.interview_name
ORDER BY hire_rate DESC
