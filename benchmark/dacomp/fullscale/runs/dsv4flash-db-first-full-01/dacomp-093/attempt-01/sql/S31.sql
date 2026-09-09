SELECT timezone, COUNT(*) AS n,
       ROUND(AVG(active_retention_rate_week), 4) AS avg_ret_week,
       ROUND(AVG(active_retention_rate_month), 4) AS avg_ret_month,
       ROUND(AVG(email_open_rate), 4) AS avg_open_rate,
       ROUND(AVG(count_received_email), 0) AS avg_received,
       ROUND(AVG(count_opened_email), 0) AS avg_opened
FROM klaviyo__persons
GROUP BY timezone
ORDER BY n DESC