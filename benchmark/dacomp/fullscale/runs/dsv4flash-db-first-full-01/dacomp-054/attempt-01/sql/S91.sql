-- Check state distribution
SELECT state, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE state IS NOT NULL AND state != ''
GROUP BY state
ORDER BY cnt DESC
LIMIT 20