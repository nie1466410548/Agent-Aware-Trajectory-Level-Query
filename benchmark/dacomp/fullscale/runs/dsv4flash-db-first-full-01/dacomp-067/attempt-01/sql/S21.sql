SELECT source_id, sourced_from, sourced_from_type, COUNT(*) as cnt
FROM greenhouse__application_enhanced 
WHERE source_id IS NOT NULL
GROUP BY source_id, sourced_from, sourced_from_type
ORDER BY cnt DESC
LIMIT 20