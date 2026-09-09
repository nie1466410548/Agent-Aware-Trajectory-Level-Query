SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Associated Symptoms (Cough/Headache/Vomiting)" AS symptom,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, symptom
ORDER BY outcome, n DESC;