WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  cpl."Management measures (observation/treatment/referral)" AS mgmt,
  cpl."Complication outcome (recovered/sequelae)" AS comp_outcome,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, mgmt, comp_outcome ORDER BY grp, n DESC;