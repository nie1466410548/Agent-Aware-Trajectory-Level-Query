SELECT lr."Login Method",
       lr."Two-Factor Authentication Method",
       COUNT(DISTINCT al."Anomaly ID") AS anomaly_cnt,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       SUM(al."Device Anomaly Indicators") AS dev_ind,
       SUM(al."Network Anomaly Indicators") AS net_ind,
       SUM(al."Behavior Anomaly Indicators") AS beh_ind
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomaly_cnt DESC