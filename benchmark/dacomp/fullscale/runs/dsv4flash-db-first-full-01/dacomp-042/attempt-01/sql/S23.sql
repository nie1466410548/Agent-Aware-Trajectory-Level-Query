SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM encounters e
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, n DESC