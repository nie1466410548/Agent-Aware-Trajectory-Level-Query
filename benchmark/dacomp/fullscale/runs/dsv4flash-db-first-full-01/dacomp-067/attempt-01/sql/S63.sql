
SELECT sourced_from,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  COUNT(*) as applications,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
GROUP BY sourced_from
ORDER BY hires DESC
