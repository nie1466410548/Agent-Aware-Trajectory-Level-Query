WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ei."Vaccine Origin (Domestic/Imported)" AS vacc_origin,
  ei."Shared Exposure History (Group Dining/Group Activity)" AS shared_exposure,
  ei."Environmental Sample Test Result" AS env_result,
  COUNT(*) AS n
FROM epidemiological_investigation ei JOIN case_outcome co ON ei."Case ID"=co."Case ID"
GROUP BY grp, vacc_origin, shared_exposure, env_result ORDER BY grp, n DESC;