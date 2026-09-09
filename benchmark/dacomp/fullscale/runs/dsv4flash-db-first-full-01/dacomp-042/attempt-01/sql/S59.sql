SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  d."Primary Diagnosis" AS diagnosis,
  COUNT(*) AS n
FROM assessmentsocialanddiagnosis d
JOIN assessmentbasics a ON a."Assessment ID" = d."Social Diagnosis Assessment ID"
JOIN encounters e ON e."Assessment Reference" = a."Assessment ID"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, diagnosis
ORDER BY age_group, n DESC