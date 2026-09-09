
SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Lipoprotein (mmol/L)" AS lipo
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
