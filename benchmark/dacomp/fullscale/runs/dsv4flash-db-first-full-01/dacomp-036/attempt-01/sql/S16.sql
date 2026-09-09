SELECT lr."Login Method", lr."Two-Factor Authentication Method", lr."Two-Factor Authentication Status",
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anomaly_per_login
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY anomaly_per_login DESC