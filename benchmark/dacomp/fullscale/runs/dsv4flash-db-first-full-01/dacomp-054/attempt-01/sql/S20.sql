SELECT primary_email, COUNT(*) AS cnt
FROM customer360__conversion_funnel_analysis
GROUP BY primary_email
ORDER BY cnt DESC
LIMIT 10