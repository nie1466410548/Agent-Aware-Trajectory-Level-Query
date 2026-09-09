SELECT 
  u.Department,
  COUNT(DISTINCT a."Anomaly ID") AS anomaly_count,
  COUNT(DISTINCT a."Login Record ID") AS login_records_with_anomalies,
  COUNT(DISTINCT u."User ID") AS users_with_anomalies,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(a."Device Anomaly Indicators"), 2) AS avg_device_indicator,
  ROUND(AVG(a."Network Anomaly Indicators"), 2) AS avg_network_indicator,
  ROUND(AVG(a."Behavior Anomaly Indicators"), 2) AS avg_behavior_indicator
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomaly_count DESC