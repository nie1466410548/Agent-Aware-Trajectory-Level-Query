
SELECT u.Department AS dept, l."Two-Factor Authentication Status" AS tfa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
