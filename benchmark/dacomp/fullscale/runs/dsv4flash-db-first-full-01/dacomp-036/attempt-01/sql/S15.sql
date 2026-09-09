SELECT lr."Login Method",
       COUNT(DISTINCT se."Event ID") AS sev_evt,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Critical','Severe') THEN se."Event ID" END) AS high_sev
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1
ORDER BY sev_evt DESC