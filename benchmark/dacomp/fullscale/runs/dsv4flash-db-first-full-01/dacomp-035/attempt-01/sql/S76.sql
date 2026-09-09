
SELECT u.Department AS dept,
  COUNT(*) AS total_logs,
  SUM(CASE WHEN sl."Handling Status" = 'Unprocessed' THEN 1 ELSE 0 END) AS unprocessed
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
