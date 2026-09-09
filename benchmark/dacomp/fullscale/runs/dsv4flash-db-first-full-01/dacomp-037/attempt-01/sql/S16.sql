SELECT
  s."Medical history",
  MIN(i."Blood Pressure (Systolic)") AS sbp_min,
  MAX(i."Blood Pressure (Systolic)") AS sbp_max,
  MIN(i."Blood Pressure (Diastolic)") AS dbp_min,
  MAX(i."Blood Pressure (Diastolic)") AS dbp_max,
  MIN(i."Blood Glucose (mmol/L)") AS glu_min,
  MAX(i."Blood Glucose (mmol/L)") AS glu_max,
  MIN(i."Serum Potassium (mmol/L)") AS k_min,
  MAX(i."Serum Potassium (mmol/L)") AS k_max
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"