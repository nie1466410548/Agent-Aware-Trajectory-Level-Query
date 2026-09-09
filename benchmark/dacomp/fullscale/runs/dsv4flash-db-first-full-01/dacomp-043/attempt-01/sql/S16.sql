SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Hospitalization (Yes/No)" AS hospitalized,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, hospitalized
ORDER BY outcome, n DESC;