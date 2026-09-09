SELECT primary_email, COUNT(*) AS cnt
FROM customer360__customer_activity_metrics
GROUP BY primary_email
ORDER BY cnt DESC
LIMIT 10