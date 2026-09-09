SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  COUNT(DISTINCT p."Patient number") as n_patients,
  COUNT(DISTINCT e."Visit Record Number") as n_visits
FROM patients p
LEFT JOIN encounters e ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group