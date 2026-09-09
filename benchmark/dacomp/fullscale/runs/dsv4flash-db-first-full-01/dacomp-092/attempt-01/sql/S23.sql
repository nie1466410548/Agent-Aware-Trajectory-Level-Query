WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY vol) AS p75
FROM cust_vol