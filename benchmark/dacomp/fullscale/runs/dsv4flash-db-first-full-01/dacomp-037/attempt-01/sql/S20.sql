
SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
