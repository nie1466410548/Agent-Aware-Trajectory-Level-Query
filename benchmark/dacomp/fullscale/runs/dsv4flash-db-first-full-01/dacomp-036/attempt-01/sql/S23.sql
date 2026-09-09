SELECT lr."Login Method", lr."Two-Factor Authentication Status", lr."Two-Factor Authentication Method",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(DISTINCT lr."Login Record ID"),1) AS fail_pct,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anom_rate,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY logins DESC