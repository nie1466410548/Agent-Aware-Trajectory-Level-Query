SELECT MAX(days_span - active_days) as max_inactive_days,
       AVG(count_received_email) as avg_emails,
       MAX(count_received_email) as max_emails,
       SUM(CASE WHEN email_open_rate < 0.3 THEN 1 ELSE 0 END) as low_open_n,
       SUM(CASE WHEN email_open_rate >= 0.3 AND email_open_rate < 0.5 THEN 1 ELSE 0 END) as mid_open_n,
       SUM(CASE WHEN email_open_rate >= 0.5 THEN 1 ELSE 0 END) as high_open_n
FROM klaviyo__persons