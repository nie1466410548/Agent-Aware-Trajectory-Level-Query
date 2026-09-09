SELECT 
  u.Department,
  SUM(CASE WHEN CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) AS off_hours_anomalies,
  COUNT(*) AS total_anomalies,
  ROUND(100.0 * SUM(CASE WHEN CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_off_hours
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_off_hours DESC