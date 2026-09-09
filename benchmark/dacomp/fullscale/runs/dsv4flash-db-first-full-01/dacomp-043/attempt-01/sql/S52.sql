WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(id."Disinfection Frequency (times/day)"),2) AS avg_disfreq,
  ROUND(AVG(id."Disinfected Area (m²)"),2) AS avg_area,
  ROUND(AVG(id."Isolation Cost"),2) AS avg_cost
FROM isolation_and_disinfection id JOIN case_outcome co ON id."Case ID"=co."Case ID"
GROUP BY grp;