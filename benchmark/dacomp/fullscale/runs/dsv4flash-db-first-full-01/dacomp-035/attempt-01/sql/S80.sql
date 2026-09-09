SELECT 
  u.Department,
  strftime('%H', a."Detection Time") AS hour,
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6
GROUP BY u.Department
ORDER BY u.Department