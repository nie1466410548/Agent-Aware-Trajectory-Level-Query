SELECT "Two-Factor Authentication Method", COUNT(*) AS total_2024,
       SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(*),1) AS fail_pct
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1
ORDER BY total_2024 DESC