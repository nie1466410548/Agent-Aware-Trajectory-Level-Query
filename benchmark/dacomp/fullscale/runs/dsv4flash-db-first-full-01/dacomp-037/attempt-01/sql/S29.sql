
SELECT s."Medical history" AS medhx, i.Gender,
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history", i.Gender
ORDER BY s."Medical history", i.Gender
