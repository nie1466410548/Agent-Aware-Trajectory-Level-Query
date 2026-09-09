
  SELECT state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE state IS NOT NULL AND state != ''
  GROUP BY state
  ORDER BY customer_count DESC
  LIMIT 15
