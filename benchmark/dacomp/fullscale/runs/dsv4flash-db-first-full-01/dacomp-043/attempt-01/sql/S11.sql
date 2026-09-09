SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  COUNT(*) AS n,
  ROUND(AVG("Highest Body Temperature (°C)"),2) AS avg_temp,
  ROUND(MIN("Highest Body Temperature (°C)"),2) AS min_temp,
  ROUND(MAX("Highest Body Temperature (°C)"),2) AS max_temp,
  ROUND(AVG("Data Completeness Score"),2) AS avg_completeness
FROM clinical_manifestations cm
JOIN basic_medical_record_informatio b ON cm."Case ID" = b."Case ID"
GROUP BY outcome;