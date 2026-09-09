SELECT lr."Two-Factor Authentication Status",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anom_rate,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1