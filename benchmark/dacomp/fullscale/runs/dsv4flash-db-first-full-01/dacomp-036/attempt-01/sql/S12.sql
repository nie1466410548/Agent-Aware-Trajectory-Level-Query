SELECT "Login Method", 
       "Authentication Status", 
       COUNT(*) AS cnt,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY "Login Method"), 1) AS pct
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY "Login Method", "Authentication Status"
ORDER BY "Login Method", cnt DESC