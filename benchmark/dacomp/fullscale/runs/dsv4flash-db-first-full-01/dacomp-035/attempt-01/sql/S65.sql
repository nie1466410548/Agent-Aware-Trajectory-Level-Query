
SELECT u.Department AS dept, l."Login Duration" AS dur, l."Authentication Status" AS auth
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
