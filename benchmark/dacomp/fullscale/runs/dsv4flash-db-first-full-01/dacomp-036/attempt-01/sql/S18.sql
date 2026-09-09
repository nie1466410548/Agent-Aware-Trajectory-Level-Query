SELECT COUNT(*) AS total_2024,
       COUNT(DISTINCT CASE WHEN al."Anomaly ID" IS NOT NULL THEN lr."Login Record ID" END) AS with_anomaly
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'