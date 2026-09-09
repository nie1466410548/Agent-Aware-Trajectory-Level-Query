
SELECT
  SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS age_null,
  SUM(CASE WHEN "Weight (kg)" IS NULL THEN 1 ELSE 0 END) AS weight_null,
  SUM(CASE WHEN "Blood Pressure (Systolic)" IS NULL THEN 1 ELSE 0 END) AS sbp_null,
  SUM(CASE WHEN "Blood Glucose (mmol/L)" IS NULL THEN 1 ELSE 0 END) AS glu_null
FROM health_checkup_indicators
