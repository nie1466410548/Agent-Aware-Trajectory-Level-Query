SELECT customer_id, COUNT(DISTINCT customer_margin_volatility) AS n_distinct_vol, COUNT(DISTINCT customer_margin_volatility) 
FROM quickbooks__profitability_analysis
GROUP BY customer_id
HAVING COUNT(DISTINCT customer_margin_volatility) > 1
LIMIT 5