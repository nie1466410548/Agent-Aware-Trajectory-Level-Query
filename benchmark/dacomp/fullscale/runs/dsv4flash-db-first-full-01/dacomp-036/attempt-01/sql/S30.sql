SELECT "Authentication Method Name",
       COUNT(*) AS n,
       ROUND(AVG("security level"),1) AS avg_sec_level,
       ROUND(AVG("Authentication Priority"),1) AS avg_priority,
       SUM(CASE WHEN "Enabled"='Enabled' THEN 1 ELSE 0 END) AS enabled_count,
       ROUND(AVG("Maximum Attempts"),1) AS avg_max_attempts,
       ROUND(AVG("Lockout Duration"),1) AS avg_lockout
FROM authentication_methods_table
WHERE "Authentication Method Name" IN ('SMS verification code','Email verification code','Dynamic Token','Fingerprint recognition','QR Code Scanning','Password Login')
GROUP BY 1
ORDER BY avg_sec_level DESC