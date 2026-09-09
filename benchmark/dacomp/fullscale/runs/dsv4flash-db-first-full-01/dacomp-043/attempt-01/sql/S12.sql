SELECT "Outcome (Cured/Improved/Deceased)" AS outcome, "Hospitalization (Yes/No)" AS hosp,
  "Isolation Status (Yes/No)" AS iso, "Treatment (Antiviral/Symptomatic)" AS trt, COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, hosp, iso, trt
ORDER BY outcome, n DESC;