SELECT 
  u.Department,
  CASE WHEN user_anomaly_count.anomaly_count >= 2 THEN 'Multiple' ELSE 'Single' END AS anomaly_frequency,
  COUNT(DISTINCT u."User ID") AS user_count,
  SUM(user_anomaly_count.anomaly_count) AS total_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) user_anomaly_count
JOIN user_information_table u ON user_anomaly_count."User ID" = u."User ID"
GROUP BY u.Department, anomaly_frequency
ORDER BY u.Department, anomaly_frequency