SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  COUNT(DISTINCT "Case ID") AS n_cases,
  COUNT(*) AS n_records
FROM clinical_manifestations
GROUP BY outcome;