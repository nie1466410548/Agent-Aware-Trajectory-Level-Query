SELECT lr."Login Method", lr."Two-Factor Authentication Status", lr."Two-Factor Authentication Method",
       lr."Authentication Level",
       COUNT(*) AS cnt,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures
FROM login_records_table lr
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4