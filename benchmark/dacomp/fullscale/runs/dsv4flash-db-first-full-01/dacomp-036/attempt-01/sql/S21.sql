SELECT "Authentication Method Name", "security level", "Enabled", "Maximum Attempts", "Lockout Duration", "Applicable User Types", "Authentication Protocol", "Encryption Method"
FROM authentication_methods_table
ORDER BY "security level" DESC