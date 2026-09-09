SELECT
  s."Medical history",
  COUNT(*) AS n,
  ROUND(AVG(i.Age),2) AS age_mean,
  ROUND(AVG(i."Height (cm)"),2) AS height_mean,
  ROUND(AVG(i."Weight (kg)"),2) AS weight_mean,
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(AVG(i."Heart Rate (bpm)"),2) AS hr_mean,
  ROUND(AVG(i."Respiratory Rate (breaths/min)"),2) AS rr_mean,
  ROUND(AVG(i."Blood Oxygen Saturation (%)"),2) AS spo2_mean,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(AVG(i."Lipoprotein (mmol/L)"),2) AS lipo_mean,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(AVG(i."Blood Urea Nitrogen (mmol/L)"),2) AS bun_mean,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(AVG(i."Serum Potassium (mmol/L)"),2) AS k_mean
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"