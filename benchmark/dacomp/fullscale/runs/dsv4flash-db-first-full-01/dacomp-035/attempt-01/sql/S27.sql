SELECT 
  u.Department,
  COUNT(DISTINCT l."User ID") AS active_users_with_logins,
  COUNT(DISTINCT l."Login Record ID") AS logins,
  ROUND(1.0 * COUNT(DISTINCT a."Login Record ID") / COUNT(DISTINCT l."Login Record ID"), 3) AS anomaly_rate_per_login
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
LEFT JOIN abnormal_logins_table a ON l."Login Record ID" = a."Login Record ID"
GROUP BY u.Department
ORDER BY anomaly_rate_per_login DESC