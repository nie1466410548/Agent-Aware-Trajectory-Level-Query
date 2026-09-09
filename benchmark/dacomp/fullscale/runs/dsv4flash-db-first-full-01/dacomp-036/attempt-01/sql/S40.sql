
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
