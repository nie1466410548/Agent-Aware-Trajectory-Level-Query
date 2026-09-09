SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, complication
ORDER BY outcome, n DESC;