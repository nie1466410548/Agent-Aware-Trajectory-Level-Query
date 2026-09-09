SELECT
  s."Medical history",
  s."Health status",
  COUNT(*) AS n
FROM health_status s
WHERE s."Medical history" = 'None'
GROUP BY s."Medical history", s."Health status"
ORDER BY s."Medical history", s."Health status"