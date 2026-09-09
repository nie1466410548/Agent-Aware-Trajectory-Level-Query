SELECT
  s."Medical history",
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(SQRT(AVG(i."Blood Pressure (Systolic)"*i."Blood Pressure (Systolic)") - AVG(i."Blood Pressure (Systolic)")*AVG(i."Blood Pressure (Systolic)")),2) AS sbp_std,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(SQRT(AVG(i."Blood Pressure (Diastolic)"*i."Blood Pressure (Diastolic)") - AVG(i."Blood Pressure (Diastolic)")*AVG(i."Blood Pressure (Diastolic)")),2) AS dbp_std,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(SQRT(AVG(i."Blood Glucose (mmol/L)"*i."Blood Glucose (mmol/L)") - AVG(i."Blood Glucose (mmol/L)")*AVG(i."Blood Glucose (mmol/L)")),2) AS glucose_std,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(SQRT(AVG(i."Total Cholesterol (mmol/L)"*i."Total Cholesterol (mmol/L)") - AVG(i."Total Cholesterol (mmol/L)")*AVG(i."Total Cholesterol (mmol/L)")),2) AS chol_std,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(SQRT(AVG(i."Triglycerides (mmol/L)"*i."Triglycerides (mmol/L)") - AVG(i."Triglycerides (mmol/L)")*AVG(i."Triglycerides (mmol/L)")),2) AS tg_std,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(SQRT(AVG(i."Uric Acid (umol/L)"*i."Uric Acid (umol/L)") - AVG(i."Uric Acid (umol/L)")*AVG(i."Uric Acid (umol/L)")),2) AS uric_std,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(SQRT(AVG(i."Alanine Aminotransferase (U/L)"*i."Alanine Aminotransferase (U/L)") - AVG(i."Alanine Aminotransferase (U/L)")*AVG(i."Alanine Aminotransferase (U/L)")),2) AS alt_std
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"