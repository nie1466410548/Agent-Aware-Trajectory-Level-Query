SELECT
  s."Medical history",
  s."Health status",
  COUNT(*) AS n
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history", s."Health status"
ORDER BY s."Medical history", s."Health status"