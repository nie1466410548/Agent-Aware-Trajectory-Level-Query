SELECT al."Anomaly Type", lr."Login Method", lr."Two-Factor Authentication Method", COUNT(*) AS cnt
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY cnt DESC