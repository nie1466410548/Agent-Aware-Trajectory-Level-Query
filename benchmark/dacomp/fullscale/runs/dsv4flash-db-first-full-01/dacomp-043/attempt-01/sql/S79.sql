WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  b."Past Medical History (Disease Code)" AS past_med,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp, past_med ORDER BY grp, n_cases DESC;