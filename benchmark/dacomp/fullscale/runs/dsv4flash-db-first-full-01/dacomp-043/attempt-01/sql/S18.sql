SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Isolation Status (Yes/No)" AS isolation,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, isolation
ORDER BY outcome, n DESC;