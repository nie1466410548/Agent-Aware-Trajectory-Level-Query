WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  MIN(b."Date of Discovery") AS min_date,
  MAX(b."Date of Discovery") AS max_date,
  COUNT(DISTINCT b."Case ID") AS n_cases
FROM basic_medical_record_informatio b JOIN case_outcome co ON b."Case ID"=co."Case ID"
GROUP BY grp;