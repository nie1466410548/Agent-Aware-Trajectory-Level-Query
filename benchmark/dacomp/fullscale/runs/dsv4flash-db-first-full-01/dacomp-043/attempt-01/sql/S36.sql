WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  COUNT(DISTINCT cm."Case ID") AS n_cases,
  COUNT(*) AS n_records,
  ROUND(AVG("Highest Body Temperature (°C)"),2) AS avg_temp,
  ROUND(MIN("Highest Body Temperature (°C)"),2) AS min_temp,
  ROUND(MAX("Highest Body Temperature (°C)"),2) AS max_temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
GROUP BY grp;