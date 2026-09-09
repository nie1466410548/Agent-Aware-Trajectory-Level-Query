SELECT 
  u.Department,
  l."Login Method",
  COUNT(*) AS cnt
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, l."Login Method"
ORDER BY u.Department, cnt DESC