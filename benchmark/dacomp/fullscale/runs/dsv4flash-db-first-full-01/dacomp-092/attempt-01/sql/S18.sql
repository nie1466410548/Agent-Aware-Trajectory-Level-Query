SELECT customer_margin_volatility, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
WHERE customer_margin_volatility IS NOT NULL
GROUP BY customer_margin_volatility
ORDER BY customer_margin_volatility DESC
LIMIT 20