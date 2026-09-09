SELECT person_id, timezone, count_received_email, count_opened_email, email_open_rate, active_retention_rate_week, active_retention_rate_month, first_event_on, last_event_on, active_weeks, weeks_span
FROM klaviyo__persons
ORDER BY person_id LIMIT 20