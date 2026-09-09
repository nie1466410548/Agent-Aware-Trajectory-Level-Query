SELECT cm."Outcome (Cured/Improved/Deceased)" AS outcome,
  cpl."Complication type (pneumonia/encephalitis/hepatitis)" AS comp_type,
  cpl."Severity grading (mild/moderate/severe)" AS severity,
  cpl."Management measures (observation/treatment/referral)" AS mgmt,
  cpl."Complication outcome (recovered/sequelae)" AS comp_outcome,
  COUNT(*) AS n
FROM complication_management cpl
JOIN clinical_manifestations cm ON cpl."Case ID" = cm."Case ID"
GROUP BY outcome, comp_type, severity, mgmt, comp_outcome
ORDER BY outcome, n DESC;