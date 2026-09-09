SELECT status, trigger_type, source_relation, COUNT(*) AS n
FROM klaviyo__flows
GROUP BY status, trigger_type, source_relation
ORDER BY n DESC