SELECT "Login Method", "Authentication Status", "Authentication Level", "Two-Factor Authentication Status", "Two-Factor Authentication Method", COUNT(*) AS cnt
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1,2,3,4,5
ORDER BY cnt DESC