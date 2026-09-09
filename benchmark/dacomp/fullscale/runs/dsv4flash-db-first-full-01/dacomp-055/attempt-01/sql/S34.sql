SELECT 
  investment_priority_score,
  COUNT(*) AS cnt
FROM customer360__customer_value_analysis
GROUP BY investment_priority_score
ORDER BY investment_priority_score