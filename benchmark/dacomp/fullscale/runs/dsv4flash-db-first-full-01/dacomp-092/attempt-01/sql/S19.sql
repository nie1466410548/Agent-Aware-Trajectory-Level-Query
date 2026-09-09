WITH cust_vol AS (
  SELECT customer_id, MAX(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  COUNT(*) AS n_customers,
  MIN(vol) AS min_vol,
  MAX(vol) AS max_vol,
  AVG(vol) AS mean_vol
FROM cust_vol