SELECT lifecycle_stage, COUNT(*) AS cnt, 
  SUM(CASE WHEN product_adoption_rate IS NULL THEN 1 ELSE 0 END) AS null_par
FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis)
GROUP BY lifecycle_stage
ORDER BY cnt DESC