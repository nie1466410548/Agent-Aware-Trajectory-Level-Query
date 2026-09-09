SELECT 
  u.Department,
  a."Risk Level",
  a."Confirmation Status",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE u.Department = 'Technical Department' AND a."Risk Level" IN ('High', 'Severe')
GROUP BY u.Department, a."Risk Level", a."Confirmation Status"
ORDER BY u.Department, a."Risk Level"