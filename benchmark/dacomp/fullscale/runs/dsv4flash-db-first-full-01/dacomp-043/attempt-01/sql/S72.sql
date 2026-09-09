WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  dc."Diagnostic Delay Analysis" AS delay,
  COUNT(*) AS n
FROM diagnosis_and_classification dc JOIN case_outcome co ON dc."Case ID"=co."Case ID"
GROUP BY grp, delay ORDER BY grp, n DESC;