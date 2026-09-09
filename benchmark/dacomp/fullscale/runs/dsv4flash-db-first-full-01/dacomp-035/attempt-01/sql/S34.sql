SELECT 
  u.Department,
  sl."Log Level",
  COUNT(*) AS cnt
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, sl."Log Level"
ORDER BY u.Department, sl."Log Level"