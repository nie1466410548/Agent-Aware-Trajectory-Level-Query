
  SELECT country, country_code, state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE country IS NOT NULL AND country != ''
  GROUP BY country
  ORDER BY customer_count DESC
  LIMIT 15
