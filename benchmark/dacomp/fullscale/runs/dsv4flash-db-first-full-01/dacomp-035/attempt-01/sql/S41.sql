SELECT 
  u.Department,
  l."Authentication Level",
  COUNT(*) AS cnt
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, l."Authentication Level"
ORDER BY u.Department, l."Authentication Level"