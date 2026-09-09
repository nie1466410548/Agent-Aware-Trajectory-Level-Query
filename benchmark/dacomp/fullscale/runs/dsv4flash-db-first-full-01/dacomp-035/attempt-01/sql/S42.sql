SELECT 
  u.Department,
  ip."Province",
  COUNT(*) AS cnt
FROM ip_address_information_table ip
JOIN login_records_table l ON ip."Login record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, ip."Province"
ORDER BY u.Department, cnt DESC