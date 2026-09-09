SELECT lr."Login Method", lr."Two-Factor Authentication Status",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),3) AS anom_per_login,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       ROUND(1.0*SUM(se."Risk Score")/COUNT(DISTINCT lr."Login Record ID"),1) AS risk_per_login
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY 1,2