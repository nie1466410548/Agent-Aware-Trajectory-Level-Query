SELECT
  s."Medical history",
  COUNT(*) AS n,
  ROUND(100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_elevated_bp,
  ROUND(100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_bp,
  ROUND(100.0*SUM(CASE WHEN i."Weight (kg)" >= 75 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_wt_ge75,
  ROUND(100.0*SUM(CASE WHEN i."Blood Glucose (mmol/L)" >= 5.6 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_glu_ge5_6,
  ROUND(100.0*SUM(CASE WHEN i."Alanine Aminotransferase (U/L)" >= 40 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_alt_ge40
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"