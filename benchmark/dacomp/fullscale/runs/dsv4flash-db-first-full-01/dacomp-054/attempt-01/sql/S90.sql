-- Check real country info
SELECT country_code, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE country_code IS NOT NULL AND country_code != ''
GROUP BY country_code
ORDER BY cnt DESC
LIMIT 20