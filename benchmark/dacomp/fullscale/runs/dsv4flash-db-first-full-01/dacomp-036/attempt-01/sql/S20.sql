SELECT se."Type", se."Severity", COUNT(*) AS cnt
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY cnt DESC