SELECT flow_name, COUNT(*) AS n
FROM klaviyo__flows
GROUP BY flow_name
ORDER BY n DESC
LIMIT 100