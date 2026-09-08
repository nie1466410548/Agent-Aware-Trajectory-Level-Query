SELECT business_ref, AVG(rating) AS avg_rating, COUNT(*) AS n
FROM review
WHERE date >= '2016-01-01' AND date <= '2016-06-30'
GROUP BY business_ref
HAVING COUNT(*) >= 5
ORDER BY avg_rating DESC, n DESC
LIMIT 20

