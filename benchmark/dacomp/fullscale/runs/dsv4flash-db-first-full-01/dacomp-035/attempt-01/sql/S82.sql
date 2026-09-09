SELECT 
  u.Department,
  COUNT(DISTINCT a."Anomaly ID") AS anomaly_count,
  COUNT(DISTINCT l."User ID") AS distinct_users,
  ROUND(1.0 * COUNT(DISTINCT a."Anomaly ID") / NULLIF(COUNT(DISTINCT l."User ID"), 0), 2) AS anomalies_per_affected_user
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomalies_per_affected_user DESC