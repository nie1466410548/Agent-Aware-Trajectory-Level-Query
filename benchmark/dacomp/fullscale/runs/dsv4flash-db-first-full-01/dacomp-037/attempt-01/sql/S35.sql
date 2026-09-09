
SELECT
  s."Medical history" AS medhx,
  COUNT(*) AS n,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*) AS pct_elev,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*) AS pct_high
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
