SELECT 
  u.Department,
  CASE WHEN ua.anomaly_count >= 3 THEN '3+' 
       WHEN ua.anomaly_count = 2 THEN '2' 
       ELSE '1' END AS anomaly_bucket,
  COUNT(DISTINCT u."User ID") AS user_count,
  SUM(ua.anomaly_count) AS anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department, anomaly_bucket
ORDER BY u.Department, anomaly_bucket