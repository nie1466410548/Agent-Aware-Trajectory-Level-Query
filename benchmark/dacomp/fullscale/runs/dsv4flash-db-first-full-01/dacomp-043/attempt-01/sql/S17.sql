SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Treatment (Antiviral/Symptomatic)" AS treatment,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, treatment
ORDER BY outcome, n DESC;