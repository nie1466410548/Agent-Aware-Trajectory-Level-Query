
SELECT u.Department AS dept, COUNT(*) AS remote_cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE a."Anomaly Type" = 'Remote Login'
GROUP BY u.Department
