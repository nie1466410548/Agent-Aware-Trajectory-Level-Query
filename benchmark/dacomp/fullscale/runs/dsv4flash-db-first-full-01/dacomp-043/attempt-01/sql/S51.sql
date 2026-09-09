WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  id."PPE Usage" AS ppe,
  id."Symptom Monitoring During Isolation" AS monitor,
  COUNT(*) AS n
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp, ppe, monitor ORDER BY grp, n DESC;