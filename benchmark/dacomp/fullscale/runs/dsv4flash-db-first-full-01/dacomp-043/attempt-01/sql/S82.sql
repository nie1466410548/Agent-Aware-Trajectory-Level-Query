WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Emergency Response Activation Time" AS response_time,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, response_time ORDER BY grp, n DESC;