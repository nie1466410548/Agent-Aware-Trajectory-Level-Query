SELECT COUNT(*) AS n_persons,
       COUNT(DISTINCT person_id) AS n_ids,
       AVG(active_retention_rate_week) AS avg_ret_week,
       AVG(active_retention_rate_month) AS avg_ret_month,
       AVG(count_received_email) AS avg_received,
       MIN(first_event_on) AS min_first, MAX(last_event_on) AS max_last
FROM klaviyo__persons