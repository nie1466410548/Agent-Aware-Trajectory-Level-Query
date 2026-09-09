WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  ROUND(AVG(cpl."Complication treatment cost"),2) AS avg_cost,
  ROUND(MIN(cpl."Complication treatment cost"),2) AS min_cost,
  ROUND(MAX(cpl."Complication treatment cost"),2) AS max_cost,
  ROUND(AVG(cpl."Medical Insurance Reimbursement Percentage"),2) AS avg_reimb,
  cpl."Complication reporting timeliness" AS report_time,
  cpl."Complication management timeliness" AS mgmt_time,
  COUNT(*) AS n
FROM complication_management cpl JOIN case_outcome co ON cpl."Case ID"=co."Case ID"
GROUP BY grp, report_time, mgmt_time ORDER BY grp, n DESC;