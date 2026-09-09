
SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COALESCE(ROUND(AVG(al."Anomaly Score"),1),0) AS avg_anom_score,
       COALESCE(SUM(al."Device Anomaly Indicators"),0) AS device_ind,
       COALESCE(SUM(al."Network Anomaly Indicators"),0) AS net_ind,
       COALESCE(SUM(al."Behavior Anomaly Indicators"),0) AS beh_ind,
       COUNT(DISTINCT se."Event ID") AS events,
       COALESCE(SUM(se."Risk Score"),0) AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events,
       COUNT(DISTINCT CASE WHEN se."Severity"='Severe' THEN se."Event ID" END) AS severe_events,
       COUNT(DISTINCT sl."Log ID") AS logs,
       COUNT(DISTINCT CASE WHEN sl."Log Level"='ERROR' THEN sl."Log ID" END) AS error_logs
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
LEFT JOIN system_logs_table sl ON sl."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomalies DESC
