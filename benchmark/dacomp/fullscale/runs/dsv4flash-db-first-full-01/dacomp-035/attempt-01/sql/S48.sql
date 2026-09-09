
SELECT 
  u.Department,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) AS high_sev_events,
  AVG(se."Risk Score") AS avg_risk_score
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
