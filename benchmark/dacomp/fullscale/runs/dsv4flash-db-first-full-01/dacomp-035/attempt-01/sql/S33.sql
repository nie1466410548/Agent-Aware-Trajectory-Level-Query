SELECT 
  u.Department,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN a."Anomaly Score" ELSE NULL END), 2) AS avg_high_severe_score,
  ROUND(100.0 * SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_severe,
  ROUND(100.0 * SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_confirmed
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_high_severe DESC