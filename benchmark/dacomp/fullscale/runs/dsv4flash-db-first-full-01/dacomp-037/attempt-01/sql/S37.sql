
SELECT s."Medical history" AS medhx, s."Health status" AS hs,
  s."Smoking status" AS smoke, s."Drinking Status" AS drink
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
