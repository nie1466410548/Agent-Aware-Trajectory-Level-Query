SELECT
  s."Medical history",
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(stdev(i."Blood Pressure (Systolic)"),2) AS sbp_std,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(stdev(i."Blood Pressure (Diastolic)"),2) AS dbp_std,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(stdev(i."Blood Glucose (mmol/L)"),2) AS glucose_std,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(stdev(i."Total Cholesterol (mmol/L)"),2) AS chol_std,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(stdev(i."Triglycerides (mmol/L)"),2) AS tg_std,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(stdev(i."Uric Acid (umol/L)"),2) AS uric_std,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(stdev(i."Alanine Aminotransferase (U/L)"),2) AS alt_std,
  ROUND(AVG(i."Serum Potassium (mmol/L)"),2) AS k_mean,
  ROUND(stdev(i."Serum Potassium (mmol/L)"),2) AS k_std
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"