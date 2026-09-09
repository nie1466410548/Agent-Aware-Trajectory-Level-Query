SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       sl."Log Level", COUNT(*) AS cnt
FROM system_logs_table sl
JOIN login_records_table lr ON sl."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY cnt DESC