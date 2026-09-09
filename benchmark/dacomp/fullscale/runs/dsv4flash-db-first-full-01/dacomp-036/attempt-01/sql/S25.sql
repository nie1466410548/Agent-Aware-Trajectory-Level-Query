SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       al."Anomaly Type",
       COUNT(*) AS cnt,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       ROUND(AVG(al."Device Anomaly Indicators"),2) AS avg_dev,
       ROUND(AVG(al."Network Anomaly Indicators"),2) AS avg_net,
       ROUND(AVG(al."Behavior Anomaly Indicators"),2) AS avg_beh
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY 1,2,3