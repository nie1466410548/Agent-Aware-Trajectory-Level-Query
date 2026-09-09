SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Isolation Type (Home/Hospital)" AS iso_type,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, iso_type
ORDER BY outcome, n DESC;