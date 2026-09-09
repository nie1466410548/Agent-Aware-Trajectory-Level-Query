WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(cpl."Medical Insurance Reimbursement Percentage"),2) AS avg_reimb
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp;