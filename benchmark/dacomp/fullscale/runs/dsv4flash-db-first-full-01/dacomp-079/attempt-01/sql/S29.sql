SELECT COUNT(*) AS n, MIN(last_event_on) AS min_last, MAX(last_event_on) AS max_last
FROM pendo__visitor