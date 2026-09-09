SELECT
  s."Medical history",
  ROUND(AVG(i."Age"),2) AS age_mean,
  ROUND(AVG(i."Weight (kg)"),2) AS weight_mean,
  ROUND(AVG(i."Heart Rate (bpm)"),2) AS hr_mean
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"