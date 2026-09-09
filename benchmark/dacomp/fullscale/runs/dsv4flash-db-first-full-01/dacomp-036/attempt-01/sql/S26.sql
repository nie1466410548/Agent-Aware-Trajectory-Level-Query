SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       se."Type", se."Severity",
       COUNT(*) AS cnt,
       ROUND(AVG(se."Risk Score"),1) AS avg_risk
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4