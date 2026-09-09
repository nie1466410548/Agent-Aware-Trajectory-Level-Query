
SELECT u.Department AS dept, a."Anomaly Score" AS score, a."Risk Level" AS risk,
       a."Device Anomaly Indicators" AS dev, a."Network Anomaly Indicators" AS net,
       a."Behavior Anomaly Indicators" AS beh
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
