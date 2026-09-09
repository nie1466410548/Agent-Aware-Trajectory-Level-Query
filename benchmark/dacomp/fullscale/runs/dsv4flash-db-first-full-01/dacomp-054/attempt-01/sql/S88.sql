-- Check the address table country distribution
SELECT country, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE country IS NOT NULL AND country != ''
GROUP BY country
ORDER BY cnt DESC
LIMIT 20