SELECT "Login Method",
       "Two-Factor Authentication Status",
       "Two-Factor Authentication Method",
       "Authentication Status",
       COUNT(*) AS cnt
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY "Login Method", "Two-Factor Authentication Status", "Authentication Status"