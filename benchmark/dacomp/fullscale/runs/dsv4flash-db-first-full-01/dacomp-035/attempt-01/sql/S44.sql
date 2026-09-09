
SELECT 
  u.Department,
  COUNT(*) AS anomaly_count,
  COUNT(DISTINCT l."User ID") AS users_with_anomalies,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(a."Device Anomaly Indicators"), 2) AS avg_device_indicator,
  ROUND(AVG(a."Network Anomaly Indicators"), 2) AS avg_network_indicator,
  ROUND(AVG(a."Behavior Anomaly Indicators"), 2) AS avg_behavior_indicator,
  ROUND(100.0 * SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_severe,
  ROUND(100.0 * SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_confirmed
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
