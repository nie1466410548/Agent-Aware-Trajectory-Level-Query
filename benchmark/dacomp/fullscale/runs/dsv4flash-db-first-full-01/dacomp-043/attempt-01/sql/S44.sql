WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  CASE WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '0%' THEN '0 dose/None'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '1%' THEN '1 dose'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '2%' THEN '2 doses'
       WHEN ei."Vaccination History (Doses/Date/Type)" LIKE '3%' THEN '3 doses'
       ELSE 'No vaccination' END AS vacc_cat,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc_cat ORDER BY grp, n DESC;