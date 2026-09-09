
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Housing stability" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val
