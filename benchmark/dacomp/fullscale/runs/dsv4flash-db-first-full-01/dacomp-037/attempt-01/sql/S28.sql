
SELECT s."Medical history" AS medhx, i.Gender, i."Weight (kg)" AS weight
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
