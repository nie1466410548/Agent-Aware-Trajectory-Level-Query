
SELECT 
  u.Department,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  COUNT(DISTINCT u."User ID") AS total_users_with_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
