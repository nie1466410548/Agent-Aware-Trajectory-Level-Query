SELECT 
  u.Department,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins,
  ROUND(100.0 * SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_failed,
  ROUND(100.0 * SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_no_2fa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_failed DESC