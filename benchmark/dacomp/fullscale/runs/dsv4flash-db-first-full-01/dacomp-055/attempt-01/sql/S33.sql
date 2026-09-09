SELECT 
  PERCENTILE_CONT(0.3) WITHIN GROUP (ORDER BY investment_priority_score) AS top30_threshold,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY investment_priority_score) AS median_ips
FROM customer360__customer_value_analysis