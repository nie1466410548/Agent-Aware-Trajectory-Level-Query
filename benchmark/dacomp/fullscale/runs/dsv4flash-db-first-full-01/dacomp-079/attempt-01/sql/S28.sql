SELECT last_event_on, COUNT(*) AS n
FROM pendo__visitor
GROUP BY last_event_on
ORDER BY n DESC
LIMIT 10